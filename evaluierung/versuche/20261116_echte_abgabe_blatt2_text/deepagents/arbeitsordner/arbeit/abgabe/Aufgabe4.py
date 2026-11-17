from wypp import *

# Beschreibung: Begrenzt eine Zahl auf den Bereich von l bis u
# Eingabe: x, untere Grenze l und obere Grenze u (Typ: float)
# Ergebnis: x innerhalb des bereiches (Typ: float)

def clamp(x: float, l: float, u: float) -> float:
    if x < l:
        return l
    elif x > u:
        return u
    else:
        return x


check(clamp(5, 67.5, 89.5), 67.5)
check(clamp(-2, 0, 10), 0)
check(clamp(27.5, 0, 10), 10)
check(clamp(5.5, 0 , 0), 0)
check(clamp(10, 0, 10), 10)
check(clamp(2.5, 1 , 3), 2.5)
check(clamp(-4, -3, -1), -3)
check(clamp(7, 3, 3), 3)