#Automatically extracted from ./03_boolesche-werte-und-fallunterscheidung.md on 2026-09-29 07:12:26.822639 UTC



#----
#Quiz
#----

#[./03_boolesche-werte-und-fallunterscheidung.md:181]
def foo(x):
    return False or x == 5 and True or not (not x)

x = 10
print(foo(11 > x))



#--------------------------------------------
#Vergleiche und boolesche Werte in Aktion (1)
#--------------------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:200]
from wypp import *


#[./03_boolesche-werte-und-fallunterscheidung.md:205]
# Berechnet ob eine Person zu ermäßigtem Eintritt berechtigt ist.


#[./03_boolesche-werte-und-fallunterscheidung.md:213]
# Eingabe: Alter der Person, ein int
# Ergebnis: ein bool, True falls ermäßigter Eintritt möglich.


#[./03_boolesche-werte-und-fallunterscheidung.md:222]
def istErmäßigterEintrittMöglich(alter: int) -> bool:
    todo()



#--------------------------------------------
#Vergleiche und boolesche Werte in Aktion (2)
#--------------------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:241]
def istErmäßigterEintrittMöglich(alter: int) -> bool:
    return alter < 13 or alter >= 70



#--------
#Beispiel
#--------

#[./03_boolesche-werte-und-fallunterscheidung.md:265]
# Berechnet ob eine Person anhand ihrer Altersklassifikation zu ermäßigtem
# Eintritt berechtigt ist.



#------------------------------------------
#Schritt 2: Datenanalyse Fallunterscheidung
#------------------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:278]
# DATENBESCHREIBUNG
# Eine Altersklassifikation ist eins der folgenden:
# - Baby
# - Kleinkind
# - Kind
# - Teenager
# - Erwachsene
# - Erfahrene



#----------------------------------
#Schritt 2: Datenanalyse Aufzählung
#----------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:299]
# TYPDEFINITION
type Altersklassifikation = Literal['Baby', 'Kleinkind', 'Kind',
                                    'Teenager', 'Erwachsene', 'Erfahrene']



#-----------------------------------
#Datenbeschreibung vs. Typdefinition
#-----------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:310]
# DATENBESCHREIBUNG
# Eine Altersklassifikation ist eins der folgenden:
# - Baby
# - Kleinkind
# - Kind
# - Teenager
# - Erwachsene
# - Erfahrene


#[./03_boolesche-werte-und-fallunterscheidung.md:323]
# TYPDEFINITION
type Altersklassifikation = Literal['Baby', 'Kleinkind', 'Kind',
                                    'Teenager', 'Erwachsene', 'Erfahrene']



#------------------------
#Schritt 3: Funktionskopf
#------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:335]
# Berechnet ob eine Person anhand ihrer Altersklassifikation zu ermäßigtem
# Eintritt berechtigt ist.
# Eingabe: Altersklassifikation
# Ergebnis: ein bool, True falls ermäßigter Eintritt möglich.
def istErmäßigterEintrittMöglich2(altersklasse: Altersklassifikation) -> bool:
    todo()



#------------------------------
#Schritt 6: Rumpf komplettieren
#------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:441]
def istErmäßigterEintrittMöglich2(altersklasse: Altersklassifikation) -> bool:
    if altersklasse == 'Baby':
        return True
    elif altersklasse == 'Kleinkind':
        return True
    elif altersklasse == 'Kind':
        return True
    elif altersklasse == 'Teenager':
        return False
    elif altersklasse == 'Erwachsene':
        return False
    else: # altersklasse == 'Erfahrene'
        return True



#--------------------------------
#Varianten von `if-elif-else` (1)
#--------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:490]
def istErmäßigterEintrittMöglich3(altersklasse: Altersklassifikation) -> bool:
    if altersklasse == 'Baby':
        return True
    elif altersklasse == 'Kleinkind':
        return True
    elif altersklasse == 'Kind':
        return True
    elif altersklasse == 'Teenager':
        return False
    elif altersklasse == 'Erwachsene':
        return False
    elif altersklasse == 'Erfahrene':
        return True



#--------------------------------
#Varianten von `if-elif-else` (2)
#--------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:522]
def istErmäßigterEintrittMöglich4(altersklasse: Altersklassifikation) -> bool:
    if altersklasse == 'Baby':
        return True



#--------------------------------
#Varianten von `if-elif-else` (3)
#--------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:544]
def istErmäßigterEintrittMöglich5(altersklasse: Altersklassifikation) -> bool:
    if altersklasse == 'Baby':
        return True
    else:
        return False



#-----------------------------------
#Noch mehr Details zu `if-elif-else`
#-----------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:563]
def istErmäßigterEintrittMöglich6(altersklasse: Altersklassifikation) -> bool:
    if altersklasse == 'Baby':
        return True
    else:
        print("I'm so lazy, just returning False")
        return False



#----
#Quiz
#----

#[./03_boolesche-werte-und-fallunterscheidung.md:582]
def foo(x: Any) -> Any:
    if x == 42:
        return 'magic'
    elif False:
        return 'crocodile'
    elif x == 'Programmierung':
        return 42



#-----------------------------------
#Konstruktionsanleitung Datenanalyse
#-----------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:601]
# Eingaben: ...
# Ergebnis: ...



#-----------------------------------------
#Konstruktionsanleitung Fallunterscheidung
#-----------------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:628]
# Ein X ist eins der folgenden:
# - Fall 1
# - Fall 2
# - ...
# - Fall n


#[./03_boolesche-werte-und-fallunterscheidung.md:638]
# Eine Altersklassifikation ist eins der folgenden:
# - Baby
# - Kleinkind
# - Kind



#----------------------------------------------
#Ein weiteres Beispiel: Modellierung von Ampeln
#----------------------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:712]
# Berechnet den nächsten Zustand einer Ampel



#-------------------------------------------
#Schritt 2: Datenanalyse (Datenbeschreibung)
#-------------------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:723]
# Ein Ampelzustand ist eins der folgenden:
# - rot
# - rot-gelb
# - grün
# - gelb



#---------------------------------------
#Schritt 2: Datenanalyse (Typdefinition)
#---------------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:738]
type Ampelzustand = Literal['rot', 'rot-gelb', 'grün', 'gelb']



#-----------------------------------------
#Schritte 3 und 4: Funktionskopf und Tests
#-----------------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:744]
# Berechnet den nächsten Zustand einer Ampel
# Eingabe: Ampelzustand
# Ergebnis: der nächste Ampelzustand
def nächsterAmpelzustand(ampel: Ampelzustand) -> Ampelzustand:
    todo()



#----------------
#Schritt 6: Rumpf
#----------------

#[./03_boolesche-werte-und-fallunterscheidung.md:778]
def nächsterAmpelzustand(ampel: Ampelzustand) -> Ampelzustand:
    if ampel == 'rot':
        return 'rot-gelb'
    elif ampel == 'rot-gelb':
        return 'grün'
    elif ampel == 'grün':
        return 'gelb'
    elif ampel == 'gelb':
        return 'rot'



#---------------------------
#Schritt 1: Kurzbeschreibung
#---------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:807]
# Berechnet die Altersklassifikation für das gegebene Alter.



#-----------------------
#Schritt 2: Datenanalyse
#-----------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:812]
# Berechnet die Altersklassifikation für das gegebene Alter.
# * Eingabe: das Alter, ein int
# * Ausgabe: die Altersklassifikation (die bereits bekannte
#   Aufzählung Altersklassifikation)



#------------------------
#Schritt 3: Funktionskopf
#------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:821]
# Berechnet die Altersklassifikation für das gegebene Alter.
# * Eingabe: das Alter, ein int
# * Ausgabe: die Altersklassifikation (die bereits bekannte
#   Aufzählung Altersklassifikation)
def klassifiziereAlter(alter: int) -> Altersklassifikation:
    todo()



#----------------
#Schritt 6: Rumpf
#----------------

#[./03_boolesche-werte-und-fallunterscheidung.md:868]
def klassifiziereAlter(alter: int) -> Altersklassifikation:
    if alter < 1:
        return 'Baby'
    elif alter == 1 or alter == 2:
        return 'Kleinkind'
    elif alter >= 3 and alter <= 12:
        return 'Kind'
    elif alter >= 13 and alter <= 17:
        return 'Teenager'
    elif alter >= 18 and alter <= 69:
        return 'Erwachsene'
    elif alter >= 70:
        return 'Erfahrene'



#--------------------------------------------
#Vergleiche und boolesche Werte in Aktion (2)
#--------------------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:231]
check(istErmäßigterEintrittMöglich(12), True)
check(istErmäßigterEintrittMöglich(13), False)
check(istErmäßigterEintrittMöglich(69), False)
check(istErmäßigterEintrittMöglich(70), True)



#----------------
#Schritt 4: Tests
#----------------

#[./03_boolesche-werte-und-fallunterscheidung.md:349]
check(istErmäßigterEintrittMöglich2('Baby'), True)
check(istErmäßigterEintrittMöglich2('Kleinkind'), True)
check(istErmäßigterEintrittMöglich2('Kind'), True)
check(istErmäßigterEintrittMöglich2('Teenager'), False)
check(istErmäßigterEintrittMöglich2('Erwachsene'), False)
check(istErmäßigterEintrittMöglich2('Erfahrene'), True)



#-----------------------------------------
#Schritte 3 und 4: Funktionskopf und Tests
#-----------------------------------------

#[./03_boolesche-werte-und-fallunterscheidung.md:752]
check(nächsterAmpelzustand('rot'), 'rot-gelb')
check(nächsterAmpelzustand('rot-gelb'), 'grün')
check(nächsterAmpelzustand('grün'), 'gelb')
check(nächsterAmpelzustand('gelb'), 'rot')



#----------------
#Schritt 4: Tests
#----------------

#[./03_boolesche-werte-und-fallunterscheidung.md:832]
check(klassifiziereAlter(0), 'Baby')
check(klassifiziereAlter(1), 'Kleinkind')
check(klassifiziereAlter(2), 'Kleinkind')
check(klassifiziereAlter(3), 'Kind')
check(klassifiziereAlter(12), 'Kind')
check(klassifiziereAlter(13), 'Teenager')
check(klassifiziereAlter(17), 'Teenager')
check(klassifiziereAlter(18), 'Erwachsene')
check(klassifiziereAlter(69), 'Erwachsene')
check(klassifiziereAlter(70), 'Erfahrene')

