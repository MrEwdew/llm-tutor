# Unterstützter Kleinstfall

Stand: 2026-11-16. Je ein Lauf mit OpenCode 2.3.0 und DeepAgents 0.7.32,
Modell Qwen_3_30B_A3B_Instruct_2507. Keine automatische Wiederholung.

## Material und Auftrag

Eine neu erstellte, einseitige Text-PDF enthält die beiden bereits im Webchat
verwendeten Anforderungen: quadrat berechnet x*x; positiv liefert genau für
x > 0 True. Allgemeine Vorgaben: eigene Python-Datei pro Aufgabe, keine festen
Dateinamen, keine Pflicht zu Abgabetests, keine Reparatur des Abgabecodes.
Die PDF wurde textuell und als gerenderte Seite geprüft.

Eine neue ZIP enthält ausschließlich die zwei synthetischen fehlerhaften
Abgaben: quadrat liefert x+x und positiv verwendet x>=0. Beide Dateien liegen
unter abgabe/. Keine echten studentischen Daten verwendet.

Der Harness soll selbst PDF und ZIP erschließen, Dateien zuordnen, sinnvolle
WYPP-Checks mit begründeten Sollwerten schreiben, unveränderten Code prüfen und
Feedback geben. Ein expliziter Umgebungshinweis nennt Python, pypdf, zipfile,
WYPP und pytest. Keine fertige Extraktion, Zuordnung, Sollwerte oder Fachtests
mitgegeben. Paketinstallation, Websuche und Delegation untersagt.

Kein Import aus src, kein common.py, correction_agent.py oder eigener
studentischer Test-Runner. start.py übernimmt nur Konfiguration, Containerstart,
Begrenzung und Aufzeichnung. Die Modell-Werkzeug-Schleife stammt vom Harness.

## Begrenzung und Unterschiede

Je frischer Container mit demselben Image und identischen Materialbytes.
Maximal 120 Sekunden einschließlich Prozessstart, 4 GB RAM, zwei CPUs.
Originalmaterialien schreibgeschützt. Arbeitsdateien bleiben separat erhalten.

OpenCode verwendet die native Einstellung agents.build.steps=6. Im letzten
Schritt werden Werkzeuge entfernt und eine Zusammenfassung angefordert.
Unteragenten und Webwerkzeuge sind durch native Berechtigungen deaktiviert.

DeepAgents verwendet die vorhandene ModelCallLimitMiddleware(run_limit=6).
Ein Callback begrenzt zusätzlich sämtliche Modellstarts einschließlich
möglicher Unteragenten auf sechs und protokolliert Modelle sowie Toolrückgaben.
Delegation ist im Auftrag untersagt, nicht zusätzlich aus den Tools entfernt.
Das Stopverhalten unterscheidet sich: OpenCode reserviert eine letzte
Zusammenfassung; DeepAgents kann bei Erreichen der Grenze abbrechen.
Die Modellgrenze gilt bei DeepAgents für Starts, nicht nur erfolgreiche Antworten.
Temperatur 0, Ausgabelimit 1000, Requesttimeout 60 Sekunden, keine Retries.

## OpenCode

Nach rund 10 Sekunden mit sechs protokollierten Modellantworten beendet.
Die ZIP wurde tatsächlich aufgelistet und unter arbeit/ entpackt.
Die PDF wurde dreimal mit dem direkten read-Werkzeug angefordert. Das Werkzeug
liefert einen Dateiblock und den Text "PDF read successfully", aber keinen
extrahierten Aufgabentext. Diese Rückgabe ist kein Nachweis des Textverständnisses.
Das Modell nutzt die ausdrücklich genannte Bibliothek pypdf nicht.

Eine Rückfrage wird im nicht interaktiven Modus abgebrochen. Im Abschluss wird
behauptet, die Aufgabenstellung sei aus der ZIP extrahiert worden. Die ZIP enthält
jedoch nur Code, und ein entsprechender Lesevorgang ist nicht belegt.
Keine Codeanalyse, keine eigenen Checks, keine Ausführung der Abgabe und kein
fachliches Korrekturfeedback. Exitcode 0 bedeutet hier nur normales Prozessende.

## DeepAgents

Nach rund 4 Sekunden am Modelllimit gestoppt. Fünf erfolgreiche Modellantworten
liegen im Protokoll; die Startbegrenzung verhindert einen weiteren Aufruf.
Die Dateisuche verwendet ls und glob. read_file gibt die PDF als Dateiblock
zurück. Anschließend wird die ZIP mittels execute/unzip -l aufgelistet.
Kein pypdf-Aufruf, keine Entpackung, keine Abgabecode-Lektüre und keine Tests.
Eine abschließende Korrekturantwort wurde nicht erreicht.

## Verbrauch und Schlussfolgerung

Die genauen Zeit- und Verbrauchswerte stehen in auswertung.json und den beiden
bericht.json-Dateien. Gemeldete Tokenwerte aus erfolgreichen Antworten werden
summiert; bei fehlgeschlagenen Anfragen können Angaben fehlen.

Alle Originalmaterial-Hashes blieben unverändert. Beide Container wurden beendet
und entfernt. Die Rohverläufe und erzeugten Arbeitsdateien wurden erhalten.

Das vollständige Ziel wurde mit keinem Harness unter diesem Prompt und dieser
Begrenzung erreicht. ZIP-Auflisten ist für beide, Entpacken für OpenCode belegt.
Ein allgemeines Unvermögen der Modelle folgt daraus nicht. Sechs Modellschritte
reichen in diesen Läufen nicht für den Gesamtauftrag, weil sie bereits bei der
Materialerschließung aufgebraucht werden. Mehr Laufzeit hätte hier allein nichts
geändert; das Modellschrittlimit griff vorher.

Ein möglicher nächster, separat auszuweisender Versuch wäre die ausdrückliche
Anweisung, PDFs über pypdf auszulesen statt als Dateiblock zu senden. Daraus keine
Freigabe für weitere Modellläufe oder ein höheres Budget ableiten.
