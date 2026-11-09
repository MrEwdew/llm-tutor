from wypp import *

#   Kurzbeschreibung: Berechnet die tatsächliche Strecke des Boots.
#   Eingaben: Flussbreite a in Metern in (float) ab 0 & Bootsgeschwindigkeit vBoot in m/s in(float) größer als 0 & Strömungsgeschwindigkeit vFluss in m/s ab 0 in (float)
#   Ergebnis: Zurückgelegte Strecke in Metern in float)

def bootstrecke(a: float, vBoot: float, vFluss: float) -> float:
    t = ueberquerungszeit(a, vBoot)
    b = abdrift(t, vFluss)
    return (a * a + b * b) ** 0.5

#   Kurzbeschreibung: Berechnet die Überquerungszeit.
#   Eingaben: Flussbreite a in Metern in (float) & Bootsgeschwindigkeit vBoot in m/s in (float)
#   Ergebnis: Zeit in Sekunden in (float)

def ueberquerungszeit(a: float, vBoot: float) -> float:
    return a / vBoot

check(ueberquerungszeit(4.0, 2.0), 2.0)
check(ueberquerungszeit(0.0, 2.0), 0.0)


#   Kurzbeschreibung: Berechnet die Abdrift durch die Strömung.
#   Eingaben: Zeit t in Sekunden in (float) & Strömungsgeschwindigkeit vFluss in m/s in (float)
#   Ergebnis: Abdrift in Metern in (float)

def abdrift(t: float, vFluss: float) -> float:
    return t * vFluss

check(abdrift(2.0, 1.5), 3.0)
check(abdrift(2.0, 0.0), 0.0)
check(bootstrecke(4.0, 2.0, 1.5), 5.0)
check(bootstrecke(10.0, 2.0, 0.0), 10.0)
check(bootstrecke(0.0, 2.0, 1.5), 0.0)