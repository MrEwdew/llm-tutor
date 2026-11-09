import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from korrektur_prompt import PROMPT

ROOT = Path(__file__).resolve().parent
MODELL = "Qwen_3_30B_A3B_Instruct_2507"
IMAGE = "tutor-python-test"


def run_tests(code):
    name = "tutor-demo-" + uuid4().hex
    payload = {
        "code": code,
        "tests": json.loads((ROOT / "vergleichstests.json").read_text(encoding="utf-8")),
    }
    command = [
        "docker", "run", "--rm", "-i", "--name", name,
        "--network", "none", "--memory", "256m", "--memory-swap", "256m",
        "--cpus", "1", "--pids-limit", "64", "--read-only",
        "--tmpfs", "/tmp:rw,noexec,nosuid,size=16m",
        "--cap-drop", "ALL", "--security-opt", "no-new-privileges=true",
        IMAGE, "timeout", "--kill-after=2s", "10s", "python", "-B", "-c",
        (ROOT / "container_runner.py").read_text(encoding="utf-8"),
    ]
    try:
        process = subprocess.run(
            command, input=json.dumps(payload), capture_output=True,
            text=True, encoding="utf-8", timeout=20,
        )
        if process.returncode == 0:
            result = json.loads(process.stdout)
        else:
            result = {
                "status": "timeout" if process.returncode == 124 else "execution_error",
                "exit_code": process.returncode,
                "stdout": process.stdout[:1500],
                "stderr": process.stderr[:1500],
            }
    except subprocess.TimeoutExpired:
        result = {"status": "outer_timeout"}
    except Exception as error:
        result = {"status": "tool_error", "message": f"{type(error).__name__}: {error}"}
    finally:
        try:
            subprocess.run(
                ["docker", "rm", "-f", name], capture_output=True, timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired):
            print("Hinweis: Containerbereinigung pruefen:", name, flush=True)
    return result


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


def correct_submission(code):
    from dotenv import load_dotenv
    from deepagents import create_deep_agent
    from langchain_openai import ChatOpenAI
    from langchain.agents.middleware import wrap_model_call
    from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

    load_dotenv(ROOT.parent / ".env", override=True)
    test_result = []

    def run_submission_tests() -> str:
        """Prüft die Abgabe mit drei festen Vergleichstests."""
        if not test_result:
            test_result.append(run_tests(code))
            show_tests(test_result[0])
        return json.dumps(test_result[0], ensure_ascii=False)

    @wrap_model_call
    def restrict_tools(request, handler):
        tested = any(
            isinstance(message, ToolMessage) and message.name == "run_submission_tests"
            for message in request.state["messages"]
        )
        tools = [] if tested else [
            tool for tool in request.tools if tool.name == "run_submission_tests"
        ]
        return handler(request.override(tools=tools))

    llm = ChatOpenAI(
        model=MODELL, api_key=os.environ["KICONNECT_API_KEY"],
        base_url=os.environ["KICONNECT_BASE_URL"], temperature=0,
        timeout=60, max_retries=0, max_tokens=700,
    )
    agent = create_deep_agent(
        model=llm, tools=[run_submission_tests],
        middleware=[restrict_tools], system_prompt=PROMPT,
    )
    task = (ROOT / "material" / "aufgabe_06.txt").read_text(encoding="utf-8")
    content = f"{task}\n\nDatei: aufgabe_06.py\n```python\n{code}\n```"
    start = time.perf_counter()
    result = agent.invoke(
        {"messages": [HumanMessage(content=content)]}, {"recursion_limit": 8}
    )
    duration = round(time.perf_counter() - start, 2)
    answers = [message for message in result["messages"] if isinstance(message, AIMessage)]
    if not test_result or answers[-1].tool_calls or not answers[-1].content:
        raise RuntimeError("Testausführung oder Abschlussantwort fehlt.")
    usage = {}
    for field in ("input_tokens", "output_tokens", "total_tokens"):
        values = [(answer.usage_metadata or {}).get(field) for answer in answers]
        usage[field] = sum(values) if all(value is not None for value in values) else None
    return {
        "model": MODELL, "feedback": answers[-1].content,
        "test_result": test_result[0], "usage": usage,
        "model_calls": len(answers), "duration_seconds": duration,
    }


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
    python = ROOT / ".venv" / "Scripts" / "python.exe"
    if not python.is_file():
        raise SystemExit("Zuerst DEMO/einrichten.py ausführen.")
    if Path(sys.executable).resolve() != python.resolve():
        raise SystemExit(subprocess.call([str(python), "-X", "utf8", str(Path(__file__).resolve())]))
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        main()
    except Exception as error:
        print(f"Abbruch: {type(error).__name__}: {error}")
        raise SystemExit(1)
