import contextlib
import io
import json
import math
import runpy
import sys
from pathlib import Path


# Ruft die angegebene Funktion auf und prüft ihren Rückgabewert.
def run_test(module: dict, test: dict) -> dict:
    result = {
        "function": test["function"],
        "args": test["args"],
        "expected": test["expected"],
    }

    try:
        actual = module[test["function"]](*test["args"])
        numeric = (
            isinstance(actual, (int, float))
            and not isinstance(actual, bool)
            and math.isfinite(actual)
        )

        result["actual"] = actual if numeric else repr(actual)
        result["passed"] = numeric and math.isclose(
            actual,
            test["expected"],
            rel_tol=1e-9,
            abs_tol=1e-9,
        )

    except Exception as error:
        result["passed"] = False
        result["error"] = f"{type(error).__name__}: {error}"

    return result


# Lädt die Abgabe und hält ihre Ausgabe vom JSON-Ergebnis getrennt.
def main():
    payload = json.load(sys.stdin)
    path = Path("abgabe.py")
    path.write_text(payload["code"], encoding="utf-8")

    embedded_output = io.StringIO()
    with contextlib.redirect_stdout(embedded_output):
        module = runpy.run_path(str(path))

    test_output = io.StringIO()
    with contextlib.redirect_stdout(test_output):
        results = [
            run_test(module, test)
            for test in payload["tests"]
        ]

    print(json.dumps({
        "status": "completed",
        "tests": results,
        "embedded_output": embedded_output.getvalue()[:1500],
        "test_output": test_output.getvalue()[:1500],
        "note": "Abgabeausgabe und Vergleichstestergebnisse sind getrennt.",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()