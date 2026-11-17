# Eigene Tests ohne PDF- und ZIP-Verarbeitung

Stand: 2026-11-16. Genau ein Lauf mit OpenCode 2.3.0 und
Qwen_3_30B_A3B_Instruct_2507. Maximal sechs Modellschritte und 120 Sekunden.
Keine Wiederholung, Fortsetzung oder zusätzliche manuelle Testausführung.

## Anlass und Aufbau

Der vorherige vollständige Kleinstfall erreichte bei acht Schritten noch keine
Testgenerierung. Deshalb entfielen diesmal PDF und ZIP im Agentenauftrag.
Die gleichen zwei synthetischen Abgabedateien wurden unverändert direkt unter
material/ bereitgestellt. Die beiden Funktionsanforderungen standen im Prompt.
Keine konkreten Testeingaben oder Sollwerte vorgegeben.

Der Auftrag verlangt eigene WYPP-checks, Ausführung gegen die Originaldateien
und auf tatsächlichen Testergebnissen beruhendes Feedback. Python und WYPP sind
vorhanden. Keine Reparaturen, Paketinstallation, Websuche oder Delegation.
Kein src-Import, eigener studentischer Test-Runner oder fertige Fachtests.

## Tatsächlicher Verlauf

1. Zwei glob-Aufrufe mit absoluten Mustern melden keine Dateien.
2. Das read-Werkzeug listet das Materialverzeichnis erfolgreich auf.
3. Erste Abgabedatei gelesen: quadrat liefert x+x.
4. Zweite Abgabedatei gelesen: positiv verwendet x>=0.
5. Zwei eigene Testdateien unter arbeit/ geschrieben.
6. Native Abschlussantwort nach Erreichen der Schrittgrenze.

Ein direkter shell-Aufruf zur Testausführung findet nicht statt. Die
Abschlussantwort kennzeichnet die Ausführung als noch offene Arbeit und
erfindet kein Testergebnis.

## Testauswahl und technische Form

test_aufgabe_01.py prüft die Eingaben 2, -3, 0 und 1 mit den Sollwerten
4, 9, 0 und 1. Diese Sollwerte stimmen mit der Aufgabenstellung überein.
-3 und 1 unterscheiden die fehlerhafte Addition von der verlangten Multiplikation.
2 und 0 allein würden den Fehler nicht entdecken.

test_aufgabe_02.py prüft 5, -1, 0 und 100 mit True, False, False und True.
Alle Sollwerte sind fachlich richtig. Der Grenzfall 0 entdeckt den Fehler >=0.

Beide Dateien verwenden assert, keine der angeforderten WYPP-check-Aufrufe.
Zudem werden quadrat und positiv weder importiert noch definiert. Als
eigenständig gestartete Dateien fehlt ihnen daher die Anbindung an die Abgabe.
Eine tatsächlich beobachtete NameError-Ausgabe liegt nicht vor, weil kein
Testprozess gestartet wurde. Die fehlende Anbindung ist ein statischer Befund.

## Ergebnis und Grenzen

Beide Dateien korrekt zugeordnet. Acht eigene Prüfbedingungen mit fachlich
richtigen Sollwerten erstellt; darunter je ein fehleraufdeckender Fall.
Kein funktionierender Testlauf und kein aus Ausführungsbefunden abgeleitetes
Feedback. Die Fehler werden lediglich aus dem Code richtig beschrieben.

Sechs Modellantworten, rund elf Sekunden. Die genaue Dauer und gemeldeten Tokens
stehen in opencode/bericht.json; vollständige Werkzeugaufrufe und Rückgaben in
opencode/ausgabe/verlauf.jsonl. Die Originaldateien und Material-Hashes blieben
unverändert. Der Container wurde entfernt.

Testauswahl ist in diesem Lauf besser belegt als zuvor. Ob der Agent die
Importprobleme selbst behebt und die Originalfunktionen korrekt testet, ist
weiterhin offen. Ein Lauf ist kein Nachweis allgemeiner Zuverlässigkeit.
Aus dieser Notiz keine Freigabe für zusätzliche Modellaufrufe ableiten.
