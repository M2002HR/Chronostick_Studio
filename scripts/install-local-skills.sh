#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skill_source="$repo_root/skills"
codex_root="${CODEX_HOME:-${HOME}/.codex}"
skill_target="$codex_root/skills"

mkdir -p "$skill_target"

while IFS= read -r skill_file; do
  source_dir="$(dirname "$skill_file")"
  skill_name="$(basename "$source_dir")"
  target="$skill_target/$skill_name"
  if [[ -L "$target" && "$(readlink -f "$target")" == "$source_dir" ]]; then
    printf 'OK already linked: %s\n' "$skill_name"
    continue
  fi
  if [[ -e "$target" || -L "$target" ]]; then
    printf 'ERROR refusing to replace existing skill: %s\n' "$target" >&2
    exit 1
  fi
  ln -s "$source_dir" "$target"
  printf 'OK linked: %s -> %s\n' "$skill_name" "$source_dir"
done < <(find "$skill_source" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | sort)
