from wypp import *


# Automatisches zuordnen von Bußgeldern für zu Langes Parken
# Eingabe: Stunden anzahl in Minuten (Typ: int)
# Ergebnis: Bußgeldbescheid in Euro (Typ: int)

def bussgeldbescheid(parkzeitueberschritt: int) -> int:
    if parkzeitueberschritt <= 30:
        return (10)
    elif parkzeitueberschritt <= 60 :
        return (15)
    elif parkzeitueberschritt <= 120:
        return (20)
    elif parkzeitueberschritt <= 180:
        return (25)
    elif parkzeitueberschritt > 180:
       return (((math.ceil(parkzeitueberschritt/60) - 1) * 10)) 
    



check(bussgeldbescheid(30), 10)
check(bussgeldbescheid(31), 15)
check(bussgeldbescheid(60), 15)
check(bussgeldbescheid(61), 20)
check(bussgeldbescheid(120), 20)
check(bussgeldbescheid(121), 25)
check(bussgeldbescheid(180), 25)
check(bussgeldbescheid(181), 30)
check(bussgeldbescheid(600), 90)