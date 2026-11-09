from wypp import *

# Eine Bußgeldstrafe hat mehrere Aspekte:
# - Bußgeld (in Euro)
# - Punkte (in Flensburg)
# - Fahrverbot (in Monaten)
@record
class Strafe:
    bußgeld: float
    punkte: int
    fahrverbot: int

# Ein Vergehen hat mehrere Aspekte:
# - ampelRotZeit: Wie lange war die Ampel rot? (in Sekunden) (int)
# - drittePersonGefährdet: Wurde eine dritte Person gefährdet? (bool)
# - unfallVerursacht: Wurde durch das Überfahren ein Unfall verursacht? (bool)
@record
class Vergehen:
    ampelRotZeit: int
    drittePersonGefährdet: bool
    unfallVerursacht: bool

# Bestimmt für ein Rotlichtvergehen die passende Strafe.
# Eingabe: vergehen (Vergehen)
# Ausgabe: strafe (Strafe)
def bestimmeStrafe(vergehen: Vergehen) -> Strafe:
    if vergehen.ampelRotZeit <= 0:
        return Strafe(0, 0, 0)
    
    if vergehen.ampelRotZeit > 1:
        if vergehen.unfallVerursacht:
            return Strafe(100 + vergehen.ampelRotZeit * 10, 4, 4)
        if vergehen.drittePersonGefährdet:
            return Strafe(100 + vergehen.ampelRotZeit * 10, 4, 1)
        return Strafe(100 + vergehen.ampelRotZeit * 10, 0, 0)
    else:
        if vergehen.unfallVerursacht:
            return Strafe(150, 1, 0)
        if vergehen.drittePersonGefährdet:
            return Strafe(50, 1, 0)
        return Strafe(50, 0, 0)


check(bestimmeStrafe(Vergehen(0, False, False)), Strafe(0, 0, 0))

check(bestimmeStrafe(Vergehen(1, False, False)), Strafe(50, 0, 0))
check(bestimmeStrafe(Vergehen(1, True, False)), Strafe(50, 1, 0))
check(bestimmeStrafe(Vergehen(1, False, True)), Strafe(150, 1, 0))
check(bestimmeStrafe(Vergehen(1, True, True)), Strafe(150, 1, 0))

check(bestimmeStrafe(Vergehen(2, False, False)), Strafe(120, 0, 0))
check(bestimmeStrafe(Vergehen(4, False, False)), Strafe(140, 0, 0))

check(bestimmeStrafe(Vergehen(2, True, False)), Strafe(120, 4, 1))
check(bestimmeStrafe(Vergehen(5, True, False)), Strafe(150, 4, 1))

check(bestimmeStrafe(Vergehen(2, False, True)), Strafe(120, 4, 4))
check(bestimmeStrafe(Vergehen(5, False, True)), Strafe(150, 4, 4))
check(bestimmeStrafe(Vergehen(6, True, True)), Strafe(160, 4, 4))