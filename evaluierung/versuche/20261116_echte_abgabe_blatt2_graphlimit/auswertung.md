# Echte Abgabe: internes Graphlimit 100

Datum: 2026-11-16. Ein DeepAgents-Lauf mit Qwen_3_30B_A3B_Instruct_2507. Gegenueber dem vorherigen Versuch ausschliesslich recursion_limit von 30 auf 100 erhoeht. Promptgleichheit kontrolliert, identisches anonymisiertes Material. Zehn Modellstarts und 120 Sekunden unveraendert. Keine src-Funktionen.

## Beobachtung

ZIP entpackt, mehrere Verzeichnisse einzeln aufgelistet. Erneut trotz Hinweis das PDF direkt mit read_file geladen. Naechster API-Aufruf scheiterte mit HTTP 400 am Dateiblock-Typ file. Danach erfolgreiche PDF-Textextraktion durch Python/pypdf. Anschliessend Aufgabe1.py, Aufgabe2.py und Aufgabe3.py einzeln gelesen. Aufgabe4.py nicht mehr gelesen. Keine Testdateien erzeugt, kein Abgabecode gestartet, kein Abschlussfeedback.

Nach zehn gezaehlten Modellstarts blockierte der Callback den Versuch eines weiteren Starts. Neun erfolgreiche Modellantworten, ein fehlgeschlagener API-Aufruf. Der Callback zaehlt fehlgeschlagene Starts mit; das native Middleware-Limit alleine bildet diese Grenze nicht gleich ab. Das hoehere Graphlimit griff nicht vorzeitig; die Modellstartgrenze funktionierte wie vorgesehen. Kein weiterer Modellrequest nach der Callback-Sperre ausgefuehrt.

## Messung und Einordnung

Dauer: 5.038 Sekunden. Gemeldete Tokens: 40841 aus 9 erfolgreichen Antworten. Usage des gescheiterten API-Aufrufs unbekannt. Ausgangsmaterial und entpackte Codebytes erneut unveraendert bestaetigt. Prozessfehler bedeutet hier beabsichtigten Budgetabbruch, keinen Fehler im studentischen Programm.

Die Graphlimit-Konfiguration ist damit fuer diesen Verlauf kein vorzeitiger Engpass mehr. Nun verbrauchten Dateierkundung, PDF-Fehlversuch und einzelne Leseaufrufe das Modellbudget. Die Ausfuehrungsvorgabe konnte in diesem Budget nicht bis zur Testphase untersucht werden. Keine allgemeine Aussage, dass zehn Schritte stets unzureichend sind: Der erste echte Lauf las die Dateien in weniger Aufrufen, uebersprang aber anschliessend die Tests.

Keine weitere Wiederholung gestartet. Vor einer weiteren Budgeterhoehung waere eine getrennte Bedingung mit vorab extrahiertem Aufgabenblatttext sinnvoll, um Dateiverarbeitung von eigentlicher Korrektur zu trennen. Diese Unterstuetzung muesste offen ausgewiesen werden und waere kein Nachweis selbststaendigen PDF-Lesens. Der urspruengliche PDF/ZIP-Befund bleibt erhalten.
