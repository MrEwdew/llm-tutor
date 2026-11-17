import json
import time

from langchain_core.tools import tool
from python_tests import run_python_tests
from deepagents import create_deep_agent
from langchain.agents.middleware import wrap_model_call
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langchain_core.tools import BaseTool


# Erstellt den Korrekturagenten mit dem übergebenen Testwerkzeug.
def build_correction_agent(llm, prompt: str, test_tool: BaseTool):
    @wrap_model_call
    def restrict_tools(request, handler):
        tested = any(
            isinstance(message, ToolMessage)
            and message.name == test_tool.name
            for message in request.state["messages"]
        )

        tools = []
        if not tested:
            tools = [
                tool
                for tool in request.tools
                if tool.name == test_tool.name
            ]

        return handler(request.override(tools=tools))

    return create_deep_agent(
        model=llm,
        tools=[test_tool],
        middleware=[restrict_tools],
        system_prompt=prompt,
    )


# Übergibt die vorbereitete Eingabe und liefert den Nachrichtenverlauf zurück.
def run_correction(
    content: str,
    llm,
    prompt: str,
    test_tool: BaseTool,
    recursion_limit: int = 8,
) -> dict:
    agent = build_correction_agent(llm, prompt, test_tool)

    return agent.invoke(
        {"messages": [HumanMessage(content=content)]},
        config={"recursion_limit": recursion_limit},
    )

# Liest Abschlussfeedback und gemeldeten Tokenverbrauch aus dem Verlauf.
def prepare_correction_result(result: dict) -> dict:
    messages = result["messages"]

    if not messages or not isinstance(messages[-1], AIMessage):
        raise ValueError("Abschliessende Modellantwort fehlt.")

    final = messages[-1]

    if (
        final.tool_calls
        or not isinstance(final.content, str)
        or not final.content.strip()
    ):
        raise ValueError("Abschlussfeedback fehlt.")

    answers = [
        message
        for message in messages
        if isinstance(message, AIMessage)
    ]

    usage = {}
    for field in ("input_tokens", "output_tokens", "total_tokens"):
        values = [
            (answer.usage_metadata or {}).get(field)
            for answer in answers
        ]
        usage[field] = (
            sum(values)
            if all(value is not None for value in values)
            else None
        )

    return {
        "feedback": final.content,
        "usage": usage,
        "model_calls": len(answers),
    }

# Korrigiert eine Python-Abgabe anhand vorbereiteter Vergleichstests.
def correct_python_submission(
    content: str,
    code: str,
    tests: list,
    llm,
    prompt: str,
    timeout: float = 10,
    recursion_limit: int = 8,
) -> dict:
    test_result = []

    @tool
    def run_submission_tests() -> str:
        """Prüft die Abgabe mit den vorbereiteten Vergleichstests."""
        if not test_result:
            test_result.append(
                run_python_tests(code, tests, timeout=timeout)
            )

        return json.dumps(test_result[0], ensure_ascii=False)

    start = time.perf_counter()
    result = run_correction(
        content=content,
        llm=llm,
        prompt=prompt,
        test_tool=run_submission_tests,
        recursion_limit=recursion_limit,
    )
    duration = round(time.perf_counter() - start, 2)

    if not test_result:
        raise RuntimeError("Testwerkzeug wurde nicht ausgeführt.")

    summary = prepare_correction_result(result)
    summary["test_result"] = test_result[0]
    summary["duration_seconds"] = duration

    return summary