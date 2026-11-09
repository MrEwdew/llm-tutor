import json
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from common import load_exercise_submission, prepare_python_correction_input


def load_input(variant):
    if variant not in ("gut", "mittel", "schlecht"):
        raise ValueError("Unbekannte Abgabe.")

    sheet = PROJECT_ROOT / "data/python/tasks/P01-simple-funs_blatt-01.pdf"
    submission = (
        PROJECT_ROOT
        / "loesungen_der_schueler_vom_praktomat_runtergeladen"
        / "Uebungsblatt_1_Sayed_Hussaini.zip"
    )
    # reference = (
    #     PROJECT_ROOT.parent
    #     / "Musterloesungen_und_Vorlesungen"
    #     / "Alaref/alaref/alaref/solutions/boot.py"
    # )
    reference = PROJECT_ROOT / "Musterloesungen/solutions/boot.py"
    code = (
        PROJECT_ROOT / "DEMO_lokal/abgaben" / variant / "aufgabe_06.py"
    ).read_bytes()

    # Nur Aufgabe 6 in einer temporären Kopie der Abgabe austauschen.
    with tempfile.TemporaryDirectory(prefix="tutor-eingabe-") as directory:
        archive = Path(directory) / "abgabe.zip"
        matches = 0

        with ZipFile(submission) as original, ZipFile(archive, "w") as copy:
            for entry in original.infolist():
                content = original.read(entry)

                if Path(entry.filename).name == "aufgabe_06.py":
                    content = code
                    matches += 1

                copy.writestr(entry, content)

        if matches != 1:
            raise ValueError("Aufgabe 6 ist im Originalarchiv nicht eindeutig.")

        data = load_exercise_submission(sheet, archive, {6: reference})

    prepared = prepare_python_correction_input(data, 6)
    task = data["tasks"][6]

    prepared["functions"] = task["files"][prepared["filename"]]["functions"]
    prepared["task_count"] = len(data["tasks"])
    prepared["reference_checks"] = len(task["reference"]["checks"])

    return prepared


if __name__ == "__main__":
    print(json.dumps(load_input(sys.argv[1]), ensure_ascii=False))