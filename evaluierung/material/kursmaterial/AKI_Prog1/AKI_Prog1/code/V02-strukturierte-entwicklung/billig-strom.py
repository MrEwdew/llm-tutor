from wypp import *

# Monatlichen Rechnungsbetrag für Tarif Billig-Strom berechnen
# Eingabe: monatlicher Verbauch in kWh (float)
# Ergebnis: montlicher Preis in Euro (float)
def monatsbetragBilligStrom(verbrauch: float) -> float:
    return verbrauch * 0.19 + 4.99

check(monatsbetragBilligStrom(10), 6.89)
check(monatsbetragBilligStrom(0), 4.99)
