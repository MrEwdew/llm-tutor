#Automatically extracted from ./02_strukturierte-entwicklung.md on 2026-09-29 07:08:11.96568 UTC



#------------
#Vorbereitung
#------------

#[./02_strukturierte-entwicklung.md:46]
from wypp import *



#---------------------------
#Schritt 1: Kurzbeschreibung
#---------------------------

#[./02_strukturierte-entwicklung.md:64]
# monatlichen Rechnungsbetrag für Tarif Billig-Strom berechnen



#-----------------------
#Schritt 2: Datenanalyse
#-----------------------

#[./02_strukturierte-entwicklung.md:82]
# Eingabe: Monatsverbrauch in Kilowattstunden, als float.
# Ergebnis: den monatlich zu zahlenden Betrag, als float.



#------------------------
#Schritt 3: Funktionskopf
#------------------------

#[./02_strukturierte-entwicklung.md:109]
def billigStrom(kwh: float) -> float:
    todo()



#----------------------
#Typen im Funktionskopf
#----------------------

#[./02_strukturierte-entwicklung.md:130]
def billigStrom(kwh: float) -> float:
    todo()



#----------------
#Schritt 6: Rumpf
#----------------

#[./02_strukturierte-entwicklung.md:245]
def billigStrom(kwh: float) -> float:
    return kwh * 0.19 + 4.99



#------------------------------------
#"Watt für wenig" im Schnelldurchgang
#------------------------------------

#[./02_strukturierte-entwicklung.md:308]
# monatlichen Rechnungsbetrag für Tarif "Watt für wenig" berechnen


#[./02_strukturierte-entwicklung.md:316]
# Eingabe: Monatsverbrauch in Kilowattstunden, ein float.
# Ergebnis: Rechnungsbetrag, ein float.


#[./02_strukturierte-entwicklung.md:323]
def wattFuerWenig(kwh: float) -> float:
    todo()


#[./02_strukturierte-entwicklung.md:343]
def wattFuerWenig(kwh: float) -> float:
    return kwh * 0.16 + 8.2



#----------------
#Schritt 4: Tests
#----------------

#[./02_strukturierte-entwicklung.md:179]
check(billigStrom(10), 6.89)
check(billigStrom(0), 4.99)
check(billigStrom(-2), 4.61)



#------------------------------------
#"Watt für wenig" im Schnelldurchgang
#------------------------------------

#[./02_strukturierte-entwicklung.md:332]
check(wattFuerWenig(10), 9.8)
check(wattFuerWenig(0), 8.20)
check(wattFuerWenig(-2), 7.88)

