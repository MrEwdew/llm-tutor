# Echte Abgabe mit ausdruecklichem Ausfuehrungsnachweis

Datum: 2026-11-16. Genau ein DeepAgents-Lauf mit Qwen_3_30B_A3B_Instruct_2507, derselben anonymisierten Blatt-2-Abgabe und demselben Aufgaben-PDF wie zuvor. Keine src-Bausteine. Keine aufgabenspezifischen Imports, Testfaelle oder Sollwerte vorgegeben.

## Anlass

Der vorherige Agentenlauf endete freiwillig nach dem Lesen aller Dateien und behauptete unzutreffend eine Ausfuehrung. Modelllimit war zehn, beobachtet wurden sieben Starts einschliesslich eines fehlgeschlagenen Requests; somit war der vorige Abschluss nicht durch das Modelllimit erzwungen. Ein technischer PDF-Fehler trat vorher auf, wurde aber ueber Python/pypdf ueberwunden. Ob und wie dieser Fehler die spaetere Entscheidung beeinflusste, ist nicht nachweisbar.

Zum vorhandenen Prompt kam nur eine ausdrueckliche Nachweispflicht: eigene Tests vor Abschluss schreiben und starten, je Aufgabe Befehl und beobachtete Ausgabe nennen, blosses Lesen nicht als Ausfuehrung ausgeben, ungetestete Teile offen kennzeichnen. Keine technische Pflicht zum Werkzeugabruf eingebaut.

## Verlauf

ZIP entpackt, Verzeichnisse mehrfach einzeln aufgelistet. PDF entgegen Hinweis direkt gelesen; naechster API-Aufruf scheiterte am nicht unterstuetzten Inhaltstyp file. Innerhalb des Harness-Laufs erfolgte anschliessend eine Fortsetzung mit erfolgreicher Python/pypdf-Textextraktion. Danach nur Aufgabe1.py gelesen.

Abbruch durch GraphRecursionError: recursion_limit=30. Acht Modellstarts und sieben erfolgreiche Antworten; die zehn erlaubten Starts wurden nicht ausgeschoepft. Kein eigener Testcode, kein Start von Abgabecode und kein fachliches Abschlussfeedback. Kein zweiter Hostlauf gestartet.

## Einordnung

Dieser Lauf ist ein technischer Abbruch und kein verwertbarer Nachweis fuer Wirkung oder Wirkungslosigkeit der Prompt-Ergaenzung. Das interne Graphlimit begrenzt Graphschritte, nicht Modellaufrufe, und kann daher vorher greifen. Das unveraendert uebernommene Limit von 30 war fuer diesen beobachteten Verlauf zu klein. Dies ist eine Beschraenkung der Versuchssteuerung, nicht als fachliches Versagen der Abgabe oder des Modells zu zaehlen.

Ein naechster Vergleich muesste das interne Graphlimit ausreichend hoeher setzen, waehrend zehn Modellstarts und 120 Sekunden die vereinbarten eigentlichen Grenzen beibehalten. Das waere ein eigener weiterer Lauf und wurde hier nicht automatisch gestartet. Fuer einen fairen Promptvergleich sind ungleiche Abbrueche und die weiterhin variable Werkzeugwahl zu beruecksichtigen.

Dauer: 7.547 Sekunden. Gemeldete Tokens: 29027 aus 7 erfolgreichen Antworten. Verbrauch des fehlgeschlagenen API-Aufrufs unbekannt. Eingangs-PDF/ZIP und entpackte Codebytes erneut unveraendert bestaetigt. Rohverlauf und Fehlerdatei gespeichert. Keine falsche Ausfuehrungsbehauptung in diesem Lauf bewertbar, da kein Abschlussfeedback vorliegt.
