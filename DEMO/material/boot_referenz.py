from wypp import *

# Zeit ausrechnen, die das Boot zur Ueberquerung braucht.
# Eingaben:
# - a: Breites des Flusses in Meter (float)
# - vBoot: Geschwindigkeit des Boots in Meter pro Sekunde (float)
# Ergebnis: Zeit zur Ueberquerung in Sekunden (float)
def querungsZeit(a: float, vBoot: float) -> float:
    return a/vBoot

check(querungsZeit(4, 2), 2)
check(querungsZeit(10, 2), 5)

# Länge von Strecke b ermitteln.
# Eingaben:
# - Zeit t in Sekunden, die das Boot zur Querung braucht (float)
# - Geschwindigkeit vFluss in Meter pro Sekunde (float)
# Ergebnis: Länge von b (float)
def längeB(t: float, vFluss: float) -> float:
    return t * vFluss

check(längeB(6, 2), 12)

# Berechne die Strecke c, die ein Boot beim Ueberqueren des Flusses zurücklegt.
# Eingaben:
# - a: Breites des Flusses in Meter (float)
# - vBoot: Geschwindigkeit des Boots in Meter pro Sekunde (float)
# - vFluss: Geschwindigkeit des Flusses in Meter pro Sekunde (float)
# Ergebnis: zurücklegte Strecke c in Meter (float)
def zurückgelegteStrecke(a: float, vBoot: float, vFluss: float) -> float:
    t = querungsZeit(a, vBoot)
    b = längeB(t, vFluss)
    c = math.sqrt(a**2 + b**2)
    return c

check(zurückgelegteStrecke(4, 2, 1.5), 5)
check(zurückgelegteStrecke(3, 1, 4/3), 5)

# Zeit, die das Boot zur Ueberquerung braucht: 2 Sekunden
# Länge von b: 3 Meter
# Satz von Pythagoras: a^2 + b^2 = c^2
# Also c = sqrt(a^2 + b^2) = sqrt(16 + 9) = sqrt(25) = 5
