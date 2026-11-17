import sys
sys.path.insert(0, "/work/material")
from aufgabe_01 import quadrat
from aufgabe_02 import positiv
from wypp import check

# Testaufgabe 1: quadrat(x) -> x*x
check(quadrat(0), 0)      # 0*0 = 0
check(quadrat(3), 9)      # 3*3 = 9
check(quadrat(-2), 4)     # (-2)*(-2) = 4

# Testaufgabe 2: positiv(x) -> x > 0
check(positiv(5), True)   # 5 > 0
check(positiv(0), False)  # 0 > 0 -> falsch
check(positiv(-3), False) # -3 > 0 -> falsch
