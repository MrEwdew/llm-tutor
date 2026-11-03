import sys
from chatbot import build_Agent_Graph
from common import detect_language, load_prompts, print_full_evaluation_stream, load_code, load_pdf, get_language_config
from config.meta_config import *
from langchain_core.messages import  HumanMessage


# need to take a look at avaible Models in the system 
modelle = ["gpt-4.1-mini"]
# make just sure that all data exist under data/......
pdf_names = ["blatt-03.pdf","blatt-04.pdf","blatt-07.pdf","blatt-10.pdf"]
task_names =["LinkedList.java","InsertionSort.java","SearchTree.java", "HashTableChaining.java"]
task_number = ["Aufgabe 1", "Aufgabe 2","Aufgabe 2","Aufgabe 2", ]



def run_llm_assessment_experiments(models, task_number, task_pfad, submission_pfad, solution_pfad):
    user_input = f""" 
        Es handelt um die {task_number} in der pdf:\n{load_pdf(task_pfad)}
        Hier ist die Lösung des Studenten:\n{load_code(submission_pfad)}
        """
    
    detected_language= detect_language(submission_pfad)
    agent_prompt = load_prompts(detected_language)

    print_full_evaluation_stream(build_Agent_Graph(models, API_KEY, prompts= agent_prompt).stream({
                                                "human_assignment_state": [HumanMessage(content=user_input)], 
                                                "sample_solution": f"Hier ist die Musterlösung\n {load_code(solution_pfad)}"
                                                },
                                                
                                                 stream_mode="values"))
    
    

def logging(modell:str ,task_number,  task_pdf, task_name):
    """
    Runs the solution evaluation and logs all console output to a file.
    """

    # Target directory
    config = get_language_config(task_name)
    task_path = config["tasks_dir"] / task_pdf
    student_solution_path = (config["student_solution_dir"] / task_name)
    muster_solution_path = (config["sample_solution_dir"] / task_name)

    log_dir = config["llm_log_dir"] / modell
    log_dir.mkdir(parents=True, exist_ok=True) 
    log_path = log_dir / f"{task_pdf}.txt"

    # Open the file and redirect stdout
    with open(log_path, "w", encoding="utf-8") as log_file:
        old_stdout = sys.stdout
        try:
            sys.stdout = log_file
            run_llm_assessment_experiments(
                models= modell, 
                task_number = task_number, 
                task_pfad= task_path,
                submission_pfad= student_solution_path, 
                solution_pfad=  muster_solution_path             
                
            )
        finally:
            sys.stdout = old_stdout 

    print(f"✅ Log wurde gespeichert unter: {log_path}")

def main():
    for gpt in modelle:
        for i, pdf in enumerate(pdf_names):
            logging(gpt,task_number[i],pdf, task_names[i])


if __name__ == "__main__":
    main()