from __future__ import annotations
from wypp import *

@record
class File:
    name: str
    size: int

@record
class Dir:
    name: str
    subDirs: list[Dir]
    files: list[File]

lectures = \
    Dir("Lectures",
        [Dir("AKI_Programmierung_1", [],
             [File("vorlesung-01.md", 8761),
              File("vorlesung-02.md", 3051),
              File("blatt-01.tex", 5407)]),
         Dir("AI_AdvancedProgramming", [],
             [File("vorlesung-01.md", 9810),
              File("blatt-01.tex", 7619)])],
        [File("planning.org", 4661)])

root = Dir("/", [lectures, Dir("Research", [], [])], [])

# Nach einer Datei in einem Verzeichnis rekursiv suchen.
# Eingabe: das Verzeichnis (Dir) und den Namen der Datei (str)
# Ergebnis: True wenn die Datei gefunden wird, sonst False (bool)
def findFile(d: Dir, name: str) -> bool:
    for f in d.files:
        if f.name == name:
            return True
    for sub in d.subDirs:
        if findFile(sub, name):
            return True
    return False

check(findFile(lectures, 'planning.org'), True)
check(findFile(lectures, 'blatt-01.tex'), True)
check(findFile(lectures, 'blub.txt'), False)

# Alle Dateien eines Verzeichnisses rekursiv zurückliefern.
# Eingabe: das Verzeichnis (Dir)
# Ergebnis: die Liste der Dateien list[File]
def listFiles(d: Dir) -> list[File]:
    result = d.files
    for sub in d.subDirs:
        result = result + listFiles(sub)
    return result

check(listFiles(lectures), [File("planning.org", 4661),
                            File("vorlesung-01.md", 8761),
                            File("vorlesung-02.md", 3051),
                            File("blatt-01.tex", 5407),
                            File("vorlesung-01.md", 9810),
                            File("blatt-01.tex", 7619)])
