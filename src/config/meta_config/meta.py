from dotenv import load_dotenv
import os

load_dotenv()  # liest .env-Datei und setzt Variablen in os.environ
# API_KEY = os.getenv("KI_COACH")
# GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# # name des Modells
# # "gemini-2.0-flash"
# MODELL = "gpt-4.1-mini"

# # API
# OPENAI_HSO_PROXY = False
# OPENAI_DIRECT = True
# GEMINI_DIRECT = False



API_KEY = os.getenv("KICONNECT_API_KEY")
KICONNECT_BASE_URL = os.getenv(
    "KICONNECT_BASE_URL",
    "https://chat.kiconnect.nrw/api/v1",
)
MODELL = os.getenv(
    "KICONNECT_MODEL",
    "Meta_Llama_3.1_8B_Instruct",
)

LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0"))
LLM_TIMEOUT_SECONDS = int(os.getenv("LLM_TIMEOUT_SECONDS", "120"))







# for evaluation_code
TASK= "P08-mutable_blatt-08.pdf"
TASK_NUMBER= "aufgabe 4"
STUDENT_SOLUTION ="removeSlice.py"
MUSTER_SOLUTION = "removeSlice.py"

