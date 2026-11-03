from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import  HumanMessage
from chatbot import build_Agent_Graph
from config.meta_config import  MODELL
from config.locations.paths import *
import importlib
import markdown
from pathlib import Path



def load_code(path):
    try:
        with open(path, "r") as f:
            content = f.read()
            return content if content else ""
    except FileNotFoundError:
        print(f"Es gibt keine Datei: {path}")
        return None

def load_pdf(path):
    loader = PyPDFLoader(path)
    pages = loader.load()
    return "\n".join([p.page_content for p in pages])


def detect_language(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()

    language_mapping = {
        ".py": "python",
        ".java": "java"
    }

    if suffix in language_mapping:
        return language_mapping[suffix]

    raise ValueError(
        f"Unbekannte Programmiersprache für Datei: {file_path}"
    )

def get_language_config(student_solution: str):
    language = detect_language(student_solution)

    language_config = {
        "python": {
            "data_dir": PYTHON_DATA_DIR,
            "tasks_dir": PYTHON_TASKS_DIR,
            "sample_solution_dir": PYTHON_SAMPLE_SOLUTION,
            "student_solution_dir": PYTHON_STUDENT_SOLUTION,
            "llm_log_dir": PYTHON_LLM_LOG,
        },

        "java": {
            "data_dir": JAVA_DATA_DIR,
            "tasks_dir": JAVA_TASKS_DIR,
            "sample_solution_dir": JAVA_SAMPLE_SOLUTION,
            "student_solution_dir": JAVA_STUDENT_SOLUTION,
            "llm_log_dir": JAVA_LLM_LOG,
        }
    }

    return language_config[language]

def load_prompts(language: str):
    module_name = f"config.prompts.{language}"
    prompt_module = importlib.import_module(module_name)

    return {
        "aggregator": prompt_module.AGGREGATOR_AGENT_SYSTEMMESSAGE,
        "assignment": prompt_module.ASSIGNMENT_AGENT_SYSTEMMESSAGE,
        "muster": prompt_module.MUSTER_AGENT_SYSTEMMESSAGE,
        "retriever": prompt_module.RETRIEVER_AGENT_SYSTEMMESSAGE,
    }




def print_evaluation_stream_praktomat(stream):
    last_aggregator_state= None
    result_text = ""

    for s in stream:
        if s["aggregator_state"] != last_aggregator_state:
            if s["aggregator_state"]:
                message = s["aggregator_state"][-1]
                result_text += message.content + "\n\n"
        last_aggregator_state = list(s["aggregator_state"])
        
    return result_text

def print_full_evaluation_stream(stream):
    last_retriever_state = None
    last_muster_state= None
    last_aggregator_state= None
    last_message_state= None
    for s in stream:
        if s["human_assignment_state"] != last_message_state:
            if s["human_assignment_state"]:
                s["human_assignment_state"][-1].pretty_print()
        last_message_state = list(s["human_assignment_state"])
    
        if s["retriever_state"] != last_retriever_state:
            if s["retriever_state"]:
                s["retriever_state"][-1].pretty_print()
        last_retriever_state = list(s["retriever_state"])

        if s["muster_state"] != last_muster_state:
            if s["muster_state"]:
                s["muster_state"][-1].pretty_print()
        last_muster_state = list(s["muster_state"])

        if s["aggregator_state"] != last_aggregator_state:
            if s["aggregator_state"]:
                s["aggregator_state"][-1].pretty_print()
        last_aggregator_state = list(s["aggregator_state"])
        

# code for praktomat
def save_result_to_markdown(result, output_path):
    output_path = Path(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Ergebnis\n\n")
        f.write("```text\n")
        f.write(str(result))
        f.write("\n```")

    absolute_path = output_path.resolve()
    return absolute_path

def analyze_submission_praktomat(pdf,model_solution,student_solution,assignment,api):
    # not necessary for muster_solution
    student_code = load_code(student_solution)
    if student_code is None:
        return

    user_input = f""" 
    Es handelt um die Aufgabe {assignment} in der pdf:
    {load_pdf(pdf)}

    Hier ist die Lösung des Studenten:
    {load_code(student_solution)}
    """

    detected_language = detect_language(student_solution)
    agent_prompt = load_prompts(detected_language)

    stream = build_Agent_Graph(MODELL,api,prompts=agent_prompt).stream({
            "human_assignment_state": [HumanMessage(content=user_input)],
            "sample_solution": f"Hier ist die Musterlösung\n {load_code(model_solution)}"},
        stream_mode="values")

    html_output = output_in_html(print_evaluation_stream_praktomat(stream))
    print(html_output)

   

# if you want to use it, you must use  print_evaluation_stream instead of print_full_evaluation_stream !
def output_in_html(content):

    cleaned = content.replace(
        "================================== Ai Message ==================================",
        ""
    )

    html = markdown.markdown(cleaned,extensions=["tables"])

    if html == "":
        raise ValueError("markdown is not able to read the llm result from .txt")
    
    html_content = f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
        <meta charset="UTF-8">
        <title>AI Message</title>

        <style>
        body {{
            font-family: Arial;
            margin: 40px;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
        }}

        th, td {{
            border: 1px solid #ccc;
            padding: 8px;
        }}

        th {{
            background: #f2f2f2;
        }}
        </style>

        </head>
        <body>
            {html}
        </body>
        </html>
        """
    return html_content

   