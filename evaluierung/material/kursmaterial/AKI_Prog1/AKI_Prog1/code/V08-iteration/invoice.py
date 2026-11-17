from wypp import *

# Ein Rechnungsposten besteht aus
# - Artikelnummer (Typ: str)
# - Name (Typ: str)
# - Preis (Typ: float)
@record
class InvoiceItem:
    articleId: str
    articleName: str
    price: float

# Eine Rechnung besteht aus
# - Datum (Typ: str)
# - Rechnungsposten (Typ: list[InvoiceItem])
@record
class Invoice:
    date: str
    items: list[InvoiceItem]

item1 = InvoiceItem('A9810', 'Kompaktkassette', 5.99)
item2 = InvoiceItem('A3510', 'Eismaschine', 249.99)
item3 = InvoiceItem('A9614', 'Taschentrompete', 89.00)
sampleInvoice = Invoice('2024-11-08', [item1, item2, item3])

# Gesamtbetrag einer Rechnung berechnen
# Eingabe: die Rechnung (Typ: Invoice)
# Ergebnis: Gesamtbetrag in Euro (Typ: float)
def totalInvoiceAmount(invoice: Invoice) -> float:
    gesamtkosten = 0
    for item in invoice.items:
        gesamtkosten = gesamtkosten + item.price
    return gesamtkosten

totalInvoiceAmount(sampleInvoice)

#check(totalInvoiceAmount(sampleInvoice), 344.98)
#check(totalInvoiceAmount(Invoice('2026-11-10', [])), 0)
