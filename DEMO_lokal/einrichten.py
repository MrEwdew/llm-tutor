import os
import subprocess
from importlib.metadata import version
from pathlib import Path

ROOT = Path(__file__).resolve().parent


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
    import wypp
    print("WYPP:", version("wypp"))
    print("Keine Modellanfrage ausgefuehrt.")


import sys


def main():
    if "--check" not in sys.argv:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")
        ], check=True)
    check_setup()


if __name__ == "__main__":
    main()
