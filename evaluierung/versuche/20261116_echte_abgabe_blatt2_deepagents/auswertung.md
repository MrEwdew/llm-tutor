# Erste echte Abgabe: Blatt 2, DeepAgents

Datum: 2026-11-16. Ein Lauf, Qwen_3_30B_A3B_Instruct_2507. Zehn Modellstarts als Obergrenze, 120 Sekunden. Kein src verwendet, keine Musterloesung und keine vorbereiteten Testfaelle uebergeben.

## Auswahl und Datenschutz

Aus dem Wochenarchiv von Blatt 2 wurde deterministisch die erste Abgabe in Archivreihenfolge mit vier Python-Dateien gewaehlt. Kein Auswaehlen nach erwartetem Modellresultat. Die vier Dateien wurden vollstaendig gelesen. Keine studentischen Namen, Matrikelnummern oder Kontakte in den Code-Inhalten festgestellt. Personenbezogene Oberordner und alle fremden Archivmetadaten wurden weggelassen; nur unveraenderte Codebytes mit urspruenglichen Basisdateinamen unter abgabe/ in ein neues ZIP uebernommen. Nicht benoetigte Praktomat-Dateien nicht uebergeben. Kurs-PDF unveraendert, einschliesslich oeffentlicher Lehrendenangaben. Herkunft intern ueber Quellarchivhash und Auswahlindex in eingaben.json nachvollziehbar; kein studentischer Name im Versuchsordner.

Anders als beim synthetischen Fall wurden keine konkreten Importzeilen vorgegeben. Erhalten blieben Hinweise auf Python/pypdf und die zweistellige WYPP-Schnittstelle. Der Auftrag verlangte Lesen aller Aufgaben und Dateien, eigene Tests, echte Ausfuehrung, formale Bewertung und ausdrueckliche Kennzeichnung offener Teile. Keine automatische Note.

## Beobachteter Ablauf

Material aufgelistet, ZIP entpackt. Trotz pypdf-Hinweis zunaechst PDF direkt ueber read_file geladen. Der folgende API-Aufruf scheiterte mit HTTP 400 wegen nicht unterstuetztem Inhaltstyp file. Danach setzte der Harness den Verlauf fort und der Agent extrahierte den Text erfolgreich mit Python/pypdf. Diese Fortsetzung trat innerhalb desselben beauftragten Harness-Laufs auf; kein zweiter Hostlauf. Adapter war mit max_retries=0 konfiguriert, dennoch ist die beobachtete interne Fehlerbehandlung des Harnesses im Rohverlauf erhalten.

Anschliessend wurden alle vier Dateien gelesen. Ein glob fuer aufgabe_0*.py fand nichts; ls zeigte Aufgabe1.py bis Aufgabe4.py. Die Zuordnung der vier Funktionen zu den Aufgaben gelang statisch. Danach gab der Agent sofort Abschlussfeedback aus. Keine Testdatei geschrieben, kein Abgabecode importiert oder gestartet und kein Zusatztest ausgefuehrt.

## Fachliche Nachpruefung des Feedbacks

- Richtig: Aufgabe 2 verwendet Ausdruecke wie 2 or 3 or 4 or 5 im Gleichheitsvergleich. Diese liefern nur 2; gueltige Rueckennummern wie 3 werden deshalb falsch zugeordnet. Dies ist hier statisch belegt, nicht dynamisch getestet.
- Falsch: Die Behauptung, Aufgabe 3 sei wegen fehlendem import math nicht ausfuehrbar. from wypp import * exportiert math ausdruecklich ueber __all__. Das wurde anhand der lokal installierten WYPP-2.3.0-Quelle geprueft, ohne Abgabecode auszufuehren. Der Agent hatte diese Abhaengigkeit nicht kontrolliert.
- Falsch: <=99 erfasse auch 100. 100 erfuellt die Bedingung nicht. Zudem erlaubt Aufgabe 2, ungueltige Eingaben zu ignorieren; eine Forderung nach deren vollstaendiger Behandlung ist hier nicht gerechtfertigt.
- Falsch: Aufgabe 1 habe keine Kurzbeschreibung. Ein beschreibender Kommentar ist vorhanden. Ihre Datenanalyse ist dagegen nur mit leeren Eingabe-/Ergebnis-Kommentaren angedeutet und unvollstaendig.
- Unbelegt: Die Nullpunkte-Aussage zu Aufgabe 3 stuetzt sich auf den falschen math-Importbefund; ein tatsaechlicher Ausfuehrungsfehler wurde nicht beobachtet.
- Uebersehen: Basisdateinamen Aufgabe1.py usw. entsprechen nicht der expliziten Dateivorgabe aufgabe_01.py usw. Der Hinweis muss die Originalbasisnamen betreffen; der fuer Datenschutz neutralisierte ZIP-Name darf nicht als studentischer Fehler bewertet werden.
- Unzulaessig: Abschliessende Aussagen ueber Teilpunktverluste und 0 Punkte trotz Auftrag ohne automatische Note.
- Falscher Ausfuehrungsnachweis: Aufgelistete Testzahlen 7/5/9/8 stammen aus vorhandenen check-Aufrufen der Abgabe. Sie wurden nur gelesen, nicht ausgefuehrt. Die Behauptung, alle Aufgaben mit eigenen Tests geprueft zu haben, widerspricht dem Werkzeugverlauf.

## Ergebnis

PDF-Auslese, ZIP-Entpacken, Lesen und statische Zuordnung gelungen. Verlangte eigene Testgenerierung und Ausfuehrung nicht erfolgt. Feedback teilweise richtig, aber mit falschen Beanstandungen und erfundener Ausfuehrungsbehauptung. Kein erfolgreicher vollstaendiger Korrekturlauf.

Dauer: 12.936 Sekunden. Modellstarts: 7; erfolgreiche Modellantworten: 6. Gemeldete Tokens: 28732; Verbrauch des fehlgeschlagenen Requests unbekannt und nicht enthalten. Original-PDF/ZIP sowie entpackte Codebytes erneut unveraendert geprueft.

Nur ein Fall, keine allgemeine Fehlerquote. Gegenueber dem synthetischen Versuch aendern sich zugleich Umfang, Aufgaben, Dateinamen und Importhilfe; der Rueckschritt ist daher nicht allein einer Ursache zuzuordnen. Keine weiteren Modelllaeufe oder Abgabetests automatisch gestartet. Naechster sinnvoller Untersuchungspunkt ist die nicht erfolgte Ausfuehrung und die behauptete Testabdeckung, statt sofort weitere Abgaben zu stapeln.
