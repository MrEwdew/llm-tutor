import os, sys, argparse
from common import analyze_submission_praktomat

def main():
    # Sicherstellen, dass relative Pfade funktionieren
    repo_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_root)

    p = argparse.ArgumentParser()
    p.add_argument("--pdf", required=True)
    p.add_argument("--model-solution", required=True)
    p.add_argument("--student-solution", required=True)
    p.add_argument("--assignment", required=True)
    p.add_argument("--api", required=True)
    args = p.parse_args()

    analyze_submission_praktomat(
        args.pdf,
        args.model_solution,
        args.student_solution,
        args.assignment,
        args.api
    )

    return 0

if __name__ == "__main__":

    sys.exit(main())