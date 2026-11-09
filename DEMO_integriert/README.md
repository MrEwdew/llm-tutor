# Demo mit vorhandener Eingabeaufbereitung

Stand: 2026-11-08.

Diese Variante verbindet den vorhandenen src-Ladeablauf mit dem DeepAgents-Ablauf
aus DEMO_lokal. Sie kopiert weder Harness noch Testprogramm. Der Nachbarordner
DEMO_lokal mit seinen Abgaben, Tests und Prompt wird weiterhin benötigt.

## Einrichtung und Start

Die geprüfte gemeinsame Umgebung wird über pyproject.toml und uv.lock beschrieben.
Für den Projekt- und Notebook-Bestand lautet der zuvor geprüfte Abgleich:

```text
uv sync --locked --inexact --group notebooks
uv pip check --python .\.venv\Scripts\python.exe
```

Das sind Installations-/Prüfbefehle, keine automatisch beim Demo-Start ausgeführten
Schritte. Installation vor der Vorführung abschließen. --inexact erhält zusätzliche
Pakete, schützt aber nicht deren Abhängigkeiten vor den Vorgaben der Lockdatei.
Notebook-Gruppe deklariert Transformers; der reine Demoablauf importiert es nicht.
Eine vollständige frische Einrichtung auf anderem Rechner ist noch nicht geprüft.

Mit dem passenden Projektinterpreter im Ordner llm-tutor starten:

```text
python DEMO_integriert/demo.py
```

Menü:

- 1: Live-Korrektur mit KI:CONNECT und lokaler Abgabeausführung.
- 2: Eingabe laden und die drei Tests lokal ausführen, ohne Modell.
- 3: Nur Eingabe aufbereiten und anzeigen, ohne Modell und Abgabeausführung.

Zuerst wird die Abgabe gewählt (1=gut, 2=mittel, 3=schlecht, a=alle), dann der Modus.
Modus 3 bedeutet bei DEMO/DEMO_lokal dagegen alte Ergebnisse anzeigen.

## Dateien und Ablauf

- demo.py: Menü, direkter load_input-Aufruf, Weitergabe an lokalen Agenten/Testadapter,
  Anzeige und Speicherung neuer Live-Ergebnisse.
- eingabe.py: Importiert load_exercise_submission und prepare_evaluation_input aus
  src/common.py; liefert die vorbereitete Eingabe und den unveränderten Code.
- Der ausführbare JSON-Einstieg am Ende von eingabe.py bleibt vorhanden, wird vom
  Demo-Menü aber nicht mehr über einen zusätzlichen Prozess aufgerufen.

Der Eingabelader liest das echte Blatt-1-PDF und die ursprüngliche Blatt-1-ZIP aus
dem Projekt. Eine temporäre ZIP-Kopie ersetzt nur Aufgabe 6 durch die bekannte
gewählte Variante aus DEMO_lokal; das Original bleibt unverändert. Der vorhandene
src-Lader teilt alle sechs Aufgaben auf, ordnet Dateien zu, erfasst Funktionen/
Syntaxbefunde und lädt die Professor-Referenz zu Aufgabe 6 mit Check-Fundstellen.
prepare_evaluation_input führt Einleitung, Aufgabe, Abschlussvorgaben und Abgabe
zusammen. Referenz bleibt separat, wird weder ausgeführt noch ans Modell gesendet.

Der frühere zusätzliche Interpreter mit festem .venv/Scripts/python.exe-Pfad,
prepare_input und JSON-Pipe wurde entfernt. Alle Ladefunktionen laufen jetzt im
selben gestarteten Python-Prozess. common.py lädt den alten Chatbot nicht mehr
mit, solange die Praktomat-Auswertung nicht aufgerufen wird. PyPDFLoader und
HumanMessage bleiben weiterhin LangChain-Bausteine. Der alte Bewertungsgraph
wird vom integrierten Menü nicht gestartet.

correct_submission aus DEMO_lokal erhält Code und vorbereiteten Text. Dessen
Testwerkzeug verwendet weiterhin einen separaten Python-Prozess mit Zeitlimit.
Dieser Prozess ist von der nun entfallenen Prozessgrenze zum bloßen Laden zu
unterscheiden. Die lokale Ausführung ist keine Rechte-/Dateisystemisolation und
bleibt für die bekannten Demo-Abgaben vorgesehen. Die drei Vergleichstests
werden weiterhin fest übergeben, nicht aus der Referenz automatisch generiert.

## Prüfstand und Grenzen

Vor dem Paketumbau wurde ein integrierter mittlerer Livefall beobachtet: 2/3,
4767 Tokens, 1.98 s und richtige return-a-Diagnose; unnötige math.sqrt-Ersatzzeile
bleibt eine Feedbackschwäche. Dies ist kein neuer Live-Nachweis unter dem nun
geänderten Paketstand oder nach Entfernung des zusätzlichen Ladeprozesses.

Am 2026-11-08 durch Nutzer geprüft: gemeinsamer Import-/Ladeweg für alle drei
Varianten, sechs Aufgaben, drei Funktionsköpfe, fünf Referenzchecks, Code unverändert
und vollständig in Nachricht. Direkter Menüeinstieg mittel/3 vor abschließendem
Paket-Sync erfolgreich. Nach Sync Imports und alle drei direkten Ladefälle erneut
erfolgreich; Paketprüfung 196 Distributionen ohne deklarierte Konflikte.
Keine neue Modellanfrage, keine Abgabeausführung in diesen Prüfungen.

PDF-Diagramm bleibt bei reiner Textextraktion aus; Formeln können auseinandergezogen
werden. Allgemeiner Java-/ganzer Blatt-Bewertungsweg ist nicht damit belegt.
Neue Live-Ergebnisse landen hier unter ergebnisse, frühere Ergebnisse bleiben erhalten.
Nächster Vorschlag ist ein regulärer src-Agentenbaustein mit übergebenen Eingaben,
nicht weiterer Ausbau einer eigenen Harness-Schleife.

Ausführlicher Vorführablauf und Quellen:
[Walkthrough](../../dokumentation/demo_walkthrough.md).
Aktueller Einstieg: [Arbeitskontext](../../dokumentation/arbeitskontext.md).


## Agentenaufbau unter src (2026-11-08)

Der lokale Demo-Aufrufer verwendet jetzt src/correction_agent.py. Die integrierte
Demo nutzt denselben Aufrufer. Aufbau/Middleware laufen damit nicht mehr doppelt
im lokalen Demo-Code. Testtool ist mittels @tool vorbereitet; sein Cache bleibt
im Demo-Adapter. Harness mit lokalem Testmodell und Demo-Anbindung mit simuliertem
Agenten/Adapter erfolgreich geprüft, aber kein neuer Live-Lauf nach diesem Umbau.

Die gemessene Laufzeit umfasst nun auch den Agentenaufbau in run_correction;
frühere Messwerte umfassten nur invoke nach dem Aufbau. Ergebnisaufbereitung und
Modellkonfiguration sind die nächsten vorgeschlagenen, noch offenen Schritte.


## Ergebnis und Modellzugang gemeinsam (2026-11-08)

Der lokale Demo-Aufrufer verwendet prepare_correction_result aus correction_agent.py
und get_llm aus llm.py. Damit ebenfalls beim integrierten Aufruf aktiv. Demo-Werte
Qwen/Temperatur 0/Timeout 60/Wiederholungen 0/Ausgabelimit 700 bleiben erhalten.
Projektdefaults im alten Chatbot bleiben über dieselbe Modellfunktion verfügbar.
Ergebnisfälle und Modell-/Demoübergaben mit künstlichen Daten und ersetzten
Konstruktor-/Agent-/Testkomponenten geprüft; kein neuer echter API-/Abgabelauf.
Nächster Vorschlag betrifft den noch festen Boot-Testadapter, nicht eine bereits
umgesetzte allgemeine Testausführung.
