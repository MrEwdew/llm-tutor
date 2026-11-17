# Vergleich mit eingefrorenen src-Bausteinen nach Runner-Erweiterung

Datum:2026-11-16. Nutzerauftrag: Runner zunächst für boolesche/textuelle Rückgaben erweitern, danach den neuen Stand unverändert vergleichen. Änderung ausschließlich python_test_runner.py (results_match und typgerechte actual-Ausgabe) sowie Kommentar in python_tests.py. Nutzeränderungen an common.py nicht überschrieben.

## Erweiterung und Prüfung

Zahlen weiterhin math.isclose rel_tol/abs_tol1e-9; bool ausdrücklich von Zahlen getrennt, bool/bool exakt; Texte exakt und typgebunden. Nicht endliche Zahlen nicht als gültige numerische Ergebnisse; nicht unterstützte Sollwerttypen erzeugen ValueError. Lokale Prüfung:14 Zahl/bool/Text-/Grenzvergleiche und ein echter Unterprozess mit drei synthetischen Funktionen erfolgreich. Keine studentische Abgabe bei diesen ersten Runner-Prüfungen. Danach Stand als src_snapshot mit Hashes eingefroren. shared llm.get_llm, correction_agent.correct_python_submission und gemeinsame Python-Prozessausführung tatsächlich verwendet. Keine weiteren Sourceänderungen während der Reihe.

## Abdeckung der heutigen Versuche

27 historische Einzelversuchsbedingungen wurden lokal über ihre Materialien erneut mit vorhandenen Lade-/AST-Bausteinen erfasst (materialabdeckung.json). Frühe Miniversuchs-Prompttypen separat in miniversuch_abdeckung.json. Die identische fachliche Eingabe aus wiederholten Budget-/Hilfestufen wurde für die festen src-Tests nicht mehrfach mit demselben Modell bezahlt. Die Verknüpfung steht in der Materialmatrix. Das sind keine27 neuen identischen Modell-Replays; neun unterschiedliche Funktionsfälle wurden neu live ausgeführt.

Der neue src-Ablauf bleibt DeepAgents-basiert, verwendet Qwen30B, Demo-Prompt, Temperatur0,max_tokens700,retries0,Graphlimit8, höchstens zehn Starts als zusätzliche Sicherung und120 Sekunden pro Container. Jede Funktion wird als Einzeldatei mit festen Tests korrigiert. Neun frische nicht-root-Container, schreibgeschützter Source-Snapshot, begrenzte Ressourcen; keine neuen Pakete. Die bisherige Demo mit drei Boot-Varianten war bereits separat neu live geprüft und wird nicht als weiterer neuer Lauf gezählt.

## Wichtiger Unterschied

Für diesen Vergleich wurden feste Sollwerte aus den bekannten Anforderungen bereitgestellt. Keine automatische Testgenerierung durch src hinzugefügt. Die fachlich geprüften Fälle vermeiden die zuvor falschen clamp-Sollwerte und unzulässige Anforderungen an ungültige Rückennummern. Damit prüfen wir kontrollierte Ausführung/Feedback bei korrekter Testbasis, nicht die Fähigkeit, diese Testbasis selbst zu erzeugen. Das ist stärkere Unterstützung als die freien Harness-Läufe und muss so ausgewiesen werden.

Selbstauskunft über allgemeine Werkzeuge, secrets-Zufallsausführung, Java, Webchat, Chatverlaufs-/Quellenrückfragen und freie Tests sind keine angebotenen Fähigkeiten dieses src-Korrektureinstiegs. Dafür keine Scheinläufe erstellt. Formale Modellbewertung ist durch den unveränderten Demo-Prompt ausdrücklich ausgeschlossen. Der frühere Prompt zur fehlenden Beschreibung/Typen wird damit nicht gleichwertig wiederholt. Ein OpenCode/Llama-Replay dieses DeepAgents-src-Einstiegs wäre ebenfalls keine identische Harness-Bedingung; nicht ausgeführt. Materiallader und AST sind lokal, nicht als freie Modellleistung gewertet.

## Neue Live-Ergebnisse

| Fall | Bestanden | Modellantworten | Gemeldete Tokens | Agentenlauf |
| --- | --- | ---: | ---: | ---: |
| synthetisch_fehlerhaft_quadrat | 1/4 | 2 | 1634 | 1.61s |
| synthetisch_fehlerhaft_positiv | 2/3 | 2 | 1555 | 1.44s |
| synthetisch_korrekt_quadrat | 4/4 | 2 | 1440 | 0.67s |
| synthetisch_korrekt_positiv | 3/3 | 2 | 1408 | 0.73s |
| blatt2_aufgabe1 | 8/8 | 2 | 3455 | 0.81s |
| blatt2_aufgabe2 | 7/14 | 2 | 4803 | 3.24s |
| blatt2_aufgabe3 | 12/12 | 2 | 3994 | 1.24s |
| blatt2_aufgabe4 | 9/9 | 2 | 3601 | 0.74s |
| magluise_korrekt | 6/6 | 2 | 2633 | 0.8s |

Gesamt:24523 gemeldete Tokens,18 Modellantworten. Zeiten Agentenaufbau/-lauf einschließlich Testprozess; Containerstart separat in Rohberichten. Summierte Einzelzeiten sind keine Gesamtzeit der Reihe.

## Fachliche Prüfung

Strukturierte Testergebnisse entsprechen allen vorbereiteten Erwartungen. Synthetisches quadrat/positiv falsch erkannt; korrekte Gegenproben akzeptiert. Echte Aufgabe1,3,4 ohne Fehler in geprüften Fällen. Aufgabe2:genau3,4,5,7,8,10,11 falsch, übrige sieben gewählte gültige Nummern korrekt. Keine ungültigen Rückennummern als Bewertungsgrundlage. clamp(-50,-75,-25) mit richtigem Sollwert-50 bestanden. magLuise korrekt, bool-Ergebnis vom Runner unterstützt.

Feedback nicht völlig fehlerfrei: Bei synthetischem positiv widersprüchlicher Eröffnungssatz (true erwartet/true zurück), anschließend korrekte expected=false/actual=true und richtige Ursache >=0. Fußballfeedback erklärt or-Problem richtig, behauptet am Ende aber alle Nummern außer1,2,6,9 würden fälschlich als Ersatzspieler eingestuft. Nummern12–99 sind jedoch tatsächlich Ersatzspieler; die Verallgemeinerung ist falsch. Die konkret genannten sieben Fehlfälle stimmen. Keine Behauptung einer allgemeinen fachlichen Vollständigkeit.

## Schlussfolgerung

Der kontrollierte src-Testpfad ist für Zahlen/bool/Text jetzt einsatzfähig und liefert in diesen neun Fällen richtige strukturierte Vergleiche mit wesentlich geringerem Tokenbedarf als freie Aufgabenerschließung. Das beweist weder allgemeine zuverlässige Korrektur noch eigene Testgenerierung. Der größte Unterschied ist die geprüfte Testbasis und das feste Testwerkzeug, nicht allein das Modell. Die sprachliche Bewertung kann trotz korrekter Werkzeugdaten widersprüchlich oder zu weitgehend sein.

Keine vollständige Blattbewertung: vier Einzelaufgaben nacheinander mit festen Tests, keine freie Entscheidung über Testauswahl und keine formale Gesamtnote. Keine Java-Unterstützung ergänzt, keine Listen-/Mutations-/Klassen-/beliebige Objektrückgaben. Legacy-main/Praktomat nicht umgestellt. Alle Daten und Messwerte tatsächlich vom2026-11-16; keine Rückdatierung.
