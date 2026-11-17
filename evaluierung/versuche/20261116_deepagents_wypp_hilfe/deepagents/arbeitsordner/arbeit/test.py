import sys
sys.path.insert(0, "/work/material")
from aufgabe_01 import quadrat
from aufgabe_02 import positiv
from wypp import check

# Aufgabe 1: quadrat(x) soll x*x zurückgeben
check(quadrat(3), 9)    # Sollwert: 3*3 = 9
check(quadrat(-2), 4)   # Sollwert: (-2)*(-2) = 4
check(quadrat(0), 0)    # Sollwert: 0*0 = 0

# Aufgabe 2: positiv(x) soll genau für x > 0 True liefern
check(positiv(5), True)   # Sollwert: 5 > 0 → True
check(positiv(-1), False) # Sollwert: -1 > 0 → False
check(positiv(0), False)  # Sollwert: 0 > 0 → False
