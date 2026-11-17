# Vollständige vorbereitete Eingabe direkt in der Nachricht

Datum: 2026-11-16. Ein DeepAgents/Qwen_3_30B_A3B_Instruct_2507-Lauf. Material, Modelleinstellungen und Limits unverändert zum vorherigen vorbereiteten Fall: zehn Modellstarts, Graphlimit100,120 Sekunden,1000 Ausgabetokens pro Antwort. Nur Übergabe geändert: vollständige8722Zeichen-Eingabe direkt an den Auftrag angehängt und Dateileseanweisung entsprechend ersetzt. Dass der ganze Inhalt einschließlich Funktionsinventar in der Startnachricht steht, gegen den gespeicherten Prompt kontrolliert. Tatsächliche semantische Nutzung aller Angaben nicht nachweisbar.

## Verlauf

Erster Aufruf ls und glob für Originaldateien. Zweiter Aufruf liest alle vier Codes erneut, obwohl sie schon in der Nachricht vorliegen. Dritter Aufruf liefert normale Antwort mit tool_call-Markierungen und JSON-Testvorschlägen, aber ohne strukturierte tool_calls. Keine Testdateien angelegt, keine Tests ausgeführt. Abschluss finish_reason=length bei1000Ausgabetokens, mitten im vierten Vorschlag abgeschnitten. Kein Modellstart- oder Graphlimit erreicht, keine API-Fehler.

Die textuellen Imports nennen erneut aufgabe_01 usw. statt tatsächlichem Aufgabe1 usw.; Unterordner nicht eingebunden. Für ungültige Rückennummern0/100 werden unbegründete Sollwerte Ersatzspieler verlangt. Passende Tests für gültige Nummern sind ebenfalls enthalten. Keine dieser Vorschläge tatsächlich ausgeführt; keine nachträgliche Umwandlung des Textes in Toolcalls.

## Einordnung

Unvollständiges dateiweises Lesen der Vorbereitung wurde durch vollständige Nachrichtenübergabe beseitigt. Der nachgeahmte Werkzeugaufruf und das Ausgabelimit bleiben bestehen. Daher kein vollständiger Korrekturerfolg und kein Nachweis, dass Eingabevorbereitung allein genügt. Nicht behaupten, der Agent habe das Inventar verstanden oder benutzt, nur weil es bereitstand.

Dauer:8.803Sekunden, drei Modellantworten,22683 gemeldete Tokens. Vorheriger dateibasierter Vorbereitungsfall:vier Antworten,21567Tokens,14,483s; nur100von260Zeilen gelesen. Weniger Schritte hier, aber früher unvollständiger Abschluss und fehlende Ausführung: keine belastbare Effizienz-/Qualitätsverbesserung. Originalmaterialien per Hash unverändert. Keine Wiederholung gestartet.

Nächste mögliche Untersuchung: Protokoll-/Ausgabeproblem getrennt prüfen oder gezielt anderes Modell/Harness unter derselben vorbereiteten Eingabe vergleichen. Nicht automatisch Antworttext ausführen oder bloß Limits erhöhen. Diese Optionen sind Planung, keine weitere Ausführungsfreigabe.
