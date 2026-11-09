from wypp import *

# Ein Computer besteht aus:
# - Prozessor
# - Festplatten-Kapazität in Gigabyte
# - Hauptspeicher-Kapazität in Gigabyte
@record
class Computer:
    prozessor: str
    festplatte: int
    hauptspeicher: int

# Gesamtspeicher berechnen
# Eingabe: ein Computer
# Ergebnis: die Summe von Haupt- und Festplattenspeicher (int)
def totalMemory(c: Computer) -> int:
    return c.festplatte + c.hauptspeicher


check(totalMemory(Computer('Intel i9', 1000, 16)), 1016)
check(totalMemory(Computer('AMD', 250, 8)), 258)


# Ein Modell ist eins der folgenden:
# - Billigmodell
# - Gamer-Modell
# - Office-Modell
type Modell = Literal['billig', 'gamer', 'office']

# Computer für ein bestimmtes Modell zusammenstellen.
# Eingabe: ein Modell
# Ergebnis: ein Computer
def standardComputer(modell: Modell) -> Computer:
    if modell == 'billig':
        return Computer('Sempron', 2, 500)
    elif modell == 'gamer':
        return Computer('Quad', 16, 1000)
    elif modell == 'office':
        return Computer('Intel i7', 8, 750)


check(standardComputer('billig'), Computer('Sempron', 2, 500))
check(standardComputer('gamer'), Computer('Quad', 16, 1000))
check(standardComputer('office'), Computer('Intel i7', 8, 750))


# ============================
# Aufgabe A
# ============================

# Berechnet einen Preis für einen Computer. Dabei gelten folgende Regeln zur Berechnung:
# - Arbeitsspeicher (GB) * 5€, mindestens 30€
# - Festplatte (500 GB) * 20€, Speicher wird auf 500 aufgerundet
# - CPU: 90€, Falls von Intel Aufschlag von 20€
# - Montage + andere Komponenten pauschal 100€
# Eingabe: Zu berechnender Computer (Computer)
# Ausgabe: Preis für den Computer
def calcComputerPreis(c: Computer) -> float:
    # Grundpreis für Montage und weitere Komponenten
    sum = 100
    # Arbeitsspeicher
    sum = sum + max(30, c.hauptspeicher * 5)
    # Festplatte
    sum = sum + math.ceil(c.festplatte / 500) * 20
    # CPU
    sum = sum + 90
    if 'Intel' in c.prozessor:
        sum = sum + 20
    return sum

check(calcComputerPreis(Computer('Intel i9', 900, 32)), 410)
check(calcComputerPreis(Computer('AMD 3700x', 900, 32)), 390)
check(calcComputerPreis(Computer('AMD 3700x', 1200, 32)), 410)
check(calcComputerPreis(Computer('AMD 3700x', 1200, 5)), 280)
check(calcComputerPreis(Computer('AMD 3700x', 500, 5)), 240)


# ============================
# Aufgabe B
# ============================

# Erweitert den Hauptspeicher eines Computers
# Eingabe:
# - Computer, der erweitert werden soll (Computer)
# - Menge des Hauptspeichers in GB, um die der Computer erweitert werden soll (int)
# Ausgabe: neuer Computer mit erweitertem Hauptspeicher
def extendRAM(c: Computer, ram: int) -> Computer:
    if ram <= 0:
        return c
    return Computer(c.prozessor, c.festplatte, c.hauptspeicher + ram)

check(extendRAM(Computer('Intel i9', 900, 32), 16), Computer('Intel i9', 900, 48))
check(extendRAM(Computer('Intel i9', 900, 16), 16), Computer('Intel i9', 900, 32))
check(extendRAM(Computer('Intel i9', 900, 16), 0), Computer('Intel i9', 900, 16))
check(extendRAM(Computer('Intel i9', 900, 32), -16), Computer('Intel i9', 900, 32))
