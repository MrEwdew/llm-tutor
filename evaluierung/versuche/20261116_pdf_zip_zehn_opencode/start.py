import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
MODEL = "Qwen_3_30B_A3B_Instruct_2507"
IMAGE = "tutor-evaluation:python-3.13-opencode-2.3.0"
PROMPT = 'Untersuche /work/material/aufgaben.pdf und /work/material/abgabe.zip.\nLies den PDF-Text mit /usr/local/bin/python und pypdf, nicht mit dem direkten PDF-Lesewerkzeug.\nEntpacke die ZIP nach /work/arbeit. Lies den enthaltenen Abgabecode und ordne die Dateien den Aufgaben zu.\nEntwickle selbst sinnvolle WYPP-checks mit aus dem PDF begruendeten Sollwerten. Speichere und fuehre sie gegen die unveraenderten entpackten Abgabedateien aus.\nErklaere gefundene Fehler pro Aufgabe anhand der tatsaechlichen Testergebnisse. Keine Ersatzloesungen, keine kopierten oder reparierten Funktionsdefinitionen. Fehlende Abgabetests nur beanstanden, wenn das PDF sie fordert.\n\nImporthilfe fuer deine Testdatei:\nimport sys\nsys.path.insert(0, "/work/arbeit/abgabe")\nfrom aufgabe_01 import quadrat\nfrom aufgabe_02 import positiv\nfrom wypp import check\n\nDer Importpfad passt zur ZIP-Struktur nach dem Entpacken nach /work/arbeit. Lies die Dateien trotzdem selbst.\nWYPP-Hilfe: check(istwert, sollwert), genau zwei Argumente. Beschreibungen als Kommentare, nicht als drittes Argument. Waehle Testeingaben und Sollwerte selbst. Prozess-Exitcode 0 allein beweist nicht, dass WYPP-Checks bestehen; beachte die Ausgabe.\n\nPython, pypdf, zipfile und wypp sind vorhanden. Keine Paketinstallation, Websuche oder Delegation. Keine Zugangsdaten oder Umgebungsvariablen lesen. Nur unter /work arbeiten. Originalmaterial und entpackten Abgabecode unveraendert lassen. Testcode und Ergebnisse unter /work/arbeit behalten. Abschlussantwort maximal 200 Woerter, ausgefuehrt und nur vorgeschlagen unterscheiden.\nMaximal zehn Modellschritte, keine automatische Wiederholung.\n'


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")




def worker(harness):
    config = {
        "$schema": "https://opencode.ai/config.json",
        "model": f"kiconnect/{MODEL}",
        "providers": {"kiconnect": {
            "name": "KI:CONNECT", "env": ["KICONNECT_API_KEY"],
            "package": "@opencode/ai/providers/openai-compatible",
            "settings": {"baseURL": os.environ["KICONNECT_BASE_URL"],
                         "apiKey": "{env:KICONNECT_API_KEY}"},
            "models": {MODEL: {"name": MODEL}},
        }},
        "agents": {"build": {"steps": 10, "permissions": [
            {"action": "subagent", "resource": "*", "effect": "deny"},
            {"action": "websearch", "resource": "*", "effect": "deny"},
            {"action": "webfetch", "resource": "*", "effect": "deny"},
        ]}},
    }
    save(Path("/work/opencode.json"), config)
    command = ["opencode", "run", "--standalone", "--auto", "--format", "json",
               "--title", "Eigene WYPP-Checks", "--model", f"kiconnect/{MODEL}", PROMPT]
    with Path("/output/verlauf.jsonl").open("w", encoding="utf-8") as output:
        result = subprocess.run(command, stdout=output, check=False)
    raise SystemExit(result.returncode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--harness", choices=["opencode"], default="opencode")
    args = parser.parse_args()
    if args.worker:
        worker(args.harness)
        return
    from dotenv import dotenv_values

    project = ROOT.parents[2]
    values = dotenv_values(project / ".env")
    credentials = {k: values.get(k) or os.environ.get(k) for k in (
        "KICONNECT_API_KEY", "KICONNECT_BASE_URL",
    )}
    if not all(credentials.values()):
        raise RuntimeError("KI:CONNECT-Konfiguration unvollstaendig.")
    image = subprocess.run(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"],
                           capture_output=True, text=True, check=True).stdout.strip()
    run = ROOT / args.harness
    run.mkdir()
    work = run / "arbeitsordner"
    work.mkdir()
    (work / "arbeit").mkdir()
    shutil.copytree(ROOT / "material", work / "material")
    output = run / "ausgabe"
    output.mkdir()
    originals = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (work / "material").iterdir()}
    report = {"model": MODEL, "harness": args.harness, "image": image,
              "status": "prepared", "model_steps_limit": 10, "wall_limit_seconds": 120,
              "prompt": PROMPT, "material_sha256": originals,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "src_used": False, "support": "Importzeilen, Suchpfad und WYPP-Schnittstelle; identischer DeepAgents-Auftrag",
              "permissions": "OpenCode: Subagent und Webtools nativ untersagt"}
    save(run / "bericht.json", report)
    (run / "auftrag.txt").write_text(PROMPT, encoding="utf-8")
    shutil.copyfile(__file__, run / "start_snapshot.py")
    name = "tutor-klein-" + uuid.uuid4().hex
    command = ["docker", "run", "--name", name, "--init", "--read-only", "--cap-drop", "ALL",
               "--security-opt", "no-new-privileges", "--memory", "4g", "--memory-swap", "4g",
               "--cpus", "2", "--pids-limit", "256", "--user", "10001:10001",
               "--tmpfs", "/tmp:rw,nosuid,nodev,size=512m,mode=1777"]
    for source, target, ro in [(work, "/work", False), (work / "material", "/work/material", True),
                                (run / "start_snapshot.py", "/runner/start.py", True),
                                (output, "/output", False)]:
        command += ["--mount", f"type=bind,source={source.resolve()},target={target}" + (",readonly" if ro else "")]
    for key in credentials:
        command += ["--env", key]
    command += [image, "python", "-B", "/runner/start.py", "--worker", "--harness", args.harness]
    started = time.perf_counter()
    print("Versuch:", run, flush=True)
    try:
        with (run / "stdout.txt").open("w", encoding="utf-8") as stdout, \
             (run / "stderr.txt").open("w", encoding="utf-8") as stderr:
            process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                       env={**os.environ, **credentials})
            try:
                report["exit_code"] = process.wait(timeout=120)
                report["status"] = "completed" if process.returncode == 0 else "process_error"
            except subprocess.TimeoutExpired:
                subprocess.run(["docker", "kill", name], capture_output=True, timeout=10)
                process.wait(timeout=10)
                report["status"] = "timeout"
    finally:
        report["duration_seconds"] = round(time.perf_counter() - started, 3)
        report["material_unchanged"] = all(hashlib.sha256(p.read_bytes()).hexdigest() == originals[p.name]
                                           for p in (work / "material").iterdir())
        save(run / "bericht.json", report)
        subprocess.run(["docker", "rm", "-f", name], capture_output=True, timeout=10)
    print(report["status"], report["duration_seconds"], flush=True)


if __name__ == "__main__":
    main()
