# OpenCode: echte Blatt-2-Abgabe mit TXT-Aufgabenstellung

Datum: 2026-11-16. Genau ein Lauf, OpenCode2.3.0/Qwen_3_30B_A3B_Instruct_2507. Identischer Nutzerprompt und identische Materialbytes wie DeepAgents-TXT-Versuch kontrolliert. Dasselbe anonymisierte ZIP mit vier Originaldateien, vollständiger Aufgabenblatttext. WYPP-Schnittstelle erläutert, keine Importzeilen oder Testfälle vorgegeben. Kein src verwendet. Zehn native Modellschritte, 120 Sekunden.

## Ablauf

Aufgabenblatttext gelesen und ZIP entpackt. Nicht rekursiver glob unter arbeit fand zunächst keine Pythondateien; zwei ls-Aufrufe erschlossen den Abgabe-Unterordner. Danach vier Originaldateien einzeln gelesen. Im neunten Modellschritt eine Testdatei für Aufgabe1 tatsächlich geschrieben. Im zehnten Schritt native Abschlusszusammenfassung am Limit. Kein Shellstart dieser Testdatei und keine Abgabecodeausführung.

Die eine Testdatei enthält sieben check-Aufrufe, die dieselben Eingaben/Sollwerte wie die sieben bereits vorhandenen Abgabetests wiederholen. Keine neue Fallabdeckung in diesem Test. Import auf aufgabe_01 statt tatsächlichem Aufgabe1 und kein Suchpfad zum Unterordner abgabe. Unter dem empfohlenen Startbefehl ist die Einbindung daher nicht korrekt vorbereitet. Dies statisch beurteilt, keine zusätzliche manuelle Ausführung.

## Abschlussbewertung

Die fehlende Testausführung wird ausdrücklich eingestanden; keine behaupteten bestandenen Vergleiche. Falsch ist jedoch die Aussage, für Aufgabe2 bis4 seien Testdateien erstellt worden: Rohverlauf und Arbeitsordner enthalten nur die Datei für Aufgabe1. Der Abschluss erwähnt zudem Tests vor Rumpf als Schemaüberprüfung, obwohl der Auftrag untersagt, die zeitliche Entwicklung aus Endcode abzuleiten. Keine vollständige fachliche Korrekturantwort.

## Vergleich und Grenzen

DeepAgents las unter derselben TXT-Bedingung alle vier Dateien und gab nach sechs Antworten nachgeahmte Werkzeugaufrufe als Text aus; keine echten Testdateien. OpenCode schrieb eine echte Testdatei, erreichte aber keine Ausführung. Bei beiden ist vollständige echte Blattkorrektur nicht nachgewiesen. Kein allgemeiner Harness-Sieger: unterschiedliche Systemprompts, Werkzeuge, Modellparameter und Stopsemantik. Keine Aussage, dass zehn Schritte stets zu wenig sind oder mehr Budget den fehlerhaften Import beheben würde.

Dauer: 13.041 Sekunden. Gemeldete Tokens: 79507 aus 10 Modellschritten. Alle Ausgangsmaterialien und entpackten Codebytes unverändert geprüft. Keine automatische Wiederholung. Als nächstes Ergebnisse für das Meeting konsolidieren; keine weiteren Hilfen oder höhere Limits ohne getrennte Versuchsentscheidung.
