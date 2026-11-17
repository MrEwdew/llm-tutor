# Echte Abgabe mit vorab extrahiertem Aufgabenblatttext

Datum: 2026-11-16. Genau ein DeepAgents-Lauf mit Qwen_3_30B_A3B_Instruct_2507. Dieselbe anonymisierte Vier-Dateien-Abgabe von Blatt 2. Keine src-Bausteine. Aufgaben-PDF durch den gesamten mit pypdf extrahierten Text beider Seiten ersetzt (4090 Zeichen); keine manuelle fachliche Zusammenfassung oder Zuordnung. Layout und Sonderzeichen sind entsprechend der Textextraktion erhalten, insbesondere zerfallene Fallklammern bei clamp. ZIP unveraendert gegen vorherigen Versuch kopiert.

Zehn Modellstarts, internes Graphlimit 100, zwei Minuten; WYPP-Hilfe ohne konkrete Importzeilen. Der Prompt wurde nur auf TXT-Lesen statt PDF-Verarbeitung abgestimmt; fachliche Aufgaben und ausdruecklicher Ausfuehrungsnachweis blieben erhalten. Kein PDF im Modellmaterial dieses Laufs.

## Verlauf

1. Vollstaendigen Aufgabenblatttext gelesen, ZIP gefunden.
2. ZIP entpackt.
3. Arbeitsordner aufgelistet.
4. Abgabeordner aufgelistet.
5. Alle vier Originalcode-Dateien gelesen.
6. Abschluss als normaler Text mit nachgeahmten tool_call-Markierungen und JSON-Inhalten fuer write_file. Keine strukturierten tool_calls und keine Werkzeugrueckgaben hierfuer. Deshalb keine Testdateien angelegt und keine Tests gestartet. Auf dem erhaltenen Arbeitsordner wurde das Fehlen eigener Testdateien kontrolliert.

Die letzte Modellantwort endete mit finish_reason=length bei 1000 Ausgabetokens. Der Text bricht im vorgeschlagenen vierten Testskript ab. Das ist das Ausgabelimit pro Modellantwort, nicht das Zehn-Aufruf-Limit und kein aufgebrauchtes API-Kontingent. Der Harness beendete den Lauf mangels strukturierter Werkzeuganforderungen; der aeussere Exitcode 0 ist kein Korrekturerfolg.

## Inhaltliche Befunde des nicht ausgefuehrten Textes

Einige Testeingaben und Sollwerte sind passend, etwa Rueckennummer 3 fuer Abwehr. Die Imports lauten aber auf aufgabe_01 bis aufgabe_04 statt der tatsaechlich gelesenen Aufgabe1 bis Aufgabe4; zudem fehlt die Einbindung ihres Unterordners. Fuer ungueltige Rueckennummern 100 und 0 wird Ersatzspieler gefordert, obwohl das Blatt ungueltige Eingaben ignorieren laesst. Diese Sollwerte sind unbegruendet. Viele vorhandene Abgabetests werden wiederholt; nur ein Teil waere neu. Alle diese Feststellungen beruhen auf Lesen des Textvorschlags, nicht auf Ausfuehrung.

## Ergebnis und Grenzen

TXT-Lesen beseitigte in diesem Lauf den frueheren PDF-Dateiblockfehler. Keine API-Fehler. Eigentliche Testgenerierung als nutzbare Dateien, Ausfuehrung und Korrekturfeedback dennoch nicht erreicht. Das Problem ist somit nicht ausschliesslich PDF-Verarbeitung. Werkzeugprotokoll und Ausgabelimit sind weitere beobachtete Engpaesse; eine Erhoehung des Ausgabelimits allein ist nicht als Loesung belegt.

Dauer: 14.465 Sekunden. Sechs Modellantworten, gemeldete Tokens: 32060. Ausgangstext/ZIP und entpackte Codebytes per Hash bzw. ZIP-Bytes unveraendert geprueft. Keine automatische Reparatur des Antworttextes in echte Werkzeugaufrufe, keine weiteren Modelllaeufe oder manuelle Ausfuehrung der vorgeschlagenen Tests.

Ein Einzelversuch, keine allgemeine Erfolgsquote. Zunaechst die bisherigen Grenzen gemeinsam auswerten; keine weiteren Budget-/Promptaenderungen automatisch anschliessen.
