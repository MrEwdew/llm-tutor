#Automatically extracted from ./02_strukturierte-entwicklung.md on 2026-09-29 07:08:11.96568 UTC



#---------------
#Zusammenfassung
#---------------

#[./02_strukturierte-entwicklung.md:260]
from wypp import *

# monatlichen Rechnungsbetrag für Tarif Billig-Strom berechnen
# Eingabe: Monatsverbrauch in Kilowattstunden, als float.
# Ergebnis: den monatlich zu zahlenden Betrag, als float.
def billigStrom(kwh: float) -> float:
    return kwh * 0.19 + 4.99

check(billigStrom(10), 6.89)
check(billigStrom(0), 4.99)
check(billigStrom(-2), 4.61)



#---------------------------------------
#Die komplette Funktion "Watt für wenig"
#---------------------------------------

#[./02_strukturierte-entwicklung.md:350]
# monatlichen Rechnungsbetrag für Tarif "Watt für wenig" berechnen
# Eingabe: Monatsverbrauch in Kilowattstunden, ein float.
# Ergebnis: Rechnungsbetrag, ein float.
def wattFuerWenig(kwh: float) -> float:
    return kwh * 0.16 + 8.2

check(wattFuerWenig(10), 9.8)
check(wattFuerWenig(0), 8.20)
check(wattFuerWenig(-2), 7.88)

