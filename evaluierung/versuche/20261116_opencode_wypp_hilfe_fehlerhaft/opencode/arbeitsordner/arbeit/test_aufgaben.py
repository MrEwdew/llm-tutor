import sys
sys.path.insert(0, "/work/material")
from aufgabe_01 import quadrat
from aufgabe_02 import positiv
from wypp import check

# Test 1: quadrat(x) soll x*x zurueckgeben
check(quadrat(3), 9)    # Sollwert: 3*3 = 9
check(quadrat(-2), 4)   # Sollwert: (-2)*(-2) = 4
check(quadrat(0), 0)    # Sollwert: 0*0 = 0

# Test 2: positiv(x) soll genau fuer x > 0 True liefern
check(positiv(5), True)   # Sollwert: 5 > 0 -> True
check(positiv(0), False)  # Sollwert: 0 > 0 -> False
check(positiv(-3), False) # Sollwert: -3 > 0 -> False
