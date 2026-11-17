# Vergleichslauf mit integrierter Demo und gemeinsamem src-Einstieg

Datum:2026-11-16. Genau ein live gestarteter Menüablauf DEMO_integriert, Auswahl alle/1. Nach Lesen der aktuellen Demo, Korrekturagent und Runner. Autorisierter Aufruf mit vorhandenen Demoabgaben. Kein Paketupgrade oder Sourceumbau. Gemeinsamer src-Einstieg: PDF/ZIP-Vorbereitung, correction_agent.correct_python_submission, gemeinsamer Modellzugang, python_tests und python_test_runner. Kein Aufruf sämtlicher Dateien unter src: Legacy-main/Praktomat-Graph nicht mitgetestet. Keine neue ganze-Blatt-Fähigkeit ergänzt.

Ein komplettes Blatt mit sechs Aufgaben geladen, nur bekannte Aufgabe6 Boot korrigiert. Drei Varianten derselben Ausgangsabgabe, keine drei unabhängigen echten Abgaben. Drei feste fachlich vorab geprüfte Vergleichstests pro Variante. Referenz nur separat geladen, nicht ausgeführt oder ans Modell gegeben. Keine eigene Testgenerierung. Ausführung über vorhandenen lokalen Python-Unterprozess mit Timeout, kein Docker in diesem Demo-Pfad.

| Variante | Bestanden | Agentenlauf | Gemeldete Tokens | Ergebnisdatei unter DEMO_integriert/ergebnisse |
| --- | --- | ---: | ---: | --- |
| gut | 3/3 | 3.34s | 4633 | 20261116_214550_830480_gut.json |
| mittel | 2/3 | 2.14s | 4902 | 20261116_214553_096297_mittel.json |
| schlecht | 0/3 | 3.03s | 5405 | 20261116_214556_256624_schlecht.json |

Je zwei Modellantworten. Feste Vergleichsergebnisse korrekt und eingebettete Abgabeausgaben getrennt. Gut auf begrenzte Aussage ohne Funktionsfehler in geprüften Fällen beschränkt. Mittel erkennt return a statt Streckenberechnung, etwas ausführlich. Schlecht erkennt beide Ursachen a*vBoot statt a/vBoot und t+vFluss statt t*vFluss korrekt.

Feedbackfehler bei schlecht: Zusatzbeispiel verwendet nach t=8 plötzlich 8*1.5=12 und errechnet Strecke12.649, obwohl Originalcode abdrift als Addition ausführt. Tatsächlich b=8+1.5=9.5 und Strecke sqrt(4²+9.5²)=10.307764064044152; dieser Wert steht korrekt im Runnerergebnis. Die Erklärung des Modells widerspricht hier dem eigenen zutreffenden Ursachenbefund. Ausführung richtig, ergänzende Modellrechnung falsch. Keine vollständige Fehlerfreiheit behaupten.

## Vergleich zum autonomen echten Blatt2-Lauf

Unser vorhandener Demoablauf funktioniert für den bekannten numerischen Einzelaufgabenfall kontrollierter, mit deutlich weniger Modellaufrufen und Tokens. Er löst jedoch weniger: geprüfte Sollwerte und ausführbares Testwerkzeug sind vorgegeben; keine freien Imports, Dateisuche oder Testentwicklung durch das Modell. Die aktuellen freien Harness-Läufe bearbeiteten vier andere Aufgaben mit booleschen/textuellen Rückgaben, eigenen Sollwerten und zusätzlicher formaler Bewertung. Kein kontrollierter Gleichaufgabenvergleich und kein allgemeiner Nachweis besserer kompletter src-Blattkorrektur.

Der vorhandene src-Runner akzeptiert nur endliche numerische Ergebnisse ohne bool. Ein unveränderter kompletter Blatt2-Lauf hiermit würde boolesche oder textuelle Rückgaben nicht fachlich korrekt behandeln. Deshalb keine solche Scheinprüfung durchgeführt. Ein echter gleicher Vergleich benötigt eine eigens festgelegte Schnittstelle/Testbasis und passende Rückgabevergleiche; noch nicht umgesetzt. Legacy-Prototyp nicht zusätzlich ausgeführt.

Fazit: feste Tests und strukturierte Ergebniserfassung beseitigen Import-/Werkzeugprobleme des Demofalls und verhindern erfundene Messwerte im Runner. Fehlerfreie sprachliche Schlussfolgerungen sind auch damit nicht garantiert.
