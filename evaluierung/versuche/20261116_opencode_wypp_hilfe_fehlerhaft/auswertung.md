# OpenCode: fehlerhafte Eingabe mit Import- und WYPP-Hilfe

Datum: 2026-11-16. Ein Lauf, Qwen_3_30B_A3B_Instruct_2507, OpenCode 2.3.0. Promptgleichheit mit dem entsprechenden DeepAgents-Versuch geprueft. Eingabetexte gleich; Zeilenenden koennen zwischen den Kopien abweichen. Originaldateien per Hash unveraendert bestaetigt. Kein src verwendet.

Importzeilen, Suchpfad und check(istwert, sollwert) waren vorgegeben. Keine konkreten Testeingaben oder Sollwerte. Maximal sechs native Modellschritte und 120 Sekunden. Der Agent las beide Dateien, erzeugte sechs fachlich korrekte WYPP-checks und fuehrte die Testdatei gegen die Originalfunktionen aus.

Ergebnis: Drei WYPP-Fehlermeldungen: quadrat(3) ergibt 6 statt 9, quadrat(-2) ergibt -4 statt 4, positiv(0) ergibt True statt False. Beide Funktionsfehler im Feedback erkannt. Die Formulierung falsche Multiplikation beim negativen Fall ist unpraezise, da der Code addiert.

Bei WYPP bedeutet Exitcode 0 allein nicht, dass alle Vergleiche bestehen: Auch die fehlerhafte Variante endete mit 0 und meldete Fehler im Ausgabetext. Die Werkzeugausgabe und der erzeugte Testcode wurden deshalb gemeinsam beurteilt.

Dauer: 9.571 Sekunden. Gemeldete Tokens: 22690. Native Modellschritte: 4. Keine Wiederholung gestartet. Ein unterstuetzter synthetischer Einzelversuch ist kein Nachweis allgemeiner Zuverlaessigkeit oder vollstaendiger Selbststaendigkeit. PDF, ZIP und echte Abgaben waren hier nicht beteiligt. Rohverlauf, Prompt, Skript, Testdatei und Abschlussantwort sind erhalten.
