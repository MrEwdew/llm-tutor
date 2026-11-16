# Evaluation mit DeepAgents und OpenCode

Die Agenten erhalten Aufgabenblatt, ZIP-Abgabe und vorhandene Referenzen als
Dateien. Sie sollen selbst zuordnen, ausfuehren, eigene Tests schreiben und
Korrekturfeedback geben. Die festen Demo-Tests werden nicht verwendet.

## Umgebung vorbereiten

Docker Desktop mit Linux-Containern starten. Im Ordner llm-tutor bauen:

```text
docker build --platform linux/amd64 -t tutor-evaluation:python-3.13-opencode-2.3.0 evaluierung
```

Der Bau laedt Pythonpakete und OpenCode 2.3.0 fuer Linux herunter. Die Windows-EXE
wird nicht in den Container kopiert. Version und Archivpruefsumme werden geprueft.
Die Python-Pins stehen in requirements.txt; aufgeloeste Pakete liegen im Image
unter /opt/evaluation. Bestehende Projektpakete und Demoimages bleiben unveraendert.
Das Image wurde noch nicht gebaut oder praktisch geprueft.

## Versuche vorbereiten

In konfiguration.py stehen Faelle, Modelle, Wiederholungen und Auftrag.
Der Blatt-1-Fall ist nur ein Pilot: Referenz allein fuer Aufgabe 6, keine separaten
Beispieltests. Vor der Evaluation Materialien und manuelle Referenzbewertung festlegen.

```text
python evaluierung/start.py
```

Erstellt nur Versuchsordner mit Materialkopien, Hashes, Auftrag und Skriptstand.
Kein Agentenstart. Vorhandene Laeufe werden nicht ueberschrieben. Ein spaeterer
Start bereitet neue Versuche vor; er setzt diese Ordner nicht fort.

## Echte Laeufe

Erst nach Umgebungspruefung und vereinbartem Pilotversuch --start verwenden.
--fall und --harness begrenzen die Auswahl, sonst laufen alle konfigurierten
Kombinationen. --lokale-ausfuehrung gibt es nicht mehr.

Der gesamte Agent laeuft im Container, einschliesslich seiner Shellwerkzeuge.
Beide Harnesses verwenden dieselbe Image-ID, Python/WYPP/pytest/pypdf und
git/unzip/ripgrep. Ohne Root-Rechte, mit schreibgeschuetztem System, zwei CPUs,
4 GB RAM, 256 Prozessen und 600 Sekunden Gesamtlimit. Material ist ein eigener
schreibgeschuetzter Mount; Arbeitskopien und Tests unter arbeit/ erstellen.

Eingebunden werden nur Versuchsort, Material, Auftrag, Skripte und Ausgabeordner.
Keine Benutzerordner, Projekt-/Demoordner, manuelle Bewertung oder Docker-Socket.
Die .env-Datei wird nicht eingebunden. Nur KI:CONNECT-Key und Basis-URL gehen als
Umgebungswerte hinein. Keine Schluessel in Berichte schreiben. Das Modell braucht
Netzwerk; Webzugriff ist nur im Auftrag untersagt, nicht technisch gesperrt.
Der Key ist im Agentencontainer vorhanden; das ist keine Geheimnisisolation
gegenueber dessen Prozessen. Container sind keine vollstaendige Sicherheitsgarantie.

Docker braucht Internet zum Bau, das Modell braucht spaeter Zugriff auf KI:CONNECT.
Neue Versuche erhalten ein frisches HOME ohne uebergeordnete Projektanweisungen,
alte Sessions oder Benutzerkonfiguration. Harness-eigene Prompts/Werkzeuge und
Defaults bleiben verschieden. DeepAgents-Graphlimit ist kein vergleichbares
OpenCode-Schrittlimit. Netzwerk/Tokenverbrauch koennen nach Abbruch serverseitig
noch weiterlaufen; das Zeitlimit beendet den lokalen Container.

Berichte und Bewertung liegen ausserhalb des Agenten-Arbeitsordners. Rohverlaeufe,
Adapterdaten und Paketlisten stehen unter ausgabe/. feedback.md soll der Agent im
Arbeitsordner erstellen. Der Bericht erfasst auch, ob diese Datei vorhanden ist.

## Auswertung

```text
python evaluierung/auswerten.py
```

Sammelt Berichte und manuell eingetragene Bewertungen in uebersicht.csv.
Prozessende und vorhandenes Feedback beweisen keine korrekte Korrektur. Ohne
fachliche Bewertung bleiben Qualitaetswerte leer. TP/FP/FN erst nach einheitlicher
Festlegung einzelner Fehlerbefunde eintragen. Eigene Tests und Ausfuehrungsbehauptungen
anhand des Verlaufs pruefen. OpenCode-Tokenparser ist noch offen; Rohereignisse
bleiben erhalten. Keine automatischen Qualitaetsurteile durch ein weiteres Modell.

Naechster Schritt: Image bauen, Umgebung ohne Modell pruefen, dann einen
vereinbarten Pilotlauf je Harness untersuchen. Noch keine Serienlaeufe durchgefuehrt.
