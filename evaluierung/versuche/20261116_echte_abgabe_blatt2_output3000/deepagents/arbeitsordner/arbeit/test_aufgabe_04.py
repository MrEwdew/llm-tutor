from wypp import *
import sys
sys.path.append('/work/material/abgabe')
from Aufgabe4 import clamp

# Testfälle für Aufgabe 4: clamp-Funktion
check(clamp(5, 67.5, 89.5), 67.5)
check(clamp(-2, 0, 10), 0)
check(clamp(27.5, 0, 10), 10)
check(clamp(5.5, 0, 0), 0)
check(clamp(10, 0, 10), 10)
check(clamp(2.5, 1, 3), 2.5)
check(clamp(-4, -3, -1), -3)
check(clamp(7, 3, 3), 3)
check(clamp(100, 50, 75), 75)
check(clamp(-50, -75, -25), -25)