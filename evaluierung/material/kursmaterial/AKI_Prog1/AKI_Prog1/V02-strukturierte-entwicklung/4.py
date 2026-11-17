#Automatically extracted from ./02_strukturierte-entwicklung.md on 2026-09-29 07:08:11.96568 UTC



#---------------------------------------
#Kurzbeschreibung, Datenanalyse und Kopf
#---------------------------------------

#[./02_strukturierte-entwicklung.md:385]
from wypp import *


#[./02_strukturierte-entwicklung.md:389]
# monatlichen Rechnungsbetrag für einen Stromtarif mit Grundgebühr und
# Verbrauchspreis berechnen.


#[./02_strukturierte-entwicklung.md:398]
# Eingaben:
#  * Monatsverbrauch in Kilowattstunden, ein float.
#  * Grundgebühr, ein float.
#  * Verbrauchspreis, ein float.
# Ergebnis: Rechnungsbetrag, ein float.


#[./02_strukturierte-entwicklung.md:410]
def stromtarifRechnungsbetrag(kwh: float,
                              grundgebuehr: float,
                              verbrauchspreis: float) -> float:
    todo()



#-----
#Rumpf
#-----

#[./02_strukturierte-entwicklung.md:436]
def stromtarifRechnungsbetrag(kwh: float,
                              grundgebuehr: float,
                              verbrauchspreis: float) -> float:
    return kwh * verbrauchspreis + grundgebuehr



#--------------------------------------------------------
#`billigStrom` und `wattFuerWenig` ohne Logik-Duplikation
#--------------------------------------------------------

#[./02_strukturierte-entwicklung.md:445]
# monatlichen Rechnungsbetrag für Tarif Billig-Strom berechnen
# Eingabe: Monatsverbrauch in Kilowattstunden, als float.
# Ergebnis: den monatlich zu zahlenden Betrag, als float.
def billigStrom(kwh: float) -> float:
    return stromtarifRechnungsbetrag(kwh, 4.99, 0.19)

check(billigStrom(10), 6.89)
check(billigStrom(0), 4.99)
check(billigStrom(-2), 4.61)

# monatlichen Rechnungsbetrag für Tarif "Watt für wenig" berechnen
# Eingabe: Monatsverbrauch in Kilowattstunden, ein float.
# Ergebnis: Rechnungsbetrag, ein float.
def wattFuerWenig(kwh: float) -> float:
    return stromtarifRechnungsbetrag(kwh, 8.2, 0.16)

check(wattFuerWenig(10), 9.8)
check(wattFuerWenig(0), 8.20)
check(wattFuerWenig(-2), 7.88)



#-----
#Tests
#-----

#[./02_strukturierte-entwicklung.md:423]
check(stromtarifRechnungsbetrag(10, 4.99, 0.19), 6.89)
check(stromtarifRechnungsbetrag(0, 4.99, 0.19), 4.99)
check(stromtarifRechnungsbetrag(-2, 4.99, 0.19), 4.61)
check(stromtarifRechnungsbetrag(10, 8.2, 0.16), 9.8)
check(stromtarifRechnungsbetrag(0, 8.2, 0.16), 8.20)
check(stromtarifRechnungsbetrag(-2, 8.2, 0.16), 7.88)

