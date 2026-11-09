import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from korrektur_prompt import PROMPT

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / "src"))
MODELL = "Qwen_3_30B_A3B_Instruct_2507"


# Lädt die festen Demo-Tests und übergibt sie an die gemeinsame Ausführung.
# Bereitet die festen Vergleichstests der Boot-Aufgabe vor.
def load_tests():
    tests = json.loads(
        (ROOT / "vergleichstests.json").read_text(encoding="utf-8")
    )

    for test in tests:
        test["function"] = "bootstrecke"

    return tests


# Führt die Demo-Tests ohne Modellbewertung aus.
def run_tests(code):
    from python_tests import run_python_tests

    return run_python_tests(code, load_tests())

def show_tests(result):
    if result.get("status") != "completed":
        print("Ausfuehrungsproblem:", json.dumps(result, ensure_ascii=False))
        return
    tests = result["tests"]
    for test in tests:
        actual = test.get("actual", test.get("error"))
        print(
            f"  {test['args']}: erwartet {test['expected']}, erhalten {actual}"
            f" -> {'BESTANDEN' if test['passed'] else 'FEHLGESCHLAGEN'}"
        )
    print(f"Vergleichstests: {sum(t['passed'] for t in tests)}/{len(tests)} bestanden")
    if result.get("embedded_output"):
        print("Zusaetzliche Meldungen enthaltener Abgabetests:")
        print(result["embedded_output"].rstrip())


def correct_submission(code, content=None):
    from dotenv import load_dotenv
    from llm import get_llm
    from correction_agent import correct_python_submission

    load_dotenv(ROOT.parent / ".env", override=True)

    llm = get_llm(
        modell_name=MODELL,
        api=os.environ["KICONNECT_API_KEY"],
        base_url=os.environ["KICONNECT_BASE_URL"],
        temperature=0,
        timeout=60,
        max_retries=0,
        max_tokens=700,
    )

    if content is None:
        task = (ROOT / "material" / "aufgabe_06.txt").read_text(
            encoding="utf-8"
        )
        content = f"{task}\n\nDatei: aufgabe_06.py\n```python\n{code}\n```"

    summary = correct_python_submission(
        content=content,
        code=code,
        tests=load_tests(),
        llm=llm,
        prompt=PROMPT,
    )
    summary["model"] = MODELL

    show_tests(summary["test_result"])

    return summary

def show_feedback(result):
    print("\nFeedback:", result["feedback"])
    print("Modell:", result["model"])
    print("Modellaufrufe:", result["model_calls"])
    print("Tokens:", result["usage"], "(None = unbekannt)")
    print("Dauer:", result["duration_seconds"], "Sekunden")


def main():
    variants = {"1": "gut", "2": "mittel", "3": "schlecht", "a": "alle"}
    choice = input("Abgabe (1=gut, 2=mittel, 3=schlecht, a=alle): ").strip().lower()
    if choice not in variants:
        raise ValueError("Unbekannte Abgabe.")
    mode = input("Modus (1=live, 2=nur Tests, 3=gespeichert): ").strip()
    if mode not in ("1", "2", "3"):
        raise ValueError("Unbekannter Modus.")
    selected = ("gut", "mittel", "schlecht") if choice == "a" else (variants[choice],)
    for name in selected:
        print("\nAbgabe:", name)
        if mode == "3":
            print("Gespeicherter Containerlauf vom 03.11.2026, kein neuer Lauf.")
            result = json.loads((ROOT / "gespeichert" / f"{name}.json").read_text(encoding="utf-8"))
            show_tests(result["test_result"])
            show_feedback(result)
            continue
        code = (ROOT / "abgaben" / name / "aufgabe_06.py").read_text(encoding="utf-8-sig")
        if mode == "2":
            result = run_tests(code)
            show_tests(result)
            if result["status"] != "completed":
                raise RuntimeError("Testausführung abgebrochen.")
            continue
        result = correct_submission(code)
        show_feedback(result)
        output = ROOT / "ergebnisse"
        output.mkdir(exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        result["variant"] = name
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
