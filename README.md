# hop-workspace

Gemeinsamer Arbeitsbereich für die aktiven Apache-Hop-Plugins und ihre Helfer.
Die [AGENTS.md](AGENTS.md) enthält die übergreifenden Arbeitsregeln und den
Projektindex. [repositories.txt](repositories.txt) bestimmt den Checkout-Bestand.

## Repositories auschecken oder aktualisieren

Voraussetzungen: Git, Bash ab 3.2 und Zugriff auf GitHub. Das Skript benötigt
keine weiteren Laufzeiten oder Pakete.

```bash
./checkout.sh
./checkout.sh hop-interlis-plugin hop-geometry-type-plugin
./checkout.sh --help
```

Beim ersten Aufruf werden alle 23 Repositories von `edigonzales` über HTTPS auf
`main` geklont. Sie liegen direkt unter diesem Workspace und bleiben eigenständige,
hier ignorierte Git-Repositories. Es gibt keine Submodules. Bereits neben dem
Workspace vorhandene Checkouts werden nicht verwendet. Das Skript funktioniert
auch beim Aufruf über einen absoluten Pfad aus einem anderen Arbeitsverzeichnis.

Weitere Aufrufe aktualisieren saubere `main`-Checkouts durch Fetch und
Fast-forward. Lokale vorausliegende Commits bleiben erhalten. Lokale Änderungen,
unversionierte Dateien, andere Branches, detached HEAD, divergierte Historien,
abweichende Origins und belegte Zielpfade werden als Fehler gemeldet. Das Skript
führt weder Stash noch Reset oder Branchwechsel aus. Für bestehende Checkouts
sind HTTPS- und übliche SSH-Origin-URLs zum selben Repository zulässig.

Nach einem Fehler werden die übrigen ausgewählten Repositories weiterbearbeitet.
Exitcodes: `0` für Erfolg, `1` für Bearbeitungsfehler und `2` für ungültige Argumente
oder eine ungültige Projektliste. Ein erneuter Aufruf kann fehlgeschlagene
Checkouts nach Behebung der Ursache nachholen.

## Mit den Projekten arbeiten

Arbeiten am besten aus diesem Workspace beginnen und die Root-[AGENTS.md](AGENTS.md)
sowie die Anweisungen des betroffenen Projekts lesen. Bei direktem Einstieg in ein
Unterrepository die Workspace-`AGENTS.md` ausdrücklich als zusätzlichen Kontext
einlesen; automatische Vererbung über Gitgrenzen ist nicht vorausgesetzt.

Build, Tests und Installation gehören in die jeweiligen Projekte. Es gibt keinen
zentralen Sammelbuild. Der Bestand umfasst 16 Plugins und sieben Helfer inklusive
Distribution und Website; ältere GDAL-/Form-Projekte, UI-Patch und leere Ansätze
sind nicht aufgenommen.

## Ein Projekt ergänzen

1. Den aktuellen GitHub-Namen in `repositories.txt` ergänzen, einen Namen pro
   Zeile, ohne URL, Kommentare oder Leerzeilen. Alle Einträge gehören zu
   `edigonzales` und benötigen einen `main`-Branch.
2. Das Verzeichnis als `/repository-name/` in `.gitignore` eintragen.
3. Zweck und vorhandene Arbeitsanweisungen im Projektindex der `AGENTS.md` ergänzen.
4. `./checkout.sh repository-name` ausführen.

## Workspace prüfen

Für die Skripttests werden zusätzlich Python 3.9 oder neuer und Git benötigt.
Sie arbeiten ausschliesslich mit temporären lokalen Repositories, ohne GitHub
oder Änderungen an den echten Projekt-Checkouts und der globalen Git-Konfiguration.

```bash
bash -n checkout.sh
python3 -m unittest discover -s tests -v
git diff --check
```

Inspiriert von [dateninfrastruktur-workspace](https://github.com/sogis/dateninfrastruktur-workspace).
