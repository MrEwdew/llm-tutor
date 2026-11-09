from wypp import *

# Eine optionale Rückennummer ist entweder ein int oder None
type Rückennummer = Union[int, None]

# Entscheidet, ob eine Rückennummer vorhanden ist oder nicht
# Eingabe: Optionale Rückennummer
# Ausgabe: True, wenn deine Rückennummer vorhanden ist. Ansonsten False.
def isRückennummerPresent(rückennummer: Rückennummer) -> bool:
    return isinstance(rückennummer, int)

check(isRückennummerPresent(7), True)
check(isRückennummerPresent(14), True)
check(isRückennummerPresent(None), False)

# Eine Kleidergröße ist eine der folgenden:
# S, M oder L
type Größe = Literal['S', 'M', 'L']

# Eine Farbe ist eine der folgenden:
# - schwarz
# - grün
# - blau
# - rot
type Farbe = Literal['schwarz', 'grün', 'blau', 'rot']

# Ein Trikot hat eine Größe, Farbe und optionale Rückennummer
@record
class Trikot:
    größe: Größe
    farbe: Farbe
    rückennummer: Rückennummer

# Eine Hose hat eine Größe und eine Farbe
@record
class Hose:
    größe: Größe
    farbe: Farbe

# Ein Stutzen hat folgende Eigenschaften:
# - Farbe
# - untere Grenze zur passenden Schuhgröße (EUR)
# - obere Grenze zur passenden Schuhgröße (EUR)
@record
class Stutzen:
    farbe: Farbe
    minSize: float
    maxSize: float

Sportartikel = Union[Trikot, Hose, Stutzen]

# Berechnet den Preis für einen Sportartikel
# Eingabe: Sportartikel (Trikot, Hose oder Stutzen)
# Ausgabe: Preis in Euro -> float
def calcSportartikelPreis(artikel: Sportartikel) -> float:
    if isinstance(artikel, Trikot):
        return calcTrikotPreis(artikel)

    elif isinstance(artikel, Hose):
        return calcHosenPreis(artikel)

    elif isinstance(artikel, Stutzen):
        return calcStutzenPreis(artikel)

# Berechnet den Preis für ein Trikot
def calcTrikotPreis(trikot: Trikot) -> float:
    if isRückennummerPresent(trikot.rückennummer):
        return 25
    else:
        return 20

check(calcTrikotPreis(Trikot('S', 'schwarz', 1)), 25)
check(calcTrikotPreis(Trikot('S', 'rot', 7)), 25)
check(calcTrikotPreis(Trikot('L', 'rot', 7)), 25)
check(calcTrikotPreis(Trikot('S', 'schwarz', None)), 20)
check(calcTrikotPreis(Trikot('S', 'rot', None)), 20)
check(calcTrikotPreis(Trikot('L', 'rot', None)), 20)

# Berechnet den Preis für eine Hose
def calcHosenPreis(hose: Hose) -> float:
    if hose.größe == 'S':
        return 10
    elif hose.größe == 'M':
        return 12
    elif hose.größe == 'L':
        return 15

check(calcHosenPreis(Hose('S', 'schwarz')), 10)
check(calcHosenPreis(Hose('S', 'grün')), 10)
check(calcHosenPreis(Hose('M', 'schwarz')), 12)
check(calcHosenPreis(Hose('M', 'rot')), 12)
check(calcHosenPreis(Hose('L', 'blau')), 15)
check(calcHosenPreis(Hose('L', 'rot')), 15)

# Berechnet den Preis für einen Stutzen
def calcStutzenPreis(stutzen: Stutzen) -> float:
    if stutzen.maxSize > 38:
        return 9
    return 5

check(calcStutzenPreis(Stutzen('schwarz', 32, 36)), 5)
check(calcStutzenPreis(Stutzen('grün', 36, 38)), 5)
check(calcStutzenPreis(Stutzen('grün', 35, 39)), 9)
check(calcStutzenPreis(Stutzen('blau', 38, 41)), 9)
check(calcStutzenPreis(Stutzen('rot', 41, 45)), 9)

# Test Trikots
check(calcSportartikelPreis(Trikot('S', 'schwarz', 1)), 25)
check(calcSportartikelPreis(Trikot('S', 'rot', 7)), 25)
check(calcSportartikelPreis(Trikot('L', 'rot', 7)), 25)
check(calcSportartikelPreis(Trikot('S', 'schwarz', None)), 20)
check(calcSportartikelPreis(Trikot('S', 'rot', None)), 20)
check(calcSportartikelPreis(Trikot('L', 'rot', None)), 20)

# Test Hosen
check(calcSportartikelPreis(Hose('S', 'schwarz')), 10)
check(calcSportartikelPreis(Hose('S', 'grün')), 10)
check(calcSportartikelPreis(Hose('M', 'schwarz')), 12)
check(calcSportartikelPreis(Hose('M', 'rot')), 12)
check(calcSportartikelPreis(Hose('L', 'blau')), 15)
check(calcSportartikelPreis(Hose('L', 'rot')), 15)

# Test Stutzen
check(calcSportartikelPreis(Stutzen('schwarz', 32, 36)), 5)
check(calcSportartikelPreis(Stutzen('grün', 36, 38)), 5)
check(calcSportartikelPreis(Stutzen('grün', 35, 39)), 9)
check(calcSportartikelPreis(Stutzen('blau', 38, 41)), 9)
check(calcSportartikelPreis(Stutzen('rot', 41, 45)), 9)
