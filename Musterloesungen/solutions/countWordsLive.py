from wypp import *

# String in Liste von Wörtern konvertieren.
# Eingabe: ein String
# Ergebnis: Liste mit den Wörtern, die im String enthalten sind.
def stringToWords(s: str) -> list[str]:
    satzzeichen = [',', '?', '.', ';', ':', '!']
    for x in satzzeichen:
        s = s.replace(x, ' ')
    return s.split()

sampleString = """Hallo Stefan,

wie geht es dir?"""

check(stringToWords(sampleString), ["Hallo", "Stefan", "wie", "geht", "es", "dir"])

# Anzahl der Vorkommen von Wörtern in einer Liste von Strings zählen
# Eingabe: eine Liste von Strings (list[str])
# Ergebnis: ein Dictionary, welches Wörter auf Häufigkeiten abbildet (dict[str, int])
def countWords(l: list[str]) -> dict[str, int]:
    result = {}
    for x in l:
        x = x.lower()
        freq = result.get(x, 0)
        result[x] = freq + 1
    return result

check(countWords(["Ding","einmal","ding"]), {"ding":2,"einmal":1})

# Gibt die am häufigsten vorkommenden Wörter einer Datei aus.
# Eingabe: der Dateinamen (str)
# Ergebnis: keins
# Seiteneffekt: erzeugt die richtige Ausgabe auf dem Bildschirm
def countWordsInFile(fileName: str) -> None:
    with open(fileName) as f:
        fileContent = f.read()
    l = stringToWords(fileContent)
    d = countWords(l)
    sortedList = sorted(d.items(), key=lambda x: x[1], reverse=True)
    for k,v in sortedList[:3]:
        print(f'{k}: {v}')
