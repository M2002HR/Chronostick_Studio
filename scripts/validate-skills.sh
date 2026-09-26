#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
validator="${CODEX_HOME:-${HOME}/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"

if [[ ! -f "$validator" ]]; then
  printf 'ERROR skill validator not found: %s\n' "$validator" >&2
  exit 1
fi

while IFS= read -r skill_file; do
  skill_dir="$(dirname "$skill_file")"
  python "$validator" "$skill_dir"
done < <(find "$repo_root/skills" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | sort)
