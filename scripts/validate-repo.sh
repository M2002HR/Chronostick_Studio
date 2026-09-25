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

if ! python - "$repo_root" <<'PY'
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
episode = root / "episodes/002-hiroshima-final-minute"
jobs = sorted((episode / "automation/jobs").glob("clip-*.json"))
errors = []
expected_seeds = list(range(1945080601, 1945080618))
seen_seeds = []

if episode.exists() and len(jobs) != 17:
    errors.append(f"Episode 002 requires 17 job JSON files; found {len(jobs)}")

for path in jobs:
    try:
        job = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{path.relative_to(root)}: invalid JSON: {exc}")
        continue
    if job.get("schema_version") != "1.0" or job.get("template") != "h3_ref2va":
        errors.append(f"{path.relative_to(root)}: wrong schema_version or template")
    prompt_value = job.get("prompt", {}).get("file")
    prompt = root / prompt_value if isinstance(prompt_value, str) else None
    if not prompt or not prompt.is_file():
        errors.append(f"{path.relative_to(root)}: prompt file does not exist")
        continue
    text = prompt.read_text(encoding="utf-8")
    refs = job.get("references")
    if not isinstance(refs, list) or not 2 <= len(refs) <= 4:
        errors.append(f"{path.relative_to(root)}: expected 2-4 ordered references")
        continue
    tags = {int(value) for value in re.findall(r"<Picture\s+(\d+)>", text, flags=re.IGNORECASE)}
    if tags != set(range(1, len(refs) + 1)):
        errors.append(f"{path.relative_to(root)}: Picture tags {sorted(tags)} do not map exactly to {len(refs)} references")
    for index, ref in enumerate(refs, 1):
        value = ref.get("path") if isinstance(ref, dict) else ref
        if not isinstance(value, str) or not (root / value).is_file():
            errors.append(f"{path.relative_to(root)}: missing Picture {index} asset {value!r}")
    generation = job.get("generation", {})
    required_generation = {
        "aspect_ratio": "9:16", "megapixel": 0.4, "width": 480, "height": 864,
        "duration_seconds": 5, "fps": 24, "steps": 12, "sampler": "res_multistep",
        "scheduler": "beta", "lightning": False, "ref_image_size": "match",
    }
    for key, expected in required_generation.items():
        if generation.get(key) != expected:
            errors.append(f"{path.relative_to(root)}: generation.{key} must be {expected!r}")
    seed = generation.get("seed")
    if not isinstance(seed, int) or generation.get("seed_mode") != "fixed":
        errors.append(f"{path.relative_to(root)}: explicit fixed seed required")
    else:
        seen_seeds.append(seed)
    audio = job.get("audio", {})
    required_audio = {"enabled": True, "mode": "sfx_only", "dialogue": False, "narration": False, "music": False, "require_audio_stream": True}
    for key, expected in required_audio.items():
        if audio.get(key) != expected:
            errors.append(f"{path.relative_to(root)}: audio.{key} must be {expected!r}")
    output = job.get("output", {})
    if output.get("overwrite") is not False or output.get("editorial_duration_seconds") != 5:
        errors.append(f"{path.relative_to(root)}: output must be revision-safe with 5-second editorial normalization")
    if output.get("directory") != "episodes/002-hiroshima-final-minute/renders/raw" or output.get("editorial_directory") != "episodes/002-hiroshima-final-minute/renders/editorial":
        errors.append(f"{path.relative_to(root)}: raw/editorial output directories are incorrect")
    if text.count("NO BACKGROUND MUSIC. Natural diegetic sound effects only.") != 1:
        errors.append(f"{prompt.relative_to(root)}: exact audio policy must occur once")
    for required in ("NON-NEGOTIABLE STICK-WORLD STYLE LOCK", "AUDIO LOCK — SFX ONLY", "HOOK"):
        if required not in text:
            errors.append(f"{prompt.relative_to(root)}: missing {required!r}")
    if text.count("HARD CUT") < 6:
        errors.append(f"{prompt.relative_to(root)}: at least six explicit HARD CUT instructions required")
    spans = [(float(start), float(end)) for start, end in re.findall(r"(?m)^(\d+\.\d+)–(\d+\.\d+):", text)]
    if not 7 <= len(spans) <= 9:
        errors.append(f"{prompt.relative_to(root)}: expected 7-9 precisely timed shots; found {len(spans)}")
    elif spans[0][0] != 0 or spans[-1][1] != 5 or any(left[1] != right[0] for left, right in zip(spans, spans[1:])):
        errors.append(f"{prompt.relative_to(root)}: shot timing must be contiguous from 0.00 through 5.00")
    if not re.search(r"\b(?:no|zero)\b[^.\n]{0,100}\b(?:photoreal\w*|photograph\w*)\b", text, flags=re.IGNORECASE):
        errors.append(f"{prompt.relative_to(root)}: missing explicit photorealism prohibition")
    clip_number = int(path.name.split("-")[1])
    expected_revision = f"episode-002-clip-{clip_number:02d}-r002"
    if job.get("job_identity") != expected_revision:
        errors.append(f"{path.relative_to(root)}: job_identity must be {expected_revision}")
    prefix = output.get("prefix", "")
    if not prefix.endswith("-r002"):
        errors.append(f"{path.relative_to(root)}: output prefix must use revision r002")

if jobs and sorted(seen_seeds) != expected_seeds:
    errors.append("Episode 002 seeds must be the unique fixed range 1945080601-1945080617")

settings_path = episode / "automation/batch-settings.json"
if episode.exists():
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        expected = {"continue_on_error": True, "stop_on_error": False, "max_retries": 2, "concat_on_complete": False, "upscale_on_complete": False}
        if settings != expected:
            errors.append("Episode 002 batch settings do not match the approved first-pass policy")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Episode 002 batch settings are invalid: {exc}")

for error in errors:
    print(f"FAIL {error}")
raise SystemExit(bool(errors))
PY
then
  failures=$((failures + 1))
fi

if find assets -type f \( -name '*.png.png' -o -path '*/assets/worlds/assets/*' \) | grep -q .; then
  printf 'FAIL malformed asset path or duplicate extension found\n'
  failures=$((failures + 1))
fi

while IFS= read -r asset_path; do
  if [[ ! -f "$asset_path" ]]; then
    printf 'FAIL referenced asset does not exist: %s\n' "$asset_path"
    failures=$((failures + 1))
  fi
done < <(rg -No 'assets/[a-zA-Z0-9_./-]+\.(png|jpg|jpeg|webp)' docs/specs/README.md docs/specs/worlds/world-hiroshima-summer-1945.md docs/specs/characters/character-hiroshima-*.md docs/specs/vehicles episodes/*/README.md episodes/*/plan/*.md | awk -F: '{print $NF}' | sort -u)

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
