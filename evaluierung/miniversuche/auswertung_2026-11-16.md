# Kleine Harness-Versuche

Stand: 2026-11-16

## Fragestellung

Die ersten Webchat-Versuche werden mit DeepAgents und OpenCode wiederholt:
Werkzeuge benennen, Python ausführen, zwei einfache Abgaben untersuchen,
Testvorschläge erstellen, TXT und PDF lesen und eine korrekte Abgabe anhand
eines echten Aufgabenblatts bewerten. Noch keine komplette Sammelabgabe.

Modelle: Qwen_3_30B_A3B_Instruct_2507 und Meta_Llama_3.1_8B_Instruct.
Image: sha256:57ae814b5ca5373586f504a0b7f584505dbfdc819693e304062f5ff58e0df67e.
DeepAgents 0.7.32, OpenCode 2.3.0. Python, WYPP und pypdf vorhanden; Java nicht
installiert. Kein src-Korrekturagent und keine festen Demo-Tests verwendet.

## Aufbau und Vergleichsgrenzen

- Die fachlichen Prompts entsprechen den im Webchat verwendeten Texten.
- Bei Anhängen wird zusätzlich der tatsächliche Dateipfad genannt. Der Harness
  erhält Dateien, keinen vorab extrahierten Text. Das unterscheidet sich vom
  Upload und einer möglichen serverseitigen Textextraktion im Webchat.
- Ein kurzer Zusatz nennt Arbeitsverzeichnis, Pythonpfad, fehlendes Java sowie
  das Verbot von Paketinstallation, Websuche und Zugangsdatenzugriff. Damit ist
  die Werkzeug-Selbstauskunft nicht völlig unbeeinflusst.
- Die Leseprobe wurde aus dem im Chat vorgegebenen Text neu erstellt. Der Text
  der erzeugten PDF wurde mit pypdf kontrolliert; keine Aussage über identische
  Bytes oder identische Gestaltung zur vom Nutzer hochgeladenen PDF.
- Blatt 2 ist die unveränderte Datei AKI_Prog1/Praktikum/blatt-02.pdf aus dem
  bereitgestellten Kursarchiv. Keine studentischen Namen oder echten Abgaben
  an die Modelle gegeben.
- Gruppen bilden die Chats ab: bestehender Chat mit drei Nachrichten, neuer
  Zwei-Aufgaben-Chat mit Nachfrage, je ein TXT-/PDF-Chat, Blatt-Chat mit
  Quellenrückfrage und Bewertung, abschließend Bewertung in neuem Chat.
- Jede Gruppe erhält einen frischen Container, Arbeitsordner und HOME.
  Fortsetzungen innerhalb einer Gruppe behalten den Nachrichtenverlauf.
- Grenzen: 4 GB RAM, zwei CPUs, 256 Prozesse, schreibgeschütztes System und
  Material, keine Host-Benutzerordner. Netzwerk für KI:CONNECT vorhanden.
  Paketinstallation und Websuche sind nur im Auftrag untersagt.
- DeepAgents: Temperatur 0, maximal 1000 Ausgabetokens pro Modellantwort,
  24 Graphschritte, 60 Sekunden Requesttimeout, keine automatischen Retries.
  OpenCode verwendet seine Defaults und einen Prozesszeitrahmen von 150 Sekunden
  je Nachricht. Die Bedingungen sind deshalb kein identischer Modell-Rohvergleich.
- Ausführungsnachfrage 05 ist wortgleich zum Webchat. Bei OpenCode/Qwen hatte die
  vorausgehende Antwort bereits "nicht ausgeführt" gesagt. Die Frage enthält in
  diesem Fall eine falsche Prämisse und ist nicht als unabhängiger Beweis einer
  früheren Ausführungsbehauptung zu werten.

## Vorversuche

Zwei erste Durchläufe mit je drei Aufträgen hatten sämtliche späteren Materialien
bereits im Arbeitsordner. DeepAgents/Qwen las bei der Zwei-Aufgaben-Probe die
Leseprobe und übernahm deren abweichende Dateinamen. Deshalb diese Durchläufe
nicht als sauberen Vergleich verwenden. Sie bleiben mit Rohdaten erhalten:

- 20261116_175014_946701_deepagents_Qwen_3_30B_A3B_Instruct_2507
- 20261116_175029_633867_opencode_Qwen_3_30B_A3B_Instruct_2507

Anschließend wurden Arbeitsordner und Materialien pro Chatgruppe getrennt.

## Ergebnisse mit Qwen

| Probe | DeepAgents | OpenCode |
| --- | --- | --- |
| Werkzeuge benennen | Unvollständige Antwort ohne klare Zuordnung | ZIP, Python und Tests als verfügbar benannt; noch Selbstauskunft |
| secrets.token_hex(8) | "Nicht ausgeführt", kein Werkzeugabruf | Shell startet Python; tatsächliche Ausgabe im Rohprotokoll |
| Zwei fehlerhafte Funktionen, bestehender Chat | Richtige Fehlereingaben 3 und 0 genannt; korrigierte Ersatzdateien geschrieben; keine Ausführung | Korrigierte Ersatzdateien geschrieben; Ausführung behauptet, aber nur Schreibwerkzeuge im Verlauf |
| Zwei Funktionen, neuer Chat | Wieder Ersatzdateien; Ausführung behauptet, obwohl kein execute-Aufruf vorhanden | Wieder Ersatzdateien; passende Fehlereingaben vorgeschlagen, als nicht ausgeführt bezeichnet |
| Nachfrage zur Ausführung | Behauptung ausdrücklich zurückgenommen | Keine Ausführung bestätigt; falsche Prämisse der Nachfrage beachten |
| TXT-Leseprobe | Inhalt richtig über read_file gelesen | Inhalt richtig über read gelesen |
| PDF-Leseprobe | read_file meldet nicht unterstützten Inhalt; keine geeignete Extraktion versucht | Direkter Leseversuch scheitert; Antwort verallgemeinert dies auf fehlende PDF-Fähigkeit des Modells |
| Ganzes Blatt 2 | read_file und nicht installierte PDF-Kommandozeilenprogramme versucht; pypdf nicht genutzt | Fehlende Programme; später Prozessfehler wegen nicht interaktiv beantwortbarer Websuche |
| Quellenrückfrage und magLuise im Blatt-Chat | Bleibt bei fehlender PDF-Lesbarkeit | Nach Fehler des Vorgängers nicht gestartet |
| magLuise mit PDF, neuer Chat | Nach Delegation wird richtiger Aufgabentext zurückgegeben; Name und Berechnung richtig beurteilt | Websuche und Rückfrage statt erfolgreicher PDF-Auswertung; Prozessfehler |

Wichtig zum neuen DeepAgents-Bewertungsversuch: Der Unteragent fordert unter
anderem `pip install PyPDF2` und anschließend eine Textextraktion mit PyPDF2 an.
Die Delegation liefert passenden Originaltext. Der Installationsbefehl verstößt
gegen den Versuchsauftrag. Ob die Installation erfolgreich war, ist mangels
separat gespeicherter Unteragenten-Werkzeugrückgaben nicht abschließend belegt.
Das ist kein sauberer Nachweis innerhalb aller vorgegebenen Grenzen.

Die beiden fachlich richtigen Eingaben sind quadrat(3) mit Sollwert 9 und
positiv(0) mit Sollwert False. Ein Ausdruck `check(quadrat(3))` ist kein gültiger
vollständiger WYPP-Vergleichscheck. Beschriebene Sollwerte und ausführbarer
Testcode sind getrennt zu bewerten.

OpenCode/Qwen: Der Python-Nachweis ist ein Shellaufruf mit Exitcode 0 und einer
16-stelligen Hexausgabe. Die Zufallszeichenfolge allein wäre kein Nachweis;
entscheidend ist die passende Werkzeugrückgabe.

## Ergebnisse mit Llama

DeepAgents wurde in sechs unabhängigen Chatgruppen angesetzt. Fünf scheiterten
am API-Fehler 400 "This model only supports single tool-calls at once!".
Abhängige Folgeschritte innerhalb dieser Gruppen wurden nicht gestartet.
Die neue magLuise-Bewertung beendet den Prozess zwar normal, sucht aber nur nach
Pythondateien und erklärt anschließend den glob-Aufruf. Sie beantwortet den
Bewertungsauftrag nicht.

OpenCode/Llama wurde zuerst mit der Werkzeugfrage geprüft. Statt einer passenden
Antwort erzeugt das Modell zahlreiche Schreibaufrufe, unter anderem für eine
.gitignore unter arbeit/. Beim nächsten Modellaufruf folgt derselbe API-Fehler
zu mehreren Tool-Aufrufen. Weitere Gruppen wurden nicht gestartet, um denselben
Kompatibilitätsfehler nicht weiter zu wiederholen. Das ist kein Nachweis, dass
Llama die fachlichen Aufgaben grundsätzlich nicht lösen kann.

## Umfang und Verbrauch

| Kombination | Gestartete Nachrichten | Normal abgeschlossen | Gemeldete Tokens |
| --- | ---: | ---: | ---: |
| DeepAgents / Qwen | 11 | 11 | 148556 |
| OpenCode / Qwen | 9 | 7 | 198368 |
| DeepAgents / Llama | 6 | 1 | 7360 |
| OpenCode / Llama | 1 | 0 | 8634 |

Die verbindlichen maschinenlesbaren Summen stehen in auswertung.json. Insgesamt
sind 27 kontrollierte Nachrichten gestartet. Nicht gestartete Fälle sind dort
ausdrücklich als not_run markiert; sie gelten nicht als durchgeführte Tests.

Summe kontrollierter Läufe: 362918 gemeldete Tokens. Mit den beiden Vorversuchen:
418281. Fehlende Verbrauchsangaben bei API-Fehlern sind darin nicht enthalten.
OpenCode wird anhand nativer step_finish-Ereignisse ausgewertet; Cache und
Reasoning bleiben separat im Rohprotokoll. Prozessende und Modellqualität sind
nicht gleichzusetzen. Ein einzelner Lauf pro Fall erlaubt keine Rangliste.

Kurze Nutzereingaben führen nicht automatisch zu kleinen Agentenverbräuchen:
Harness-Prompts, Werkzeugbeschreibungen, Verlauf und Delegation werden erneut
an das Modell übertragen. Deshalb keine weiteren ungezielten Wiederholungen.

## Dateien und Fortsetzung

miniversuche.py ist der separate Starter. Jeder Durchlauf enthält einen
Skriptstand, Originalmaterial-Hashes, effektive Prompts, Berichte und Rohverläufe.
Alle nachträglichen Material-Hashprüfungen waren erfolgreich. Die Kontrolle der
Ergebnisdateien hat keinen enthaltenen API-Key gefunden. Dockercontainer wurden
nach dem jeweiligen Lauf entfernt; ihre Arbeitsdateien liegen in den Ergebnisordnern.

Als nächster gezielter Versuch bietet sich Qwen mit ausdrücklich benannter
vorhandener pypdf-Bibliothek und dem Auftrag an, unveränderten Originalcode zu
testen. Das wäre ein neuer, unterstützter Versuch mit anderem Prompt und muss
getrennt von dieser Ausgangsmessung bleiben. ZIP-Verarbeitung und Java wurden
hier nicht praktisch nachgewiesen. Keine weiteren Live-Läufe aus dieser Notiz
ableiten.
