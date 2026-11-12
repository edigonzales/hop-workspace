#!/usr/bin/env bash
# Eigenständige Repositories direkt neben diesem Skript klonen/aktualisieren.
set -o pipefail

usage() {
  cat <<'EOF'
Aufruf: ./checkout.sh [REPOSITORY ...]
        ./checkout.sh --help

Ohne Argumente werden alle Einträge aus repositories.txt bearbeitet.
Fehlende Repos werden auf main geklont; saubere main-Checkouts werden
ausschliesslich per Fast-forward aktualisiert. Lokale Arbeit bleibt erhalten.

Exitcodes: 0 = Erfolg, 1 = Bearbeitungsfehler, 2 = ungültiger Aufruf/Projektliste.
EOF
}

contains() {
  local needle="$1" item
  shift
  for item in "$@"; do
    [[ "$item" != "$needle" ]] || return 0
  done
  return 1
}

checkout_repo() {
  local repo="$1" destination="$workspace_dir/$1"
  local url="https://github.com/edigonzales/$1.git" top origin branch status

  if [[ ! -e "$destination" && ! -L "$destination" ]]; then
    printf '%s: klonen (main)\n' "$repo"
    git clone --branch main -- "$url" "$destination" || return 1
    return 0
  fi

  if [[ ! -d "$destination" || -L "$destination" ]]; then
    printf '%s: Zielpfad ist belegt oder ein Symlink.\n' "$repo" >&2
    return 1
  fi
  top="$(git -C "$destination" rev-parse --show-toplevel 2>/dev/null)" || top=""
  if [[ "$top" != "$destination" ]]; then
    printf '%s: Ziel ist kein eigenes Git-Toplevel.\n' "$repo" >&2
    return 1
  fi

  # Die konfigurierte URL prüfen; Git darf sie z.B. für lokale Tests umschreiben.
  origin="$(git -C "$destination" config --get-all remote.origin.url)" || origin=""
  case "$origin" in
    "https://github.com/edigonzales/$repo"|"https://github.com/edigonzales/$repo.git"|\
    "git@github.com:edigonzales/$repo"|"git@github.com:edigonzales/$repo.git"|\
    "ssh://git@github.com/edigonzales/$repo"|"ssh://git@github.com/edigonzales/$repo.git") ;;
    *) printf '%s: Origin entspricht nicht dem erwarteten GitHub-Repository.\n' "$repo" >&2
       return 1 ;;
  esac

  branch="$(git -C "$destination" symbolic-ref --quiet --short HEAD)" || branch=""
  if [[ "$branch" != main ]]; then
    printf '%s: Branch ist %s; main erforderlich.\n' "$repo" "${branch:-detached HEAD}" >&2
    return 1
  fi
  status="$(git -C "$destination" status --porcelain --untracked-files=normal)" || return 1
  if [[ -n "$status" ]]; then
    printf '%s: Lokale Änderungen oder unversionierte Dateien; kein Update.\n' "$repo" >&2
    return 1
  fi

  printf '%s: main prüfen/aktualisieren\n' "$repo"
  git -C "$destination" fetch --no-tags origin refs/heads/main || return 1
  git -C "$destination" merge --ff-only FETCH_HEAD || return 1
}

if [[ $# -eq 1 && "$1" == --help ]]; then
  usage
  exit 0
fi
workspace_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)" || exit 1
if ! command -v git >/dev/null 2>&1; then
  printf 'Git wird benötigt.\n' >&2
  exit 1
fi
if [[ ! -r "$workspace_dir/repositories.txt" ]]; then
  printf 'repositories.txt fehlt oder ist nicht lesbar.\n' >&2
  exit 2
fi

repositories=()
while IFS= read -r repo || [[ -n "$repo" ]]; do
  if [[ ! "$repo" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || contains "$repo" "${repositories[@]}"; then
    printf 'Ungültiger oder doppelter Eintrag in repositories.txt: %s\n' "$repo" >&2
    exit 2
  fi
  repositories+=("$repo")
done < "$workspace_dir/repositories.txt"
if [[ ${#repositories[@]} -eq 0 ]]; then
  printf 'repositories.txt ist leer.\n' >&2
  exit 2
fi

selected=("$@")
if [[ $# -eq 0 ]]; then
  selected=("${repositories[@]}")
fi
# Alle Argumente vor der ersten Gitoperation prüfen.
for repo in "${selected[@]}"; do
  if ! contains "$repo" "${repositories[@]}"; then
    printf 'Unbekanntes Repository: %s\n' "$repo" >&2
    usage >&2
    exit 2
  fi
done

failed=0
for repo in "${selected[@]}"; do
  if ! checkout_repo "$repo"; then
    printf '%s: FEHLER; weitere Repositories werden bearbeitet.\n' "$repo" >&2
    failed=$((failed + 1))
  fi
done
printf '%s Repositories bearbeitet, %s Fehler.\n' "${#selected[@]}" "$failed"
[[ "$failed" -eq 0 ]]
