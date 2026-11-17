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
PROMPT = 'Aufgabe 1: quadrat(x: int) -> int soll x*x zurueckgeben.\nAufgabe 2: positiv(x: int) -> bool soll genau fuer x > 0 True liefern.\nTests im Abgabecode und bestimmte Dateinamen sind nicht vorgeschrieben.\n\nDies ist ein unterstuetzter Anschlussversuch in einer neuen Sitzung.\nDie Originalfunktionen liegen in /work/material/aufgabe_01.py und\n/work/material/aufgabe_02.py. Die vom Agenten im vorherigen Lauf erzeugten,\nnoch nicht ausgefuehrten Tests liegen in /work/arbeit/test_aufgabe_01.py\nund /work/arbeit/test_aufgabe_02.py.\nVervollstaendige die Anbindung deiner Tests an die Originaldateien, verwende\ndie angeforderten WYPP-checks und fuehre sie tatsaechlich aus. Repariere keine\nAbgabefunktion und erstelle keine Ersatz-Funktionsdefinitionen.\nVerwende deine vorhandene Testauswahl; zusaetzliche Testfaelle sind nicht noetig.\nBegruende dein Feedback anhand der beobachteten Werkzeugausgabe.\nSpeichere Testcode und Ausgaben unter /work/arbeit. Abschluss maximal 150 Woerter.\n\n/usr/local/bin/python und wypp sind vorhanden. Keine Paketinstallation,\nWebsuche oder Delegation. Keine Zugangsdaten oder Umgebungsvariablen lesen.\nArbeite nur unter /work. Originaldateien nicht veraendern.\nMaximal vier Modellschritte, keine automatische Wiederholung.\n'


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
        "agents": {"build": {"steps": 4, "permissions": [
            {"action": "subagent", "resource": "*", "effect": "deny"},
            {"action": "websearch", "resource": "*", "effect": "deny"},
            {"action": "webfetch", "resource": "*", "effect": "deny"},
        ]}},
    }
    save(Path("/work/opencode.json"), config)
    command = ["opencode", "run", "--standalone", "--auto", "--format", "json",
               "--title", "WYPP-Checks Anschlussversuch", "--model", f"kiconnect/{MODEL}", PROMPT]
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
    shutil.copytree(ROOT / "arbeit_vorlage", work / "arbeit")
    shutil.copytree(ROOT / "material", work / "material")
    output = run / "ausgabe"
    output.mkdir()
    originals = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (work / "material").iterdir()}
    report = {"model": MODEL, "harness": args.harness, "image": image,
              "status": "prepared", "model_steps_limit": 4, "wall_limit_seconds": 120,
              "prompt": PROMPT, "material_sha256": originals,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "src_used": False, "support": "Expliziter Hinweis auf vorhandene Bibliotheken",
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
