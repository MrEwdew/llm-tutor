from wypp import *

# Ermäßung bei Eintritt in Zoo: ja/nein?
# Eingabe: Alter einer Person in Jahren als int
# Ergebnis: True wenn ermäßigter Eintritt, False sonst (bool)
def istErmäßigterEintrittMöglich(alter: int) -> bool:
    return alter < 13 or alter >= 70

check(istErmäßigterEintrittMöglich(13), False)
check(istErmäßigterEintrittMöglich(12), True)
check(istErmäßigterEintrittMöglich(70), True)
check(istErmäßigterEintrittMöglich(69), False)

# Eine Altersgruppe hat folgende Alternativen:
# - Baby
# - Kleinkind
# - Kind
# - Teenager
# - Erwachsene
# - Erfahrene
type Altersgruppe = Literal['Baby', 'Kleinkind', 'Kind', 'Teenager', 'Erwachsene', 'Erfahrene']

# Berechnet ob eine Person anhand ihrer Altersklassifikation zu ermäßigtem
# Eintritt berechtigt ist.
# Eingabe: die Altersgruppe (Typ: Altersgruppe)
# Ergebnis: True wenn ermäßigter Eintritt, False sonst (bool)
def istErmäßigterEintrittMöglichFürAltersgruppe(altersgruppe: Altersgruppe) -> bool:
    if altersgruppe == 'Baby':
        return True
    elif altersgruppe == 'Kleinkind':
        return True
    elif altersgruppe == 'Kind':
        return True
    elif altersgruppe == 'Teenager':
        return False
    elif altersgruppe == 'Erwachsene':
        return False
    elif altersgruppe == 'Erfahrene':
        return True

check(istErmäßigterEintrittMöglichFürAltersgruppe('Baby'), True)
check(istErmäßigterEintrittMöglichFürAltersgruppe('Kleinkind'), True)
check(istErmäßigterEintrittMöglichFürAltersgruppe('Kind'), True)
check(istErmäßigterEintrittMöglichFürAltersgruppe('Teenager'), False)
check(istErmäßigterEintrittMöglichFürAltersgruppe('Erwachsene'), False)
check(istErmäßigterEintrittMöglichFürAltersgruppe('Erfahrene'), True)
