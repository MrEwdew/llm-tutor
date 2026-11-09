# Boot-Aufgabe

Drei Abgaben zur gleichen Aufgabe: gut, mittel und schlecht.
DeepAgents steuert den Ablauf, Qwen über KI:CONNECT schreibt das Feedback.
Das Modell erhält die Aufgabenstellung, den Code und die Testergebnisse.

## Start

Im Ordner `llm-tutor` starten:

```text
python DEMO/demo.py
```

Im Menü zuerst die Abgabe, dann den Modus auswählen: live, nur Tests oder
gespeicherte Ergebnisse. Der Live-Modus ruft KI:CONNECT auf und speichert
Feedback und Messwerte unter `ergebnisse/`.
Gespeicherte Ergebnisse stammen aus früheren Containerläufen vom 03.11.2026.

## Einrichtung

Python 3.13, uv und Docker Desktop werden benötigt.

```text
python DEMO/einrichten.py
```

Die Einrichtung nutzt zunächst den uv-Cache. Für Downloads `--online` ergänzen.
Danach wird uv zum Starten nicht mehr benötigt.
Die eigene Umgebung liegt unter `DEMO/.venv`.
Docker Desktop muss laufen und das Image `tutor-python-test` vorhanden sein.
Ein Neubau ist mit `docker build -t tutor-python-test DEMO` möglich.

Die Zugangsdaten werden aus `llm-tutor/.env` geladen:
`KICONNECT_API_KEY` und `KICONNECT_BASE_URL`.
Für Live-Aufrufe braucht der Rechner eine Verbindung zu KI:CONNECT.

## Dateien

- `demo.py`: Auswahl, Agent, Testwerkzeug und Ausgabe.
- `korrektur_prompt.py`: Korrekturanweisung als Python-Konstante.
- `container_runner.py`: führt die drei Vergleichstests aus.
- `vergleichstests.json`: Eingaben und Sollwerte.
- `abgaben/`: die drei vorbereiteten Varianten.
- `material/`: Blatt 1, Aufgabentext und Referenz zur Einsicht.
- `gespeichert/`: frühere Ergebnisse als Reserve.

Die gute Abgabe ist eine unveränderte Kopie aus der vorhandenen Blatt-1-ZIP.
Bei mittel gibt `bootstrecke` nur die Flussbreite zurück. Bei schlecht wurden
Division und Multiplikation in den beiden Hilfsfunktionen durch falsche
Operationen ersetzt. Kommentare und enthaltene Tests bleiben erhalten.
Erwartet werden 3/3, 2/3 und 0/3 bestandene Vergleichstests.

Die Ausführung findet im Docker-Container ohne Netzwerk oder Hostmounts statt,
mit Ressourcenlimits und zehn Sekunden Zeitlimit.

## Umfang

Die Demo nutzt vorbereitete Dateien und bindet `src` bisher nicht ein.
Die Referenzdatei wird zur Laufzeit weder ausgeführt noch ans Modell geschickt.
Es gibt keine Testgenerierung, Benotung oder Java-Korrektur.
Enthaltene WYPP-Tests werden getrennt von den drei Vergleichstests angezeigt.
Bestandene Tests beweisen keine vollständige Korrektheit.
Die fachliche Qualität des Modellfeedbacks muss geprüft werden.
Beide Demo-Versionen wurden live geprüft; der aktuelle Prompt zuletzt nur mit der mittleren Abgabe.

Der Agent läuft mit `invoke()`. Tokenzahlen werden aus dem fertigen Verlauf
gezählt. Bei einem Abbruch gibt es eine Fehlermeldung, keine Teilmesswerte.
Einrichtungsprüfung: `python DEMO/einrichten.py --check`.


## Festgelegter Vorführungsstand vom 2026-11-03

Aktuellen Code und Prompt für die Vorbereitung beibehalten. Die letzte Probe
mit diesem Prompt betraf nur die mittlere Abgabe: In beiden Versionen wurde
`return a` als Ursache für 4.0 statt 5.0 erkannt. Die Antwort schreibt jedoch
unnötig `math.sqrt` als Ersatz vor; `** 0.5` ist ebenso möglich.
Gut und schlecht wurden mit früheren Prompts live geprüft, mit dem aktuellen
Prompt noch nicht erneut. Es gab dabei auch falsche Modellbewertungen.
Die Testzahlen kommen deshalb sichtbar aus dem Testprogramm.

## Ablauf der Vorführung

1. Aufgabenstellung in `material/aufgabe_06.txt` zeigen: Flussbreite,
   Bootsgeschwindigkeit und Strömung ergeben die zurückgelegte Strecke.
2. `abgaben/` zeigen: gute Lösung unverändert, mittel mit `return a`,
   schlecht mit falschen Operationen in den Hilfsfunktionen.
3. `vergleichstests.json` zeigen. Diese drei Tests samt Sollwerten sind
   vorbereitet; das Modell erzeugt sie in der Demo nicht.
4. `demo.py` in VS Code mit dem passenden Python-Interpreter starten.
   Abgabe `2` und Modus `1` wählen. Das löst einen echten KI:CONNECT-Lauf aus.
5. Ablauf erklären: DeepAgents ruft das Testwerkzeug auf. Das Werkzeug liefert
   tatsächliche Ergebnisse. Qwen erhält diese und formuliert eine Erklärung.
   Erwarteter Befund: zwei Tests bestanden, einmal 4.0 statt 5.0.
6. Rückmeldung am Code prüfen. Falls Zeit bleibt, gut (`1`) und schlecht (`3`)
   separat oder alle (`a`) zeigen. Neue Antworten können von früheren abweichen.
7. Modell, Tokenverbrauch und Laufzeit zeigen. Drei Testfälle und eine kurze
   Modellantwort sind keine vollständige Korrektur oder Note.

Vorher die Pakete und KI:CONNECT-Verbindung auf dem Vorführrechner einrichten.
Ohne API Modus `3` wählen und ausdrücklich sagen, dass frühere Containerläufe
gezeigt werden. Modus `2` führt die Tests frisch ohne Modell aus.
Die Reserve unter `gespeichert/` stammt von früheren Versuchen und nicht vom
aktuellen Prompt. Neue Live-Ergebnisse bleiben getrennt unter `ergebnisse/`.

## Was sich daran erklären lässt

Der vorhandene Harness ist DeepAgents; unser Code stellt die Aufgabe bereit,
führt Tests aus und zeigt das Ergebnis. Das Modell repariert die Abgabe nicht.
Die Musterlösung im Materialordner dient hier nur der Einsicht.
Der bisherige Ladeablauf aus `src` wird noch nicht genutzt. Die Demo zeigt
somit den Harness mit Testwerkzeug an einer Aufgabe, keinen ganzen Blattlauf.

Offen bleibt die zuverlässige Erklärung durch das Modell. Frühere Antworten
beanstandeten vorhandene Kommentare, erfanden einen Importfehler, übersahen
einen Fehler oder widersprachen der tatsächlichen Testzahl. Diese Befunde
gehören zur Untersuchung und werden durch die Vorführung nicht widerlegt.


Ausführlicher Ablauf mit Sprechtexten und Dateiquellen: [Walkthrough](../../dokumentation/demo_walkthrough.md).


## Nachgetragener Prüfstand (2026-11-05)

Die lokale Abschlussprobe aller drei Varianten mit aktuellem Prompt ist inzwischen
belegt (3/3, 2/3, 0/3, passende Kernbefunde). Der integrierte mittlere Livefall
ist ebenfalls belegt (2/3, 4767 Tokens, 1.98 s). Frühere Angaben, diese Proben
stünden noch aus, sind historisch überholt. Das beweist keine allgemeine
Zuverlässigkeit oder einen integrierten guten/schlechten Livefall.
Aktueller Einstieg: [Arbeitskontext](../../dokumentation/arbeitskontext.md).


## Gemeinsame Projektbasis (2026-11-08)

Die Tutor-Umgebung wurde inzwischen über pyproject.toml und uv.lock mit
DeepAgents 0.7.32 abgeglichen. Die ursprünglichen Paketpins dieser Demo-Dateien
wurden dabei nicht ersetzt. DEMO_integriert lädt nun direkt im gestarteten
Projektinterpreter über src, statt einen zweiten Interpreter zum Laden zu starten.
Benötigte Imports und alle drei Eingabevarianten wurden nach Paketabgleich geprüft.
Ein neuer Modell-/Werkzeuglauf mit diesem endgültigen neuen Paketstand wurde nicht
durchgeführt. Ältere Live-Ergebnisse bleiben historische Nachweise ihrer Bedingungen.
Der reguläre DeepAgents-Baustein unter src ist erst der nächste Vorschlag.
