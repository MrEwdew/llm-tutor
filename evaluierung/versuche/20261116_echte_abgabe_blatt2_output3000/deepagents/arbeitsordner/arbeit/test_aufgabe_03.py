from wypp import *
import sys
sys.path.append('/work/material/abgabe')
from Aufgabe3 import bussgeldbescheid

# Testfälle für Aufgabe 3: Bußgeldberechnung
check(bussgeldbescheid(30), 10)
check(bussgeldbescheid(31), 15)
check(bussgeldbescheid(60), 15)
check(bussgeldbescheid(61), 20)
check(bussgeldbescheid(120), 20)
check(bussgeldbescheid(121), 25)
check(bussgeldbescheid(180), 25)
check(bussgeldbescheid(181), 30)
check(bussgeldbescheid(600), 90)
check(bussgeldbescheid(0), 10)