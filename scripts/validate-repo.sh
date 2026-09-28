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
    if not isinstance(refs, list) or not 1 <= len(refs) <= 2:
        errors.append(f"{path.relative_to(root)}: expected 1-2 generation-safe ordered references")
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
        "duration_seconds": 5, "fps": 24, "steps": 16, "sampler": "res_multistep",
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
    clip_number = int(path.name.split("-")[1])
    for required in ("REFERENCE", "AUDIO", "HOOK", "END STATE"):
        if required not in text:
            errors.append(f"{prompt.relative_to(root)}: missing {required!r}")
    if clip_number != 17 and text.count("HARD CUT") < 1:
        errors.append(f"{prompt.relative_to(root)}: at least one explicit HARD CUT instruction required")
    spans = [(float(start), float(end)) for start, end in re.findall(r"(?m)^(\d+\.\d+)–(\d+\.\d+)(?::|\s+[—-])", text)]
    if not 3 <= len(spans) <= 4:
        errors.append(f"{prompt.relative_to(root)}: expected 3-4 precisely timed shots; found {len(spans)}")
    elif spans[0][0] != 0 or spans[-1][1] != 5 or any(left[1] != right[0] for left, right in zip(spans, spans[1:])):
        errors.append(f"{prompt.relative_to(root)}: shot timing must be contiguous from 0.00 through 5.00")
    if not re.search(r"\b(?:no|zero)\b[^.\n]{0,100}\b(?:photoreal\w*|photograph\w*)\b", text, flags=re.IGNORECASE):
        errors.append(f"{prompt.relative_to(root)}: missing explicit photorealism prohibition")
    expected_revision = f"episode-002-clip-{clip_number:02d}-r003"
    if job.get("job_identity") != expected_revision:
        errors.append(f"{path.relative_to(root)}: job_identity must be {expected_revision}")
    prefix = output.get("prefix", "")
    if not prefix.endswith("-r003"):
        errors.append(f"{path.relative_to(root)}: output prefix must use revision r003")

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

if ! python - "$repo_root" <<'PY'
import hashlib
import json
import math
import os
import sys
from pathlib import Path

root = Path(sys.argv[1])
errors = []
defaults_path = root / "docs/pipeline/production-defaults.json"

try:
    defaults = json.loads(defaults_path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError) as exc:
    errors.append(f"{defaults_path.relative_to(root)}: invalid JSON: {exc}")
    defaults = {}

tail_defaults = defaults.get("tail_extension", {})
expected_tail_defaults = {
    "enabled": True,
    "mode": "freeze_last_frame",
    "maximum_seconds": 1.0,
    "apply_after_concat_before_upscale": True,
    "generated_audio_fill": "silence",
    "external_narration_continues": True,
    "requires_resolved_final_frame": True,
    "script": "scripts/extend-last-frame.sh",
}
for key, expected in expected_tail_defaults.items():
    if tail_defaults.get(key) != expected:
        errors.append(f"docs/pipeline/production-defaults.json: tail_extension.{key} must be {expected!r}")

tail_script = root / str(tail_defaults.get("script", ""))
if not tail_script.is_file() or not os.access(tail_script, os.X_OK):
    errors.append("Configured tail-extension script is missing or not executable")

for timing_path in sorted(root.glob("episodes/*/timestamps/timing-map.json")):
    try:
        timing = json.loads(timing_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"{timing_path.relative_to(root)}: invalid JSON: {exc}")
        continue

    editorial = timing.get("editorial", {})
    tail = editorial.get("tail_extension", {})
    if not tail.get("enabled"):
        continue

    episode_root = timing_path.parent.parent
    clip_seconds = editorial.get("clip_seconds")
    generated_count = editorial.get("generated_clip_count")
    narration_end = timing.get("narration", {}).get("spoken_end")
    duration = tail.get("duration_seconds")
    maximum = tail.get("maximum_allowed_seconds")
    start = tail.get("start")
    end = tail.get("end")

    numeric_values = [clip_seconds, generated_count, narration_end, duration, maximum, start, end]
    if not all(isinstance(value, (int, float)) for value in numeric_values):
        errors.append(f"{timing_path.relative_to(root)}: tail-extension timing values must be numeric")
        continue

    if tail.get("mode") != "freeze_last_frame":
        errors.append(f"{timing_path.relative_to(root)}: unsupported tail extension mode")
    if duration <= 0 or duration > maximum or maximum > tail_defaults.get("maximum_seconds", 0):
        errors.append(f"{timing_path.relative_to(root)}: tail extension exceeds the configured limit")
    if not math.isclose(generated_count * clip_seconds, start, abs_tol=1e-6):
        errors.append(f"{timing_path.relative_to(root)}: tail start does not follow complete generated slots")
    if not math.isclose(end, narration_end, abs_tol=1e-6):
        errors.append(f"{timing_path.relative_to(root)}: tail end must equal narration end")
    if not math.isclose(duration, end - start, abs_tol=1e-6):
        errors.append(f"{timing_path.relative_to(root)}: tail duration arithmetic is inconsistent")
    if editorial.get("default_ceil_clip_count") != math.ceil(narration_end / clip_seconds):
        errors.append(f"{timing_path.relative_to(root)}: default ceiling clip count is incorrect")
    if editorial.get("final_duration_seconds") != narration_end:
        errors.append(f"{timing_path.relative_to(root)}: final duration must equal narration end")
    if tail.get("generated_audio_fill") != "silence" or tail.get("external_narration_continues") is not True:
        errors.append(f"{timing_path.relative_to(root)}: tail audio policy is invalid")
    if tail.get("requires_resolved_final_frame") is not True:
        errors.append(f"{timing_path.relative_to(root)}: tail must require a resolved final frame")

    source = timing.get("source", {})
    source_path = episode_root / str(source.get("path", ""))
    if not source_path.is_file():
        errors.append(f"{timing_path.relative_to(root)}: timing source does not exist")
    elif hashlib.sha256(source_path.read_bytes()).hexdigest() != source.get("sha256"):
        errors.append(f"{timing_path.relative_to(root)}: timing source hash mismatch")

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

if ! python scripts/validate-localizations.py "$repo_root"; then
  failures=$((failures + 1))
fi

if (( failures > 0 )); then
  printf 'Validation failed with %d issue(s).\n' "$failures"
  exit 1
fi

printf 'Validation passed. Warnings above are intentional gaps that must remain documented.\n'
