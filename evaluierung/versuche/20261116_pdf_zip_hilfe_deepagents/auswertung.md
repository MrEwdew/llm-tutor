# PDF und ZIP im unterstuetzten Kleinstfall

Datum: 2026-11-16. Je ein Lauf mit DeepAgents und OpenCode, Qwen_3_30B_A3B_Instruct_2507. Synthetisches Aufgaben-PDF und ZIP mit zwei fehlerhaften Funktionen. Keine echten Studierendendaten, keine src-Funktionen. Dieselben Originalmaterialien wie im frueheren Kleinstfall.

## Aufbau und Hilfe

Nach erfolgreichen Versuchen mit einzelnen Python-Dateien wurden PDF und ZIP wieder hinzugefuegt. Beide Harnesses erhielten denselben Nutzerprompt mit ausdruecklicher Vorgabe, pypdf ueber Python zu verwenden, sowie konkreten Funktionsimporten, dem zur ZIP-Struktur passenden Suchpfad und check(istwert, sollwert). Dadurch war ein Teil der Dateizuordnung bereits vorgegeben; dies ist kein unabhaengiger Nachweis freier Zuordnung unbekannter Dateinamen. Keine Testeingaben oder Sollwerte vorgegeben. Sechs native Modellschritte, 120 Sekunden je Lauf; keine Wiederholungen.

## DeepAgents

1. Materialdateien aufgelistet und gesucht.
2. PDF-Text tatsaechlich mit Python/pypdf extrahiert und ZIP entpackt. Eine gleichzeitig angeforderte Verzeichnisliste kam vor Abschluss der Extraktion zurueck und war leer; danach wurde erneut gesucht.
3. Entpackte Python-Dateien gefunden.
4. Beide Originaldateien gelesen.
5. Zwei eigene Testdateien mit zusammen zehn korrekten WYPP-checks geschrieben.
6. Beide Testdateien tatsaechlich ausgefuehrt. Vier gemeldete Vergleichsfehler: quadrat(1)=2 statt 1, quadrat(-3)=-6 statt 9, quadrat(4)=8 statt 16; positiv(0)=True statt False. Die uebrigen sechs Checks meldeten keinen Fehler.

Das native Modelllimit beendete danach den Ablauf. Kein fachliches Abschlussfeedback. Testgenerierung und Ausfuehrung gelungen, vollstaendige Korrekturrueckmeldung nicht erreicht.

## OpenCode

Zunaechst direkter PDF-Leser trotz gegenteiliger Vorgabe, ausserdem ZIP entpackt. Anschliessend pip install pypdf entgegen dem Installationsverbot; Ausgabe meldete bereits vorhandene Version 6.1.1. Kein erfolgreicher Paketwechsel belegt. Danach falscher Versuch, pypdf im JavaScript-Code-Mode zu laden; Werkzeug meldete die unzulaessige Verwendung. Anschliessend gelang echte Textextraktion ueber Python/pypdf. Entpackte Python-Dateien wurden gefunden, aber nicht gelesen, keine Tests geschrieben oder ausgefuehrt. Der letzte Modellschritt gab einen zutreffenden unvollstaendigen Zwischenstand aus.

## Messwerte

| Harness | Dauer | Gemeldete Tokens | Ergebnis |
| --- | ---: | ---: | --- |
| deepagents | 6.498 s | 23644 | Zehn Checks ausgefuehrt, kein Abschlussfeedback |
| opencode | 6.596 s | 34106 | PDF/ZIP gelesen bzw. entpackt, keine Tests |

## Grenzen und Fortsetzung

Archive und PDFs sowie die entpackten Abgabedateien wurden nach dem Lauf gegen Hashwerte beziehungsweise ZIP-Bytes geprueft und blieben unveraendert. WYPP-Prozesse endeten trotz gemeldeter Vergleichsfehler mit Exitcode 0; Ausgabe ist deshalb mitzubeurteilen.

Gleicher Nutzerprompt bedeutet keine identischen Systemprompts, Werkzeuge, Modellparameter oder Limitsemantik. Nur Einzelmessungen, keine allgemeine Ueberlegenheit eines Harnesses. Die technische Unterstuetzung und das enge Budget beeinflussen den Befund. Kein weiterer Lauf automatisch gestartet. Ein groesseres Budget oder eine Fortsetzung waere eine eigene Versuchsbedingung und wurde hier nicht getestet.
