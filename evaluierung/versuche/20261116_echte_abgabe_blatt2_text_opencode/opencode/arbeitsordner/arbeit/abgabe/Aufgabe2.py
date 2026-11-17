from wypp import *

# Gibt der Spielertyp eine Rückennummer
# Eingabe: Spielertyp
# Ergebnis: Rückennummer als int
# DATENBESCHREIBUNG
# Eine spielerKlasse ist:
# - Torhueter -
# - Abwehrspieler -
# - Mittelfeldspieler -
# - Stuermer -
# - Ersatzspieler -
# TYPDEFINITION
type spielerKlasse = Literal["Torhueter", "Abwehrspieler", "Mittelfeldspieler", "Stuermer", "Ersatzspieler" ]




def rueckenNummer(rueckenNummer: int) -> str:
    if rueckenNummer == (1):
        return "Torhueter"
    elif rueckenNummer == (2 or 3 or 4 or 5):
        return "Abwehrspieler"
    elif rueckenNummer == (6 or 7 or 8 or 10):
        return "Mittelfeldspieler"
    elif rueckenNummer == (9 or 11):
        return "Stuermer"
    elif rueckenNummer <= 99:
        return "Ersatzspieler"
    
    
    






check(rueckenNummer(1), "Torhueter")
check(rueckenNummer(2), "Abwehrspieler")
check(rueckenNummer(6), "Mittelfeldspieler")
check(rueckenNummer(9), "Stuermer")
check(rueckenNummer(67), "Ersatzspieler")
