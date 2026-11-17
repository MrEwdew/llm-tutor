import sys
sys.path.insert(0, "/work/arbeit/abgabe")
from aufgabe_02 import positiv
from wypp import check

# Sollwerte aus Aufgabe 2: positiv(x) = (x > 0)
check(positiv(1), True)
check(positiv(0), False)
check(positiv(-1), False)
check(positiv(5), True)
check(positiv(-10), False)
