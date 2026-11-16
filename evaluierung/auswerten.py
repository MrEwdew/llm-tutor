import csv
import json

from konfiguration import ROOT


# Prozessstatus ist keine fachliche Bewertung. Leere Felder bleiben unbekannt.
def main():
    rows = []
    for path in sorted((ROOT / "laeufe").glob("*/bericht.json")):
        report = json.loads(path.read_text(encoding="utf-8"))
        review = json.loads(path.with_name("bewertung.json").read_text(encoding="utf-8"))
        row = {key: report.get(key) for key in (
            "case", "harness", "model", "repeat", "status", "duration_seconds",
            "material_unchanged",
        )}
        row["run"] = path.parent.name
        row["total_tokens"] = (report.get("usage") or {}).get("total_tokens")
        row["reviewed"] = review["reviewed"]
        for key in ("true_positives", "false_positives", "false_negatives"):
            row[key] = review.get(key) if review["reviewed"] else None
        tp, fp, fn = (row[key] for key in (
            "true_positives", "false_positives", "false_negatives",
        ))
        row["precision"] = tp / (tp + fp) if tp is not None and fp is not None and tp + fp else None
        row["recall"] = tp / (tp + fn) if tp is not None and fn is not None and tp + fn else None
        rows.append(row)
    if not rows:
        print("Noch keine vorbereiteten Versuche vorhanden.")
        return
    with (ROOT / "uebersicht.csv").open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]), delimiter=";")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} Versuche in uebersicht.csv; fachliche Bewertung separat eintragen.")


if __name__ == "__main__":
    main()
