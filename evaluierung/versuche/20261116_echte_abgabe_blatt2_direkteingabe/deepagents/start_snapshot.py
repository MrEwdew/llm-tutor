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
PROMPT = 'Pruefe eine vollstaendige studentische Abgabe zu einem Aufgabenblatt.\nDie vollstaendige vorbereitete Eingabe folgt direkt in dieser Nachricht. Lies sie vollstaendig; kein Dateiaufruf zum Nachladen dieser Eingabe erforderlich. Sie enthaelt Aufgaben, allgemeine und abschliessende Blattvorgaben, unveraenderten Code, tatsaechliche Archivpfade und statische Python-Funktionsinventare. Die Vorbereitung stammt aus unserem Projektcode; sie enthaelt keine ausgefuehrten Tests. Dateinamensvorschlaege sind unbestaetigt: pruefe die fachliche Zuordnung selbst.\nDie unveraenderten Originaldateien liegen unter /work/material/ gefolgt vom jeweiligen Archivpfad, beispielsweise entspricht Archivpfad abgabe/DATEI.py dem Pfad /work/material/abgabe/DATEI.py. Keine ZIP oder PDF mehr erschliessen. Keine Dateien umbenennen oder reparieren.\nEntwickle eigene Tests mit aus den Aufgaben begruendeten Sollwerten. Erstelle Testdateien unter /work/arbeit und starte sie tatsaechlich gegen die Originaldateien. Funktionsnamen und benoetigte Imports selbst aus dem Inventar bzw. Code bestimmen. Keine Ersatzloesungen, keine kopierten oder reparierten Funktionsdefinitionen. Nur vorhandene check-Aufrufe zu lesen ist keine Ausfuehrung und kein eigener Test.\nWYPP-Hilfe: from wypp import check; check(istwert, sollwert), genau zwei Argumente. Beschreibungen als Kommentare. Exitcode 0 allein beweist nicht, dass Checks bestehen: Ausgabe beachten. Eingebettete Abgabetests von Zusatztests unterscheiden. Fehler des eigenen Testaufbaus nicht als Abgabefehler ausgeben.\nFunktionsnamen und Typen nur als vorgeschrieben behandeln, wenn die Aufgabenstellung sie vorgibt; Hinweise nicht als zwingende Operationsvorgaben erfinden. Kommentare, Datenbeschreibung, Typangaben und Abgabetests anhand Code und Blattvorgaben bewerten. Keine zeitliche Entwicklungsreihenfolge unterstellen. Keine automatische Note.\nPython 3.13, wypp und pytest sind vorhanden. Keine Paketinstallation, Websuche oder Delegation. Keine Zugangsdaten oder Umgebungsvariablen lesen. Nur unter /work arbeiten. Originale nicht veraendern.\nAbschluss maximal 400 Woerter: Zuordnung, je Aufgabe tatsaechlich gestarteter Testbefehl und beobachtete Ausgabe, belegte Fehler, formale Befunde und offene Punkte. Nicht getestete Teile ausdruecklich als Nicht ausgefuehrt kennzeichnen. Keine Ausfuehrung erfinden. Maximal zehn Modellstarts, keine automatische Wiederholung.\n\n\n=== VOLLSTAENDIGE VORBEREITETE EINGABE ===\nAllgemeine Blattvorgaben:\nProf. Dr. Stefan Wehr, Simon Rösch\nÜbungsblatt 2\nAKI Programmierung 1, Wintersemester 2026/2027\nDeadline: 26.10.2026, 23:00 Uhr\n20.10.2026\nGehen Sie beim Lösen aller Programmieraufgaben strikt nach unserem Schema vor:\n1. Schreiben Sie zuerst eine Kurzbeschreibung als Kommentar.\n2. Führen Sie dann eine Datenanalyse durch. Schreiben Sie das Ergebnis Ihrer Datenanalyse\nebenfalls als Kommentar in die Zeile nach der Kurzbeschreibung.\n3. Schreiben Sie dann den Funktionskopf inkl. der Typen für Argumente und Ergebnis hin.\n4. Schreiben Sie dann Tests mittels check.\n5. Setzen Sie die passenden Schablonen in den Rumpf der Funktion ein.\n6. Schreiben Sie erst dann den Funktionsrumpf hin.\nEine Lösung, in der nicht ersichtlich ist, dass Sie gemäß des Schemas aggiert haben, erhält keine\nPunkte. Insbesondere erhält eine Lösung, bei der nur der Funktionsrumpf da steht, keine Punkte,\nauch wenn die Funktion korrekt ist.\nDahingegen erhalten Sie Teilpunkte wenn Sie dem Schema folgen, aber an einem gewissen Punkt\nnicht weiterkommen.\n\nAufgaben:\n\nAufgabe 1 (6 Punkte)\nGeorg fragt die kleine Luise nach ihrer Lieblingszahl. Luise sagt: „Also, ich habe vielen Lieb-\nlingszahlen. Ich mag die 6, weil ich 6 Jahre alt. Außerdem mag ich die 11 und die 13. Die 12\nmag ich aber nicht. Dafür mag ich alle Zahlen größer als 100. “\nGeorg ist leicht überfordert. Helfen Sie ihm, indem Sie eine Funktion schreiben, welche den\nbooleschen Wert für „wahr“ liefert falls die Eingabezahl eine von Luises Lieblingszahlen ist.\n\nExakt zugeordnete Dateien:\n\nErwartete Datei: aufgabe_01.py\nKeine exakt passende Datei zugeordnet. Weitere Dateien stehen im Abschnitt unten.\n\nAufgabe 2 (8 Punkte)\nBeim Fußball lässt die Rückennummer einer Spielerin häufig Rückschlüsse auf ihre Position zu.\nWir machen dabei folgende Annahmen:\n• Ein Torhüterin hat die Rückennummer 1.\n• Ein Abwehrspielerin hat die Rückennummer 2, 3, 4 oder 5.\n• Ein Mittelfeldspielerin hat die Rückennummer 6, 7, 8 oder 10.\n• Ein Stürmerin hat die Rückennummer 9 oder 11.\n• Ein Ersatzspielerin hat eine Rückennummer zwischen 12 und 99\n1\nÜbungsblatt 2 AKI Programmierung 1\n• Alle anderen Rückennummern sind ungültig.\nSchreiben Sie zunächst eine Datenbeschreibung für Positionen und dann eine passende Typde-\nfinition. Schreiben Sie dann eine Funktion, die für eine Rückennummer die passende Position\nbestimmt. Dabei dürfen Sie eine ungültige Eingabe ignorieren.\n\nExakt zugeordnete Dateien:\n\nErwartete Datei: aufgabe_02.py\nKeine exakt passende Datei zugeordnet. Weitere Dateien stehen im Abschnitt unten.\n\nAufgabe 3 (8 Punkte)\nSchreibe ein Programm, mit dem Bußgelder für zu langes Parken automatisch bestimmt werden.\nDie Bußgelder sind in Abhängigkeit der Überschreitungsdauer der Höchstparkdauer wie folgt\nfestgelegt:\n• Bis zu 30 Minuten: 10 Euro.\n• Bis zu einer Stunde: 15 Euro.\n• Bis zu zwei Stunden: 20 Euro\n• Bis zu drei Stunden: 25 Euro\n• Länger als drei Stunden: (n − 1) · 10 Euro, wobei n die Parkdauer aufgerundet auf die\nnächste ganze Stunde ist.\nAufrunden funktioniert mit math.ceil.\n\nExakt zugeordnete Dateien:\n\nErwartete Datei: aufgabe_03.py\nKeine exakt passende Datei zugeordnet. Weitere Dateien stehen im Abschnitt unten.\n\nAufgabe 4 (8 Punkte)\nSchreiben Sie eine Funktion clamp, die wie folgt definiert ist:\nclamp(x, l, u) =\n\uf8f1\n\uf8f2\n\uf8f3\nx if l ≤ x ≤ u\nl if x < l\nu if x > u\nDabei sind x, l, u∈ R. Der Name l steht dabei für „lower bound“, da l eine untere Schranke für\nden Wert von x angibt. Analog steht u für „upper bound“ .\n\nExakt zugeordnete Dateien:\n\nErwartete Datei: aufgabe_04.py\nKeine exakt passende Datei zugeordnet. Weitere Dateien stehen im Abschnitt unten.\n\nAbschliessende Blattvorgaben:\nGesamtpunkte: 30\nAbgabe\nVia Upload im Praktomat bis 26.10.2026, 23:00 Uhr . Speichern Sie jede Programmieren-\naufgabe in eine eigene Datei. Der Name der Datei muss dabei aufgabe_0N.py sein, wobei N\ndie Nummer der Aufgabe ist. Zum Beispiel lautet für Aufgabe 1 der Name der Datei dann\naufgabe_01.py.\nVerpacken Sie alle Dateien in einem zip-Archiv (Standard-Zip, keine 7zip, rar o.ä.), welches den\nNamen NAME_MATRIKELNUMMER.zip hat. Ersetzen Sie dabei NAME und MATRIKELNUMMER durch\nIhren Namen und Ihre Matrikelnummer. Es ist wichtig, dass Sie sich an die Namenskonventionen\nhalten, die wir Abgaben automatisch überprüfen.\nWichtig: Die Lösungen für alle Programmieraufgaben müssen ohne Fehler ausführbar sein, sonst\nakzeptiert der Praktomat Ihre Abgabe nicht. Wenn der Praktomat nach dem Upload für eine\noder mehrere Aufgaben den Status failed anzeigt, wird ihre komplette Abgabe nicht akzpe-\ntiert und Sie erhalten für das komplette Blatt 0 Punkte! Kommentieren Sie fehlerhafte\nCodestellen in einem solche Fall aus, so dass der Praktomat Ihre Abgabe akzeptiert.\n2\n\nNicht exakt zugeordnete Dateien:\n\nDatei: Aufgabe4.py\nArchivpfad: abgabe/Aufgabe4.py\nUnbestaetigter Dateinamensvorschlag: Aufgabe 4. Die fachliche Zugehoerigkeit ist noch zu pruefen.\nCode:\nfrom wypp import *\n\n# Beschreibung: Begrenzt eine Zahl auf den Bereich von l bis u\n# Eingabe: x, untere Grenze l und obere Grenze u (Typ: float)\n# Ergebnis: x innerhalb des bereiches (Typ: float)\n\ndef clamp(x: float, l: float, u: float) -> float:\n    if x < l:\n        return l\n    elif x > u:\n        return u\n    else:\n        return x\n\n\ncheck(clamp(5, 67.5, 89.5), 67.5)\ncheck(clamp(-2, 0, 10), 0)\ncheck(clamp(27.5, 0, 10), 10)\ncheck(clamp(5.5, 0 , 0), 0)\ncheck(clamp(10, 0, 10), 10)\ncheck(clamp(2.5, 1 , 3), 2.5)\ncheck(clamp(-4, -3, -1), -3)\ncheck(clamp(7, 3, 3), 3)\n\nDatei: Aufgabe1.py\nArchivpfad: abgabe/Aufgabe1.py\nUnbestaetigter Dateinamensvorschlag: Aufgabe 1. Die fachliche Zugehoerigkeit ist noch zu pruefen.\nCode:\nfrom wypp import *\n\n# Funktion schreiben für einen booleschen wert der TRUE ergibt wenn es Luisaslieblingszahl ist\n# Eingabe\n# Ergebnis\n\ndef luisasLieblingsZahlen(Zahl: float) -> bool:\n   return Zahl in(6, 11, 13) or Zahl > 100\n\ncheck(luisasLieblingsZahlen(6), True)\ncheck(luisasLieblingsZahlen(11), True)\ncheck(luisasLieblingsZahlen(12), False)\ncheck(luisasLieblingsZahlen(13), True)\ncheck(luisasLieblingsZahlen(100), False)\ncheck(luisasLieblingsZahlen(100.1), True)\ncheck(luisasLieblingsZahlen(9999), True)\n\n\nDatei: Aufgabe2.py\nArchivpfad: abgabe/Aufgabe2.py\nUnbestaetigter Dateinamensvorschlag: Aufgabe 2. Die fachliche Zugehoerigkeit ist noch zu pruefen.\nCode:\nfrom wypp import *\n\n# Gibt der Spielertyp eine Rückennummer\n# Eingabe: Spielertyp\n# Ergebnis: Rückennummer als int\n# DATENBESCHREIBUNG\n# Eine spielerKlasse ist:\n# - Torhueter -\n# - Abwehrspieler -\n# - Mittelfeldspieler -\n# - Stuermer -\n# - Ersatzspieler -\n# TYPDEFINITION\ntype spielerKlasse = Literal["Torhueter", "Abwehrspieler", "Mittelfeldspieler", "Stuermer", "Ersatzspieler" ]\n\n\n\n\ndef rueckenNummer(rueckenNummer: int) -> str:\n    if rueckenNummer == (1):\n        return "Torhueter"\n    elif rueckenNummer == (2 or 3 or 4 or 5):\n        return "Abwehrspieler"\n    elif rueckenNummer == (6 or 7 or 8 or 10):\n        return "Mittelfeldspieler"\n    elif rueckenNummer == (9 or 11):\n        return "Stuermer"\n    elif rueckenNummer <= 99:\n        return "Ersatzspieler"\n    \n    \n    \n\n\n\n\n\n\ncheck(rueckenNummer(1), "Torhueter")\ncheck(rueckenNummer(2), "Abwehrspieler")\ncheck(rueckenNummer(6), "Mittelfeldspieler")\ncheck(rueckenNummer(9), "Stuermer")\ncheck(rueckenNummer(67), "Ersatzspieler")\n\n\nDatei: Aufgabe3.py\nArchivpfad: abgabe/Aufgabe3.py\nUnbestaetigter Dateinamensvorschlag: Aufgabe 3. Die fachliche Zugehoerigkeit ist noch zu pruefen.\nCode:\nfrom wypp import *\n\n\n# Automatisches zuordnen von Bußgeldern für zu Langes Parken\n# Eingabe: Stunden anzahl in Minuten (Typ: int)\n# Ergebnis: Bußgeldbescheid in Euro (Typ: int)\n\ndef bussgeldbescheid(parkzeitueberschritt: int) -> int:\n    if parkzeitueberschritt <= 30:\n        return (10)\n    elif parkzeitueberschritt <= 60 :\n        return (15)\n    elif parkzeitueberschritt <= 120:\n        return (20)\n    elif parkzeitueberschritt <= 180:\n        return (25)\n    elif parkzeitueberschritt > 180:\n       return (((math.ceil(parkzeitueberschritt/60) - 1) * 10)) \n    \n\n\n\ncheck(bussgeldbescheid(30), 10)\ncheck(bussgeldbescheid(31), 15)\ncheck(bussgeldbescheid(60), 15)\ncheck(bussgeldbescheid(61), 20)\ncheck(bussgeldbescheid(120), 20)\ncheck(bussgeldbescheid(121), 25)\ncheck(bussgeldbescheid(180), 25)\ncheck(bussgeldbescheid(181), 30)\ncheck(bussgeldbescheid(600), 90)\n\nStatische Python-Befunde, ohne Codeausfuehrung:\n\nArchivpfad: abgabe/Aufgabe4.py\n\nZeile 7: clamp(x: float, l: float, u: float) -> float\n\nArchivpfad: abgabe/Aufgabe1.py\n\nZeile 7: luisasLieblingsZahlen(Zahl: float) -> bool\n\nArchivpfad: abgabe/Aufgabe2.py\n\nZeile 19: rueckenNummer(rueckenNummer: int) -> str\n\nArchivpfad: abgabe/Aufgabe3.py\n\nZeile 8: bussgeldbescheid(parkzeitueberschritt: int) -> int'









def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def deepagents_worker():
    from deepagents import create_deep_agent
    from deepagents.backends import LocalShellBackend
    from langchain.agents.middleware import ModelCallLimitMiddleware
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_openai import ChatOpenAI

    class Record(BaseCallbackHandler):
        raise_error = True
        calls = 0

        def on_chat_model_start(self, serialized, messages, **kwargs):
            if self.calls >= 10:
                raise RuntimeError("Modelllimit erreicht: zehn Aufrufe einschliesslich Unteragenten.")
            self.calls += 1
            self.write("model_start", {"number": self.calls})

        def on_llm_error(self, error, **kwargs):
            self.write("model_error", {"type": type(error).__name__, "message": str(error)})

        def on_llm_end(self, response, **kwargs):
            self.write("model", response.generations[0][0].message.model_dump(mode="json"))

        def on_tool_end(self, output, **kwargs):
            value = output.model_dump(mode="json") if hasattr(output, "model_dump") else str(output)
            self.write("tool", value)

        def write(self, kind, value):
            with Path("/output/verlauf.jsonl").open("a", encoding="utf-8") as f:
                f.write(json.dumps({"kind": kind, "value": value}, ensure_ascii=False, default=str) + "\n")

    backend = LocalShellBackend(root_dir=Path("/work"), virtual_mode=False, timeout=20,
                               env={k: os.environ[k] for k in ("PATH", "HOME", "LANG") if k in os.environ},
                               inherit_env=False)
    llm = ChatOpenAI(model=MODEL, api_key=os.environ["KICONNECT_API_KEY"],
                     base_url=os.environ["KICONNECT_BASE_URL"], temperature=0,
                     max_tokens=1000, timeout=60, max_retries=0)
    agent = create_deep_agent(model=llm, backend=backend,
                             middleware=[ModelCallLimitMiddleware(run_limit=10)])
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": PROMPT}]},
                              config={"recursion_limit": 100, "callbacks": [Record()]})
        save(Path("/output/nachrichten.json"), [m.model_dump(mode="json") for m in result["messages"]])
    except Exception as e:
        save(Path("/output/fehler.json"), {"type": type(e).__name__, "message": str(e)})
        raise


def worker(harness):
    deepagents_worker()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--harness", choices=["deepagents"], default="deepagents")
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
    originals = {str(p.relative_to(work / "material")).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (work / "material").rglob("*") if p.is_file()}
    report = {"model": MODEL, "harness": args.harness, "image": image,
              "status": "prepared", "model_steps_limit": 10, "wall_limit_seconds": 120,
              "prompt": PROMPT, "material_sha256": originals,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "src_used": True, "support": "pypdf-Hinweis und WYPP-Schnittstelle; keine konkreten Imports oder Tests",
              "permissions": "OpenCode: Subagent und Webtools nativ untersagt; DeepAgents: Auftrag untersagt Delegation, Callback begrenzt alle Modellstarts"}
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
        report["material_unchanged"] = all(hashlib.sha256(p.read_bytes()).hexdigest() == originals[str(p.relative_to(work / "material")).replace("\\", "/")]
                                           for p in (work / "material").rglob("*") if p.is_file())
        save(run / "bericht.json", report)
        subprocess.run(["docker", "rm", "-f", name], capture_output=True, timeout=10)
    print(report["status"], report["duration_seconds"], flush=True)


if __name__ == "__main__":
    main()
