# hop-workspace

Gemeinsamer Einstiegspunkt für die Apache-Hop-Plugins und ihre Helfer.
[repositories.txt](repositories.txt) bestimmt, welche Repositories zum Workspace
gehören. Sie liegen direkt unter diesem Verzeichnis und sind vom Workspace-Git
ignoriert. Jedes Repository verwaltet seinen eigenen Build, seine Commits und
seine Pull Requests. Es gibt keine Git-Submodules und keinen Sammelbuild.

## Repositories bereitstellen

`checkout.sh` benötigt Git, Bash ab 3.2 und Zugriff auf GitHub. Gib die benötigten
Repositories an oder verwende den Aufruf ohne Argumente für die gesamte Liste.

```bash
./checkout.sh hop-interlis-plugin hop-geometry-type-plugin
./checkout.sh --help
```

Das Skript klont fehlende Repositories auf `main` und aktualisiert vorhandene
saubere `main`-Checkouts per Fast-forward. Es schützt lokale Arbeit und meldet
unter anderem geänderte, divergierte oder auf einem anderen Branch stehende
Checkouts als Fehler. Weitere ausgewählte Repositories werden trotzdem bearbeitet.
Für ein neues Projekt den Namen des `edigonzales`-Repositories mit Branch
`main` in `repositories.txt` eintragen, einen Namen pro Zeile. Bindestriche
trennen Gruppen aus Kleinbuchstaben und Ziffern. Das Verzeichnis in
`.gitignore` ergänzen.

## Mit Codex arbeiten

Codex vorzugsweise in `hop-workspace/` starten. Die Root-[AGENTS.md](AGENTS.md)
enthält die dauerhaften Arbeitsregeln. Lies vor Pluginänderungen auch die
projektspezifischen Anweisungen. Benenne im Auftrag Ziele, betroffene Repositories
und Abnahmebedingungen. Führe Git-Befehle im zuständigen Repository aus, zum
Beispiel `git -C hop-interlis-plugin status --short --branch`. Für Änderungen
an einem Plugin gehört der PR in dessen Repository.

Codex kann die Workspace-Skills unter `.agents/skills/` passend zum Auftrag
auswählen. Du kannst sie auch ausdrücklich aufrufen.

- [`$radical-cleanup`](.agents/skills/radical-cleanup/SKILL.md) hilft beim Entfernen
  unnötiger Mechanismen und beim Vereinfachen verbleibender Funktionen.
- [`$hop-functional-review`](.agents/skills/hop-functional-review/SKILL.md) prüft
  Hop-Plugins vom Dialog und den Metadaten bis zum Ergebnis in der Laufzeit.

Beispielauftrag für mehrere Repositories

> Nutze $radical-cleanup, um doppelte Packaging-Prüfungen in
> hop-interlis-plugin und hop-plugin-ci zu untersuchen. Prüfe zuerst die
> Verbraucher und entferne nur nachweislich redundante Prüfungen.
> Führe die betroffenen Projektchecks aus und halte die Diffs getrennt.

Codex ermittelt AGENTS-Dateien und Repository-Skills relativ zum aktuellen
Git-Root. Starte für Workspace-Discovery im Workspace-Root. Wenn du direkt in
einem Plugin startest, bitte Codex bei Bedarf ausdrücklich, `../AGENTS.md` und
die passende `../.agents/skills/<name>/SKILL.md` zu lesen. [AGENTS.md-Discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
und [Skill-Discovery](https://learn.chatgpt.com/docs/build-skills).

### Codex Cloud

Auch in Codex Cloud müssen `hop-workspace` und die für den Auftrag nötigen
Unterrepositories beim Arbeitsbeginn in der erwarteten Verzeichnisstruktur
verfügbar sein. Ein Checkout des Workspace-Repositories allein enthält die
Plugins nicht. Wenn du sie über `checkout.sh` bereitstellst, muss die Umgebung
GitHub erreichen können. Commits und PRs bleiben pro Repository getrennt.
Der Start eines Cloud-Auftrags mit dieser Checkout-Struktur ist noch zu prüfen.
[Codex-Cloud-Umgebungen](https://learn.chatgpt.com/docs/environments/cloud-environments).

## Workspace prüfen

Die Skripttests benötigen Git und Python ab 3.9 und verwenden temporäre lokale
Git-Repositories.

```bash
bash -n checkout.sh
./checkout.sh --help
python3 -m unittest discover -s tests -v
git diff --check
```

Inspiriert von [dateninfrastruktur-workspace](https://github.com/sogis/dateninfrastruktur-workspace).
