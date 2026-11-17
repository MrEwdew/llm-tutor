# OpenCode: vollständiger Kleinstfall mit acht Schritten

Stand: 2026-11-16. Ein beauftragter Lauf mit OpenCode 2.3.0 und
Qwen_3_30B_A3B_Instruct_2507. Keine Wiederholung oder nachträgliche Fortsetzung.

## Auftrag und Bedingungen

Unveränderte Materialkopien des vorherigen Kleinstfalls: einseitige Aufgaben-PDF
und ZIP mit den beiden synthetischen fehlerhaften Funktionen. Keine echten
studentischen Daten. Konkrete Anweisung zur PDF-Textextraktion mit pypdf;
ZIP entpacken, Code lesen, Aufgaben zuordnen, eigene WYPP-Checks und begründete
Sollwerte entwickeln, unveränderten Code testen und Fehler erklären.

Keine Tests oder Sollwerte vorgegeben. Kein src-Import, kein eigener
studentischer Test-Runner und keine fachliche Vorverarbeitung. Der Starter
konfiguriert nur den vorhandenen Harness, Docker, Grenzen und Aufzeichnung.

Maximal acht native OpenCode-Modellschritte und 120 Sekunden einschließlich
Start. Unteragenten, websearch und webfetch nativ untersagt. Paketinstallation
im Auftrag untersagt. Dasselbe vorhandene Image, frischer Container und HOME,
4 GB RAM, zwei CPUs, Originalmaterialien schreibgeschützt. OpenCode reserviert
den letzten Schritt für eine Abschlussantwort ohne Werkzeuge.

## Tatsächlicher Verlauf

1. Direkter PDF-Leseversuch entgegen der Vorgabe; gleichzeitig ZIP entpackt.
2. execute-Werkzeug versucht intern tools.shell aufzurufen: Unknown tool 'shell'.
3. Derselbe Werkzeugfehler nach veränderter Zeichenkettenmaskierung erneut.
4. Direkter shell-Aufruf startet Python und pypdf erfolgreich. Die Werkzeugausgabe
   enthält den vollständigen erwarteten Aufgabentext.
5. glob findet beide Python-Dateien in der entpackten Abgabe.
6. aufgabe_01.py gelesen.
7. aufgabe_02.py gelesen.
8. Native Abschlusszusammenfassung wegen erreichtem Schrittlimit.

Der Modelltext behauptet keine abgeschlossenen Tests, sondern benennt sie als
noch offen. Seine Empfehlung, einen neuen Chat mit vollem Werkzeugzugriff zu
verwenden, ist keine nachgewiesene Voraussetzung: Im Versuch war die Shell
vorhanden und wurde erfolgreich genutzt. Das native Schrittlimit war erschöpft.

## Ergebnis

PDF-Text tatsächlich extrahiert, ZIP tatsächlich entpackt und beide Abgabecodes
gelesen. Keine eigenen Tests geschrieben, keine Abgabefunktion ausgeführt und
kein abgeschlossenes fachliches Korrekturfeedback. Die Arbeitsdateien enthalten
nur die beiden unveränderten entpackten Abgaben.

Material-Hashes und die entpackten Codebytes wurden gegen die Original-ZIP
geprüft und blieben unverändert. Exitcode 0 bezeichnet normales Prozessende,
nicht einen erfolgreichen Korrekturauftrag. Der Container wurde entfernt.

Der Lauf dauerte rund sechs Sekunden. Exakte Dauer, acht Modellantworten und
gemeldete Tokens stehen in opencode/bericht.json; Rohereignisse und vollständige
Werkzeugrückgaben in opencode/ausgabe/verlauf.jsonl.

Das Gesamtziel ist unter diesen Bedingungen nicht erreicht. Ob der Agent mit
mehr Schritten selbst richtige Checks erstellt und ausführt, bleibt offen.
Ein größeres Zeitlimit allein hätte diesen Lauf nicht weitergeführt, da die
Schrittgrenze vorher griff. Die Werkzeugwahl und zwei vermeidbare Fehlaufrufe
verbrauchten einen wesentlichen Teil des Budgets.

Diese Notiz erteilt keine Freigabe für weitere Modellläufe oder höhere Limits.
