from wypp import *

# Der Lebensstatus ist entweder tot oder lebendig
type Lebensstatus = Literal['tot', 'lebendig']

# Ein Gürteltiert hat folgende Eigenschaften
# - Lebensstatus: tot oder lebendig (Typ: ??)
# - Gewicht in Gramm (Typ: int)
@record
class Gürteltier:
    lebenstatus: Lebensstatus
    gewicht: int

dora = Gürteltier('lebendig', 25000)
daniel = Gürteltier('tot', 30000)

# Gürteltier nach Fütterung bestimmen
# Eingaben:
# - Futtermenge in Gramm (Typ: int)
# - Gürteltier (Typ: Gürteltier)
# Ergebnis: Gürteltier (Typ: Gürteltier)
def füttereGürteltier(futtermenge: int, gürteltier: Gürteltier) -> Gürteltier:
    if gürteltier.lebenstatus == 'lebendig':
        return Gürteltier('lebendig', round(gürteltier.gewicht + 0.5 * futtermenge))
    else:
        return gürteltier

check(füttereGürteltier(20, dora), Gürteltier('lebendig', 25010))
check(füttereGürteltier(1000, daniel), daniel)
