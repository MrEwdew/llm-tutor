# PDF/ZIP-Versuch mit zehn Modellschritten

Datum: 2026-11-16. Je genau ein Lauf mit DeepAgents und OpenCode und Qwen_3_30B_A3B_Instruct_2507. Gleiche synthetische Materialien wie beim Sechs-Schritte-Versuch. Technisches Limit und Budgetangabe im Prompt auf zehn angepasst; fachlicher Prompt, Import-/WYPP-Hilfe und Zwei-Minuten-Limit blieben gleich. Keine src-Funktionen. Keine Wiederholungen.

## DeepAgents

Sieben Modellaufrufe: Materialsuche; PDF-Textextraktion und erstes Entpacken; Verzeichniskontrolle und erneutes Entpacken; Lesen von Aufgabentext und beiden Abgabedateien; Schreiben und Ausfuehren zweier Testdateien; Lesen der umgeleiteten Testergebnisse; Abschlussfeedback.

Beim ersten Entpacken waehlte der Agent /work/arbeit/abgabe statt /work/arbeit. Dadurch entstand ein zusaetzlicher abgabe-Unterordner. Er entpackte anschliessend nochmals an den vorgesehenen Ort. Einige abhaengige Werkzeuge wurden im selben Modellschritt angefordert, darunter Verzeichnislesen zusammen mit Entpacken und Teststart zusammen mit Schreiben. Ein fruehes Verzeichnislesen scheiterte; die spaeteren Teststarts gelangen in diesem Lauf. Diese Buendelung ist keine allgemein abgesicherte Ausfuehrungsreihenfolge.

Zehn fachlich korrekte WYPP-checks wurden ausgefuehrt. Vier meldeten Fehler: quadrat(1)=2 statt 1, quadrat(-3)=-6 statt 9, quadrat(5)=10 statt 25 und positiv(0)=True statt False. Beide Prozesse endeten mit Exitcode 0; Fehlermeldungen wurden aus den Ergebnisdateien gelesen. Das Abschlussfeedback benennt Addition statt Quadrat und >= statt > korrekt und nennt passende beobachtete Werte. Originale wurden nicht repariert.

## OpenCode

Acht Modellschritte, dann freiwilliger Abschluss vor dem Zehn-Schritte-Limit. ZIP erfolgreich entpackt. PDF zuerst mit direktem Reader versucht, danach fehlendes pdfinfo aufgerufen. Zweimal pip install pypdf trotz Installationsverbot; jeweils bereits vorhanden, kein neues Paket laut Ausgabe installiert. Weitere Versuche verwendeten die Python-Bibliothek in der JavaScript-Code-Umgebung beziehungsweise nicht verfuegbare fs-Importe. Abschliessend erneut direkter PDF-Reader.

Kein erfolgreicher Python-pypdf-Extraktionsaufruf in diesem Lauf, keine gelesenen Abgabecodes und keine Tests. Die Abschlussbehauptung, Textextraktion sei nicht moeglich, ist nicht belegt: Python und pypdf sind vorhanden, und vorherige Laeufe zeigten ihre erfolgreiche Nutzung. Zutreffend ist nur, dass der Agent hier keinen funktionierenden Weg verwendete. Mehr Budget allein loeste den Engpass nicht.

## Messwerte

| Harness | Genutzte Modellschritte | Dauer | Gemeldete Tokens | Abschluss |
| --- | ---: | ---: | ---: | --- |
| deepagents | 7 | 9.089 s | 29248 | Korrektur abgeschlossen |
| opencode | 8 | 9.523 s | 46432 | Ohne Tests beendet |

## Kann das Limit wieder sinken?

DeepAgents brauchte in diesem Einzelversuch sieben Aufrufe. Ein vorlaeufiges Limit von acht bietet einen Schritt Reserve und waere als naechste Einstellung plausibel; es wurde hier nicht erneut getestet. Genau sieben waere die beobachtete Mindestzahl fuer diesen konkreten Verlauf, keine Zuverlaessigkeitsgarantie. Sechs reichten im vorherigen Lauf nicht fuer das Abschlussfeedback. Laufwege variieren, daher ist aus einem gelungenen Lauf kein allgemein ausreichendes Minimum ableitbar.

Fuer OpenCode ist kein erfolgreiches kleineres Budget ableitbar. Es nutzte acht von zehn Schritten und brach inhaltlich ab. Zuerst waere die Werkzeugwahl beim PDF-Lesen zu untersuchen statt weitere Schritte hinzuzugeben. Kein weiterer Lauf automatisch gestartet.

Beide Ausgangsmaterialien und die entpackten Abgabedateien gegen Hashwerte bzw. ZIP-Bytes unveraendert geprueft. Gleicher Nutzerprompt und gleiches Image bedeuten keine identischen Systemprompts, Werkzeugbeschreibungen, Modellparameter oder Limitsemantik. Nur Einzelmessungen; keine allgemeine Rangfolge der Harnesses. Keine echten studentischen Abgaben, keine korrekte PDF/ZIP-Gegenprobe unter diesen Bedingungen.
