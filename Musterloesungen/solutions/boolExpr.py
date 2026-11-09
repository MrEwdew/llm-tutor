from __future__ import annotations
from wypp import *

@record
class Basisknoten:
    name: str

@record
class Operatorknoten:
    links: Ausdruck
    name: str
    rechts: Ausdruck

type Ausdruck = Union[Basisknoten, Operatorknoten]

# 5 + 7 * 4 * 2
# 5 + ((7 * 4) * 2)
beispiel1 = Operatorknoten(Basisknoten("5"), "+",
                           Operatorknoten(Operatorknoten(Basisknoten("7"), "*", Basisknoten("4")),
                                          "*",
                                          Basisknoten("2")))

# ((4 + 8) * -3) < (42 + 1)
beispiel21 = Operatorknoten(Operatorknoten(Basisknoten("4"), "+", Basisknoten("8")),
                            "*",
                            Basisknoten("-3"))
beispiel22 = Operatorknoten(Basisknoten("42"), "+", Basisknoten("1"))
beispiel2 = Operatorknoten(beispiel21, "<", beispiel22)

# Teil (c): Anzahl der Elemente eines Ausdrucks zählen
def countElems(e: Ausdruck) -> int:
    if isinstance(e, Basisknoten):
        return 1
    else:
        return countElems(e.links) + countElems(e.rechts) + 1

check(countElems(beispiel1), 7)
check(countElems(beispiel2), 9)

# Teil (d)
def containsString(e: Ausdruck, s: str) -> bool:
    if isinstance(e, Basisknoten):
        return s == e.name
    else:
        return s == e.name or containsString(e.links, s) or containsString(e.rechts, s)

check(containsString(beispiel2, "42"), True)
check(containsString(beispiel2, "<"), True)
check(containsString(beispiel2, ">"), False)
