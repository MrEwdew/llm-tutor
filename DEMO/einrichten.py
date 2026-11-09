import argparse
import os
import subprocess
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMAGE = "tutor-python-test"


def check_setup():
    from deepagents import create_deep_agent
    from langchain_openai import ChatOpenAI
    from dotenv import dotenv_values

    print("DeepAgents und ChatOpenAI importierbar.")
    for name in ("deepagents", "langchain", "langchain-openai", "langgraph"):
        print(f"{name}: {version(name)}")
    values = dotenv_values(ROOT.parent / ".env")
    for name in ("KICONNECT_API_KEY", "KICONNECT_BASE_URL"):
        print(name + ":", "vorhanden" if values.get(name) or os.getenv(name) else "fehlt")
    process = subprocess.run(
        ["docker", "image", "inspect", IMAGE, "--format", "{{.Id}} {{.Config.User}}"],
        capture_output=True, text=True, timeout=15,
    )
    if process.returncode != 0:
        raise RuntimeError("Docker Desktop starten und Testimage bereitstellen.")
    print("Docker-Testimage:", process.stdout.strip())
    print("Keine Modellanfrage ausgefuehrt.")


def main():
    parser = argparse.ArgumentParser(description="Separate Demo-Umgebung vorbereiten")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--online", action="store_true", help="Downloads erlauben")
    args = parser.parse_args()
    if args.check:
        check_setup()
        return

    root = Path(__file__).resolve().parent
    environment = root / ".venv"
    python = environment / "Scripts" / "python.exe"
    options = [] if args.online else ["--offline"]

    if not python.is_file():
        subprocess.run(
            ["uv", "venv", *options, "--python", "3.13", str(environment)],
            check=True,
        )

    subprocess.run([
        "uv", "pip", "install", *options, "--python", str(python),
        "-r", str(root / "requirements.txt"),
    ], check=True)
    subprocess.run([
        str(python), "-X", "utf8", str(root / "einrichten.py"), "--check"
    ], check=True)


if __name__ == "__main__":
    try:
        main()
    except (OSError, subprocess.CalledProcessError) as error:
        print(f"Einrichtung fehlgeschlagen: {error}")
        print("Bei fehlenden Downloads: python DEMO/einrichten.py --online")
        raise SystemExit(1)
