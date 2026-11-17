from wypp import *
import sys
sys.path.append('/work/material/abgabe')
from Aufgabe1 import luisasLieblingsZahlen

# Testfälle für Aufgabe 1: Luises Lieblingszahlen
check(luisasLieblingsZahlen(6), True)
check(luisasLieblingsZahlen(11), True)
check(luisasLieblingsZahlen(13), True)
check(luisasLieblingsZahlen(12), False)
check(luisasLieblingsZahlen(100), False)
check(luisasLieblingsZahlen(100.1), True)
check(luisasLieblingsZahlen(9999), True)
check(luisasLieblingsZahlen(5), False)
check(luisasLieblingsZahlen(101), True)