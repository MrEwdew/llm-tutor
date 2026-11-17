#Automatically extracted from ./05_gemischte-daten.md on 2026-09-29 07:13:42.420429 UTC



#----------------------
#Beispiel: Tiere wiegen
#----------------------

#[./05_gemischte-daten.md:54]
from wypp import *

# Gewicht eines Tiers feststellen.



#------------------
#Datenanalyse Tiere
#------------------

#[./05_gemischte-daten.md:65]
# Ein Tier ist eins der folgenden
# - Gürteltier
# - Papagei



#--------------------------
#Datenanalyse für Papageien
#--------------------------

#[./05_gemischte-daten.md:76]
# Ein Papagei hat folgende Eigenschaften:
# - Gewichtsklasse
# - Satz den er sagt (String)
#
# Eine Gewichtsklasse ist eins der folgenden
# - leicht
# - mittel
# - schwer



#--------------------------------------
#Typen für Gewichtsklasse und Papageien
#--------------------------------------

#[./05_gemischte-daten.md:91]
type Gewichtsklasse = Literal['leicht', 'mittel', 'schwer']


#[./05_gemischte-daten.md:97]
@record
class Papagei:
    gewichtsklasse: Gewichtsklasse
    satz: str
# Papagei: (Gewichtsklasse, str) -> Papagei
# Für einen Papagei p gilt:
# p.gewichtsklasse: Gewichtsklasse
# p.satz: str


#[./05_gemischte-daten.md:110]
paula = Papagei('mittel', "Let's go to the punkrock show")
peter = Papagei('leicht', 'oh no, not again')



#---------------------
#Typen für Gürteltiere
#---------------------

#[./05_gemischte-daten.md:119]
type Status = Literal['tot', 'lebendig']

@record
class Gürteltier:
    gewicht: int
    totOderLebendig: Status
dora = Gürteltier(25000, 'lebendig')
daniel = Gürteltier(30000, 'tot')



#---------------
#Typen für Tiere
#---------------

#[./05_gemischte-daten.md:135]
type Tier = Union[Gürteltier, Papagei]



#--------------------------------------
#Funktionskopf und Tests für das Wiegen
#--------------------------------------

#[./05_gemischte-daten.md:148]
# Gewicht eines Tiers feststellen.
# Eingabe: ein Tier (animal)
# Ergebnis: das Gewicht (int)
def wiegeTier(animal: Tier) -> int:
    todo()



#---------------------------------------------------
#Kurzbeschreibung und Funktionskopf für `isinstance`
#---------------------------------------------------

#[./05_gemischte-daten.md:212]
# isinstance(x, t) prüft ob der Wert x vom Typ t ist.
# def isinstance(x: Any, t: type) -> bool



#-----
#Rumpf
#-----

#[./05_gemischte-daten.md:280]
# Gewicht eines Tiers feststellen.
# Eingabe: ein Tier (animal)
# Ergebnis: das Gewicht (int)
def wiegeTier(animal: Tier) -> int:
    if isinstance(animal, Gürteltier):
        return animal.gewicht
    elif isinstance(animal, Papagei):
        if animal.gewichtsklasse == 'leicht':
            return 900
        elif animal.gewichtsklasse == 'mittel':
            return 1200
        else:
            return 1600



#-----------------------------
#Einführen einer Hilfsfunktion
#-----------------------------

#[./05_gemischte-daten.md:311]
# Bestimmt das Gewicht für eine Gewichtsklasse
# Eingabe: die Gewichtsklasse
# Ergebnis: das Gewicht für die Klasse (int)
def gewichtFürGewichtsklasse(weightClass: Gewichtsklasse) -> int:
    if weightClass == 'leicht':
        return 900
    elif weightClass == 'mittel':
        return 1200
    else:
        return 1600

check(gewichtFürGewichtsklasse('leicht'), 900)
check(gewichtFürGewichtsklasse('mittel'), 1200)
check(gewichtFürGewichtsklasse('schwer'), 1600)



#--------------------------
#Benutzen der Hilfsfunktion
#--------------------------

#[./05_gemischte-daten.md:330]
# Gewicht eines Tiers feststellen.
# Eingabe: ein Tier (animal)
# Ergebnis: das Gewicht (int)
def wiegeTier2(animal: Tier) -> int:
    if isinstance(animal, Gürteltier):
        return animal.gewicht
    elif isinstance(animal, Papagei):
        return gewichtFürGewichtsklasse(animal.gewichtsklasse)



#--------------------------------------
#Konstruktionsanleitung gemischte Daten
#--------------------------------------

#[./05_gemischte-daten.md:405]
type Tier = Union[Gürteltier, Papagei]



#------------------------------------------------
#Kurzbeschreibung, Datenanalyse und Funktionskopf
#------------------------------------------------

#[./05_gemischte-daten.md:440]
# Tier füttern
# Eingaben: das Tier und die Futtermenge in Gramm (int)
# Ergebnis: das Tier nach der Fütterung
def füttereTier(animal: Tier, foodWeight: int) -> Tier:
    todo()



#---------
#Schablone
#---------

#[./05_gemischte-daten.md:475]
def füttereGürteltier(dillo, foodWeight):
    if dillo.totOderLebendig == 'tot':
       return dillo
    else:
       return Gürteltier(
           dillo.gewicht + foodWeight // 2,
           dillo.totOderLebendig
       )



#-----
#Rumpf
#-----

#[./05_gemischte-daten.md:514]
# Tier füttern
# Eingaben: das Tier und die Futtermenge in Gramm (int)
# Ergebnis: das Tier nach der Fütterung
def füttereTier(animal, foodWeight):
    if isinstance(animal, Gürteltier):
        return füttereGürteltier(animal, foodWeight)
    elif isinstance(animal, Papagei):
        return fütterePapagei(animal, foodWeight)



#-----------------
#Papageien füttern
#-----------------

#[./05_gemischte-daten.md:532]
# Füttere einen Papagei
# Eingaben: ein Papagei und die Futtermenge in Gramm (int)
# Ergebnis: der gefütterte Papagei
def fütterePapagei(p: Papagei, foodWeight: int) -> Papagei:
    todo()



#-----
#Rumpf
#-----

#[./05_gemischte-daten.md:570]
# Füttere einen Papagei
# Eingaben: ein Papagei und die Futtermenge in Gramm (int)
# Ergebnis: der gefütterte Papagei
def fütterePapagei(p: Papagei, foodWeight: int) -> Papagei:
    newClass = nächsteGewichtsklasse(p.gewichtsklasse, foodWeight)
    return Papagei(newClass, p.satz)



#-----------------------
#`nächsteGewichtsklasse`
#-----------------------

#[./05_gemischte-daten.md:583]
# Gibt die nächsthöhere Gewichtsklasse wieder
# Eingaben: eine Gewichtsklasse und die Futtermenge in Gramm (int)
# Ergebnis: die Gewichtsklasse nach der Fütterung.
def nächsteGewichtsklasse(weightClass: Gewichtsklasse,
                          foodWeight: int) -> Gewichtsklasse:
    todo()



#--------------------------------------
#`nächsteGewichtsklasse` implementieren
#--------------------------------------

#[./05_gemischte-daten.md:648]
# Gibt die nächsthöhere Gewichtsklasse wieder
# Eingaben: eine Gewichtsklasse und die Futtermenge in Gramm (int)
# Ergebnis: die Gewichtsklasse nach der Fütterung.
def nächsteGewichtsklasse(weightClass: Gewichtsklasse,
                          foodWeight: int) -> Gewichtsklasse:
    if foodWeight < 500:
        return weightClass
    else:
        if weightClass == 'leicht':
            return 'mittel'
        elif weightClass == 'mittel':
            return 'schwer'
        else:
            return 'schwer'



#--------------------------
#Repräsentation von Fehlern
#--------------------------

#[./05_gemischte-daten.md:682]
# Ein Fehler besitzt folgende Eigenschaften:
# - Fehlermeldung (str)
@record
class Error:
    message: str



#--------------------------
#Gemischte Daten für Fehler
#--------------------------

#[./05_gemischte-daten.md:701]
# Füttert ein Gürteltier, aber nur wenn es lebt.
def füttereLebendesGürteltier(dillo: Gürteltier,
                              foodWeight: int) -> Union[Error, Gürteltier]:
    todo()



#-------------------------
#Tests und Implementierung
#-------------------------

#[./05_gemischte-daten.md:726]
def füttereLebendesGürteltier(dillo: Gürteltier,
                              foodWeight: int) -> Union[Error, Gürteltier]:
    if dillo.totOderLebendig == 'tot':
       return Error('Gürteltier tot')
    else:
       return Gürteltier(
           dillo.gewicht + foodWeight // 2,
           'lebendig'
       )



#--------------------------------------
#Funktionskopf und Tests für das Wiegen
#--------------------------------------

#[./05_gemischte-daten.md:156]
check(wiegeTier(dora), 25000)
check(wiegeTier(peter), 900)


#[./05_gemischte-daten.md:161]
check(wiegeTier2(dora), 25000)
check(wiegeTier2(peter), 900)



#-----
#Tests
#-----

#[./05_gemischte-daten.md:452]
check(füttereTier(dora, 2000), Gürteltier(26000, 'lebendig'))
check(füttereTier(daniel, 1000), Gürteltier(30000, 'tot'))


#[./05_gemischte-daten.md:459]
check(füttereTier(paula, 600), Papagei('schwer', "Let's go to the punkrock show"))
check(füttereTier(paula, 400), Papagei('mittel', "Let's go to the punkrock show"))
check(füttereTier(füttereTier(paula, 600), 600),
      Papagei('schwer', "Let's go to the punkrock show"))
check(füttereTier(peter, 500), Papagei('mittel', "oh no, not again"))
check(füttereTier(peter, 499), peter)



#-----------------
#Papageien füttern
#-----------------

#[./05_gemischte-daten.md:542]
check(fütterePapagei(paula, 500),
      Papagei('schwer', "Let's go to the punkrock show"))
check(fütterePapagei(paula, 499), paula)
check(fütterePapagei(peter, 500), Papagei('mittel', "oh no, not again"))
check(fütterePapagei(peter, 499), peter)



#-----------------------
#`nächsteGewichtsklasse`
#-----------------------

#[./05_gemischte-daten.md:594]
check(nächsteGewichtsklasse('mittel', 500), 'schwer')
check(nächsteGewichtsklasse('leicht', 600), 'mittel')
check(nächsteGewichtsklasse('leicht', 2000), 'mittel')
check(nächsteGewichtsklasse('leicht', 499), 'leicht')
check(nächsteGewichtsklasse('schwer', 1000), 'schwer')



#-------------------------
#Tests und Implementierung
#-------------------------

#[./05_gemischte-daten.md:715]
check(füttereLebendesGürteltier(dora, 2000), Gürteltier(26000, 'lebendig'))
check(füttereLebendesGürteltier(daniel, 1000), Error('Gürteltier tot'))

