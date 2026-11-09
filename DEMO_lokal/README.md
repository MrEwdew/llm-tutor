# Demo ohne Docker

Boot-Aufgabe mit drei Abgaben. DeepAgents und Qwen über KI:CONNECT verwenden
unsere festen Tests. Python und die Projektpakete einschließlich WYPP müssen
installiert sein.

Im Ordner llm-tutor mit dem Projektinterpreter starten:

```text
python DEMO_lokal/demo.py
```

Abgabe wählen: 1=gut, 2=mittel, 3=schlecht, a=alle.
Modus wählen:

- 1: Tests und Modellfeedback. Speichert das Ergebnis unter ergebnisse/.
- 2: Nur Tests.
- 3: Gespeicherte Containerläufe vom 03.11.2026 anzeigen.

Für Live-Aufrufe stehen KICONNECT_API_KEY und KICONNECT_BASE_URL in llm-tutor/.env.
Die Projektpakete sind in pyproject.toml und uv.lock festgelegt. Der bisher
verwendete Abgleich war:

```text
uv sync --locked --inexact --group notebooks
```

uv wird zum Starten nicht benötigt. Das ältere einrichten.py installiert andere
Paketversionen aus requirements.txt, nicht den zuletzt geprüften Projektstand.

Die Demo verwendet src für Modellzugang, Agent und Testausführung. Den src-Ordner
mitnehmen. test_runner.py in diesem Demoordner wird nicht mehr aufgerufen.

Gut ist die Originalabgabe aus der Beispiel-ZIP, mittel und schlecht sind gezielte
Änderungen. Erwartet: 3/3, 2/3 und 0/3 bestandene Tests. Die Tests sind vorgegeben.
Enthaltene WYPP-Ausgaben zählen getrennt. Der Testprozess hat zehn Sekunden Zeit,
läuft aber mit den Rechten des Benutzers. Nur die bekannten Demoabgaben verwenden.

Der gemeinsame Korrekturablauf wurde am 09.11.2026 über DEMO_integriert mit allen
drei Varianten geprüft. Modellfeedback muss trotzdem fachlich kontrolliert werden.
