# Korrekte Gegenprobe mit Import- und WYPP-Hilfe

Datum: 2026-11-16. Genau ein DeepAgents-Lauf mit Qwen_3_30B_A3B_Instruct_2507. Sechs Modellaufrufe und 120 Sekunden als Grenzen. Derselbe Prompt wie im erfolgreichen Versuch mit fehlerhaften Funktionen; Gleichheit kontrolliert. Nur die Eingabefunktionen wurden durch die korrekten Implementierungen x*x und x>0 ersetzt. Keine Funktionen aus src verwendet.

## Ablauf

Der Agent listete die Dateien auf, las beide und erzeugte eine gemeinsame Testdatei. Importe und Suchpfad entsprachen der vorgegebenen technischen Hilfe. Die sechs selbst gewaehlten WYPP-checks hatten korrekte Sollwerte: quadrat(0)=0, quadrat(3)=9, quadrat(-2)=4; positiv(5)=True, positiv(0)=False, positiv(-3)=False.

Die Testdatei wurde tatsaechlich mit Python ausgefuehrt. Werkzeugausgabe: keine Ausgabe, Exitcode 0. Der gelesene Testcode enthaelt sechs direkte check-Aufrufe, keine Fehlerunterdrueckung und keine Ersatzdefinitionen. Zusammen mit dem vollstaendigen Prozesslauf und dem bekannten WYPP-Verhalten ist dies ein Nachweis, dass diese sechs Vergleiche ohne gemeldeten Fehler durchliefen. Es handelt sich nicht um einen strukturierten Testreport mit einzeln protokollierten Erfolgen.

Der sechste Modellaufruf lieferte das Abschlussfeedback: alle Tests bestanden, keine Fehler gefunden. Keine falschen Beanstandungen oder Forderungen nach Kommentaren oder Abgabetests beobachtet. Die allgemeine Formulierung der Korrektheit im Feedback geht ueber die endliche Testauswahl hinaus; die kleinen Originalfunktionen entsprechen nach eigener statischer Kontrolle allerdings ebenfalls der Spezifikation.

## Ergebnis und Vergleich

| Eingabe | Gemeldete fehlerhafte Checks | Abschlussfeedback | Dauer | Tokens |
| --- | ---: | --- | ---: | ---: |
| Fehlerhafte Funktionen, vorheriger Lauf | 3 von 6 | Beide Funktionsfehler erkannt | 5,887 s | 22.377 |
| Korrekte Funktionen, dieser Lauf | 0 von 6 | Keine Fehler beanstandet | 17.894 s | 22074 |

Die Originaldateien blieben unveraendert; Hashwerte erneut kontrolliert. Beide Laeufe benoetigten sechs Modellantworten. Laufzeitunterschiede sind Einzelmessungen, keine belastbare Geschwindigkeitsaussage.

Unter den unterstuetzten Bedingungen gelang damit jeweils ein vollstaendiger kleiner Ablauf fuer eine fehlerhafte und eine korrekte Eingabe. Importzeilen und WYPP-Schnittstelle waren vorgegeben, Testeingaben und Sollwerte nicht. Keine allgemeine Zuverlaessigkeit, keine echte studentische Abgabe, keine PDF- oder ZIP-Verarbeitung in diesen beiden Versuchen. Keine automatische Wiederholung gestartet.
