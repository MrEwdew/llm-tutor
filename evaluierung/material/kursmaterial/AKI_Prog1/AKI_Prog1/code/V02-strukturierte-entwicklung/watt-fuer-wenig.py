from wypp import *

# Monatsendbetrag für Tarif Watt-für-Wenig berechnen.
# Eingabe: monatliche Verbrauch in kWh (float)
# Ergebnis: Monatsendbetrag in Euro (float)
def rechnungsbetragWattFuerWenig(kwh: float) -> float:
    return 8.2 + kwh * 0.16

check(rechnungsbetragWattFuerWenig(100), 24.2)
check(rechnungsbetragWattFuerWenig(0), 8.2)
