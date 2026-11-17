# Echte Blatt-2-Abgabe mit gemeinsamer src-Eingabevorbereitung

Datum: 2026-11-16. Genau ein DeepAgents-Lauf mit Qwen_3_30B_A3B_Instruct_2507. Zehn Modellstarts, Graphlimit100, 120 Sekunden, Temperatur0 und maximal1000 Ausgabetokens pro Antwort. Erste Bedingung dieser Reihe mit fachlicher Eingabevorbereitung aus src/common.py. Kein src-Korrekturagent und kein src-Test-Runner verwendet.

## Vorbereitung und lokale Nachweise

load_exercise_submission und prepare_sheet_evaluation_input lesen das echte PDF und anonymisierte ZIP. Vier Aufgaben, allgemeine/abschliessende Vorgaben und vier Originalcodes vorbereitet. Exakte Dateinamen aufgabe_01.py usw. fehlen; vorhandene Aufgabe1.py usw. werden separat mit unbestaetigten Namensvorschlaegen erhalten. Keine automatische fachliche Zuordnung. prepare_code_file erfasst Funktionen/Syntaxbefunde gemeinsam fuer beide Dateigruppen. Lokal geprueft: gueltig, Syntaxfehler, leer, fehlend, Java ohne Pythonanalyse; Syntaxfehler blockiert andere Datei nicht. Alle vier echten Funktionen erkannt, Code unveraendert. Kein Abgabecode fuer diese Vorbereitung ausgefuehrt.

Gesamteingabe:8722 Zeichen. Originaldateien zusaetzlich unter material/abgabe/ mit unveraenderten Bytes bereitgestellt, damit der Agent sie selbst importieren kann. PDF/ZIP werden durch unsere Vorbereitung ersetzt. Keine konkreten Imports, Testeingaben oder Sollwerte vorgegeben. common.py-Hash und Herkunft im Manifest gespeichert.

## Beobachteter Lauf

1. read_file fuer eingabe.txt und ls. Das Lesewerkzeug lieferte nur Zeilen1–100 von 260 und wies mit next offset100 auf weitere Seiten hin.
2. Pythondateien unter material/abgabe per glob gefunden.
3. Alle vier Originaldateien separat gelesen.
4. Antworttext mit tool_call-Markierungen und JSON-Testvorschlaegen, aber leere strukturierte tool_calls. Keine Dateien geschrieben und keine Tests gestartet. Antwort am Ausgabelimit1000 mit finish_reason=length abgeschnitten.

Der Agent las die vorbereitete Gesamteingabe trotz Auftrag nicht vollstaendig. Das statische Funktionsinventar beginnt erst in Zeile244 und wurde nicht zugestellt. Deshalb ist kein erfolgreicher Einsatz dieses Inventars nachgewiesen. Der Modellkontext hatte zwar die separat gelesenen Originalcodes, aber nicht alle vorbereiteten Abschnitte. Die Vollstaendigkeit der erzeugten Eingabe ist von ihrer tatsaechlichen Aufnahme durch den Agenten zu unterscheiden.

Die textuell vorgeschlagenen Imports verwenden erneut aufgabe_01 statt tatsächlichem Aufgabe1 usw.; Unterordner nicht eingebunden. Einige zusaetzliche Tests fuer gueltige Rueckennummern sind passend, fuer ungueltige Nummern0/100 wird aber unbegruendet Ersatzspieler verlangt. Diese Vorschlaege nicht ausgefuehrt und nicht nachtraeglich in echte Toolcalls umgewandelt.

## Ergebnis und Vergleich

Dauer:14.483 Sekunden. Vier Modellantworten,21567 gemeldete Tokens. Vorheriger DeepAgents-TXT-Fall ohne src-Vorbereitung:sechs Antworten,32060Tokens,14,465s; ebenfalls keine Tests. Weniger Aufrufe/Tokens in diesem einzelnen Verlauf ist beobachtet, aber kein belastbarer Effizienzgewinn: die Eingabe wurde unvollstaendig gelesen und der Auftrag erneut nicht abgeschlossen. Mehrere Bedingungen aendern sich (Vorbereitung, kein ZIP-Entpacken, Materialpfade, Prompt), daher keine isolierte Aussage ueber eine einzelne Funktion.

Alle bereitgestellten Materialdateien unveraendert per Hash kontrolliert. Keine API-Fehler, keine Testdateien, keine Abgabeausfuehrung. Hoststatus completed bedeutet nur Prozessende. Keine automatische Wiederholung.

## Naechster Untersuchungspunkt

Zuerst sicherstellen, dass die Gesamteingabe im Modell wirklich vollstaendig ankommt, etwa direkt als Nachricht oder durch kontrolliertes vollstaendiges Lesen. Das waere ein transparenter weiterer Vorbereitungsschritt und ist noch nicht umgesetzt oder live getestet. Danach Werkzeugprotokoll und Ausgabelimit getrennt untersuchen. Nicht aus diesem Lauf ableiten, dass unser Funktionsinventar nicht hilft: es wurde hier nicht gelesen.
