#Automatically extracted from ./konstruktionsanleitungen.md on 2026-09-29 07:07:15.041455 UTC



#------------
#Datenanalyse
#------------

#[./konstruktionsanleitungen.md:108]
# Eingaben: ...
# Ergebnis: ...



#------------------------------------
#Datenbeschreibung Fallunterscheidung
#------------------------------------

#[./konstruktionsanleitungen.md:134]
# Ein X ist eins der folgenden:
# - Fall 1
# - Fall 2
# - ...
# - Fall n


#[./konstruktionsanleitungen.md:144]
# Eine Altersklassifikation ist eins der folgenden:
# - Baby
# - Kleinkind
# - Kind



#----------------------------------------
#Datenbeschreibung zusammengesetzte Daten
#----------------------------------------

#[./konstruktionsanleitungen.md:182]
# Ein X hat / besteht aus / ist charakterisiert durch:
# - Bestandteil / Eigenschaft 1 (Typ 1)
# - Bestandteil / Eigenschaft 2 (Typ 2)
# ...
# - Bestandteil / Eigenschaft n (Typ n)


#[./konstruktionsanleitungen.md:192]
# Ein Computer besteht aus:
# - Prozessor (str)
# - Festplatten-Kapazität in Gigabyte (int)
# - Hauptspeicher-Kapazität in Gigabyte (int)



#------------------------------------
#Typdefinition zusammengesetzte Daten
#------------------------------------

#[./konstruktionsanleitungen.md:227]
@record
class Computer:
    prozessor: str
    festplatte: int
    hauptspeicher: int



#-----------------------------
#Typdefinition gemischte Daten
#-----------------------------

#[./konstruktionsanleitungen.md:320]
type Tier = Union[Gürteltier, Papagei]

