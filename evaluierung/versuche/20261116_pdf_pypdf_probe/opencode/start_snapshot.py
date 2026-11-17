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
PROMPT = 'Lies /work/material/aufgaben.pdf. Extrahiere den Text mit\n/usr/local/bin/python und der bereits installierten Bibliothek pypdf.\nVerwende nicht das direkte PDF-Lesewerkzeug, sondern Python fuer die Textextraktion.\nGib danach beide Funktionsanforderungen und die allgemeinen Vorgaben wieder.\nMaximal 100 Woerter. Behaupte keine Extraktion ohne tatsaechliche Ausfuehrung.\nKeine Paketinstallation, Websuche oder Delegation. Keine Zugangsdaten oder\nUmgebungsvariablen lesen. Arbeite nur unter /work und veraendere das PDF nicht.\nDu hast hoechstens drei Modellaufrufe. Keine Abgabe pruefen und keine Tests erstellen.\n'


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
            if self.calls >= 3:
                raise RuntimeError("Modelllimit erreicht: drei Aufrufe einschliesslich Unteragenten.")
            self.calls += 1

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
                     max_tokens=500, timeout=30, max_retries=0)
    agent = create_deep_agent(model=llm, backend=backend,
                             middleware=[ModelCallLimitMiddleware(run_limit=3)])
    try:
        result = agent.invoke({"messages": [{"role": "user", "content": PROMPT}]},
                              config={"recursion_limit": 30, "callbacks": [Record()]})
        save(Path("/output/nachrichten.json"), [m.model_dump(mode="json") for m in result["messages"]])
    except Exception as e:
        save(Path("/output/fehler.json"), {"type": type(e).__name__, "message": str(e)})
        raise


def worker(harness):
    if harness == "deepagents":
        deepagents_worker()
        return
    config = {
        "$schema": "https://opencode.ai/config.json",
        "model": f"kiconnect/{MODEL}",
        "providers": {"kiconnect": {
            "name": "KI:CONNECT", "env": ["KICONNECT_API_KEY"],
            "package": "@opencode/ai/providers/openai-compatible",
            "settings": {"baseURL": os.environ["KICONNECT_BASE_URL"],
                         "apiKey": "{env:KICONNECT_API_KEY}"},
            "models": {MODEL: {"name": MODEL}},
        }},
        "agents": {"build": {"steps": 3, "permissions": [
            {"action": "subagent", "resource": "*", "effect": "deny"},
            {"action": "websearch", "resource": "*", "effect": "deny"},
            {"action": "webfetch", "resource": "*", "effect": "deny"},
        ]}},
    }
    save(Path("/work/opencode.json"), config)
    command = ["opencode", "run", "--standalone", "--auto", "--format", "json",
               "--title", "PDF-pypdf-Probe", "--model", f"kiconnect/{MODEL}", PROMPT]
    with Path("/output/verlauf.jsonl").open("w", encoding="utf-8") as output:
        result = subprocess.run(command, stdout=output, check=False)
    raise SystemExit(result.returncode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--harness", choices=["opencode", "deepagents"], default="opencode")
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
    originals = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in (work / "material").iterdir()}
    report = {"model": MODEL, "harness": args.harness, "image": image,
              "status": "prepared", "model_steps_limit": 3, "wall_limit_seconds": 45,
              "prompt": PROMPT, "material_sha256": originals,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "src_used": False, "support": "Expliziter Hinweis auf vorhandene Bibliotheken",
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
                report["exit_code"] = process.wait(timeout=45)
                report["status"] = "completed" if process.returncode == 0 else "process_error"
            except subprocess.TimeoutExpired:
                subprocess.run(["docker", "kill", name], capture_output=True, timeout=10)
                process.wait(timeout=10)
                report["status"] = "timeout"
    finally:
        report["duration_seconds"] = round(time.perf_counter() - started, 3)
        report["material_unchanged"] = all(hashlib.sha256(p.read_bytes()).hexdigest() == originals[p.name]
                                           for p in (work / "material").iterdir())
        save(run / "bericht.json", report)
        subprocess.run(["docker", "rm", "-f", name], capture_output=True, timeout=10)
    print(report["status"], report["duration_seconds"], flush=True)


if __name__ == "__main__":
    main()
