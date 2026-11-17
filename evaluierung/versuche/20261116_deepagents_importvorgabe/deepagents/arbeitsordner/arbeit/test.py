import sys
sys.path.insert(0, "/work/material")
from aufgabe_01 import quadrat
from aufgabe_02 import positiv
from wypp import check

# Test 1: quadrat(x) should return x*x
check(quadrat(4) == 16, "quadrat(4) should be 16")
check(quadrat(-3) == 9, "quadrat(-3) should be 9")
check(quadrat(0) == 0, "quadrat(0) should be 0")

# Test 2: positiv(x) should return True only for x > 0
check(positiv(5) == True, "positiv(5) should be True")
check(positiv(0) == False, "positiv(0) should be False")
check(positiv(-2) == False, "positiv(-2) should be False")
