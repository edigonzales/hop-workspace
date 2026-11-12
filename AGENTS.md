# Hop-Workspace: gemeinsame Arbeitsregeln

## Einstieg und Gitgrenzen

Diese Regeln gelten für die Arbeit im gemeinsamen Workspace. Vor Änderungen auch
die `AGENTS.md` des betroffenen Projekts lesen; dessen konkrete Regeln präzisieren
die allgemeinen Vorgaben. Bei einem direkten Einstieg in ein Unterrepository
diese Root-Datei ausdrücklich einlesen: automatische Vererbung über Gitgrenzen
ist nicht vorausgesetzt. Fehlt eine Projekt-`AGENTS.md`, README, Build und lokale
Entwicklungsdokumentation verwenden.

Der Root verwaltet nur Workspace-Dateien. Die Einträge aus `repositories.txt`
sind eigenständige Git-Repositories, keine Submodules und kein gemeinsamer
Maven-Reaktor. Vor Gitoperationen Toplevel, Branch, Origin und lokale Änderungen
prüfen. Änderungen und Commits dem jeweiligen Repo zuordnen; fremde lokale
Arbeit erhalten. Nur die für den Auftrag erforderlichen Projekte ändern.
`checkout.sh` dient dem ausdrücklich gewünschten Checkout/Update; es ist kein
automatischer Vorbereitungsschritt vor jeder Arbeit.

## Werkzeuge und gemeinsame Verträge

Versionen und Befehle aus dem tatsächlichen Projektbuild und dessen Anweisungen
übernehmen. Die aktuelle Hop-Basis ist 2.19.0; die meisten Plugins bauen mit
Java 21 und testen zusätzlich Java 25. PDAL und `pdal-java-bindings` benötigen
Java 25 und die dokumentierte Freigabe des nativen Zugriffs. Das ist keine
Aufforderung, Projektversionen oder gebundene Abhängigkeiten zu aktualisieren.

Maven Wrapper bevorzugen, wenn vorhanden. Maven-Kommandos vom jeweiligen
Repository-Root ausführen; projektlokale `.mvn`-Einstellungen beachten. Für
Repositories mit gemeinsamem CI-Setup dessen `write_maven_settings.py` verwenden.
`HOP_CI_DIR` muss zur vom Projekt verwendeten Helper-Revision passen.
`pdal-java-bindings` verwendet Gradle, die Distribution Python und die Website
Quarto. Keine Entwicklerpfade wie `/Users/stefan/...` in gemeinsame Skripte
übernehmen; Repository-Pfade, Parameter oder Umgebungsvariablen verwenden.

Vor Änderungen an CI, Testaufbau oder Repository-Struktur die bestehenden
[CI-Regeln](hop-plugin-ci/docs/ci-contract.md) und den
[Repository-Vertrag](hop-plugin-ci/docs/plugin-repository-contract.md) lesen.
Die konkreten Workflow- und Helper-Revisionen des Projekts bleiben massgeblich;
ein Link auf `main` aktualisiert keine Pins. Gemeinsame Build-, CI- und
Dokumentationslogik bei ihren Besitzern pflegen, statt sie im Workspace zu kopieren.

## Hop-Architektur und gemeinsame Laufzeit

Fachlogik, Hop-Runtime/Metadaten und SWT-Oberflächen trennen. Tatsächliche APIs
der konfigurierten Hop- und Bibliotheksversion prüfen. Metadatenvorschau,
`getFields(...)`, gespeicherte Konfiguration und Laufzeit müssen dieselbe
Semantik verwenden. Bestehende Plugin-IDs, XML-Felder und öffentliche Formate
kompatibel halten; notwendige Änderungen mit passenden Tests dokumentieren.
Hop-Logging und vorhandene Übersetzungsmechanismen verwenden. Für SWT-Dialoge
passende Komponenten aus `hop-plugin-commons` wiederverwenden.

Gemeinsame Typen und ihre Classloader-Grenzen erhalten:

- **Geometry Type** besitzt den Geometry-Typ und die gemeinsame Geometry/JTS-,
  GeoTools- und weitere dafür gebündelte Laufzeit im `sogeo-geometry`-Verbund.
- **Raster Type** besitzt das gemeinsame Rastermodell. Vector/Raster stellt
  die Benutzertransforms und den GeoTools-Rasteradapter bereit.
- **Point Cloud Type** besitzt das gemeinsame Punktwolkenmodell im
  `sogeo-pointcloud`-Verbund; PDAL stellt die Verarbeitung und nativen Bindings bereit.

Verbraucher deklarieren die vorgesehenen Abhängigkeiten, unter anderem über
`dependencies.xml`, statt gemeinsame Modell- oder Laufzeit-JARs erneut zu bündeln.
Raster- und Punktwolkenwerte enthalten Referenzen, Metadaten und Pläne;
geöffnete Reader oder native Handles gehören in begrenzte, schliessbare
Ausführungskontexte. SRID, Z/M und Kurven nach dem jeweiligen Vertrag erhalten;
keine stillschweigende Linearisierung oder Koordinatenumdeutung.

## Tests und Dokumentation

Für Codeänderungen die betroffenen Verhaltensweisen prüfen und die jeweiligen
Pflichtchecks aus der Projekt-`AGENTS.md` ausführen: Maven/Gradle, Paketprüfung,
installierte Plugin-Tests und gegebenenfalls Dokumentationsprüfung. Tests nicht
eigenmächtig überspringen. Projektseitig dokumentierte Schritte zum Verpacken
von Abhängigkeiten ersetzen nicht die Prüfung des bearbeiteten Plugins.

Installierte Tests verwenden isolierte, entbehrliche Hop-Verzeichnisse. Die
persönliche Hop-Installation nur bei einem ausdrücklich beauftragten Installieren
verwenden. CI-E2E prüft das bereits erzeugte kanonische Artefakt ohne Neubau;
unterschiedliche Projekt-Testketten nicht durch einen pauschalen Sammelbefehl ersetzen.
Kleine synthetische Fixtures und deterministische Tests bevorzugen. Nur tatsächlich
ausgeführte Checks als bestanden melden; fehlende Voraussetzungen benennen.

Verhalten, kanonische Dokumentation, ausführbare Beispiele und erwartete Ergebnisse
zusammen pflegen. In Plugins liegen Handbücher überwiegend als AsciiDoc unter
`docs/`; den dokumentierten Biblios-Aufbau und das jeweilige Profil beachten.
GUI-Änderungen in den `[.gui-mockup]`-Skizzen nachführen. `examples/` dient
Benutzern, `e2e/` den automatisierten Prüfungen. Website und andere Helfer folgen
ihren eigenen Dokumentationswerkzeugen. Generierte Seiten, Testausgaben,
Downloads und lokale Einstellungen nicht einchecken.

Für reine Workspace-Änderungen: `bash -n checkout.sh`,
`python3 -m unittest discover -s tests -v`, `git diff --check` und betroffene Links
prüfen. Dokumentationskorrekturen benötigen keine vollständigen Plugin-Builds.

## Projektindex

Die Links gelten nach `./checkout.sh`. Bei ausdrücklich als fehlend markierter
Projekt-`AGENTS.md` steht die Entwicklungsanleitung im verlinkten README.

| Repository | Zuständigkeit | Arbeitsregeln / Entwicklung |
| --- | --- | --- |
| `hop-geometry-type-plugin` | Geometry-Typ, gemeinsame Geo-Laufzeit und Codecs | [AGENTS.md](hop-geometry-type-plugin/AGENTS.md) |
| `hop-raster-type-plugin` | Rastermodell und GeoTools-Adapter | [AGENTS.md](hop-raster-type-plugin/AGENTS.md) |
| `hop-pointcloud-type-plugin` | Backendneutrales Punktwolkenmodell | Keine AGENTS.md; [README](hop-pointcloud-type-plugin/README.md), [Architektur](hop-pointcloud-type-plugin/docs/architecture.md) |
| `hop-vector-raster-plugin` | Vektorformate und Rastertransforms | [AGENTS.md](hop-vector-raster-plugin/AGENTS.md) |
| `hop-geoprocessing-plugin` | Geometrieoperationen, Überlagerung, Aggregation und Reprojektion | [AGENTS.md](hop-geoprocessing-plugin/AGENTS.md) |
| `hop-geometry-calculator-plugin` | Zeilenweise Geometrieberechnungen | [AGENTS.md](hop-geometry-calculator-plugin/AGENTS.md) |
| `hop-geometry-inspector-plugin` | Desktop-Inspektion von Zeilen und Geometrien | [AGENTS.md](hop-geometry-inspector-plugin/AGENTS.md) |
| `hop-interlis-plugin` | INTERLIS-Transferdaten und typisierte Hop-Zeilen | [AGENTS.md](hop-interlis-plugin/AGENTS.md) |
| `hop-interlis-row-validator-plugin` | INTERLIS-Prüfung endlicher Zeilenströme | [AGENTS.md](hop-interlis-row-validator-plugin/AGENTS.md) |
| `hop-ili2db-plugin` | ili2db als Action und Transform | [AGENTS.md](hop-ili2db-plugin/AGENTS.md) |
| `hop-ilivalidator-plugin` | Dateivalidierung als Action und Transform | [AGENTS.md](hop-ilivalidator-plugin/AGENTS.md) |
| `hop-json-object-builder-plugin` | Typisierte JSON-Objekte und Arrays | [AGENTS.md](hop-json-object-builder-plugin/AGENTS.md) |
| `hop-python-plugin` | Eingebettetes GraalPy für Zeilenverarbeitung | Keine AGENTS.md; [README mit Build und Tests](hop-python-plugin/README.md) |
| `hop-application-launcher-plugin` | Desktop-Start parametrisierter Git-Anwendungen | [AGENTS.md](hop-application-launcher-plugin/AGENTS.md) |
| `hop-sdmx-plugin` | SDMX-Datensuche und Streaming-Input | [AGENTS.md](hop-sdmx-plugin/AGENTS.md) |
| `hop-pdal-plugin` | Punktwolkenverarbeitung mit PDAL | Keine AGENTS.md; [README mit Build und CI](hop-pdal-plugin/README.md) |
| `hop-plugin-ci` | Gemeinsame Workflows, Helfer und Repository-Verträge | [AGENTS.md](hop-plugin-ci/AGENTS.md) |
| `hop-plugin-parent` | Gemeinsamer Maven-Parent und DocLint-Anbindung | [AGENTS.md](hop-plugin-parent/AGENTS.md) |
| `hop-plugin-doclint-maven-plugin` | Prüfung von Plugin-Dokumentation und Beispielen | [AGENTS.md](hop-plugin-doclint-maven-plugin/AGENTS.md) |
| `hop-plugin-commons` | Wiederverwendbare Core- und SWT-Komponenten | [AGENTS.md](hop-plugin-commons/AGENTS.md) |
| `pdal-java-bindings` | FFM-Bindings und plattformspezifische PDAL-Laufzeit | Keine AGENTS.md; [README mit Build und Integrationstests](pdal-java-bindings/README.md) |
| `hop-distributions` | Zusammenstellung und Prüfung der Hop-Distribution | Keine AGENTS.md; [README mit Build und E2E](hop-distributions/README.md) |
| `hop-plugins-site` | Quarto-Website, Katalog und Tutorials | Keine AGENTS.md; [README mit Entwicklung und Validierung](hop-plugins-site/README.md) |
