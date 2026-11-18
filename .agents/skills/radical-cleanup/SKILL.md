---
name: radical-cleanup
description: >-
  Für radikale Bereinigungen bestehender Codebasen, auch über Repositorygrenzen.
  Entfernt unnötige Infrastruktur und vereinfacht Build, CI, Tests, Packaging,
  Caches, Fingerprints und Zustandsmaschinen. Ein gewöhnlicher Featureauftrag
  allein löst diesen Skill nicht aus.
---

# Radikale Bereinigung

1. **Verstehen.** Verfolge den Mechanismus von seinen Einstiegspunkten bis zu
   seinen tatsächlichen Verbrauchern. Kläre Funktion, verantwortliche
   Komponente und öffentliche oder gespeicherte Verträge. Prüfe, welche
   vorhandene Standardfunktion dieselbe Aufgabe erfüllt.
2. **Hinterfragen.** Kann der Mechanismus ganz weg? Ist die Aufgabe bereits
   anderswo gelöst? Suche doppelte Zustände, Prüfungen und Metadatenquellen,
   ungenutzte Kompatibilität, Prüfungen für andere Prüfungen und Tests für
   produktiv ungenutzte Implementierungen. Benenne bei jedem Hash den
   konkreten Entscheid, den er absichert.
3. **Entscheiden.**
   - **KEEP** gilt bei einem konkret belegten Bedarf, etwa einer fachlichen
     Funktion, einem verwendeten Vertrag oder einer echten Schutzgrenze.
   - **DELETE** entfernt den Mechanismus mitsamt dadurch überflüssigen Tests,
     Konfigurationen, Dokumentation und Hilfsmechanismen.
   - **SIMPLIFY** reduziert eine notwendige Funktion auf einfachere vorhandene
     Mechanismen.
4. **Umsetzen.** Ändere in kleinen Schritten beim zuständigen Projekt. Vermeide
   vorsorgliche Abstraktionen, Frameworks, Kompatibilitätsschichten,
   Ersatz-Fingerprints und eigene Prüfprotokolle.
5. **Verifizieren.** Prüfe fachliche Auswirkungen über betroffene Verbraucher
   und führe relevante Tests aus. Vergleiche entfernten und hinzugefügten Code,
   Zustand und Infrastruktur. Prüfe, ob mitgelöschte Tests und Dokumentation
   wirklich entbehrlich sind. Verwende ein unabhängiges Review, wenn beauftragt.

Fasse kurz zusammen, was entfernt, vereinfacht und bewusst behalten wurde,
welche fachlichen Risiken du geprüft und welche Tests du ausgeführt hast
und was offen bleibt.
