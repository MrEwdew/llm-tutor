#Automatically extracted from ./02_strukturierte-entwicklung.md on 2026-09-29 07:08:11.96568 UTC



#-------------------------
#Die Macht der Abstraktion
#-------------------------

#[./02_strukturierte-entwicklung.md:364]
def wattFuerWenig(kwh: float) -> float:
    return kwh * 0.16 + 8.2

def billigStrom(kwh: float) -> float:
    return kwh * 0.19 + 4.99

