import sys
sys.path.insert(0, "/work/arbeit/abgabe")
from aufgabe_01 import quadrat
from wypp import check

# Sollwerte aus Aufgabenstellung: quadrat(x) = x*x
check(quadrat(0), 0)
check(quadrat(1), 1)
check(quadrat(2), 4)
check(quadrat(-3), 9)
check(quadrat(5), 25)