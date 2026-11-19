# Hop-Workspace

## Arbeitsbereich

Der Workspace ist der gemeinsame Einstiegspunkt. [repositories.txt](repositories.txt)
bestimmt den Checkout-Bestand. Jedes Unterrepository hat sein eigenes Git,
seinen eigenen Build und seine eigenen Pull Requests. Der Workspace verwaltet
seine eigenen Dateien.

Vor Änderungen die `AGENTS.md` des betroffenen Projekts und die einschlägigen
Projektanleitungen lesen. Fehlt eine `AGENTS.md`, gelten README, Build und
Entwicklungsdokumentation als Einstieg. Beim direkten Einstieg in ein Plugin
den Workspace-Kontext bei Bedarf ausdrücklich einlesen. Über Git-Grenzen hinweg
keine automatische Vererbung voraussetzen.

Vor Git-Operationen Toplevel, Branch, Origin und lokale Änderungen prüfen.
Änderungen und Commits dem verantwortlichen Repository zuordnen, fremde lokale
Arbeit schützen und nur die für den Auftrag nötigen Repositories bearbeiten.
`checkout.sh` gezielt für einen benötigten Checkout oder ein beauftragtes
Update verwenden. Nur auf ausdrücklichen Auftrag mergen.

## Vereinfachung und Verträge

Ockhams Rasiermesser gilt verbindlich. Zuerst prüfen, ob ein Mechanismus ganz
entfallen kann. Wo er gebraucht wird, vorhandene Standardfunktionen bevorzugen
und Code, Zustand, Infrastruktur und Sonderfälle klein halten. Für jede
fachliche oder technische Entscheidung eine massgebliche Quelle pflegen.

Abstraktionen, generische Frameworks, Adapter, Kompatibilitätsschichten und
Zustandsmaschinen brauchen einen konkreten Anwendungsfall. Prüfinfrastruktur
braucht einen Fehler, den sie tatsächlich verhindert oder sichtbar macht.
Doppelte Manifeste oder Nachweissysteme, rein kosmetische Prüfungen und Tests
der eigenen Prüfinfrastruktur vermeiden. Prüfsummen und Fingerprints brauchen
einen konkreten Zweck, etwa Artefaktintegrität oder sichere Strukturupdates.
Zusätzliche Sicherheitsprüfungen brauchen einen realen Schutzbedarf.
Gelöschte Infrastruktur nur ersetzen, wenn eine benötigte Funktion sonst entfällt.

Fachliche Validierung, Datenintegrität, reale Sicherheitsgrenzen,
Ressourcenfreigabe, Transaktions- und Fehlersemantik, notwendige Streaming- und
Speichergrenzen sowie produktive Benutzerabläufe erhalten. Gemeinsame
Geometry-, Raster- und Point-Cloud-Typen und ihre Classloader-Identität an den
vorgesehenen Grenzen bewahren. Gemeinsame Bibliotheken über die vorgesehenen
Plugin-Abhängigkeiten beziehen.

Bei Änderungen an veröffentlichten Plugin-IDs, Datenformaten oder gespeicherten
Hop-Pipelines und Metadaten tatsächliche Verbraucher und Auswirkungen prüfen.
Genutzte Verträge erhalten oder eine notwendige Migration absichern.
Ungenutzte Interna und unveröffentlichte Prototypen direkt ändern oder entfernen.
Deprecation-Schichten brauchen tatsächlich betroffene Verbraucher.

## Umsetzung und Prüfung

Mit einer Bestandsaufnahme beginnen und in kleinen Schritten ändern. Gemeinsame
Logik und Dokumentation beim zuständigen Projekt pflegen. Überholte Anleitungen
und Beispiele mit der betreffenden Funktion entfernen oder aktualisieren.
Versionen und Buildbefehle aus dem jeweiligen Projekt übernehmen. Bestehende
Projektregeln und Pflichtchecks zuerst verstehen. Bei ausdrücklich beauftragten
Bereinigungen dürfen unnötige Checks, Konventionen, Kompatibilitätsschichten
und ihre Infrastruktur vollständig entfallen. Fachlich und technisch
erforderliche Prüfungen bleiben erhalten.

Den Prüfumfang an der Änderung ausrichten. Wenige aussagekräftige
Regressionstests für beobachtbares Verhalten bevorzugen und relevante
Abdeckung erhalten. Feste Coverage-Quoten vermeiden. Eigene Testharnesses
nur bei zwingendem Bedarf einführen. Echte Pipeline-, Plugin- und
Integrationstests einsetzen, wenn die Änderung diese Grenzen berührt.
Gemeinsame Laufzeittypen, native Bibliotheken und Classloader mit den
erforderlichen Integrationsprüfungen absichern. Installierte Tests in einer
isolierten Hop-Installation ausführen. Für reine Workspace-Änderungen die
[Workspace-Checks](README.md#workspace-prüfen) und betroffene Links prüfen.

Den Diff abschliessend auf verbliebene Komplexität und fachliche Risiken prüfen.
Ein beauftragtes unabhängiges Review auf konkrete Fehler und Risiken ausrichten.
Ausgeführte Checks und Blockierungen benennen.
