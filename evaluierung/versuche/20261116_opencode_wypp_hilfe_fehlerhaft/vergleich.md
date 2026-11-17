# Vergleich: eigene WYPP-Tests mit technischer Hilfe

Datum: 2026-11-16. Qwen_3_30B_A3B_Instruct_2507; je eine korrekte und eine fehlerhafte synthetische Eingabe pro Harness. Identischer Nutzerprompt, gleiche fachliche Eingaben und dasselbe Containerimage. Keine src-Funktionen. Imports, Suchpfad und WYPP-Schnittstelle vorgegeben; Tests und Sollwerte selbst erzeugt.

| Harness | Eingabe | Ergebnis | Modellschritte | Dauer | Gemeldete Tokens |
| --- | --- | --- | ---: | ---: | ---: |
| DeepAgents | fehlerhaft | Beide Fehler erkannt | 6 | 5,887 s | 22.377 |
| DeepAgents | korrekt | Keine falschen Beanstandungen | 6 | 17,894 s | 22.074 |
| OpenCode | fehlerhaft | Beide Fehler erkannt | 4 | 9.571 s | 22690 |
| OpenCode | korrekt | Keine falschen Beanstandungen | 3 | 5.045 s | 16681 |

Beide Harnesses haben hier eigene fachlich passende Tests geschrieben, wirklich gegen die unveraenderten Originaldateien ausgefuehrt und ein im Kern passendes Feedback erstellt. Beide beschrieben den negativen Quadratfall stellenweise unpraezise als Multiplikationsproblem, obwohl Addition die Ursache ist.

Kein kontrollierter Vergleich identischer Systemprompts: Harness-Prompts, Werkzeugbeschreibungen, parallele Werkzeugbuendelung und native Limitsemantik unterscheiden sich. OpenCode kann mehrere Werkzeuge in einem Modellschritt buendeln. Gleiche Obergrenzen bedeuten deshalb keine identischen internen Ablaeufe. OpenCode-Modellparameter wurden im Adapter nicht eigens auf dieselben Temperatur-/Ausgabelimits wie DeepAgents gesetzt. Nur Einzelmessungen, keine statistische Aussage zu Laufzeit, Kosten oder Ueberlegenheit.

Naechste moegliche Stufe: PDF und ZIP im synthetischen Kleinstfall wieder hinzufuegen. Dies wurde hier nicht gestartet. Echte anonymisierte Abgaben und ganze Wochenarchive bleiben weitere, getrennte Versuche.
