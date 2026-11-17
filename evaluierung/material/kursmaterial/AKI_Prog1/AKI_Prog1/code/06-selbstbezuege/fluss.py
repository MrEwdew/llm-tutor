from wypp import *

# Ein Bach hat einen Namen und den Ort der Quelle
@record
class Creek:
    name: str      # Der Name des Bachs
    origin: str    # Ort an dem der Bach entspringt (Quelle)

# Ein Zusammenfluss hat einen
# - Hauptflussabschnitt (Typ: RiverSection)
# - Nebenflussabschnitt (Typ: RiverSection)
# - Ort des Zusammefluss (Typ: str)
@record
class Confluence:
    mainStem: RiverSection
    tributary: RiverSection
    location: str

# Ein Flußabschnitt ist entweder ein Bach (Typ: Creek) oder ein Zusammenfluss (Typ: Confluence)
type RiverSection = Union[Creek, Confluence]

kinzig1 = Creek('Kinzig', 'Loßburg')
gutach = Creek('Gutach', 'Schönwald')
kinzig2 = Confluence(kinzig1, gutach, 'Hausach')

schutter1 = Creek('Schutter', 'Schweighausen')
heidengraben = Creek('Heidengraben', 'Lahr')
schutter2 = Confluence(schutter1, heidengraben, 'Lahr')

kinzig3 = Confluence(kinzig2, schutter2, 'Kehl')

# Name eines Flussabschnitts bestimmen
# Eingabe: der Flussabschnitt (Typ: RiverSection)
# Ergebnis: Name des Abschnitts (Typ: str)
def riverName(river: RiverSection) -> str:
    if isinstance(river, Creek):
        return river.name
    elif isinstance(river, Confluence):
        return riverName(river.mainStem)

riverName(kinzig3)


check(riverName(kinzig1), 'Kinzig')
check(riverName(kinzig2), 'Kinzig')
check(riverName(kinzig3), 'Kinzig')
check(riverName(schutter2), 'Schutter')

