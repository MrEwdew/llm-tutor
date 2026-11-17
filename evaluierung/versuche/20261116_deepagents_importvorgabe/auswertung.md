# DeepAgents mit konkreter Importvorgabe

Datum: 2026-11-16. Ein unterstuetzter Einzelversuch nach dem erfolglosen allgemeinen Importhinweis.

## Bedingungen

Qwen_3_30B_A3B_Instruct_2507 mit DeepAgents, maximal sechs Modellaufrufe und 120 Sekunden. Dieselben zwei synthetischen fehlerhaften Originaldateien wie zuvor, schreibgeschuetzt eingebunden. Zusaetzlich wurden konkrete Zeilen fuer sys.path, die beiden Funktionsimporte und den WYPP-Import vorgegeben. Keine Testeingaben, Sollwerte oder Ersatzloesungen vorgegeben. Keine Funktionen aus src verwendet.

## Ablauf

1. Materialordner aufgelistet.
2. quadrat-Datei gelesen.
3. positiv-Datei gelesen.
4. Eine gemeinsame Testdatei mit den vorgegebenen Importen und sechs selbst gewaehlten Tests geschrieben. Die Sollwerte waren fachlich korrekt: quadrat(4)=16, quadrat(-3)=9, quadrat(0)=0; positiv(5)=True, positiv(0)=False, positiv(-2)=False.
5. Testdatei tatsaechlich mit Python ausgefuehrt. Die Importe gelangen. Beim ersten Ausdruck wurde quadrat(4) aus der Originaldatei aufgerufen. Anschliessend scheiterte check am zusaetzlichen dritten Argument: TypeError: check() takes 2 positional arguments but 3 were given. Es fand kein gueltiger WYPP-Vergleich statt; die folgenden Tests wurden nicht erreicht.
6. Agent bearbeitete seine Testdatei. Er ersetzte beispielsweise check(quadrat(4), 16, Beschreibung) durch check(quadrat(4) == 16, Beschreibung). Das entspricht weiterhin nicht dem vorgesehenen Vergleich check(Istwert, Sollwert): Ein boolescher Vergleich wird gegen einen Beschreibungstext gestellt. Diese Einschaetzung beruht auf Lesen des erzeugten Codes, nicht auf erneuter Ausfuehrung.

Danach beendete das native Modelllimit den Ablauf. Die bearbeitete Testdatei wurde nicht erneut ausgefuehrt. Kein fachliches Abschlussfeedback vorhanden.

## Ergebnis und Grenzen

Die konkrete Importvorgabe loeste den bisherigen Einbindungsfehler. Testauswahl und Sollwerte waren sinnvoll, die Verwendung der WYPP-Schnittstelle jedoch fehlerhaft. Der Lauf belegt einen echten Aufruf der Originalfunktion, aber keine abgeschlossene Testauswertung oder Korrektur. Originaldateien per Hash unveraendert bestaetigt. Exitcode 0 des aeusseren Harness-Prozesses bedeutet keinen erfolgreichen Korrekturlauf.

Dauer: 10.98 Sekunden. Gemeldeter Verbrauch: 22207 Tokens aus sechs Modellantworten. Ein Lauf; keine Aussage ueber allgemeine Zuverlaessigkeit oder Verhalten mit groesserem Budget. Keine automatische Wiederholung.
