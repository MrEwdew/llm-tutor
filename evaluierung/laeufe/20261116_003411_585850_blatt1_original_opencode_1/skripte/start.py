import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from konfiguration import (
    AUFTRAG, FAELLE, GRAPH_LIMIT, HARNESSES, MODELLE,
    ROOT, WIEDERHOLUNGEN, ZEITLIMIT,
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

    (workspace / "material/hinweise.txt").write_text(case["hinweis"], encoding="utf-8")
    (workspace / "arbeit").mkdir()
    (run / "auftrag.txt").write_text(AUFTRAG, encoding="utf-8")
    snapshot = run / "skripte"
    snapshot.mkdir()
    for source in ROOT.glob("*.py"):
        shutil.copyfile(source, snapshot / source.name)
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
        "python": sys.version, "packages": packages,
        "limits": {"wall_seconds": ZEITLIMIT, "deepagents_graph_steps": GRAPH_LIMIT},
        "usage": None, "quality_review": "pending",
        "execution_environment": "local_host_not_isolated",
        "project_root": str(ROOT.parent),
    }
    save_json(run / "bericht.json", report)
    save_json(run / "bewertung.json", {
        "reviewed": False, "reviewer": "", "notes": "",
        "true_positives": None, "false_positives": None, "false_negatives": None,
        "own_tests_valid": None, "execution_claims_verified": None,
    })
    return run, report


# Das Limit beendet auch lokale Kindprozesse, nicht nur den Adapter.
def stop_process(process):
    if os.name == "nt":
        subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    else:
        os.killpg(process.pid, signal.SIGKILL)
    process.wait()


def execute(run, report):
    worker = run / "skripte" / f"{report['harness']}_lauf.py"
    command = [sys.executable, "-B", str(worker), str(run), report["model"]]
    start = time.perf_counter()
    report["status"] = "running"
    save_json(run / "bericht.json", report)
    try:
        with (run / "stdout.txt").open("w", encoding="utf-8") as out, \
             (run / "stderr.txt").open("w", encoding="utf-8") as err:
            process = subprocess.Popen(
                command, cwd=run / "arbeitsordner", stdout=out, stderr=err,
                start_new_session=os.name != "nt",
            )
            try:
                report["exit_code"] = process.wait(timeout=ZEITLIMIT)
                report["status"] = "process_finished" if process.returncode == 0 else "process_error"
            except subprocess.TimeoutExpired:
                stop_process(process)
                report["status"] = "timeout"
    except OSError as error:
        report["status"] = "start_error"
        report["error"] = type(error).__name__
    finally:
        report["duration_seconds"] = round(time.perf_counter() - start, 3)
        report["material_unchanged"] = all(
            (run / "arbeitsordner" / item["file"]).is_file()
            and fingerprint(run / "arbeitsordner" / item["file"]) == item["sha256"]
            for item in report["material"]
        )
        adapter = run / "adapter.json"
        if adapter.is_file():
            report["adapter"] = json.loads(adapter.read_text(encoding="utf-8"))
            report["usage"] = report["adapter"].get("usage")
        save_json(run / "bericht.json", report)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", action="store_true", help="Echte Agentenlaeufe starten")
    parser.add_argument("--lokale-ausfuehrung", action="store_true",
                        help="Agenten duerfen Code mit Benutzerrechten ausfuehren")
    parser.add_argument("--fall", choices=list(FAELLE))
    parser.add_argument("--harness", choices=HARNESSES)
    args = parser.parse_args()
    if args.start and not args.lokale_ausfuehrung:
        parser.error("Ausfuehrungsumgebung festlegen: lokale Laeufe brauchen --lokale-ausfuehrung.")
    for case in ([args.fall] if args.fall else FAELLE):
        for model in MODELLE:
            for harness in ([args.harness] if args.harness else HARNESSES):
                for repeat in range(1, WIEDERHOLUNGEN + 1):
                    run, report = prepare(case, harness, model, repeat)
                    if args.start:
                        execute(run, report)
                    print(case, harness, report["status"], run.name)


if __name__ == "__main__":
    main()
