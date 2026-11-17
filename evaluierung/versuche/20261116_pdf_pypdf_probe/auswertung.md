# PDF-Auslesen mit pypdf

Stand: 2026-11-16. Je ein Versuch mit Qwen_3_30B_A3B_Instruct_2507 über
OpenCode 2.3.0 und DeepAgents 0.7.32. Keine Wiederholung.

## Anlass und Aufbau

Im vorausgehenden Kleinstfall hatten beide Harnesses bei der Materialerschließung
keinen geeigneten PDF-Textzugriff erreicht. Nun wurde ausdrücklich verlangt,
den Text mit Python und der vorhandenen Bibliothek pypdf auszulesen und nicht
das direkte PDF-Lesewerkzeug zu verwenden. Anschließend sollten die beiden
Funktionsanforderungen und allgemeinen Vorgaben kurz wiedergegeben werden.

Identische Kopie der bereits geprüften einseitigen Aufgaben-PDF. Keine ZIP,
Abgabe oder vorab extrahierter Text mitgegeben. Keine Tests beauftragt.
Die PDF wurde nicht neu erzeugt. Beide Harnesses erhalten dieselben Materialbytes.
Kein Baustein aus src verwendet. Der Starter ist eine getrennte Kopie des
vorherigen Versuchstarters mit anderem Auftrag und engeren Limits.

Grenzen: drei Modellschritte bei OpenCode; drei Modellstarts einschließlich
möglicher interner Wiederholungen bei DeepAgents; je 45 Sekunden Gesamtzeit.
Die DeepAgents-Antworten sind auf 500 Ausgabetokens begrenzt. OpenCode verwendet
seine Defaults. Der bereits dokumentierte Unterschied des Stopverhaltens bleibt:
OpenCode reserviert eine letzte Zusammenfassung, DeepAgents kann am Startlimit
abbrechen. Keine automatische Erhöhung oder Wiederholung nach dem Abbruch.

## Beobachtungen

Beide Modelle wählen zunächst trotz ausdrücklicher Vorgabe das direkte
PDF-Lesewerkzeug. Danach starten beide tatsächlich Python mit pypdf.
Die Werkzeugrückgaben enthalten den vollständigen erwarteten Aufgabentext.
Damit ist die Textauslese für diese PDF über beide Harnesses nachgewiesen.

OpenCode beendet drei Modellantworten in rund vier Sekunden. Die Abschlussantwort
bestätigt zwar die Extraktion, gibt die geforderten Inhalte aber nicht vollständig
wieder. Stattdessen bezeichnet sie das Anlegen von Lösungsdateien als noch offene
Arbeit, obwohl dies gar nicht beauftragt war. Kein vollständiger Auftragserfolg.

DeepAgents liefert zwei erfolgreiche Modellantworten und danach die vollständige
Python-Werkzeugausgabe mit Exitcode 0. Anschließend greift die Begrenzung auf drei
Modellstarts. Eine fachliche Abschlussantwort liegt nicht vor. Modellstarts und
erfolgreich abgeschlossene Antworten dürfen deshalb nicht gleichgesetzt werden.
Der Rohverlauf erklärt nicht abschließend, warum ein Start ohne abgeschlossene
Modellantwort blieb. Keine Diagnose eines API-Fehlers daraus ableiten.

Die exakten Zeiten und gemeldeten Tokens stehen in auswertung.json. Fehlende
Verbrauchsangaben fehlgeschlagener oder interner Anfragen sind nicht ergänzt.
Originalmaterialien blieben unverändert; beide Container wurden entfernt.

## Bedeutung

Die vorhandene Umgebung kann den PDF-Text auslesen. Aus den früheren Fehlschlägen
folgt deshalb keine grundsätzliche PDF-Unfähigkeit des Modells oder Harnesses.
Eine konkrete Werkzeuganweisung hilft in diesen beiden Einzelversuchen bis zur
Extraktion. Zuverlässige Instruktionsbefolgung und vollständige Ergebnisdarstellung
sind damit noch nicht nachgewiesen. Kein Nachweis für gescannte PDFs oder Bilder.

Die nächste Entscheidung betrifft einen erneuten vollständigen Korrekturversuch
mit dieser konkreten Umgebungshilfe und einem vorher vereinbarten Budget.
Aus dieser Notiz keine Freigabe für weitere Live-Läufe ableiten.
