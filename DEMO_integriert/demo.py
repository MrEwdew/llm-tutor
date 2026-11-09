import json
import sys
from datetime import datetime
from pathlib import Path

from eingabe import load_input

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "DEMO_lokal"))

import demo as local_demo


def main():
    variants = {"1": "gut", "2": "mittel", "3": "schlecht", "a": "alle"}
    choice = input("Abgabe (1=gut, 2=mittel, 3=schlecht, a=alle): ").strip().lower()
    mode = input("Modus (1=live, 2=nur Tests, 3=nur Eingabe prüfen): ").strip()
    if choice not in variants or mode not in ("1", "2", "3"):
        raise ValueError("Unbekannte Auswahl.")
    selected = ("gut", "mittel", "schlecht") if choice == "a" else (variants[choice],)
    for name in selected:
        prepared = load_input(name)
        print("\nAbgabe:", name)
        print("Aufgaben im Blatt:", prepared["task_count"])
        print("Datei zu Aufgabe 6:", prepared["path"])
        print("Funktionen:", [function["name"] for function in prepared["functions"] or []])
        print("Checks in der Referenz:", prepared["reference_checks"])
        if prepared["syntax_error"]:
            raise ValueError("Syntaxfehler: " + str(prepared["syntax_error"]))
        if mode == "3":
            print(prepared["content"])
            print("Referenz separat geladen, nicht ausgeführt und nicht ans Modell gesendet.")
            continue
        if mode == "2":
            result = local_demo.run_tests(prepared["code"])
            local_demo.show_tests(result)
            if result["status"] != "completed":
                raise RuntimeError("Testausführung abgebrochen.")
            continue
        result = local_demo.correct_submission(prepared["code"], prepared["content"])
        local_demo.show_feedback(result)
        output = ROOT / "ergebnisse"
        output.mkdir(exist_ok=True)
        result["variant"] = name
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        (output / f"{stamp}_{name}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        main()
    except Exception as error:
        print(f"Abbruch: {type(error).__name__}: {error}")
        raise SystemExit(1)
