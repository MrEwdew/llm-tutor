#Automatically extracted from ./09-polynome.md on 2026-11-06 13:52:27.789197 UTC



#---------------------
#Skalar-Multiplikation
#---------------------

#[./09-polynome.md:87]
from wypp import *

# Skalar-Multiplikation auf Polynomen
# Eingaben: eine Zahl (float) und ein Polynom (list[float])
# Ausgabe: ein Polynom
def scalarMult(c: float, p: list[float]) -> list[float]:
    todo()



#-------------------------------------
#Implementierung Skalar-Multiplikation
#-------------------------------------

#[./09-polynome.md:118]
def scalarMult(c: float, p: list[float]) -> list[float]:
    result = []
    for a in p:
        result = result + [c * a]
    return result



#----------
#Auswertung
#----------

#[./09-polynome.md:131]
# Auswertung eines Polynoms
# Eingaben: Polynom (list[float]) und Argument sigma (float)
# Ausgabe: Wert des Polynoms an Stelle sigma (float)
def polyEval(p: list[float], sigma: float) -> float:
    todo()



#--------------------------
#Implementierung Auswertung
#--------------------------

#[./09-polynome.md:166]
def polyEval(p: list[float], sigma: float) -> float:
    result = 0                      # Akkumulator
    for i, a in enumerate(p):       # Iteration mit Index
        result = result + a * sigma**i
    return result



#---------
#Ableitung
#---------

#[./09-polynome.md:184]
# Ableitung eines Polynoms berechnen
# Eingabe: Polynom vom Grad n (list[float])
# Ausgabe: Polynom vom Grad n-1 bzw. vom Grad -1 falls n=-1 (list[float])
def derivative(p: list[float]) -> list[float]:
    todo()



#----------------------------
#Implementierung `derivative`
#----------------------------

#[./09-polynome.md:222]
def derivative(p: list[float]) -> list[float]:
    result = []
    for i, a in enumerate(p):
        if i > 0:
            result = result + [i * a]
    return result



#--------
#Addition
#--------

#[./09-polynome.md:278]
# Punktweise Addition zweier Polynome
# Eingabe: zwei Polynome (list[float])
# Ausgabe: Addiertes Polynom.
# Achtung: Grade der Polynome können unterschiedlich sein, wir machen keine
# Annahme über die Reihenfolge der Parameter.
def polyAdd(p: list[float], q: list[float]) -> list[float]:
    todo()



#----------------------------
#Implementierung der Addition
#----------------------------

#[./09-polynome.md:330]
def polyAdd(p: list[float], q: list[float]) -> list[float]:
    result = []
    resultLen = max(len(p), len(q))
    for i in range(resultLen):
        c = 0
        if i < len(p):
            c = c + p[i]
        if i < len(q):
            c = c + q[i]
        result = result + [c]
    return result



#----------------
#Code-Duplikation
#----------------

#[./09-polynome.md:361]
def polyAdd(p: list[float], q: list[float]) -> list[float]:
    result = []
    resultLen = max(len(p), len(q))
    for i in range(resultLen):
        result = result + [safeIndex(p, i, 0) + safeIndex(q, i, 0)]
    return result



#-------------------------
#Hilfsfunktion `safeIndex`
#-------------------------

#[./09-polynome.md:375]
# Zugriff auf Element einer Sequenz, Defaultwert für ungültige Indexe.
# Eingaben: Sequenz, Index (int) und Defaultwert (Any)
# Ausgabe: Element am Index oder Defaultwert (Any)
def safeIndex(seq: Sequence, i: int, d: Any) -> Any:
    n = len(seq)
    if i >= -n and i < n:
        return seq[i]
    else:
        return d

check(safeIndex([1,2,3], 0, 'foo'), 1)
check(safeIndex([1,2,3], 2, 'foo'), 3)
check(safeIndex([1,2,3], -1, 'foo'), 3)
check(safeIndex([1,2,3], -3, 'foo'), 1)
check(safeIndex([1,2,3], -4, 'foo'), 'foo')
check(safeIndex([1,2,3], 3, 'foo'), 'foo')



#------------------
#Bedingter Ausdruck
#------------------

#[./09-polynome.md:398]
def safeIndexShort(seq: Sequence, i: int, d: Any) -> Any:
    n = len(seq)
    return seq[i] if (i >= -n and i < n) else d


#[./09-polynome.md:404]
check(safeIndexShort([1,2,3], 0, 'foo'), 1)
check(safeIndexShort([1,2,3], 2, 'foo'), 3)
check(safeIndexShort([1,2,3], -1, 'foo'), 3)
check(safeIndexShort([1,2,3], -3, 'foo'), 1)
check(safeIndexShort([1,2,3], -4, 'foo'), 'foo')
check(safeIndexShort([1,2,3], 3, 'foo'), 'foo')



#--------------
#Multiplikation
#--------------

#[./09-polynome.md:448]
# Multiplikation zweier Polynome
# Eingabe: zwei Polynome (list[float])
# Ausgabe: Polynom (list[float])
def polyMult(p: list[float], q: list[float]) -> list[float]:
    todo()



#----------------------------------------------
#Implementierung der Multiplikation (Schritt 2)
#----------------------------------------------

#[./09-polynome.md:539]
def polyMult(p: list[float], q: list[float]) -> list[float]:
    if len(p) == 0 or len(q) == 0:
        return []
    result = []
    for i in range(len(p) + len(q) - 1):
        ci = 0
        for k in range(i + 1): # iterate over 0,1,...,i
            a = safeIndex(p, k, 0)
            b = safeIndex(q, i - k, 0)
            ci = ci + (a * b)
        result = result + [ci]
    return result



#---------------------
#Skalar-Multiplikation
#---------------------

#[./09-polynome.md:97]
check(scalarMult(42, []), [])
check(scalarMult(42, [1,2,3]), [42,84,126])
check(scalarMult(-0.5, [1,2,3]), [-0.5,-1.0,-1.5])



#----------
#Auswertung
#----------

#[./09-polynome.md:144]
check(polyEval([], 2), 0)
check(polyEval([1,2,3], 2), 17)
check(polyEval([1,2,3], -0.1), 0.83)



#----------------------
#Tests für `derivative`
#----------------------

#[./09-polynome.md:199]
check(derivative([]), [])
check(derivative([42]), [])
check(derivative([1,2,3]), [2,6])
check(derivative([0,5,0,0,-4]), [5,0,0,-16])



#--------
#Addition
#--------

#[./09-polynome.md:288]
check(polyAdd([], []), [])
check(polyAdd([42], []), [42])
check(polyAdd([], [11]), [11])
check(polyAdd([3,6,11], [2,0,-4,8]), [5,6,7,8])



#-----------------------
#Mehr Tests für Addition
#-----------------------

#[./09-polynome.md:303]
def checkAddEvalCommutes(p: list[float], q: list[float]) -> None:
    # Prüfe die Eigenschaft für ein paar Beispiele
    for sigma in [0, -4, 5.2]:
        check(polyEval(polyAdd(p, q), sigma),
              polyEval(p, sigma) + polyEval(q, sigma))

checkAddEvalCommutes([3,6,11], [2,0,-4,8])
checkAddEvalCommutes([3,6,11], [5])
checkAddEvalCommutes([3,6,11], [])



#----------------
#Schritt 4: Tests
#----------------

#[./09-polynome.md:457]
check(polyMult([], []), [])
check(polyMult([42], []), [])
check(polyMult([11], []), [])
check(polyMult([-5], [2]), [-10])
check(polyMult([1,2,3], [1]), [1,2,3])
check(polyMult([1,2,3], [0,1]), [0,1,2,3])
check(polyMult([1,2,3], [1,1]), [1,3,5,3])



#-------------
#Weitere Tests
#-------------

#[./09-polynome.md:471]
def checkMultEvalCommutes(p: list[float], q: list[float]) -> None:
    # Prüfe die Eigenschaft für ein paar Beispiele
    for sigma in [0, -4, 5.2]:
        check(polyEval(polyMult(p, q), sigma),
              polyEval(p, sigma) * polyEval(q, sigma))

checkMultEvalCommutes([3,6,11], [2,0,-4,8])
checkMultEvalCommutes([3,6,11], [5])
checkMultEvalCommutes([3,6,11], [])

