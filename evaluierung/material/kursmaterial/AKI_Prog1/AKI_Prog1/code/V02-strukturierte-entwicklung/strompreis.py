from wypp import *

# Monatsendbetrag für einen beliebigen Tarif berechnen
# Eingaben: monatliche Verbrauch in kWh (float),
#   Grundpreis in Euro (float), Verbrauchpreis in Euro pro kWh (float)
# Ergebnis: Monatsendbetrag in Euro (float)
def rechnungsbetrag(kwh: float, grundpreis: float, verbrauchpreis: float) -> float:
    return kwh * verbrauchpreis + grundpreis

check(rechnungsbetrag(12, 1, 0.1), 2.2)

# Monatsendbetrag für Tarif Watt-für-Wenig berechnen.
# Eingabe: monatliche Verbrauch in kWh (float)
# Ergebnis: Monatsendbetrag in Euro (float)
def rechnungsbetragWattFuerWenig(kwh: float) -> float:
    return rechnungsbetrag(kwh, 8.2, 0.16)

check(rechnungsbetragWattFuerWenig(100), 24.2)
check(rechnungsbetragWattFuerWenig(0), 8.2)

# Monatlichen Rechnungsbetrag für Tarif Billig-Strom berechnen
# Eingabe: monatlicher Verbauch in kWh (float)
# Ergebnis: montlicher Preis in Euro (float)
def monatsbetragBilligStrom(verbrauch: float) -> float:
    return rechnungsbetrag(verbrauch, 4.99, 0.19)

check(monatsbetragBilligStrom(10), 6.89)
check(monatsbetragBilligStrom(0), 4.99)
