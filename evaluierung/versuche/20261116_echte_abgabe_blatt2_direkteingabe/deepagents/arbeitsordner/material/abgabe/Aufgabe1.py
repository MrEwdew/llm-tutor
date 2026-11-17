from wypp import *

# Funktion schreiben für einen booleschen wert der TRUE ergibt wenn es Luisaslieblingszahl ist
# Eingabe
# Ergebnis

def luisasLieblingsZahlen(Zahl: float) -> bool:
   return Zahl in(6, 11, 13) or Zahl > 100

check(luisasLieblingsZahlen(6), True)
check(luisasLieblingsZahlen(11), True)
check(luisasLieblingsZahlen(12), False)
check(luisasLieblingsZahlen(13), True)
check(luisasLieblingsZahlen(100), False)
check(luisasLieblingsZahlen(100.1), True)
check(luisasLieblingsZahlen(9999), True)
