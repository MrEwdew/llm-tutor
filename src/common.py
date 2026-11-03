from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import  HumanMessage
from chatbot import build_Agent_Graph
from config.meta_config import  MODELL
from config.locations.paths import *
import importlib
import markdown
from pathlib import Path

#neu
import ast

def extract_python_checks(code: str) -> list[dict]:
    tree = ast.parse(code)
    checks = []

    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "check"
        ):
            checks.append({
                "line": node.lineno,
                "code": ast.get_source_segment(code, node),
            })

    return sorted(checks, key=lambda check: check["line"])
#neu ende

#neu

def extract_python_functions(code: str) -> list[dict]:
    tree = ast.parse(code)
    functions = []

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            functions.append({
                "name": node.name,
                "line": node.lineno,
                "parameters": ast.unparse(node.args),
                "return_type": (
                    ast.unparse(node.returns)
                    if node.returns is not None
                    else None
                ),
            })

    return functions


#neu ende

#meu
def prepare_python_reference(code: str) -> dict:
    return {
        "code": code,
        "checks": extract_python_checks(code),
    }
#neu ende


#neu

# def load_python_references(reference_paths: dict[int, Path]) -> dict:
#     references = {}

#     for task_number, path in reference_paths.items():
#         code = path.read_text(encoding="utf-8-sig")
#         reference = prepare_python_reference(code)
#         reference["path"] = str(path)
#         references[task_number] = reference

#     return references

def load_references(reference_paths: dict[int, Path]) -> dict:
    references = {}

    for task_number, path in reference_paths.items():
        language = detect_language(path)
        code = path.read_text(encoding="utf-8-sig")

        if language == "python":
            reference = prepare_python_reference(code)
        else:
            reference = {
                "code": code,
                "checks": None,
            }

        reference["path"] = str(path)
        reference["language"] = language
        references[task_number] = reference

    return references


#neu ende

#nue

def load_exercise_submission(pdf_path, zip_path, reference_paths=None):
    pdf_text = load_pdf(pdf_path)
    tasks, introduction, closing = split_exercises(pdf_text)
    expected_tasks = extract_expected_files(tasks, introduction, pdf_text)
    files = extract_zip(zip_path)
    assignments = assign_task_to_exercise(files, expected_tasks)

    data = build_exercise_data(
        tasks, introduction, closing, assignments, files
    )

    references = {}
    if reference_paths is not None:
        unknown_tasks = set(reference_paths) - set(tasks)
        if unknown_tasks:
            raise ValueError(
                f"Referenzen fuer unbekannte Aufgaben: {sorted(unknown_tasks)}"
            )

        references = load_references(reference_paths)

    for number, task in data["tasks"].items():
        task["reference"] = references.get(number)

    return data
# neu ende



#neu
from zipfile import ZipFile
#import re


def extract_zip(zip_path):
    files = {}
    with ZipFile(zip_path, 'r') as zip_ref:
        for datei in zip_ref.infolist():
            if datei.is_dir() or not datei.filename.lower().endswith(('.py', '.java')):
                continue
            if datei.filename in files:
                raise ValueError(f"Die Datei {datei.filename} existiert bereits im ZIP-Archiv.")
            files[datei.filename] = zip_ref.read(datei).decode('utf-8-sig') # oder utf-8-sig
    if not files:
        raise ValueError("Das ZIP-Archiv enthält keine .py oder .java Dateien.")
    return files

#neu ende

#neu

def assign_task_to_exercise(files, expected_tasks):
    assignments = {}
    for task_number, expected_names in expected_tasks.items():
        assignments[task_number] = {}
        for expected_name in expected_names:
            matches = [path for path in files if Path(path).name == expected_name]
            if len(matches) > 1:
                raise ValueError(f"Mehrere Dateien für {expected_name}: {matches}")
            assignments[task_number][expected_name] = (matches[0] if matches else None)
    return assignments
#neu ende

# neu
import re

def split_exercises(pdf_text):
    headings = list(re.finditer(r"^Aufgabe\s+(\d+)\b(?!\.)[^\n]*",pdf_text,re.MULTILINE,))
    if not headings:
        raise ValueError("Keine eindeutigen Hauptaufgaben gefunden.")
    closing_match = re.search(r"^(?:Gesamtpunkte\s*:|Abgabe\s*$)",pdf_text[headings[-1].end():],re.MULTILINE,)
    closing_start = (headings[-1].end() + closing_match.start()if closing_match else len(pdf_text))
    tasks = {}
    for index, heading in enumerate(headings):
        number = int(heading.group(1))
        if number in tasks:
            raise ValueError(f"Aufgabe {number} kommt mehrfach vor.")
        end = (headings[index + 1].start()if index + 1 < len(headings)else closing_start)
        tasks[number] = pdf_text[heading.start():end].strip()
    introduction = pdf_text[:headings[0].start()].strip()
    closing = pdf_text[closing_start:].strip()
    return tasks, introduction, closing
#neu ende


#neu

def extract_expected_files(tasks, introduction, pdf_text):
    #tasks, introduction, closing = split_exercises(pdf_text)
    filename = r"[A-Za-z_][A-Za-z0-9_-]*\.(?:py|java)\b"
    filenames = rf"{filename}(?:\s*(?:und|,)\s*{filename})*"
    introduction = " ".join(introduction.split())
    shared_files = re.findall(rf"(?:Alle Aufgaben sind in der Datei|"rf"Ihre Abgabe muss in der Datei)\s+({filename})",introduction,)
    if len(set(shared_files)) > 1:
        raise ValueError("Mehrere unterschiedliche blattweite Dateivorgaben.")
    default_names = "aufgabe_0N.py" in pdf_text
    expected_tasks = {}
    for number, section in tasks.items():
        section = " ".join(section.split())
        names = []
        patterns = [rf"\bDatei:\s*({filenames})",rf"\b(?:in|an)\s+"rf"(?:der Datei|den Dateien|einer Datei(?: namens)?)"rf"\s+({filenames})",]
        for pattern in patterns:
            for match in re.finditer(pattern, section):
                names.extend(re.findall(filename, match.group(1)))
        names = list(dict.fromkeys(names))
        if names:
            expected_tasks[number] = names
        elif shared_files:
            expected_tasks[number] = [shared_files[0]]
        elif (re.search(filename, section)or re.search(r"siehe\s+Aufgabe\s+\d", section, re.IGNORECASE)):
            raise ValueError(f"Aufgabe {number}: Dateivorgabe im Kontext prüfen.")
        elif default_names:
            expected_tasks[number] = [f"aufgabe_0{number}.py"]
        else:
            raise ValueError(f"Aufgabe {number}: Keine eindeutige Dateivorgabe.")
    return expected_tasks
#neu ende

#neu

# def build_exercise_data(tasks, introduction, closing, assignments, files):
#     exercise_data = {"introduction": introduction,"closing": closing,"tasks": {},}
#     for number, description in tasks.items():
#         task_files = {}
#         for filename, path in assignments[number].items():
#             task_files[filename] = {"path": path,"code": files[path] if path is not None else None,}
#         exercise_data["tasks"][number] = {"description": description,"files": task_files,}
#     return exercise_data

def build_exercise_data(tasks, introduction, closing, assignments, files):
    exercise_data = {
        "introduction": introduction,
        "closing": closing,
        "tasks": {},
    }

    for number, description in tasks.items():
        task_files = {}

        for filename, path in assignments[number].items():
            code = files[path] if path is not None else None
            functions = None
            syntax_error = None

            if code is not None and detect_language(filename) == "python":
                try:
                    functions = extract_python_functions(code)
                except SyntaxError as error:
                    syntax_error = {
                        "line": error.lineno,
                        "message": error.msg,
                    }

            task_files[filename] = {
                "path": path,
                "code": code,
                "functions": functions,
                "syntax_error": syntax_error,
            }

        exercise_data["tasks"][number] = {
            "description": description,
            "files": task_files,
        }

    return exercise_data

#neu ende


#neu

def prepare_evaluation_input(data: dict, task_number: int) -> dict:
    task = data["tasks"][task_number]

    sections = [
        f"Aufgabe {task_number}",
        "Allgemeine Blattvorgaben:\n" + data["introduction"],
        "Aufgabenstellung:\n" + task["description"],
        "Abschliessende Blattvorgaben:\n" + data["closing"],
        "Studentische Abgabe:",
    ]

    for filename, file in task["files"].items():
        if file["code"] is None:
            content = "Datei fehlt."
        elif file["code"] == "":
            content = "Datei vorhanden, aber leer."
        else:
            content = file["code"]

        sections.append(f"Datei: {filename}\n{content}")
        syntax_error = file.get("syntax_error")

        if syntax_error is not None:
            sections.append(
                f"Statischer Python-Syntaxbefund zu Datei: {filename}\n"
                f"Zeile {syntax_error['line']}: {syntax_error['message']}\n"
                "Beim Einlesen mit dem Python-AST-Parser festgestellt. "
                "Der Abgabecode wurde nicht ausgefuehrt."
            )

    reference = task["reference"]

    if reference is None:
        sample_solution = "Keine Musterloesung zugeordnet."
    else:
        sample_solution = (
            "Musterloesung mit enthaltenen Beispieltests:\n"
            + reference["code"]
            + "\n\nDie Beispieltests wurden nicht ausgefuehrt."
        )

    return {
        "human_assignment_state": [
            HumanMessage(content="\n\n".join(sections))
        ],
        "sample_solution": sample_solution,
    }

#neu ende

#neu

def prepare_function_assignment_input(data: dict, task_number: int) -> str:
    prepared = prepare_evaluation_input(data, task_number)

    sections = [
        prepared["human_assignment_state"][0].content,
        "Statisch erfasste Python-Funktionen:",
    ]

    for filename, file in data["tasks"][task_number]["files"].items():
        functions = file["functions"]
        sections.append(f"Datei: {filename}")

        if functions is None:
            sections.append("Kein Funktionsinventar verfuegbar.")
        elif not functions:
            sections.append("Keine normalen Funktionen auf Modulebene erkannt.")
        else:
            for function in functions:
                return_type = function["return_type"]
                if return_type is None:
                    return_type = "nicht angegeben"

                sections.append(
                    f"Zeile {function['line']}: "
                    f"{function['name']}({function['parameters']}) "
                    f"-> {return_type}"
                )

    return "\n\n".join(sections)

# neu ende


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

   