from wypp import *

# Es gibt folgende T-Shirt-Größen: S, M, L, XL
type TShirtGröße = Literal['S', 'M', 'L', 'XL']

# Es gibt folgende Farben für T-Shirts: “schwarz”, “weiß”, “gelb-grün”,
# “lila-blassblau” und viele weitere
# Keine Aufzählung, sondern modelliert als String.

# Ein T-Shirt hat folgende Eigenschaften:
# - Farbe (Typ str)
# - Größe (Typ TShirtGröße)
@record
class TShirt:
    farbe: str
    größe: TShirtGröße
