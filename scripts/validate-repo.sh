#!/usr/bin/env bash

set -u

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root" || exit 1

failures=0
no_music='NO BACKGROUND MUSIC. Natural diegetic sound effects only.'

while IFS= read -r prompt_file; do
  if [[ ! -s "$prompt_file" ]]; then
    printf 'WARN empty prompt (document in episode manifest): %s\n' "$prompt_file"
    continue
  fi

  first_line="$(sed -n '1p' "$prompt_file")"
  if [[ "$first_line" == '---' ]]; then
    printf 'FAIL prompt starts with metadata: %s\n' "$prompt_file"
    failures=$((failures + 1))
  fi

  if rg -q '^# (Purpose|Approval|Generation Log|Review Checklist)|^status:' "$prompt_file"; then
    printf 'FAIL internal documentation found in prompt: %s\n' "$prompt_file"
    failures=$((failures + 1))
  fi
done < <({ find prompts/image -type f -name '*.md'; find episodes -path '*/prompts/*.md' -type f; } | sort)

while IFS= read -r video_prompt; do
  [[ -s "$video_prompt" ]] || continue
  if ! rg -Fq "$no_music" "$video_prompt"; then
    printf 'FAIL missing exact audio policy: %s\n' "$video_prompt"
    failures=$((failures + 1))
  fi
done < <(find episodes -path '*/prompts/*.md' -type f | sort)

if find assets -type f \( -name '*.png.png' -o -path '*/assets/worlds/assets/*' \) | grep -q .; then
  printf 'FAIL malformed asset path or duplicate extension found\n'
  failures=$((failures + 1))
fi

while IFS= read -r asset_path; do
  if [[ ! -f "$asset_path" ]]; then
    printf 'FAIL referenced asset does not exist: %s\n' "$asset_path"
    failures=$((failures + 1))
  fi
done < <(rg -No 'assets/[a-zA-Z0-9_./-]+\.(png|jpg|jpeg|webp)' docs/specs/README.md episodes/*/README.md episodes/*/plan/*.md | awk -F: '{print $NF}' | sort -u)

if ! git diff --check; then
  failures=$((failures + 1))
fi

if ! git diff --cached --check; then
  failures=$((failures + 1))
fi

if (( failures > 0 )); then
  printf 'Validation failed with %d issue(s).\n' "$failures"
  exit 1
fi

printf 'Validation passed. Warnings above are intentional gaps that must remain documented.\n'
