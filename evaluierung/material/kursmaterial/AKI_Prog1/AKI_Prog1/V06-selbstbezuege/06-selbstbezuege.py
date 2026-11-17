#Automatically extracted from ./06-selbstbezuege.md on 2026-10-26 17:29:37.008152 UTC



#---------------------------
#Bäche in Python modellieren
#---------------------------

#[./06-selbstbezuege.md:81]
from wypp import *

# Ein Bach ist charakterisiert durch
# - Quelle (str)
# - Name (str)
@record
class Creek:
    origin: str
    name: str



#------------------------------------
#Zusammenflüsse in Python modellieren
#------------------------------------

#[./06-selbstbezuege.md:97]
# Das Zusammentreffen zweier Flußabschnitte ist charakterisiert durch
# - den Ort des Zusammentreffens (str)
# - den Hauptflußabschnitt (ein Flussabschnitt)
# - den Nebenflußabschnitt (ein Flussabschnitt)
@record
class Confluence:
    location: str
    mainStem: RiverSection
    tributary: RiverSection



#-------------------------------------
#Flussabschnitte in Python modellieren
#-------------------------------------

#[./06-selbstbezuege.md:119]
# Ein Flussabschnitt ist eins der folgenden:
# - ein Bach
# - ein Zusammenfluss
type RiverSection = Union[Creek, Confluence]



#--------------------
#Beispiele für Flüsse
#--------------------

#[./06-selbstbezuege.md:155]
kinzig1 = Creek('Loßburg', 'Kinzig')
gutach = Creek('Schönwald', 'Gutach')
kinzig2 = Confluence('Hausach', kinzig1, gutach)

heidengraben = Creek('Lahr', 'Heidengraben')
schutter1 = Creek('Schweighausen', 'Schutter')
schutter2 = Confluence('Lahr', schutter1, heidengraben)

kinzig3 = Confluence('Kehl', kinzig2, schutter2)



#-----------------------
#Rechnen mit Flüssen (1)
#-----------------------

#[./06-selbstbezuege.md:177]
# Ermittelt den Namen eines Flusses


#[./06-selbstbezuege.md:183]
# Eingabe: ein Flussabschnitt (RiverSection)
# Ausgabe: der Name des Abschnitts (str)



#-----------------------
#Rechnen mit Flüssen (2)
#-----------------------

#[./06-selbstbezuege.md:192]
def riverName(river: RiverSection) -> str:
    todo()



#-----------------------
#Rechnen mit Flüssen (5)
#-----------------------

#[./06-selbstbezuege.md:254]
def riverName(river: RiverSection) -> str:
    if isinstance(river, Creek):
        return river.name
    elif isinstance(river, Confluence):
        return riverName(river.mainStem)



#------
#Quiz 1
#------

#[./06-selbstbezuege.md:332]
def foo(i: int) -> None:
    print(i)
    if i >= 0:
        foo(i - 1)

foo(3)



#------
#Quiz 2
#------

#[./06-selbstbezuege.md:353]
def bar(i: int) -> int:
    if i == 0:
        return 0
    else:
        return i + bar(i - 1)



#------------
#Schritte 1-3
#------------

#[./06-selbstbezuege.md:382]
# Prüft ob Wasser von einem Ort in einen Fluss fließt
# Eingaben: ein Ort als String, ein Flussabschnitt (RiverSection).
# Ausgabe: True falls Wasser von dem Ort in den Flussabschnitt fließt,
#          ansonsten False


#[./06-selbstbezuege.md:391]
def flowsFrom(location: str, river: RiverSection) -> bool:
    todo()



#-----------
#Schritt 6.2
#-----------

#[./06-selbstbezuege.md:479]
def flowsFrom(location: str, river: RiverSection) -> bool:
    if isinstance(river, Creek):
        return river.origin == location
    elif isinstance(river, Confluence):
        if river.location == location:
            return True
        else:
            return flowsFrom(location, river.mainStem) or \
                flowsFrom(location, river.tributary)



#-----------------------
#Rechnen mit Flüssen (2)
#-----------------------

#[./06-selbstbezuege.md:199]
check(riverName(kinzig1), 'Kinzig')
check(riverName(kinzig2), 'Kinzig')
check(riverName(kinzig3), 'Kinzig')
check(riverName(heidengraben), 'Heidengraben')
check(riverName(schutter1), 'Schutter')
check(riverName(schutter2), 'Schutter')



#----------------
#Schritt 4: Tests
#----------------

#[./06-selbstbezuege.md:398]
check(flowsFrom('Loßburg', kinzig1), True)
check(flowsFrom('Loßburg', kinzig2), True)
check(flowsFrom('Loßburg', kinzig3), True)
check(flowsFrom('Loßburg', schutter1), False)
check(flowsFrom('Loßburg', schutter2), False)
check(flowsFrom('Hausach', kinzig1), False)
check(flowsFrom('Hausach', kinzig2), True)
check(flowsFrom('Hausach', kinzig3), True)
check(flowsFrom('Lahr', kinzig3), True)
check(flowsFrom('Lahr', kinzig2), False)

