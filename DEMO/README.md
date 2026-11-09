# Demo mit Docker

Boot-Aufgabe mit drei Abgaben. DeepAgents ruft die Tests auf,
Qwen über KI:CONNECT erklärt das Ergebnis.

Im Ordner llm-tutor starten, mit dem Python aus DEMO/.venv:

```text
python DEMO/demo.py
```

Abgabe wählen: 1=gut, 2=mittel, 3=schlecht, a=alle.
Modus wählen:

- 1: Tests und Modellfeedback. Speichert das Ergebnis unter ergebnisse/.
- 2: Nur Tests.
- 3: Gespeicherte Containerläufe vom 03.11.2026 anzeigen.

Benötigt Python 3.13, Docker Desktop und das Image tutor-python-test.
Für die Einrichtung wird uv verwendet:

```text
python DEMO/einrichten.py
```

Bei fehlenden Downloads --online ergänzen. Docker Desktop muss laufen.
Das Image lässt sich im Ordner llm-tutor bauen:

```text
docker build -t tutor-python-test DEMO
```

Für Live-Aufrufe stehen KICONNECT_API_KEY und KICONNECT_BASE_URL in llm-tutor/.env.

Die gute Abgabe stammt aus der Beispiel-ZIP. Die anderen beiden wurden gezielt
verändert. Drei feste Tests sollen 3/3, 2/3 und 0/3 ergeben. Meldungen der
enthaltenen WYPP-Checks werden getrennt angezeigt. Die Tests laufen im Container
mit Zeit- und Ressourcenlimits, ohne Netzwerk und ohne eingebundene Hostordner.
Die Referenz unter material/ dient nur zum Nachlesen.

Diese ältere Variante verwendet src nicht. Der Prompt wurde geändert; die letzte
Probe am 09.11.2026 lief mit DEMO_integriert, nicht mit dieser Docker-Version.
