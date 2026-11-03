from pathlib import Path

# Projekt-Root: .../Tutor_chatbot
PROJECT_ROOT = Path(__file__).resolve().parents[3]
EVAL_DIR = PROJECT_ROOT / "Evaluation"
MERMAIDE_PATH = PROJECT_ROOT / "src" / "graph"/ "visualisation"

######################################################################################
# PYTHON
PYTHON_DATA_DIR = PROJECT_ROOT / "data" / "python"
PYTHON_TASKS_DIR = PYTHON_DATA_DIR   / "tasks"
PYTHON_SAMPLE_SOLUTION = PYTHON_DATA_DIR / "sample_solution"
PYTHON_STUDENT_SOLUTION = PYTHON_DATA_DIR / "student_solution"

PYTHON_LLM_LOG = EVAL_DIR / "python_aufgaben" / "testen"
######################################################################################
# JAVA 
JAVA_DATA_DIR = PROJECT_ROOT / "data" / "java"
JAVA_TASKS_DIR = JAVA_DATA_DIR   / "tasks"
JAVA_SAMPLE_SOLUTION = JAVA_DATA_DIR / "sample_solution"
JAVA_STUDENT_SOLUTION = JAVA_DATA_DIR / "student_solution"

JAVA_LLM_LOG = EVAL_DIR / "java_aufgaben" / "musterlösung_&lösung_20%"