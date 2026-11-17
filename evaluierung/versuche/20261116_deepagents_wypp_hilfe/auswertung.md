# DeepAgents mit Importvorgabe und WYPP-Hilfe

Datum: 2026-11-16. Qwen_3_30B_A3B_Instruct_2507, genau ein Lauf. Grenzen: sechs Modellaufrufe und 120 Sekunden. Keine Tutor-Funktionen aus src verwendet.

## Anlass und Unterstuetzung

Im vorherigen Versuch gelangen die Importe, aber check wurde falsch verwendet. Zum unveraenderten Auftrag mit konkreten Importzeilen kam deshalb die Erklaerung check(istwert, sollwert), genau zwei Argumente, hinzu. Keine konkreten Testeingaben oder Sollwerte vorgegeben. Die beiden synthetischen fehlerhaften Originaldateien blieben dieselben und schreibgeschuetzt.

## Ablauf und Nachweis

Der Agent listete die Dateien auf, las beide und schrieb eine gemeinsame Testdatei. Er uebernahm die Importhilfe und erzeugte sechs eigene WYPP-checks mit korrekten Sollwerten: quadrat(3)=9, quadrat(-2)=4, quadrat(0)=0, positiv(5)=True, positiv(-1)=False, positiv(0)=False. Kommentare begruendeten die Sollwerte aus der Spezifikation.

Anschliessend startete er die Testdatei mit Python. Die echte Werkzeugausgabe meldete drei fehlschlagende Vergleiche: quadrat(3) lieferte 6 statt 9; quadrat(-2) lieferte -4 statt 4; positiv(0) lieferte True statt False. Der Prozess endete mit Exitcode 0: WYPP meldet diese Vergleichsfehler als Ausgabe, ohne hier den Prozess fehlschlagen zu lassen. Exitcode allein waere daher kein geeignetes Bestehenskriterium.

Der sechste Modellaufruf lieferte fachliches Abschlussfeedback. Beide Funktionsfehler wurden erkannt: Addition statt Quadrat und >= statt >. Eine Erklaerung war unpraezise: Der negative Quadratfall wurde als falsche Multiplikation beschrieben, obwohl der Originalcode addiert. Die beobachteten Ist- und Sollwerte wurden korrekt wiedergegeben. Keine Ersatzloesung ausgegeben.

## Einordnung

Unter dieser expliziten Unterstuetzung gelang erstmals in dieser DeepAgents-Versuchsreihe der gesamte kleine Ablauf aus selbst gewaehlten Tests, Ausfuehrung gegen Originaldateien und darauf bezogenem Feedback. Das ist kein Nachweis vollstaendiger Selbststaendigkeit: Imports und WYPP-Schnittstelle waren vorgegeben. Keine korrekte Gegenprobe unter genau diesen Bedingungen und keine echte studentische Abgabe in diesem Lauf. Ein einzelner erfolgreicher Versuch belegt keine allgemeine Zuverlaessigkeit.

Dauer: 5.887 Sekunden. Gemeldete Tokens: 22377 aus sechs Modellantworten. Originaldateien erneut per Hash unveraendert bestaetigt. Keine Wiederholung gestartet. Rohverlauf, Prompt, Skriptstand, erzeugte Tests und Antwort sind im Versuchsordner erhalten.
