#Automatically extracted from ./10-zustand.md on 2026-11-06 13:52:31.586188 UTC



#------------
#Aufwärmübung
#------------

#[./10-zustand.md:85]
from wypp import *


#[./10-zustand.md:89]
# Liste berechnen, die an geraden Indexen True ist
# Eingabe: Länge der gewünschten Liste (int)
# Ausgabe: die Liste mit den booleschen Werten
def evenTrueOddFalse(n: int) -> list[bool]:
    todo()



#---------------
#Implementierung
#---------------

#[./10-zustand.md:118]
def evenTrueOddFalse(n: int) -> list[bool]:
    result = []
    for i in range(n):
        result = result + [i % 2 == 0]
    return result



#---------------------------
#Alternative Implementierung
#---------------------------

#[./10-zustand.md:132]
def evenTrueOddFalseAlt(n: int) -> list[bool]:
    result = n * [True]
    for i in range(n):
        if i % 2 != 0:
            result[i] = False
    return result



#--------
#Debugger
#--------

#[./10-zustand.md:157]
from wypp import *

def evenTrueOddFalseAlt(n: int) -> list[bool]:
    result = n * [True]
    for i in range(n):
        if i % 2 != 0:
            result[i] = False
    return result

evenTrueOddFalseAlt(6)



#----
#Quiz
#----

#[./10-zustand.md:234]
def foo(n: int) -> list[int]:
    result = []
    for i in range(n):
        result = result + [i]
    for i in range(n):
        result[i] = 2 * result[i]
    return result



#------------
#Schritte 1-4
#------------

#[./10-zustand.md:263]
# Primzahlen mittels des Siebs von Eratosthenes berechnen.
# Eingabe: Zahl bis zu der die Primzahlen berechnet werden sollen (int)
# Ausgabe: Liste mit Primzahlen
def computePrimes(n: int) -> list[int]:
    todo()



#------------
#Eratosthenes
#------------

#[./10-zustand.md:304]
def computePrimes(n: int) -> list[int]:
    # Schreibe die Zahlen 2..n auf und markiere alle Zahlen mit `True`.
    isPrime: list[bool] = (n + 1) * [True]
    isPrime[0] = False   # 0 und 1 sind keine Primzahlen
    isPrime[1] = False
    # Schaue dir Zahlen der Reihe nach an.
    for i in range(2, len(isPrime) // 2 + 1):
        if isPrime[i]:
            # Falls die Zahl mit True markiert ist:
            # streiche die Vielfachen von i, d.h.
            # i+i, i+i+i, i+i+i+i, ...
            # 2*i, 3*i,   4*i
            for j in range(i+i, len(isPrime), i):
                isPrime[j] = False
    # Ergebnis zusammenstellen
    result = []
    for i, b in enumerate(isPrime):
        if b:
            result = result + [i]
    return result



#----------------------------------------------
#Alle Listenelemente inkrementieren (immutable)
#----------------------------------------------

#[./10-zustand.md:343]
# Alle Listenelemente um eins inkrementieren
def incByOne(lst: list[int]) -> list[int]:
    todo()


#[./10-zustand.md:357]
def incByOne(lst: list[int]) -> list[int]:
    result = []
    for x in lst:
        result = result + [x + 1]
    return result



#--------------------------------------------
#Alle Listenelemente inkrementieren (mutable)
#--------------------------------------------

#[./10-zustand.md:367]
# Alle Listenelemente um eins inkrementieren
# SEITENEFFEKT: alle Elemente der Parameterliste sind um eins inkrementiert.
def incByOneInPlace(lst: list[int]) -> None:
    for i in range(len(lst)):
        lst[i] = lst[i] + 1
    # kein return!



#---------------------------
#Tests für `incByOneInPlace`
#---------------------------

#[./10-zustand.md:396]
l1 = [1,2,3,4]         # Liste initialisieren
incByOneInPlace(l1)    # zu testende Funktion aufrufen
check(l1, [2,3,4,5])   # prüfen ob Liste den richtigen Inhalt hat



#--------------
#Visualisierung
#--------------

#[./10-zustand.md:410]
def incByOneInPlace(x):
    for i in range(len(x)):
        x[i] = x[i] + 1

lst = [1,2,3]
incByOneInPlace(lst)
print(lst)



#----
#Quiz
#----

#[./10-zustand.md:489]
def foo(l: list) -> None:
    l[0] = 0
    n = len(l)
    for i in range(n):
        j = n - 1 - i
        x = l[i]
        l[i] = l[j]
        l[j] = x

x = [1, 42, 0, -3]
foo(x)
print(x)


#[./10-zustand.md:506]
__l1 = [1,2,3,4]
foo(__l1)
check(__l1, [0,2,3,4])



#------------
#Aufwärmübung
#------------

#[./10-zustand.md:99]
check(evenTrueOddFalse(4), [True, False, True, False])
check(evenTrueOddFalse(7), [True, False, True, False, True, False, True])



#---------------------------
#Alternative Implementierung
#---------------------------

#[./10-zustand.md:141]
check(evenTrueOddFalseAlt(4), [True, False, True, False])
check(evenTrueOddFalseAlt(7), [True, False, True, False, True, False, True])



#------------
#Schritte 1-4
#------------

#[./10-zustand.md:272]
check(computePrimes(50), [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47])



#----------------------------------------------
#Alle Listenelemente inkrementieren (immutable)
#----------------------------------------------

#[./10-zustand.md:351]
check(incByOne([1,2,3]), [2,3,4])

