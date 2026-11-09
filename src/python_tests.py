import json
import subprocess
import sys
import tempfile
from pathlib import Path


# Prüft numerische Rückgabewerte in einem eigenen Python-Prozess.
def run_python_tests(code: str, tests: list, timeout: float = 10) -> dict:
    runner = Path(__file__).with_name("python_test_runner.py")
    payload = {"code": code, "tests": tests}

    try:
        with tempfile.TemporaryDirectory(prefix="tutor-test-") as directory:
            process = subprocess.run(
                [sys.executable, "-I", "-B", str(runner)],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=timeout,
                cwd=directory,
            )

        if process.returncode != 0:
            return {
                "status": "execution_error",
                "exit_code": process.returncode,
                "stdout": process.stdout[:1500],
                "stderr": process.stderr[:1500],
            }

        return json.loads(process.stdout)

    except subprocess.TimeoutExpired:
        return {"status": "timeout"}
    except (OSError, ValueError) as error:
        return {
            "status": "tool_error",
            "message": str(error),
        }