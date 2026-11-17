from wypp import *

# DATENBESCHREIBUNG
# Ein Computer besteht aus:
# - Prozessor (str)
# - Festplatten-Kapazität in Gigabyte (int)
# - Hauptspeicher-Kapazität in Gigabyte (int)

# TYPDEFINITION
@record
class Computer:
    prozessor: str
    festplatte: int
    hauptspeicher: int

# Gesamtspeicher eines Computers berechnen
# Eingabe: ein Computer-Objekt (Typ: Computer)
# Ergebnis: Gesamtspeicher in Gigabyte (Typ: int)
def totalMemory(c: Computer) -> int:
    return c.festplatte + c.hauptspeicher

workstation = Computer("Intel i9", 1000, 16)
browsing = Computer("AMD", 250, 8)

check(totalMemory(workstation), 1016)
check(totalMemory(browsing), 258)
check(totalMemory(Computer("ARM cpu", 2000, 32)), 2032)

# Ein Computermodell ist entweder billig, oder Gaming oder Office
type ComputerModel = Literal['cheap', 'gaming', 'office']

# Computer für Modell zusammenstellen.
# Eingabe: ein Computermodell (Typ: ComputerModel)
# Ergebnis: ein Computer-Objekt (Typ: Computer)
def standardModel(m: ComputerModel) -> Computer:
    todo()

check(standardModel('cheap'), Computer('Sempron', 100, 2))
check(standardModel('gaming'), Computer('R99995x3D', 4000, 64))
check(standardModel('office'), Computer('Intel i7', 1000, 16))
