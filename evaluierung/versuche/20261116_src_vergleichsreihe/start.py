import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
MODEL = "Qwen_3_30B_A3B_Instruct_2507"
IMAGE = "tutor-evaluation:python-3.13-opencode-2.3.0"


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def worker(case_id):
    sys.path.insert(0, "/frozen/src_snapshot")
    sys.path.insert(0, "/frozen")
    from correction_agent import correct_python_submission
    from llm import get_llm
    from korrektur_prompt import PROMPT
    from langchain_core.callbacks import BaseCallbackHandler

    class Record(BaseCallbackHandler):
        raise_error = True
        calls = 0

        def on_chat_model_start(self, serialized, messages, **kwargs):
            if self.calls >= 10:
                raise RuntimeError("Zehn Modellstarts erreicht.")
            self.calls += 1
            self.write("model_start", {"number": self.calls})

        def on_llm_end(self, response, **kwargs):
            self.write("model", response.generations[0][0].message.model_dump(mode="json"))

        def on_llm_error(self, error, **kwargs):
            self.write("model_error", {"type": type(error).__name__, "message": str(error)})

        def on_tool_end(self, output, **kwargs):
            value = output.model_dump(mode="json") if hasattr(output, "model_dump") else str(output)
            self.write("tool", value)

        def write(self, kind, value):
            with Path("/output/verlauf.jsonl").open("a", encoding="utf-8") as stream:
                stream.write(json.dumps({"kind": kind, "value": value}, ensure_ascii=False) + "\n")

    jobs = json.loads(Path("/frozen/faelle.json").read_text(encoding="utf-8"))
    job = next(item for item in jobs if item["id"] == case_id)
    llm = get_llm(
        MODEL, api=os.environ["KICONNECT_API_KEY"],
        base_url=os.environ["KICONNECT_BASE_URL"],
        temperature=0, timeout=60, max_retries=0, max_tokens=700,
    )
    llm.callbacks = [Record()]
    content = (
        job["task"] + "\n\nDatei: " + job["filename"]
        + "\nStudentische Abgabe:\n" + job["code"]
    )
    try:
        result = correct_python_submission(
            content=content, code=job["code"], tests=job["tests"],
            llm=llm, prompt=PROMPT, timeout=10, recursion_limit=8,
        )
        save(Path("/output/ergebnis.json"), result)
    except Exception as error:
        save(Path("/output/fehler.json"), {"type": type(error).__name__, "message": str(error)})
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker")
    args = parser.parse_args()
    if args.worker:
        worker(args.worker)
        return

    from dotenv import dotenv_values
    project = ROOT.parents[2]
    values = dotenv_values(project / ".env")
    credentials = {
        key: values.get(key) or os.environ.get(key)
        for key in ("KICONNECT_API_KEY", "KICONNECT_BASE_URL")
    }
    if not all(credentials.values()):
        raise RuntimeError("KI:CONNECT-Konfiguration unvollstaendig.")
    image = subprocess.run(
        ["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    jobs = json.loads((ROOT / "faelle.json").read_text(encoding="utf-8"))
    for job in jobs:
        output = ROOT / "laeufe" / job["id"]
        output.mkdir(parents=True)
        name = "tutor-src-vergleich-" + uuid.uuid4().hex
        command = [
            "docker", "run", "--name", name, "--init", "--read-only",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--memory", "4g", "--memory-swap", "4g", "--cpus", "2",
            "--pids-limit", "256", "--user", "10001:10001",
            "--tmpfs", "/tmp:rw,nosuid,nodev,size=512m,mode=1777",
            "--mount", f"type=bind,source={ROOT.resolve()},target=/frozen,readonly",
            "--mount", f"type=bind,source={output.resolve()},target=/output",
        ]
        for key in credentials:
            command += ["--env", key]
        command += [image, "python", "-B", "/frozen/start.py", "--worker", job["id"]]
        started = time.perf_counter()
        report = {"id": job["id"], "image": image, "status": "started"}
        try:
            with (output / "stdout.txt").open("w", encoding="utf-8") as stdout, \
                 (output / "stderr.txt").open("w", encoding="utf-8") as stderr:
                process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                           env={**os.environ, **credentials})
                try:
                    report["exit_code"] = process.wait(timeout=120)
                    report["status"] = "completed" if process.returncode == 0 else "process_error"
                except subprocess.TimeoutExpired:
                    subprocess.run(["docker", "kill", name], capture_output=True, timeout=10)
                    process.wait(timeout=10)
                    report["status"] = "timeout"
        finally:
            report["wall_seconds"] = round(time.perf_counter() - started, 3)
            save(output / "bericht.json", report)
            subprocess.run(["docker", "rm", "-f", name], capture_output=True, timeout=10)
        print(job["id"], report["status"], report["wall_seconds"], flush=True)
        if report["status"] != "completed":
            print("Reihe bei Prozessfehler angehalten; keine weiteren Modelllaeufe.", flush=True)
            break


if __name__ == "__main__":
    main()
