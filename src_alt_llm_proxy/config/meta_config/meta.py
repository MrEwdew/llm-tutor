from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

load_dotenv()  # liest .env-Datei und setzt Variablen in os.environ
API_KEY = os.getenv("KI_COACH")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# name des Modells
# "gemini-2.0-flash"
MODELL = "gpt-4.1-mini"

# API
OPENAI_HSO_PROXY = False
OPENAI_DIRECT = True
GEMINI_DIRECT = False

# for evaluation_code
TASK= "P08-mutable_blatt-08.pdf"
TASK_NUMBER= "aufgabe 4"
STUDENT_SOLUTION ="removeSlice.py"
MUSTER_SOLUTION = "removeSlice.py"

