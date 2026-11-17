import sys
sys.path.insert(0, "/work/material")
from aufgabe_01 import quadrat
from aufgabe_02 import positiv
from wypp import check

# Testaufgabe 1: quadrat(x) soll x*x zurueckgeben
check(quadrat(0), 0)
check(quadrat(3), 9)
check(quadrat(-2), 4)

# Testaufgabe 2: positiv(x) soll genau fuer x > 0 True liefern
check(positiv(5), True)
check(positiv(0), False)
check(positiv(-3), False)