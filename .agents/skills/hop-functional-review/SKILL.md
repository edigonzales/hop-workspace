---
name: hop-functional-review
description: >-
  Für funktionale Reviews von Apache-Hop-Plugins. Prüft Architektur, SWT-Dialoge,
  gespeicherte Metadaten, Schema, Laufzeit, Plugin-Integration und Distribution
  anhand konkreter Benutzerabläufe und gezielter Regressionstests.
---

# Funktionales Hop-Review

## Benutzerablauf verfolgen

Gehe eine konkrete Pipeline oder einen Workflow durch: Benutzerkonfiguration
→ gespeicherte Metadaten → `getFields(...)`/Schema bei Transforms
→ Runtime → Ergebnis. Prüfe konfigurierbare Optionen und verarbeitete Daten.
Vergleiche Vorschau und Laufzeit. Prüfe Fehlerpfade, Abbruch und
Ressourcenfreigabe. Suche dokumentierte, aber nicht ausgeführte Funktionen und
relevante Lücken in den Regressionstests.

Prüfe Transform- und Action-Lebenszyklus, Metadaten und XML-Serialisierung,
Pluginregistrierung, `RowMeta` und `ValueMeta` sowie Classloader und gemeinsame
Datentypen an ihren tatsächlichen Übergängen. Öffne repräsentative gespeicherte
Pipelines und Workflows, wo dies für den Befund nötig ist. Nutze bei
Integrationsfragen das gepackte Plugin in einer isolierten Hop-Distribution mit
`hop-run` oder den vorhandenen Runtime-E2E-Tests. Verwende die vorhandene
Hop-Laufzeit und Testinfrastruktur.

## SWT aus Benutzersicht prüfen

Durchlaufe typische Aufgaben im Dialog. Prüfe Beschriftungen, Defaults,
Pflichtfelder, nötige Bedienhandlungen und technische Optionen im normalen
Benutzerpfad. Prüfe Validierungs- und Fehlermeldungen, Mapping und Vorschau
sowie Speichern, Wiederöffnen und Abbrechen. Wenn nur der Quellcode geprüft
werden konnte, benenne die fehlende interaktive GUI-Abnahme ausdrücklich.

## INTERLIS und ilitransformer

Prüfe bei INTERLIS-Plugins die Modellsemantik und Modellversionen, OID, TID,
Basket und BID, Vererbung, Strukturen und BAG/LIST, Referenzen und Assoziationen
sowie Geometrien. Beurteile XTF-Roundtrip und Validierung anhand der fachlichen
Ergebnisse.

Bei ilitransformer gehört die Migrationssemantik in ilitransformer. Hop stellt
die Integration und Bedienoberfläche bereit. Achte auf eine einzige
Mapping-Engine und wiederverwendete Modell- und Validierungslogik. Prüfe, ob
die GUI häufige Fälle abdeckt, die DSL komplexere Fälle ermöglicht und
bestehende Grenzen für Benutzer sichtbar sind.

## Befunde

Benenne bestätigte Fehler, begründete Risiken, fehlende Funktionen, UX-Mängel,
unnötige technische Komplexität und bewusst sinnvolle Architektur. Belege
relevante Befunde mit dem betroffenen Ablauf und bereits ausgeführten Prüfungen.
Priorisiere nach fachlicher Auswirkung und Aufwand. Halte offene Prüfungen fest.
