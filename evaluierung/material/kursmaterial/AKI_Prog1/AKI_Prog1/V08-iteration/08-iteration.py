#Automatically extracted from ./08-iteration.md on 2026-10-26 17:48:09.068031 UTC



#------------
#Modellierung
#------------

#[./08-iteration.md:25]
from wypp import *

# Ein Rechnungsposten besteht aus
# - Artikelnummer (Typ: str)
# - Name (Typ: str)
# - Preis (Typ: float)
@record
class InvoiceItem:
    articleId: str
    articleName: str
    price: float

# Eine Rechnung besteht aus
# - Datum (Typ: str)
# - Rechnungsposten (Typ: list[InvoiceItem])
@record
class Invoice:
    date: str
    items: list[InvoiceItem]



#----------------
#Beispielrechnung
#----------------

#[./08-iteration.md:49]
item1 = InvoiceItem('A9810', 'Kompaktkassette', 5.99)
item2 = InvoiceItem('A3510', 'Eismaschine', 249.99)
item3 = InvoiceItem('A9614', 'Taschentrompete', 89.00)
sampleInvoice = Invoice('2024-11-08', [item1, item2, item3])



#--------------------------------
#Iteration mittels `for`-Schleife
#--------------------------------

#[./08-iteration.md:72]
# Gesamtpreis einer Rechnung berechnen
# Eingabe: Rechnung (Typ: Invoice)
# Ergebnis: Gesamtpreis in Euro (Typ: float)
def totalPrice(invoice: Invoice) -> float:
    result = 0
    for item in invoice.items:
        result = result + item.price
    return result

check(totalPrice(sampleInvoice), 344.98)



#-----------------
#`for` mit Strings
#-----------------

#[./08-iteration.md:106]
for c in 'spam':
    print(c + c)



#---------------
#`for` mit Tupel
#---------------

#[./08-iteration.md:122]
for x in ('spam', 'ham', 'egg'):
   if x == 'egg':
       print('tasty egg')
   else:
       print(x + ': würg')



#----
#Quiz
#----

#[./08-iteration.md:142]
def foo(seq: Sequence[int]) -> int:
    res = 1
    for x in seq:
        if x == 0:
            return 0
        res = res * x
    return res



#-------------------------------
#Beispiel für `break` und `else`
#-------------------------------

#[./08-iteration.md:172]
# Funktion die ein Element in einer Sequenz findet.
# Eingaben: Sequenz und Element (Any)
# Ausgabe: True wenn Element in Sequenz enthalten ist (bool)
def findElem(elem: Any, seq: Sequence) -> bool:
    todo()



#--------------------------------------
#Schritte 5 und 6: Schablonen und Rumpf
#--------------------------------------

#[./08-iteration.md:197]
def findElem(elem: Any, seq: Sequence) -> bool:
    for x in seq:
        if x == elem:
            found = True
            break
    else:
        found = False
    return found



#---------------------------------
#Alternative Implementierungen (1)
#---------------------------------

#[./08-iteration.md:212]
def findElemAlternative(elem: Any, seq: Sequence) -> bool:
    for x in seq:
        if x == elem:
            return True
    return False


#[./08-iteration.md:220]
check(findElemAlternative('x', [1, 'x', 5]), True)
check(findElemAlternative('y', (1, 'x', 5)), False)
check(findElemAlternative(1, []), False)



#---------------------------------
#Alternative Implementierungen (2)
#---------------------------------

#[./08-iteration.md:232]
def findElemAlternative2(elem: Any, seq: Sequence) -> bool:
    found = False
    for x in seq:
        if x != elem:
            continue
        found = True
    return found


#[./08-iteration.md:242]
check(findElemAlternative2('x', [1, 'x', 5]), True)
check(findElemAlternative2('y', (1, 'x', 5)), False)
check(findElemAlternative2(1, []), False)



#----
#Quiz
#----

#[./08-iteration.md:279]
def foo(seq: list[tuple[int, str]]) -> list[str]:
    res = []
    for k, v in seq:
        if k < 0:
            break
        if k == 0:
            continue
        res = res + k * [v]
    else:
        res = res + ["done"]
    return res


#[./08-iteration.md:298]
foo([(2, "two"), (1, "one")])


#[./08-iteration.md:321]
# foo wie im vorigen Quiz
def foo(seq: list[tuple[int, str]]) -> list[str]:
    res = []
    for k, v in seq:
        if k < 0:
            break
        if k == 0:
            continue
        res = res + k * [v]
    else:
        res = res + ["done"]
    return res


#[./08-iteration.md:341]
foo([(2, "two"), (0, "zero")])


#[./08-iteration.md:364]
# foo wie im vorigen Quiz
def foo(seq: list[tuple[int, str]]) -> list[str]:
    res = []
    for k, v in seq:
        if k < 0:
            break
        if k == 0:
            continue
        res = res + k * [v]
    else:
        res = res + ["done"]
    return res


#[./08-iteration.md:384]
foo([(2, "two"), (-5, "neg")])



#-----------------------------------
#Verschiedene Arten zu iterieren (1)
#-----------------------------------

#[./08-iteration.md:481]
primes = [2, 3, 5, 7]
result=0
for x in primes:
    print(f'x={x}, result={result}')
    result = result + x
print(result)



#-----------------------------------
#Verschiedene Arten zu iterieren (2)
#-----------------------------------

#[./08-iteration.md:507]
primes = [2, 3, 5, 7]
result=0
for i, x in enumerate(primes):
    print(f'x={x}, i={i}, result={result}')
    result = result + x
print(result)



#-----------------------------------
#Verschiedene Arten zu iterieren (3)
#-----------------------------------

#[./08-iteration.md:554]
primes = [2, 3, 5, 7]
result=0
for i in range(len(primes)):
    x = primes[i]
    print(f'x={x}, i={i}, result={result}')
    result = result + x
print(result)



#--------------------
#Beispiel für `range`
#--------------------

#[./08-iteration.md:577]
# zip selbst implementieren
# Eingabe: 2 Sequenzen
# Ausgabe: eine Sequenz von Paaren.
def myZip(seq1: Sequence, seq2: Sequence) -> Sequence[tuple]:
    n = min(len(seq1), len(seq2))
    result = []
    for i in range(n):
        result = result + [(seq1[i], seq2[i])]
    return result

check(myZip([1,2,3], [4,5,6,7]), [(1,4), (2,5), (3,6)])



#----------------------------
#Transformation von Sequenzen
#----------------------------

#[./08-iteration.md:613]
# Jeden String in Großbuchstaben transformieren.
# Eingabe: Liste von Strings (list[str])
# Ausgabe: Liste von Strings (list[str])
def makeAllUppercase(l: list[str]) -> list[str]:
    todo()



#--------------------------------------
#Implementierung von `makeAllUppercase`
#--------------------------------------

#[./08-iteration.md:630]
def makeAllUppercase(l: list[str]) -> list[str]:
    result = []
    for s in l:
        result = result + [s.upper()]
    return result



#-------------------
#Listen flachklopfen
#-------------------

#[./08-iteration.md:645]
# Liste von Listen flachklopfen
# Eingabe: Liste von Listen (list[list])
# Ausgabe: flachgeklopfte Liste (List)
def flatten(l: list[list]) -> list:
    todo()



#------------------------
#Verschachtelte Schleifen
#------------------------

#[./08-iteration.md:661]
def flatten(l: list[list]) -> list:
    result = []
    for innerList in l:
        for x in innerList:
            result = result + [x]
    return result



#-------------------------------------------
#Schablone zur Iteration über Zahlenbereiche
#-------------------------------------------

#[./08-iteration.md:721]
# Zahlen 1..n summieren
# Eingabe: obere Grenze n (ein int)
# Ergebnis: Summe (ein int)
def sumNumbers(n: int) -> int:
    result = 0
    for i in range(1, n+1):
        result = result + i
    return result


#[./08-iteration.md:733]
check(sumNumbers(0), 0)
check(sumNumbers(-1), 0)
check(sumNumbers(5), 15)



#----------------
#Schritt 4: Tests
#----------------

#[./08-iteration.md:185]
check(findElem('x', [1, 'x', 5]), True)
check(findElem('y', (1, 'x', 5)), False)
check(findElem(1, []), False)



#----------------------------
#Transformation von Sequenzen
#----------------------------

#[./08-iteration.md:621]
check(makeAllUppercase(['spam', 'foo', 'bar']), ['SPAM', 'FOO', 'BAR'])



#-------------------
#Listen flachklopfen
#-------------------

#[./08-iteration.md:653]
check(flatten([[1,2], [3,4,5]]), [1,2,3,4,5])

