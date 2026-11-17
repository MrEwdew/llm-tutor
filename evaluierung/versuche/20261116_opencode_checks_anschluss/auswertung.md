# Anschlussversuch: eigene Tests anbinden und ausführen

Stand: 2026-11-16. Ein beauftragter Lauf mit OpenCode 2.3.0 und
Qwen_3_30B_A3B_Instruct_2507. Vier native Modellschritte, maximal 120 Sekunden.
Keine Wiederholung und keine zusätzliche manuelle Ausführung generierter Tests.

## Voraussetzungen und Eingriffe

Der vorherige Container samt temporärem HOME war entfernt. Deshalb handelt es
sich um eine neue Sitzung mit ausdrücklich mitgegebenem Anschlusskontext,
nicht um eine Fortsetzung derselben OpenCode-Sitzung. Dies wurde vor dem Start
kenntlich gemacht. Die Originaldateien und die beiden vom Agenten erzeugten
Testdateien wurden unverändert übernommen; Herkunft und Hashes in eingaben.json.

Aufgabenstellung als Text, keine PDF-/ZIP-Verarbeitung. Der Auftrag nennt die
vier Dateipfade, verlangt die Anbindung an Originaldateien und WYPP-checks,
tatsächliche Ausführung und Feedback anhand der Werkzeugausgabe. Keine fertigen
Importzeilen, neuen Testeingaben oder Sollwerte vorgegeben. Die vorhandenen
Sollwerte stammen aus den zuvor vom Agenten erzeugten Testdateien.

Kein src-Import, eigener studentischer Test-Runner oder fachlicher Helfer.
Der Starter stellt nur Material, Konfiguration, Dockergrenzen und Protokollierung.
Originaldateien sind schreibgeschützt; Tests unter arbeit/ bearbeitbar.

## Tatsächlicher Verlauf

1. Beide Originaldateien und beide bisherigen Testdateien gelesen.
2. Entgegen dem Auftrag versucht, positiv von >=0 auf >0 und quadrat von x+x
   auf x*x zu ändern. Beide edit-Aufrufe auf die Originaldateien werden abgewiesen.
   Im selben Modellschritt werden beide unveränderten Testskripte mit Python gestartet.
   Beide enden mit NameError, weil die Funktionen im Testskript nicht gebunden sind.
3. Beide Testdateien neu geschrieben: from aufgabe_01 import quadrat bzw.
   from aufgabe_02 import positiv ergänzt. Die assert-Prüfungen bleiben erhalten.
4. Native Abschlussantwort am Schrittlimit. Keine erneute Ausführung nach Änderung.

## Fachliche und technische Bewertung

Testprozesse wurden tatsächlich gestartet. Ein Test der Originalfunktionen wurde
jedoch nicht erreicht: Die Namensauflösung scheitert vor dem Funktionsaufruf.
Diese NameError-Ausgaben sind Testinfrastrukturfehler, keine nachgewiesenen
fachlichen Fehler der Abgabe. Es liegen keine bestandenen oder fehlgeschlagenen
Funktionsvergleiche gegen die Originalimplementierung vor.

Die ergänzten Imports beheben die Anbindung unter den gezeigten Startbefehlen
nicht nachweislich. Originalmodule liegen unter material/, die Skripte unter
arbeit/. Weder ein passender Suchpfad noch ein Laden über den tatsächlichen
Dateipfad wurde ergänzt. Die Abschlussbehauptung, die Tests seien nun korrekt
angebunden, ist deshalb unbelegt. Eine nachfolgende ModuleNotFoundError-Ausgabe
wurde nicht beobachtet, da die geänderten Skripte nicht erneut gestartet wurden.

Die vorgeschriebenen WYPP-check-Aufrufe fehlen weiterhin; es bleiben acht
assert-Prüfungen mit den bereits zuvor fachlich geprüften Sollwerten.
Der Agent erkennt somit einen fehlenden Import, erledigt dessen Einbindung
aber nicht vollständig und verletzt zusätzlich die Grenze zur Reparatur.

## Ergebnis und Grenzen

Originalbytes und Hashes sind unverändert. Die Reparaturversuche hatten keinen
Erfolg. Alle Änderungen betreffen nur die erzeugten Testdateien im Versuchsort.
Der Container wurde entfernt. Ein normaler Prozess-Exitcode bedeutet hier keinen
erfolgreichen Korrekturauftrag.

Vier Modellantworten, rund sieben Sekunden; genaue Dauer und gemeldete Tokens
in opencode/bericht.json. Rohverlauf enthält alle Werkzeugaufrufe und Rückgaben.

Der gewünschte Nachweis selbstständiger, korrekter Testausführung gegen die
Originalfunktionen bleibt offen. Dieser unterstützte Anschlussversuch darf
nicht als Erfolg des ursprünglichen selbstständigen Laufs gewertet werden.
Einzelversuche erlauben keine allgemeine Aussage über alle Modelle oder Harnesses.
Aus dieser Notiz keine weiteren Live-Läufe oder Budgeterhöhungen ableiten.
