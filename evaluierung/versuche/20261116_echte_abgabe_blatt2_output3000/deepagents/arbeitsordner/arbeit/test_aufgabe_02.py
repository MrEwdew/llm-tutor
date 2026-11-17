from wypp import *
import sys
sys.path.append('/work/material/abgabe')
from Aufgabe2 import rueckenNummer

# Testfälle für Aufgabe 2: Rückennummer zu Position
check(rueckenNummer(1), "Torhueter")
check(rueckenNummer(2), "Abwehrspieler")
check(rueckenNummer(3), "Abwehrspieler")
check(rueckenNummer(4), "Abwehrspieler")
check(rueckenNummer(5), "Abwehrspieler")
check(rueckenNummer(6), "Mittelfeldspieler")
check(rueckenNummer(7), "Mittelfeldspieler")
check(rueckenNummer(8), "Mittelfeldspieler")
check(rueckenNummer(10), "Mittelfeldspieler")
check(rueckenNummer(9), "Stuermer")
check(rueckenNummer(11), "Stuermer")
check(rueckenNummer(12), "Ersatzspieler")
check(rueckenNummer(99), "Ersatzspieler")
check(rueckenNummer(100), "Ersatzspieler")