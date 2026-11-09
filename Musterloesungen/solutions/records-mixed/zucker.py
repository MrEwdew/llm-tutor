from __future__ import annotations
from wypp import *

# Ein Zuckergehalt kann in fruktose und glucose angegeben werden:
# - Fruktose in Gramm
# - Glukose in Gramm
@record
class ZuckerFrukGluc:
    fruktose: float
    glucose: float

    # Berechnet den gesamten Zuckergehalt
    def gesamt(self) -> float:
        return self.fruktose + self.glucose

# Ein Zuckergehalt kann auch pro 100g Lebensmittel angegeben werden
@record
class ZuckerPro100:
    menge: float

# Ein Zuckergehalt kann per Lebensmittelampel angegeben werden
@record
class ZuckerAmpel:
    ampel: Lebensmittelampel

# Die Lebensmittelampel klassifiziert ein Lebensmittel nach dem Zuckergehalt pro 100g
# grün: niedriger Gehalt
# gelb: mittlerer Gehalt
# rot: hoher Gehalt
type Lebensmittelampel = Literal['grün', 'gelb', 'rot']

# Ein Zuckergehalt wird angegeben durch eins der folgenden:
# - ZuckerFrukGluc (Aufgeteilt in Fructose und Glucose pro Gesamtgewicht)
# - ZuckerPro100 (In Gramm Zucker pro 100g Lebensmittel)
# - ZuckerAmpel (Als Kategorie der Lebensmittelampel)
type Zuckergehalt = Union[ZuckerFrukGluc, ZuckerPro100, ZuckerAmpel]

# Ein Lebensmittel besteht aus folgenden Eigenschaften:
# - Name
# - Packungsgröße in Gramm
# - Zuckergehalt
@record
class Lebensmittel:
    name: str
    größe: float
    zucker: Zuckergehalt

cola = Lebensmittel('Coca Cola', 500, ZuckerFrukGluc(25, 25))
schoki = Lebensmittel('Ritter Sport himmlische Beere', 100, ZuckerFrukGluc(15.29, 24.9))

# Berechnet den Zuckergehalt pro 100g für ein Lebensmittel
# Je nachdem wie der Zuckergehalt angegeben wurde, wird hier noch umgerechnet
# Kann keinen Zuckergehalt für den Typ 'ZuckerAmpel' berechnen!
# Eingabe: Lebensmittel
# Ausgabe: Zuckergehalt pro 100g (in Gramm)
def calcZuckerPro100(lebensmittel: Lebensmittel) -> float:
    if isinstance(lebensmittel.zucker, ZuckerFrukGluc):
        return (lebensmittel.zucker.gesamt() / lebensmittel.größe) * 100

    if isinstance(lebensmittel.zucker, ZuckerPro100):
        return lebensmittel.zucker.menge

check(calcZuckerPro100(cola), 10)
check(calcZuckerPro100(schoki), 40.19)

# Berechnet die Lebensmittelkategorie nach der Lebensmittelampel für ein Lebensmittel.
# grün: niedriger Gehalt, weniger als 5g pro 100g
# gelb: mittlerer Gehalt, zwischen 5g und 22,5g pro 100g
# rot: hoher Gehalt, mehr als 22,5g pro 100g
def getLebensmittelKategorie(lebensmittel: Lebensmittel) -> Lebensmittelampel:
    if isinstance(lebensmittel.zucker, ZuckerAmpel):
        return lebensmittel.zucker.ampel
    gehalt = calcZuckerPro100(lebensmittel)
    if gehalt < 5:
        return 'grün'
    elif gehalt <= 22.5:
        return 'gelb'
    else:
        return 'rot'

check(getLebensmittelKategorie(cola), 'gelb')
check(getLebensmittelKategorie(schoki), 'rot')

test = Lebensmittel('Test', 100, ZuckerFrukGluc(0, 4.9))
check(getLebensmittelKategorie(test), 'grün')
test = Lebensmittel('Test', 100, ZuckerFrukGluc(0, 5))
check(getLebensmittelKategorie(test), 'gelb')
test = Lebensmittel('Test', 100, ZuckerFrukGluc(22.5, 0))
check(getLebensmittelKategorie(test), 'gelb')
test = Lebensmittel('Test', 100, ZuckerFrukGluc(22.6, 0))
check(getLebensmittelKategorie(test), 'rot')

cola = Lebensmittel('Coca Cola', 500, ZuckerFrukGluc(25, 25))
schoki = Lebensmittel('Ritter Sport', 100, ZuckerFrukGluc(15.29, 24.9))
kürbis = Lebensmittel('Kürbis', 1000, ZuckerPro100(2.8))
gurke = Lebensmittel('Gurke', 470, ZuckerAmpel('grün'))

check(getLebensmittelKategorie(cola), 'gelb')
check(getLebensmittelKategorie(schoki), 'rot')
check(getLebensmittelKategorie(kürbis), 'grün')
check(getLebensmittelKategorie(gurke), 'grün')
