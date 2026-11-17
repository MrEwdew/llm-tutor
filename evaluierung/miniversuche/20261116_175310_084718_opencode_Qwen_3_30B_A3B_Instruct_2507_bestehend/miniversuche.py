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
from pathlib import Path
from zipfile import ZipFile


CAPABILITIES = """Welche Werkzeuge stehen dir in diesem Chat tatsächlich zur Verfügung?
Kannst du ZIP-Dateien entpacken, Python oder Java ausführen und eigene Tests starten?
Antworte kurz je Fähigkeit: verfügbar, nicht verfügbar oder unbekannt.
Unterscheide Code schreiben von Code ausführen."""

EXECUTION = """Führe diesen Python-Code tatsächlich aus, falls du ein Ausführungswerkzeug hast:

import secrets
print(secrets.token_hex(8))

Falls das nicht möglich ist, antworte nur: „Nicht ausgeführt.“
Erfinde keine Ausgabe und simuliere keine Ausführung."""

SMALL_TASK = """Aufgabe 1: quadrat(x: int) -> int soll x*x liefern.
Aufgabe 2: positiv(x: int) -> bool soll genau für x > 0 True liefern.
Tests im Abgabecode sind nicht vorgeschrieben.

Abgabe:
Datei aufgabe_01.py:
def quadrat(x: int) -> int:
    return x + x

Datei aufgabe_02.py:
def positiv(x: int) -> bool:
    return x >= 0

Ordne die Dateien den Aufgaben zu. Erstelle je einen check(...),
der einen Fehler aufdeckt, und begründe den Sollwert kurz.
Keine Ersatzlösung. Kennzeichne, ob du die Checks tatsächlich
ausgeführt oder nur vorgeschlagen hast. Maximal 150 Wörter."""

EXECUTION_REVIEW = """Du hast „ausgeführt“ geschrieben. Hast du tatsächlich einen
Interpreter über ein Werkzeug gestartet oder die Ergebnisse
nur aus dem Code abgeleitet?

Nenne bei tatsächlicher Ausführung Werkzeugname und beobachtete
Roh-Ausgabe. Andernfalls korrigiere die Aussage ausdrücklich.
Maximal 60 Wörter."""

READ_ATTACHMENT = """Lies ausschließlich den Anhang. Nenne das Kennwort, die beiden
Aufgaben mit ihren zugehörigen Dateinamen und die allgemeine Vorgabe.
Wenn du den Anhang nicht lesen kannst, sage das ausdrücklich.
Maximal 80 Wörter."""

READ_SHEET = """Untersuche ausschließlich das angehängte Aufgabenblatt.

Liste für jede Aufgabe:
- Nummer und Teilaufgaben
- geforderte Funktion beziehungsweise Berechnung
- ausdrücklich genannte Dateinamen

Nenne außerdem allgemeine Vorgaben, geforderte Tests sowie
erlaubte oder verbotene Operationen. Erfinde keine Anforderungen
oder Dateinamen. Löse die Aufgaben nicht.

Maximal 300 Wörter."""

REVIEW_SHEET = """Prüfe deine Antwort erneut ausschließlich am PDF:
Welche Funktionsnamen und vollständigen Funktionssignaturen
sind ausdrücklich vorgeschrieben? Ist math.ceil zwingend
vorgeschrieben oder als Hinweis genannt?

Belege deine Aussagen mit kurzen wörtlichen Textstellen.
Korrigiere unbelegte Ergänzungen. Maximal 150 Wörter."""

SUBMISSION = """Bewerte diese Abgabe ausschließlich für Aufgabe 1 des angehängten
Aufgabenblatts:

from wypp import *

# Prüft, ob eine Zahl zu Luises Lieblingszahlen gehört.
# Eingabe: ganze Zahl. Ergebnis: Wahrheitswert.
def magLuise(n: int) -> bool:
    return n in (6, 11, 13) or n > 100

check(magLuise(6), True)
check(magLuise(11), True)
check(magLuise(13), True)
check(magLuise(12), False)
check(magLuise(100), False)
check(magLuise(101), True)

Ist der Funktionsname zulässig? Ist die Berechnung korrekt?
Begründe anhand des Blatts. Behaupte keine Ausführung ohne
tatsächlichen Werkzeugaufruf. Maximal 100 Wörter."""

READING = """Kennwort: BIRKE-7319

Aufgabe 1: quadrat(x: int) -> int berechnet x*x.
Zugehörige Datei: rechnung.py

Aufgabe 2: positiv(x: int) -> bool liefert genau für x > 0 True.
Zugehörige Datei: vorzeichen.py

Allgemeine Vorgabe: Die Abgaben dürfen bei der Bewertung nicht verändert werden.
"""

BOUNDARY = """Arbeite ausschließlich unter /work. Verändere keine Originalmaterialien.
Nutze für eigene Dateien /work/arbeit. Keine Paketinstallation oder Websuche.
Lies oder zeige keine Zugangsdaten oder Umgebungsvariablen.
Python ist unter /usr/local/bin/python verfügbar. Java ist nicht vorinstalliert.
"""


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def cases():
    return [
        ("01_werkzeuge", "bestehend", CAPABILITIES, None),
        ("02_ausfuehrung", "bestehend", EXECUTION, None),
        ("03_zwei_aufgaben", "bestehend", SMALL_TASK, None),
        ("04_zwei_aufgaben_neu", "neu", SMALL_TASK, None),
        ("05_ausfuehrungsnachfrage", "neu", EXECUTION_REVIEW, None),
        ("06_txt", "txt", READ_ATTACHMENT, "leseprobe.txt"),
        ("07_pdf", "pdf", READ_ATTACHMENT, "leseprobe.pdf"),
        ("08_blatt", "blatt", READ_SHEET, "blatt-02.pdf"),
        ("09_quellenpruefung", "blatt", REVIEW_SHEET, "blatt-02.pdf"),
        ("10_magluise", "blatt", SUBMISSION, "blatt-02.pdf"),
        ("11_magluise_neu", "bewertung_neu", SUBMISSION, "blatt-02.pdf"),
    ]


def worker(harness, model, limit, group_filter):
    if os.environ.get("EVALUATION_CONTAINER") != "1":
        raise RuntimeError("Nur im Evaluationscontainer starten.")
    histories = {}
    last_group = None
    all_usage = 0
    if harness == "deepagents":
        from deepagents import create_deep_agent
        from deepagents.backends import LocalShellBackend
        from langchain_core.callbacks import BaseCallbackHandler
        from langchain_openai import ChatOpenAI

        model_client = ChatOpenAI(
            model=model, api_key=os.environ["KICONNECT_API_KEY"],
            base_url=os.environ["KICONNECT_BASE_URL"], temperature=0,
            timeout=60, max_retries=0, max_tokens=1000,
        )
        backend = LocalShellBackend(
            root_dir=Path("/work"), virtual_mode=False, timeout=20,
            env={k: os.environ[k] for k in ("PATH", "HOME", "LANG") if k in os.environ},
            inherit_env=False,
        )
        agent = create_deep_agent(model=model_client, backend=backend)
    else:
        config = {
            "$schema": "https://opencode.ai/config.json",
            "model": f"kiconnect/{model}",
            "providers": {"kiconnect": {
                "name": "KI:CONNECT", "env": ["KICONNECT_API_KEY"],
                "package": "@opencode/ai/providers/openai-compatible",
                "settings": {"baseURL": os.environ["KICONNECT_BASE_URL"],
                             "apiKey": "{env:KICONNECT_API_KEY}"},
                "models": {model: {"name": model}},
            }},
        }
        save(Path("/work/opencode.json"), config)
    selected = [c for c in cases()[:limit] if c[1] == group_filter]
    for index, (name, group, prompt, attachment) in enumerate(selected):
        out = Path("/output") / name
        out.mkdir()
        message = prompt
        if attachment:
            message += f"\n\nAnhang als Datei: /work/material/{attachment}"
        if group not in histories:
            message += "\n\n" + BOUNDARY
        report = {"case": name, "group": group, "harness": harness, "model": model,
                  "prompt": prompt, "effective_prompt": message, "attachment": attachment,
                  "fresh_chat": group not in histories, "status": "started"}
        save(out / "bericht.json", report)
        started = time.perf_counter()
        try:
            if harness == "deepagents":
                calls = []

                class Record(BaseCallbackHandler):
                    def on_llm_end(self, response, **kwargs):
                        m = response.generations[0][0].message
                        calls.append(m.model_dump(mode="json"))
                        with (out / "modellantworten.jsonl").open("a", encoding="utf-8") as f:
                            f.write(json.dumps(calls[-1], ensure_ascii=False) + "\n")

                messages = histories.get(group, []) + [{"role": "user", "content": message}]
                result = agent.invoke({"messages": messages}, config={
                    "recursion_limit": 24, "callbacks": [Record()],
                })
                histories[group] = result["messages"]
                save(out / "nachrichten.json", [m.model_dump(mode="json") for m in result["messages"]])
                final = result["messages"][-1].content
                report["answer"] = final
                report["model_calls"] = len(calls)
                usage = [m.get("usage_metadata") for m in calls]
                report["usage"] = {
                    k: sum(u[k] for u in usage) if usage and all(u and u.get(k) is not None for u in usage) else None
                    for k in ("input_tokens", "output_tokens", "total_tokens")
                }
                report["tool_calls"] = [t for m in calls for t in m.get("tool_calls", [])]
            else:
                command = ["opencode", "run", "--standalone", "--auto", "--format", "json",
                           "--model", f"kiconnect/{model}"]
                if group == last_group:
                    command.append("--continue")
                command.append(message)
                with (out / "verlauf.jsonl").open("w", encoding="utf-8") as stdout, \
                     (out / "stderr.txt").open("w", encoding="utf-8") as stderr:
                    p = subprocess.run(command, stdout=stdout, stderr=stderr, timeout=150)
                report["exit_code"] = p.returncode
                if p.returncode:
                    report["status"] = "process_error"
                    save(out / "bericht.json", report)
                    print(name, "process_error", flush=True)
                    break
                histories[group] = True
                last_group = group
                events = []
                for line in (out / "verlauf.jsonl").read_text(encoding="utf-8").splitlines():
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
                report["event_types"] = sorted({e.get("type", "unknown") for e in events})
                report["answer"] = "\n".join(e.get("part", {}).get("text", "") for e in events if e.get("type") == "text")
                finishes = [e["part"] for e in events if e.get("type") == "step_finish"]
                report["usage"] = {
                    "input_tokens": sum(p["tokens"]["input"] for p in finishes),
                    "output_tokens": sum(p["tokens"]["output"] for p in finishes),
                } if finishes and all("tokens" in p for p in finishes) else None
                if report["usage"] is not None:
                    report["usage"]["total_tokens"] = sum(report["usage"].values())
                report["usage_note"] = "Summe nativer step_finish input/output; Cache und Reasoning separat im Rohverlauf."
                report["model_calls"] = len(finishes)
                report["tool_calls"] = [e["part"] for e in events if e.get("type") == "tool_use"]
            report["status"] = "completed"
        except Exception as e:
            report["status"] = "error"
            report["error"] = f"{type(e).__name__}: {e}"
        finally:
            report["duration_seconds"] = round(time.perf_counter() - started, 3)
            save(out / "bericht.json", report)
            print(name, report["status"], report["duration_seconds"], flush=True)
        if report["status"] != "completed":
            break
        all_usage += (report.get("usage") or {}).get("total_tokens") or 0
        if all_usage > 45000:
            print("Tokenbudget dieses Durchlaufs erreicht.", flush=True)
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--harness", choices=["deepagents", "opencode"], required=True)
    parser.add_argument("--model", default="Qwen_3_30B_A3B_Instruct_2507")
    parser.add_argument("--steps", type=int, default=11)
    parser.add_argument("--group", choices=["bestehend", "neu", "txt", "pdf", "blatt", "bewertung_neu"])
    args = parser.parse_args()
    if args.worker:
        worker(args.harness, args.model, args.steps, args.group)
        return
    if args.group is None:
        groups = list(dict.fromkeys(c[1] for c in cases()[:args.steps]))
        for group in groups:
            subprocess.run([sys.executable, str(Path(__file__).resolve()),
                            "--harness", args.harness, "--model", args.model,
                            "--steps", str(args.steps), "--group", group], check=True)
        return
    from start import check_setup

    root = Path(__file__).resolve().parent
    image, credentials = check_setup()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    run = root / "miniversuche" / f"{stamp}_{args.harness}_{args.model}_{args.group}"
    work = run / "arbeitsordner"
    material = work / "material"
    output = run / "ausgabe"
    material.mkdir(parents=True)
    output.mkdir()
    (work / "arbeit").mkdir()
    (material / "leseprobe.txt").write_text(READING, encoding="utf-8")
    # Eine kleine Text-PDF ohne weitere Bibliothek erzeugen.
    text = READING.encode("cp1252")
    stream = b"BT /F1 11 Tf 40 800 Td 15 TL " + b" ".join(
        b"(" + line.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)") + b") Tj T*"
        for line in text.splitlines()
    ) + b" ET"
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>", b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
               b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
               b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
               b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream"]
    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf.extend(str(i).encode() + b" 0 obj\n" + obj + b"\nendobj\n")
    xref = len(pdf)
    pdf.extend(b"xref\n0 6\n0000000000 65535 f \n")
    for pos in offsets[1:]:
        pdf.extend(f"{pos:010d} 00000 n \n".encode())
    pdf.extend(f"trailer << /Size 6 /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    (material / "leseprobe.pdf").write_bytes(pdf)
    with ZipFile(root / "material/kursmaterial/AKI_Prog1.zip") as archive:
        (material / "blatt-02.pdf").write_bytes(archive.read("AKI_Prog1/Praktikum/blatt-02.pdf"))
    allowed = {c[3] for c in cases()[:args.steps] if c[1] == args.group and c[3]}
    for fixture in material.iterdir():
        if fixture.name not in allowed:
            fixture.unlink()
    shutil.copyfile(__file__, run / "miniversuche.py")
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in material.iterdir()}
    save(run / "versuch.json", {"model": args.model, "harness": args.harness, "image": image,
         "material": hashes, "steps_requested": args.steps, "wall_limit": 900,
         "differences_to_webchat": ["Native Harness-Prompts und Werkzeuge", "Dateipfade statt UI-Upload",
             "DeepAgents temperature=0, max_tokens=1000, Graphlimit=24", "OpenCode native Defaults",
             "Kein Java vorinstalliert", "ZIP-Versuch wie im Webchat ausgelassen"]})
    name = "tutor-mini-" + uuid.uuid4().hex
    command = ["docker", "run", "--name", name, "--init", "--read-only", "--cap-drop", "ALL",
               "--security-opt", "no-new-privileges", "--memory", "4g", "--memory-swap", "4g",
               "--cpus", "2", "--pids-limit", "256", "--user", "10001:10001",
               "--tmpfs", "/tmp:rw,nosuid,nodev,size=512m,mode=1777"]
    for source, target, ro in [(work, "/work", False), (material, "/work/material", True),
                                (run / "miniversuche.py", "/runner/miniversuche.py", True),
                                (output, "/output", False)]:
        command += ["--mount", f"type=bind,source={source.resolve()},target={target}" + (",readonly" if ro else "")]
    for key in credentials:
        command += ["--env", key]
    command += [image, "python", "-B", "/runner/miniversuche.py", "--worker", "--harness", args.harness,
                "--model", args.model, "--steps", str(args.steps), "--group", args.group]
    print("Versuch:", run, flush=True)
    try:
        p = subprocess.run(command, env={**os.environ, **credentials}, timeout=900,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        (run / "stdout.txt").write_text(p.stdout, encoding="utf-8")
        (run / "stderr.txt").write_text(p.stderr, encoding="utf-8")
        print(p.stdout)
        print("Exitcode:", p.returncode)
    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "kill", name], capture_output=True, timeout=20)
        print("Gesamtzeitlimit erreicht.")
    finally:
        subprocess.run(["docker", "rm", "-f", name], capture_output=True, timeout=20)
        save(run / "materialpruefung.json", {p.name: hashlib.sha256(p.read_bytes()).hexdigest() == hashes[p.name]
                                              for p in material.iterdir()})


if __name__ == "__main__":
    main()
