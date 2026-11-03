import traceback
import sys
from langchain_core.messages import  HumanMessage
from config.meta_config import *
from chatbot import build_Agent_Graph
from common import detect_language, load_prompts, print_full_evaluation_stream, load_code, load_pdf, get_language_config



def evaluate_solution(task_pfad, submission_pfad, solution_pfad):

    user_input = f""" 
        Es handelt um die {TASK_NUMBER} in der pdf:\n{load_pdf(task_pfad)}
        Hier ist die Lösung des Studenten:\n{load_code(submission_pfad)}
        """
    
    detected_language= detect_language(submission_pfad)
    agent_prompt = load_prompts(detected_language)

    print_full_evaluation_stream(build_Agent_Graph(MODELL, API_KEY, prompts= agent_prompt).stream({
                                                "human_assignment_state": [HumanMessage(content=user_input)], 
                                                "sample_solution": f"Hier ist die Musterlösung\n {load_code(solution_pfad)}"
                                                },
                                                
                                                 stream_mode="values"))
    

def main():
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            # to change the task, go to config and change the input 
            config = get_language_config(STUDENT_SOLUTION)
            task_path = config["tasks_dir"] / TASK
            student_solution_path = (config["student_solution_dir"] / STUDENT_SOLUTION)
            muster_solution_path = (config["sample_solution_dir"] / MUSTER_SOLUTION)

            log_dir = config["llm_log_dir"] / MODELL
            log_dir.mkdir(parents=True, exist_ok=True) 
            log_path = log_dir / f"{TASK}.txt"

            with open(log_path, "w", encoding="utf-8") as log_file:
                old_stdout = sys.stdout
                try:
                    sys.stdout = log_file
                    evaluate_solution(
                        task_path,
                        student_solution_path, 
                        muster_solution_path
                       
                    )
                finally:
                    sys.stdout = old_stdout 
            print(f"✅ Log wurde gespeichert unter: {log_path}")


        except Exception as e:
            sys.stdout = sys.__stdout__
            print("❌ Fehler beim Schreiben des Logs:")
            print(e)
            traceback.print_exc()
            break

if __name__ == "__main__":
    main()