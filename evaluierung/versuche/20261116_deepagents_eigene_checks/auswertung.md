# DeepAgents: eigene Tests und korrekte Gegenprobe

Datum: 2026-11-16. Modell: Qwen_3_30B_A3B_Instruct_2507.

## Anlass und Aufbau

Nach dem OpenCode-Versuch mit selbst erzeugten Tests wurde derselbe Auftrag mit DeepAgents untersucht. Anschliessend folgte genau eine Gegenprobe mit funktional korrekten Implementierungen. Damit sollte sichtbar werden, ob der Ablauf auch korrekte Abgaben sinnvoll pruefen kann.

Beide Laeufe erhielten dieselben Anforderungen und denselben Prompt. Nur die beiden Operatoren in den Eingabefunktionen unterschieden sich: fehlerhaft x+x und x>=0, korrekt x*x und x>0. Es waren synthetische Beispiele, keine echten studentischen Abgaben. Die sechs Modellschritte und 120 Sekunden waren vorab begrenzt. Der Harness erhielt Dateisystem- und Shellwerkzeuge im Container; keine Tutor-Funktionen aus src, keine vorbereiteten Tests und keine fachliche Zuordnung durch unseren Code.

## Beobachtungen

In beiden Laeufen listete der Agent die Dateien auf, las beide und schrieb zwei Testdateien. Die gewaehlten Sollwerte waren fachlich passend. Insbesondere negative Zahlen beim Quadrat und die Null bei positiv eignen sich zur Unterscheidung der Implementierungen. Statt der verlangten WYPP-checks verwendete er assert.

In beiden erzeugten Testdateien fehlten die Importe der Abgabefunktionen. Der Agent startete tatsaechlich Python. Bereits der erste Aufruf von quadrat scheiterte mit NameError. Deshalb wurde keine Originalfunktion ausgefuehrt. In der Gegenprobe verhinderte die Verknuepfung mit && zudem den Start der zweiten Testdatei.

Nach sechs Modellaufrufen beendete das native Modelllimit den Ablauf. Es entstand kein fachliches Abschlussfeedback. Der erfolgreiche Exitcode des aeusseren Prozesses ist daher kein erfolgreicher Korrekturlauf. Die Originaldateien blieben in beiden Laeufen unveraendert; Hashwerte wurden erneut kontrolliert.

| Eingabe | Dauer | Gemeldete Tokens | Ergebnis |
| --- | ---: | ---: | --- |
| Fehlerhafte Funktionen | 7.676 s | 20650 | Generierter Test scheitert vor Funktionsaufruf |
| Korrekte Funktionen | 8.887 s | 20549 | Generierter Test scheitert vor Funktionsaufruf |

## Einordnung

Dateizugriff, Testgenerierung und ein echter Interpreterstart sind belegt. Eine funktionierende Verbindung zwischen den erzeugten Tests und den Originaldateien ist unter diesen Bedingungen nicht belegt. Der Infrastrukturfehler darf weder als Fehler der Abgabe noch als erkannter fachlicher Fehler gezaehlt werden. Ohne Abschlussbewertung erlaubt die korrekte Gegenprobe auch keine Aussage zur Rate falscher Beanstandungen.

Dies sind je ein Lauf mit engem Budget, kein allgemeiner Unfaehigkeitsnachweis des Modells oder Harnesses. Eine weitere Probe koennte den Importpfad als technische Hilfe bereitstellen; sie waere als unterstuetzte Bedingung getrennt zu messen. Es erfolgte keine automatische Korrekturrunde und kein weiterer Modelllauf.

## Nachweise

- Fehlerhafter Fall: deepagents/auftrag.txt, bericht.json, ausgabe/verlauf.jsonl, ausgabe/nachrichten.json und arbeitsordner/arbeit/.
- Korrekte Gegenprobe: ../20261116_deepagents_korrekte_abgabe/ mit derselben Struktur.
- Die Startskripte und ihre Snapshots halten die Ausfuehrungsbedingungen fest.
