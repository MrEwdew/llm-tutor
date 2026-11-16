import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    from dotenv import load_dotenv

    run = Path(sys.argv[1])
    report = json.loads((run / "bericht.json").read_text(encoding="utf-8"))
    load_dotenv(Path(report["project_root"]) / ".env", override=True)
    executable = shutil.which("opencode")
    if executable is None:
        raise FileNotFoundError("OpenCode ist nicht im PATH installiert.")
    if Path(executable).suffix.lower() in {".cmd", ".bat"}:
        raise RuntimeError("Fuer diesen Adapter die native OpenCode-EXE verwenden.")
    installed = subprocess.run(
        [executable, "--version"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=20,
        check=True,
    ).stdout.strip()

    version_number = installed.removeprefix("opencode ").removeprefix("v")

    if not version_number.startswith("2."):
        raise RuntimeError(
            "OpenCode-Version zuerst pruefen: Adapter erwartet V2."
        )
    # Dieser Adapter verwendet das aktuelle V2-Konfigurationsformat.
    config = {
        "$schema": "https://opencode.ai/config.json",
        "model": f"kiconnect/{sys.argv[2]}",
        "providers": {
            "kiconnect": {
                "name": "KI:CONNECT", "env": ["KICONNECT_API_KEY"],
                "package": "@opencode/ai/providers/openai-compatible",
                "settings": {"baseURL": os.environ["KICONNECT_BASE_URL"],
                             "apiKey": "{env:KICONNECT_API_KEY}"},
                "models": {sys.argv[2]: {"name": sys.argv[2]}},
            }
        },
    }
    (run / "arbeitsordner/opencode.json").write_text(
        json.dumps(config, indent=2), encoding="utf-8",
    )
    prompt = (run / "auftrag.txt").read_text(encoding="utf-8")
    prompt += f"\nPython fuer Ausfuehrungen: {sys.executable}\n"
    command = [executable, "run", "--standalone", "--auto", "--format", "json",
               "--model", f"kiconnect/{sys.argv[2]}", prompt]
    (run / "adapter.json").write_text(json.dumps({
        "version": installed, "usage": None,
        "usage_scope": "raw_events_only_parser_pending",
        "settings": "OpenCode defaults; provider settings in workspace/opencode.json",
    }, indent=2), encoding="utf-8")
    with (run / "verlauf.jsonl").open("w", encoding="utf-8") as output:
        process = subprocess.run(command, stdout=output, check=False)
    raise SystemExit(process.returncode)


if __name__ == "__main__":
    main()
