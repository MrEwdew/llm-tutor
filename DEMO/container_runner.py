import contextlib
import io
import json
import math
import runpy
import sys
from pathlib import Path


payload = json.load(sys.stdin)
path = Path("/tmp/abgabe.py")
path.write_text(payload["code"], encoding="utf-8")

captured = io.StringIO()
with contextlib.redirect_stdout(captured):
    module = runpy.run_path(str(path))

results = []
for test in payload["tests"]:
    entry = {"args": test["args"], "expected": test["expected"]}
    try:
        actual = module["bootstrecke"](*test["args"])
        entry["actual"] = actual
        entry["passed"] = (
            isinstance(actual, (int, float))
            and not isinstance(actual, bool)
            and math.isclose(actual, test["expected"], rel_tol=1e-9, abs_tol=1e-9)
        )
    except Exception as error:
        entry["passed"] = False
        entry["error"] = f"{type(error).__name__}: {error}"
    results.append(entry)

print(json.dumps({
    "status": "completed",
    "tests": results,
    "embedded_output": captured.getvalue()[:1500],
    "note": "Embedded output is separate from the three comparison tests.",
}))
