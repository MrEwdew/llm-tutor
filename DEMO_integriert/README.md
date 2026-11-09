# Demo mit PDF und ZIP

Lädt Blatt 1 mit sechs Aufgaben und die ZIP-Abgabe. Korrigiert wird nur Aufgabe 6
mit DeepAgents und Qwen über KI:CONNECT.

Im Ordner llm-tutor mit dem Projektinterpreter starten:

```text
python DEMO_integriert/demo.py
```

Abgabe wählen: 1=gut, 2=mittel, 3=schlecht, a=alle.
Modus wählen:

- 1: Tests und Modellfeedback. Speichert das Ergebnis unter ergebnisse/.
- 2: Nur Tests.
- 3: Vorbereitete Eingabe anzeigen. Führt keinen Abgabecode aus.

Bei DEMO und DEMO_lokal zeigt Modus 3 dagegen gespeicherte Ergebnisse an.

Benötigt die Projektumgebung, src und DEMO_lokal. Die Einrichtung steht in
[DEMO_lokal/README.md](../DEMO_lokal/README.md). Für Live-Aufrufe braucht es
KICONNECT_API_KEY und KICONNECT_BASE_URL in llm-tutor/.env.

PDF und Beispiel-ZIP liegen unter data/python/tasks und
loesungen_der_schueler_vom_praktomat_runtergeladen. Die Referenz liegt unter
Musterloesungen/solutions/boot.py. Alle Pfade beziehen sich auf llm-tutor.

Für jede Variante wird nur Aufgabe 6 in einer temporären ZIP-Kopie ausgetauscht.
Das Original bleibt erhalten. src bereitet Aufgabe, Blattvorgaben und Code vor.
Die Referenz wird separat gelesen, weder ausgeführt noch ans Modell geschickt.
Die drei Vergleichstests sind fest vorgegeben. Der lokale Testprozess verwendet
dieselben Ausführungsgrenzen wie DEMO_lokal.

Probe vom 09.11.2026, je zwei Modellantworten:

| Abgabe | Tests | Tokens | Agentenlauf |
| --- | --- | --- | --- |
| gut | 3/3 | 4633 | 2.84 s |
| mittel | 2/3 | 4863 | 2.04 s |
| schlecht | 0/3 | 5389 | 3.69 s |

Die Fehlerursachen wurden richtig erklärt. Bei schlecht entsprach die Antwort
nicht ganz dem gewünschten Format. Berichte: ergebnisse/20261109_2151*.json.
Danach wurde der Referenzpfad auf die gleiche Datei innerhalb von llm-tutor
umgestellt. Der neue Pfad wurde gelesen geprüft, noch nicht erneut geladen.
