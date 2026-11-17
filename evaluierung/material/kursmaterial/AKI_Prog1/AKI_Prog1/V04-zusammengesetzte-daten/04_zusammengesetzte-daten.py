#Automatically extracted from ./04_zusammengesetzte-daten.md on 2026-09-29 07:13:22.239154 UTC



#--------------------------------------------
#Datenbeschreibung für zusammengesetzte Daten
#--------------------------------------------

#[./04_zusammengesetzte-daten.md:64]
# DATENBESCHREIBUNG
# Ein Computer besteht aus:
# - Prozessor (str)
# - Festplatten-Kapazität in Gigabyte (int)
# - Hauptspeicher-Kapazität in Gigabyte (int)



#------------------------------------------
#Modellierung in unserer Programmiersprache
#------------------------------------------

#[./04_zusammengesetzte-daten.md:81]
from wypp import *

# TYPDEFINITION
@record
class Computer:
    prozessor: str
    festplatte: int
    hauptspeicher: int



#----------------------------
#Kopf der Konstruktorfunktion
#----------------------------

#[./04_zusammengesetzte-daten.md:117]
# def Computer(prozessor: str, festplatte: int, hauptspeicher: int) -> Computer



#---------------------------------------
#Zugriff auf Eigenschaften eines Records
#---------------------------------------

#[./04_zusammengesetzte-daten.md:148]
# c.prozessor    : str
# c.festplatte   : int
# c.hauptspeicher: int



#--------------------
#Arbeiten mit Records
#--------------------

#[./04_zusammengesetzte-daten.md:161]
# Gesamtspeicher berechnen
# Eingabe: ein Computer
# Ergebnis: die Summe von Haupt- und Festplattenspeicher (int)
def totalMemory(c: Computer) -> int:
    todo()



#---------
#Der Rumpf
#---------

#[./04_zusammengesetzte-daten.md:196]
def totalMemory(c):
    return c.festplatte + c.hauptspeicher



#------------------------------------
#Funktionen die Records zurückliefern
#------------------------------------

#[./04_zusammengesetzte-daten.md:240]
# Computer für Modell zusammenstellen.



#------------
#Datenanalyse
#------------

#[./04_zusammengesetzte-daten.md:253]
# Ein Modell ist eins der folgenden:
# - Billigmodell
# - Gamer-Modell
# - Office-Modell
type Modell = Literal['billig', 'gamer', 'office']



#-----------------------
#Funktionskopf und Tests
#-----------------------

#[./04_zusammengesetzte-daten.md:263]
# Computer für ein bestimmtes Modell zusammenstellen.
# Eingabe: ein Modell
# Ergebnis: ein Computer
def standardComputer(modell: Modell) -> Computer:
    todo()



#-------
#Fertig!
#-------

#[./04_zusammengesetzte-daten.md:328]
def standardComputer(modell):
    if modell == 'billig':
        return Computer('Sempron', 500, 2)
    elif modell == 'gamer':
        return Computer('Quad', 1000, 16)
    elif modell == 'office':
        return Computer('Intel i7', 750, 8)



#----------------------------------------
#Datenbeschreibung zusammengesetzte Daten
#----------------------------------------

#[./04_zusammengesetzte-daten.md:349]
# Ein X hat / besteht aus / ist charakterisiert durch:
# - Bestandteil / Eigenschaft 1 (Typ 1)
# - Bestandteil / Eigenschaft 2 (Typ 2)
# ...
# - Bestandteil / Eigenschaft n (Typ n)


#[./04_zusammengesetzte-daten.md:359]
# Ein Computer besteht aus:
# - Prozessor (str)
# - Festplatten-Kapazität in Gigabyte (int)
# - Hauptspeicher-Kapazität in Gigabyte (int)



#------------------------------------
#Typdefinition zusammengesetzte Daten
#------------------------------------

#[./04_zusammengesetzte-daten.md:394]
@record
class Computer:
    prozessor: str
    festplatte: int
    hauptspeicher: int



#-----------------------------------
#Typen für Konstruktor und Attribute
#-----------------------------------

#[./04_zusammengesetzte-daten.md:411]
# Konstruktor:
# def T(s1: T1, s2: T2, ..., sn: Tn) -> T
#
# Für ein Record-Objekt r des Records T gibt es folgende Attribute
# r.s1 : T1
# r.s2 : T2
# ...
# r.sn : Tn



#-----------
#Gürteltiere
#-----------

#[./04_zusammengesetzte-daten.md:537]
# Gürteltier nach der Fütterung



#------------
#Datenanalyse
#------------

#[./04_zusammengesetzte-daten.md:543]
# Eingabe: ein Gürteltier und die Menge an Futter in Gramm (int).
# Ergebnis: das Gürteltier nach der Fütterung.



#----------------------------------------------
#Datenbeschreibung und Typdefinition für Status
#----------------------------------------------

#[./04_zusammengesetzte-daten.md:559]
# Ein Status ist eins der folgenden:
# - 'tot'
# - 'lebendig'
type Status = Literal['tot', 'lebendig']



#------------------------------------------------------
#Datenbeschreibung und Record-Definition für Gürteltier
#------------------------------------------------------

#[./04_zusammengesetzte-daten.md:568]
# Ein Gürteltier ist charakterisiert durch
# - sein Gewicht in Gramm (int)
# - seinen Status tot oder lebendig
@record
class Gürteltier:
    gewicht: int
    totOderLebendig: Status


#[./04_zusammengesetzte-daten.md:580]
dora = Gürteltier(25000, 'lebendig')
daniel = Gürteltier(30000, 'tot')



#-----------------------
#Funktionskopf und Tests
#-----------------------

#[./04_zusammengesetzte-daten.md:587]
# Gürteltier nach der Fütterung
# Eingabe: ein Gürteltier und die Menge an Futter in Gramm (int).
# Ergebnis: das Gürteltier nach der Fütterung.
def füttereGürteltier(dillo: Gürteltier, foodWeight: int) -> Gürteltier:
    todo()



#---------------------------
#Schablonen, vierter Streich
#---------------------------

#[./04_zusammengesetzte-daten.md:662]
# Gürteltier nach der Fütterung
# Eingabe: ein Gürteltier und die Menge an Futter in Gramm (int).
# Ergebnis: das Gürteltier nach der Fütterung.
def füttereGürteltier(dillo: Gürteltier, foodWeight: int) -> Gürteltier:
    if dillo.totOderLebendig == 'tot':
       return dillo
    else:
       return Gürteltier(
           dillo.gewicht + foodWeight // 2,
           dillo.totOderLebendig
       )



#--------------------
#Arbeiten mit Records
#--------------------

#[./04_zusammengesetzte-daten.md:171]
check(totalMemory(Computer('Intel i9', 1000, 16)), 1016)
check(totalMemory(Computer('AMD', 250, 8)), 258)



#-----------------------
#Funktionskopf und Tests
#-----------------------

#[./04_zusammengesetzte-daten.md:271]
check(standardComputer('billig'), Computer('Sempron', 500, 2))
check(standardComputer('gamer'), Computer('Quad', 1000, 16))
check(standardComputer('office'), Computer('Intel i7', 750, 8))


#[./04_zusammengesetzte-daten.md:597]
check(füttereGürteltier(dora, 2000), Gürteltier(26000, 'lebendig'))
check(füttereGürteltier(daniel, 1000), Gürteltier(30000, 'tot'))

