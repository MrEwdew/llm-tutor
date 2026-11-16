import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from konfiguration import (
    AUFTRAG, CPU_LIMIT, DOCKER_IMAGE, FAELLE, GRAPH_LIMIT, HARNESSES, MODELLE,
    ROOT, SPEICHERLIMIT, WIEDERHOLUNGEN, ZEITLIMIT,
)


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# Jeder Versuch bekommt neue Kopien, ohne Aufgabenzuordnung oder Testvorgaben.
def prepare(case_name, harness, model, repeat):
    case = FAELLE[case_name]
    sources = [
        ("aufgabenblatt", case["aufgabenblatt"]),
        ("abgabe", case["abgabe"]),
    ]
    sources += [("referenzen", path) for path in case["referenzen"]]
    sources += [("beispieltests", path) for path in case["beispieltests"]]
    for _, path in sources:
        if not path.is_file():
            raise FileNotFoundError(path)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    run = ROOT / "laeufe" / f"{stamp}_{case_name}_{harness}_{repeat}"
    workspace = run / "arbeitsordner"
    workspace.mkdir(parents=True)
    material = []
    for group, source in sources:
        target = workspace / "material" / group / source.name
        if target.exists():
            raise ValueError(f"Doppelter Materialname: {target.name}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        material.append({"file": str(target.relative_to(workspace)), "sha256": fingerprint(target)})

    notes = workspace / "material/hinweise.txt"
    notes.write_text(case["hinweis"], encoding="utf-8")
    material.append({"file": str(notes.relative_to(workspace)), "sha256": fingerprint(notes)})
    (workspace / "arbeit").mkdir()
    (run / "auftrag.txt").write_text(AUFTRAG, encoding="utf-8")
    snapshot = run / "skripte"
    snapshot.mkdir()
    for source in ROOT.glob("*.py"):
        shutil.copyfile(source, snapshot / source.name)
    for name in ("Dockerfile", "requirements.txt"):
        shutil.copyfile(ROOT / name, snapshot / name)
    packages = {}
    for name in ("deepagents", "langchain", "langchain-openai", "wypp", "pypdf"):
        try:
            packages[name] = version(name)
        except PackageNotFoundError:
            packages[name] = None
    report = {
        "case": case_name, "harness": harness, "model": model, "repeat": repeat,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "status": "prepared", "material": material, "case_note": case["hinweis"],
        "prompt_sha256": hashlib.sha256(AUFTRAG.encode("utf-8")).hexdigest(),
        "host_python": sys.version, "host_packages": packages,
        "limits": {"wall_seconds": ZEITLIMIT, "deepagents_graph_steps": GRAPH_LIMIT,
                   "memory": SPEICHERLIMIT, "cpus": CPU_LIMIT, "pids": 256},
        "usage": None, "quality_review": "pending",
        "execution_environment": "docker_whole_agent",
        "docker_image_tag": DOCKER_IMAGE,
    }
    save_json(run / "bericht.json", report)
    save_json(run / "bewertung.json", {
        "reviewed": False, "reviewer": "", "notes": "",
        "true_positives": None, "false_positives": None, "false_negatives": None,
        "own_tests_valid": None, "execution_claims_verified": None,
    })
    return run, report


# Nur die benoetigten Zugangswerte an Docker weitergeben, nicht die .env-Datei.
def check_setup():
    from dotenv import dotenv_values

    values = dotenv_values(ROOT.parent / ".env")
    credentials = {key: values.get(key) or os.environ.get(key) for key in (
        "KICONNECT_API_KEY", "KICONNECT_BASE_URL",
    )}
    if not all(credentials.values()):
        raise ValueError("KI:CONNECT-Konfiguration unvollstaendig.")
    result = subprocess.run(
        ["docker", "image", "inspect", DOCKER_IMAGE, "--format", "{{.Id}}"],
        capture_output=True, text=True, timeout=20, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Docker Desktop starten und Evaluationsimage zuerst bauen.")
    return result.stdout.strip(), credentials


def execute(run, report, image_id, credentials):
    output = run / "ausgabe"
    output.mkdir()
    container = "tutor-eval-" + uuid.uuid4().hex
    command = [
        "docker", "run", "--name", container, "--init",
        "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "--memory", SPEICHERLIMIT, "--memory-swap", SPEICHERLIMIT,
        "--cpus", CPU_LIMIT, "--pids-limit", "256", "--user", "10001:10001",
        "--tmpfs", "/tmp:rw,nosuid,nodev,size=512m,mode=1777",
    ]
    for source, target, readonly in (
        (run / "arbeitsordner", "/work", False),
        (run / "arbeitsordner/material", "/work/material", True),
        (run / "skripte", "/runner", True),
        (run / "auftrag.txt", "/auftrag.txt", True),
        (output, "/output", False),
    ):
        mount = f"type=bind,source={source.resolve()},target={target}"
        command += ["--mount", mount + (",readonly" if readonly else "")]
    for key in credentials:
        command += ["--env", key]
    command += [image_id, "python", "-B", f"/runner/{report['harness']}_lauf.py",
                "/output", report["model"]]
    start = time.perf_counter()
    report["status"] = "running"
    report["docker_image_id"] = image_id
    report["network"] = "enabled_for_model_api; no technical web restriction"
    save_json(run / "bericht.json", report)
    try:
        with (run / "stdout.txt").open("w", encoding="utf-8") as out, \
             (run / "stderr.txt").open("w", encoding="utf-8") as err:
            process = subprocess.Popen(
                command, stdout=out, stderr=err, env={**os.environ, **credentials},
            )
            try:
                report["exit_code"] = process.wait(timeout=ZEITLIMIT)
                report["status"] = "process_finished" if process.returncode == 0 else "process_error"
            except subprocess.TimeoutExpired:
                subprocess.run(["docker", "kill", container], capture_output=True, timeout=20)
                process.wait(timeout=20)
                report["status"] = "timeout"
    except (OSError, subprocess.SubprocessError) as error:
        report["status"] = "start_error"
        report["error"] = type(error).__name__
    finally:
        report["duration_seconds"] = round(time.perf_counter() - start, 3)
        report["material_unchanged"] = all(
            (run / "arbeitsordner" / item["file"]).is_file()
            and fingerprint(run / "arbeitsordner" / item["file"]) == item["sha256"]
            for item in report["material"]
        )
        adapter = output / "adapter.json"
        if adapter.is_file():
            try:
                report["adapter"] = json.loads(adapter.read_text(encoding="utf-8"))
                report["usage"] = report["adapter"].get("usage")
            except ValueError:
                report["adapter_report_error"] = "invalid_json"
        report["feedback_exists"] = (run / "arbeitsordner/feedback.md").is_file()
        save_json(run / "bericht.json", report)
        try:
            for name in ("python-packages.txt", "system-packages.txt", "opencode.sha256"):
                subprocess.run(
                    ["docker", "cp", f"{container}:/opt/evaluation/{name}", str(output / name)],
                    capture_output=True, timeout=20, check=False,
                )
        finally:
            subprocess.run(["docker", "rm", "-f", container], capture_output=True, timeout=20)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", action="store_true", help="Echte Agentenlaeufe starten")
    parser.add_argument("--fall", choices=list(FAELLE))
    parser.add_argument("--harness", choices=HARNESSES)
    args = parser.parse_args()
    if args.start:
        image_id, credentials = check_setup()
    for case in ([args.fall] if args.fall else FAELLE):
        for model in MODELLE:
            for harness in ([args.harness] if args.harness else HARNESSES):
                for repeat in range(1, WIEDERHOLUNGEN + 1):
                    run, report = prepare(case, harness, model, repeat)
                    if args.start:
                        execute(run, report, image_id, credentials)
                    print(case, harness, report["status"], run.name)


if __name__ == "__main__":
    main()
