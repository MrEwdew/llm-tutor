import os
import sys
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from operator import add as add_messages
import json
#from config.meta_config import API_KEY, MUSTER_SOLUTION, MODELL, GEMINI_KEY
#from config.meta_config import OPENAI_DIRECT, OPENAI_HSO_PROXY, GEMINI_DIRECT
from config.meta_config import API_KEY,MUSTER_SOLUTION, MODELL, KICONNECT_BASE_URL, LLM_TEMPERATURE, LLM_TIMEOUT_SECONDS
from config.locations import MERMAIDE_PATH, PYTHON_SAMPLE_SOLUTION 
from config.prompts.python import AGGREGATOR_AGENT_SYSTEMMESSAGE, ASSIGNMENT_AGENT_SYSTEMMESSAGE ,MUSTER_AGENT_SYSTEMMESSAGE, RETRIEVER_AGENT_SYSTEMMESSAGE

from langchain_openai import ChatOpenAI
from functools import partial
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI



LLM_PROXY_URL = "https://llm-proxy.imla.hs-offenburg.de"

def get_llm(modell_name, api: str | None = None):
    api_key = api or API_KEY

    if not api_key:
        raise ValueError("API Key fehlt.")
    
    # if api != '':
    #     return ChatOpenAI(
    #         model= modell_name, 
    #         api_key=api,
    #         base_url=LLM_PROXY_URL,
    #         )

    # if OPENAI_DIRECT:
    #     return init_chat_model(f"openai:{modell_name}")
    
    # elif OPENAI_HSO_PROXY:
    #     llm = ChatOpenAI(
    #         model= modell_name, 
    #         api_key=API_KEY,
    #         base_url=LLM_PROXY_URL,
    #         )
    #     return llm
    
    # elif GEMINI_DIRECT:
    #      # GEMINI
    #     gemini = ChatGoogleGenerativeAI(
    #         model= modell_name,
    #         google_api_key= GEMINI_KEY  
    #     )
    #     return gemini
    return ChatOpenAI(
        model= modell_name,
        api_key=api_key,
        base_url=KICONNECT_BASE_URL,
        temperature=LLM_TEMPERATURE,
        timeout=LLM_TIMEOUT_SECONDS,
        max_retries=2,
    )
        


class AgentState(TypedDict):
    human_assignment_state: Annotated[Sequence[BaseMessage], add_messages]
    retriever_state: Annotated[Sequence[BaseMessage], add_messages]
    muster_state: Annotated[Sequence[BaseMessage], add_messages]
    aggregator_state:  Annotated[Sequence[BaseMessage], add_messages]
    sample_solution: str


# Kontrollflussgraph eines mehrstufigen LLM-Workflows (LangGraph)
def assignment_node(state: AgentState, llm, prompt) -> AgentState:
    """
    Extracts the specific assignment from the exercise sheets.  
    This node identifies which task is being referenced and 
    returns only the assignment text itself, 
    without additional explanations or metadata. 
    The task files follow the naming pattern: PXX-topic_blatt-XX.pdf
    """
    messages = [SystemMessage(content=prompt)] +  list(state['human_assignment_state'])
    message = llm.invoke(messages)
    return {'human_assignment_state': [message]}


def retriever_node(state: AgentState, llm, prompt) -> AgentState:
    """
    The retriever node evaluates and corrects the student’s
    solution in accordance with the corresponding prompt
    """
    # Anfangsnachrichten vorbereiten von assignment_agent 
    human_messages = [HumanMessage(content= state["human_assignment_state"][-1].content)]
    response = llm.invoke([SystemMessage(content=prompt)] + human_messages)  
    return {"retriever_state": [response]}


def muster_node(state:AgentState, llm, prompt) -> AgentState:
    """
    The muster node is provided with the assignment message 
    including the sample solution and is responsible for 
    comparing both solutions and delivering feedback
    """
    human_messages = [HumanMessage(content= state['human_assignment_state'][-1].content)]
    messages = [SystemMessage(content=prompt)] + human_messages + [state["sample_solution"]]
    response  = llm.invoke(messages)
    return {'muster_state': [response]}


def aggregator_node(state: AgentState, llm, prompt) -> AgentState:
    """
    Combines the results of the retreiver and the muster
    node and summarizes them into an overall evaluation using 
    a predefined template
    """
    retreiver_agent = state["retriever_state"][-1].content
    muster_agent    = state["muster_state"][-1].content
    messages = [SystemMessage(content=prompt)] + [retreiver_agent] + [muster_agent] 
    message = llm.invoke(messages)
    return {'aggregator_state': [message]}
    

#neu
def assign_function_roles(
    content: str,
    expected_functions: list[tuple[str, str]],
    llm,
    prompt: str,
) -> dict:
    expected = set(expected_functions)

    if len(expected) != len(expected_functions):
        raise ValueError("Doppelte Funktionen im erwarteten Inventar.")

    if not expected:
        return {"functions": [], "usage": None}

    answer = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content=content),
    ])

    result = json.loads(answer.content)

    if not isinstance(result, dict):
        raise ValueError("JSON-Objekt erwartet.")

    functions = result.get("functions")
    if not isinstance(functions, list):
        raise ValueError("functions muss eine Liste sein.")

    actual = []

    for function in functions:
        if not isinstance(function, dict):
            raise ValueError("Funktionszuordnung muss ein Objekt sein.")

        if set(function) != {"file", "name", "role", "status"}:
            raise ValueError("Unerwartete Felder in Funktionszuordnung.")

        if not all(isinstance(value, str) for value in function.values()):
            raise ValueError("Alle Zuordnungsfelder muessen Text sein.")

        if not function["role"].strip():
            raise ValueError("Rollenbeschreibung fehlt.")

        if function["status"] not in {"zugeordnet", "unklar"}:
            raise ValueError("Unbekannter Zuordnungsstatus.")

        actual.append((function["file"], function["name"]))

    if len(actual) != len(set(actual)):
        raise ValueError("Doppelte Funktionszuordnung.")

    if set(actual) != expected:
        raise ValueError("Funktionen fehlen oder wurden erfunden.")

    return {
        "functions": functions,
        "usage": answer.usage_metadata,
    }
#neu ende


def build_Agent_Graph(modell_name, api, prompts: dict, prepared_input=False):

    llm = get_llm(modell_name, api)
    graph = StateGraph(AgentState)

    aggregator_prompt = prompts.get("aggregator")
    assignment_prompt = prompts.get("assignment")
    muster_prompt = prompts.get("muster")
    retriever_prompt = prompts.get("retriever")

    #graph.add_node("Aufgabenextraktion", partial(assignment_node, llm=llm, prompt=assignment_prompt))
    if not prepared_input:
        graph.add_node(
            "Aufgabenextraktion",
            partial(assignment_node, llm=llm, prompt=assignment_prompt),
        )
    graph.add_node("Abgabenanalyse",  partial(retriever_node, llm=llm, prompt= retriever_prompt))
    graph.add_node("Mustervergleich",     partial(muster_node, llm=llm, prompt= muster_prompt))
    graph.add_node("Aggregation", partial(aggregator_node, llm=llm, prompt=aggregator_prompt))

    # graph.set_entry_point("Aufgabenextraktion")

    # graph.add_edge("Aufgabenextraktion", "Abgabenanalyse")
    # graph.add_edge("Aufgabenextraktion", "Mustervergleich")
    if prepared_input:
        graph.add_edge("__start__", "Abgabenanalyse")
        graph.add_edge("__start__", "Mustervergleich")
    else:
        graph.set_entry_point("Aufgabenextraktion")
        graph.add_edge("Aufgabenextraktion", "Abgabenanalyse")
        graph.add_edge("Aufgabenextraktion", "Mustervergleich")
    graph.add_edge("Mustervergleich", "Aggregation")
    graph.add_edge("Abgabenanalyse", "Aggregation")

    graph.set_finish_point("Aggregation")

    return graph.compile()



# mermaide erstellen! 
# png_data = build_Agent_Graph("gpt-4").get_graph().draw_mermaid_png()
# output_path = os.path.join(MERMAIDE_PATH, "Agent_without_rag_2.png")
# with open(output_path, "wb") as f:
#     f.write(png_data)



