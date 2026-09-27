#!/usr/bin/env bash

set -euo pipefail

episode_root="${CHRONOSTICK_EPISODE_ROOT:-/home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute}"
automation_root="${COMFY_VIDEO_AUTOMATION_ROOT:-/home/mhr/AI/comfy-video-automation}"
service_url="${COMFY_VIDEO_SERVICE_URL:-http://127.0.0.1:8090}"
input_dir="$episode_root/renders/final-selected"
output_dir="$episode_root/final"

mkdir -p "$input_dir" "$output_dir"

mapfile -d '' -t clips < <(
  find "$input_dir" -maxdepth 1 -type f \
    \( -iname '*.mp4' -o -iname '*.mkv' -o -iname '*.webm' -o -iname '*.mov' \) \
    -print0 | sort -zV
)

if (( ${#clips[@]} != 17 )); then
  printf 'Expected exactly 17 selected video files in %s; found %d.\n' "$input_dir" "${#clips[@]}" >&2
  printf 'Keep exactly one file for each clip, named clip-01-... through clip-17-....\n' >&2
  exit 1
fi

declare -A seen=()
for clip in "${clips[@]}"; do
  filename="${clip##*/}"
  if [[ ! "$filename" =~ ^clip-([0-9]{2})-.*\.(mp4|mkv|webm|mov)$ ]]; then
    printf 'Invalid selected filename: %s\n' "$filename" >&2
    printf 'Required form: clip-NN-description-rNNN.ext\n' >&2
    exit 1
  fi
  number="${BASH_REMATCH[1]}"
  if [[ -n "${seen[$number]:-}" ]]; then
    printf 'Duplicate selected clip number %s: %s and %s\n' "$number" "${seen[$number]}" "$filename" >&2
    exit 1
  fi
  seen[$number]="$filename"
done

for number in $(seq -w 1 17); do
  if [[ -z "${seen[$number]:-}" ]]; then
    printf 'Missing selected clip number %s in %s\n' "$number" "$input_dir" >&2
    exit 1
  fi
done

revision=1
while :; do
  printf -v suffix 'r%03d' "$revision"
  output="$output_dir/episode-002-hiroshima-final-minute-$suffix.mp4"
  [[ -e "$output" || -e "${output%.mp4}.run.json" ]] || break
  revision=$((revision + 1))
done

printf 'Selected clip order:\n'
for number in $(seq -w 1 17); do
  printf '  %s  %s\n' "$number" "${seen[$number]}"
done
printf 'Output: %s\n' "$output"

curl --fail --silent --show-error "$service_url/v1/ready" >/dev/null

cd "$automation_root"
uv run comfy-video concat \
  --service-url "$service_url" \
  --directory "$input_dir" \
  --output "$output" \
  --missing-audio fail \
  --watch

printf 'Final assembly completed: %s\n' "$output"
