from wypp import check
from aufgabe_01 import luisasLieblingsZahlen

# Testfälle aus Aufgabenstellung
check(luisasLieblingsZahlen(6), True)
check(luisasLieblingsZahlen(11), True)
check(luisasLieblingsZahlen(12), False)
check(luisasLieblingsZahlen(13), True)
check(luisasLieblingsZahlen(100), False)
check(luisasLieblingsZahlen(100.1), True)
check(luisasLieblingsZahlen(9999), True)