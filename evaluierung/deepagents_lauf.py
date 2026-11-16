import json
import os
import sys
from pathlib import Path

from konfiguration import GRAPH_LIMIT


def main():
    from deepagents import create_deep_agent
    from deepagents.backends import LocalShellBackend
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain_openai import ChatOpenAI

    run = Path(sys.argv[1])
    if os.environ.get("EVALUATION_CONTAINER") != "1":
        raise RuntimeError("Diesen Adapter nur ueber den Docker-Start verwenden.")
    model = ChatOpenAI(
        model=sys.argv[2], api_key=os.environ["KICONNECT_API_KEY"],
        base_url=os.environ["KICONNECT_BASE_URL"], temperature=0,
        timeout=60, max_retries=0,
    )
    usages = []

    class RecordCalls(BaseCallbackHandler):
        def on_llm_end(self, response, **kwargs):
            message = response.generations[0][0].message
            usages.append(message.usage_metadata)
            with (run / "modellantworten.jsonl").open("a", encoding="utf-8") as file:
                file.write(json.dumps(message.model_dump(mode="json"), ensure_ascii=False) + "\n")

    # Keine fertigen Fachtests: vorhandene Datei- und Shellwerkzeuge des Harness.
    shell_env = {name: os.environ[name] for name in (
        "PATH", "HOME", "LANG", "LC_ALL", "TMPDIR",
    ) if name in os.environ}
    backend = LocalShellBackend(
        root_dir=Path("/work"), virtual_mode=False,
        timeout=30, env=shell_env, inherit_env=False,
    )
    agent = create_deep_agent(model=model, backend=backend)
    prompt = Path("/auftrag.txt").read_text(encoding="utf-8")
    prompt += f"\nPython fuer Ausfuehrungen: {sys.executable}\n"
    try:
        with (run / "verlauf.jsonl").open("w", encoding="utf-8") as file:
            for event in agent.stream(
                {"messages": [{"role": "user", "content": prompt}]},
                config={"recursion_limit": GRAPH_LIMIT, "callbacks": [RecordCalls()]},
                stream_mode="updates", subgraphs=True,
            ):
                file.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")
                file.flush()
    finally:
        usage = {}
        for field in ("input_tokens", "output_tokens", "total_tokens"):
            values = [(item or {}).get(field) for item in usages]
            usage[field] = sum(values) if values and all(v is not None for v in values) else None
        (run / "adapter.json").write_text(json.dumps({
            "model_calls_observed": len(usages), "usage": usage,
            "usage_scope": "callback_observed_calls_including_child_runs",
            "temperature": 0, "request_timeout": 60, "retries": 0,
            "shell_timeout": 30,
        }, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
