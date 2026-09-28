#!/usr/bin/env bash

set -euo pipefail

usage() {
  printf 'Usage: %s INPUT.mp4 OUTPUT.mp4 HOLD_SECONDS\n' "${0##*/}" >&2
  printf 'Clones the final video frame, pads existing audio with silence, and never overwrites output.\n' >&2
}

if (( $# != 3 )); then
  usage
  exit 2
fi

input="$1"
output="$2"
hold_seconds="$3"
max_hold_seconds="${CHRONOSTICK_MAX_TAIL_FREEZE_SECONDS:-1.0}"
sidecar="${output%.*}.freeze-tail.json"

for command_name in ffmpeg ffprobe jq sha256sum; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'Required command is unavailable: %s\n' "$command_name" >&2
    exit 1
  fi
done

if [[ ! -f "$input" ]]; then
  printf 'Input video does not exist: %s\n' "$input" >&2
  exit 1
fi

if [[ "$input" == "$output" ]]; then
  printf 'Input and output paths must differ.\n' >&2
  exit 1
fi

if [[ -e "$output" || -e "$sidecar" ]]; then
  printf 'Refusing to overwrite output or provenance sidecar: %s\n' "$output" >&2
  exit 1
fi

if [[ ! "$hold_seconds" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  printf 'HOLD_SECONDS must be a positive decimal number: %s\n' "$hold_seconds" >&2
  exit 1
fi

if ! awk -v hold="$hold_seconds" -v maximum="$max_hold_seconds" 'BEGIN { exit !(hold > 0 && hold <= maximum) }'; then
  printf 'HOLD_SECONDS must be greater than zero and no more than %s seconds.\n' "$max_hold_seconds" >&2
  exit 1
fi

input_duration="$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$input")"
if [[ -z "$input_duration" ]]; then
  printf 'Could not determine input duration: %s\n' "$input" >&2
  exit 1
fi

target_duration="$(awk -v input_duration="$input_duration" -v hold="$hold_seconds" 'BEGIN { printf "%.6f", input_duration + hold }')"
output_dir="$(dirname "$output")"
mkdir -p "$output_dir"
temporary_dir="$(mktemp -d "$output_dir/.extend-last-frame.XXXXXX")"
temporary_output="$temporary_dir/output.mp4"
temporary_sidecar="$temporary_dir/output.freeze-tail.json"

cleanup() {
  rm -rf "$temporary_dir"
}
trap cleanup EXIT

audio_stream_count="$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$input" | wc -l)"

if (( audio_stream_count > 0 )); then
  ffmpeg -hide_banner -loglevel error -i "$input" \
    -filter_complex "[0:v:0]tpad=stop_mode=clone:stop_duration=$hold_seconds[v];[0:a:0]apad=pad_dur=$hold_seconds[a]" \
    -map '[v]' -map '[a]' -map_metadata 0 -t "$target_duration" \
    -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
    -c:a aac -b:a 192k -movflags +faststart "$temporary_output"
  audio_policy="pad_existing_audio_with_silence"
else
  ffmpeg -hide_banner -loglevel error -i "$input" \
    -vf "tpad=stop_mode=clone:stop_duration=$hold_seconds" \
    -map 0:v:0 -map_metadata 0 -an -t "$target_duration" \
    -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p \
    -movflags +faststart "$temporary_output"
  audio_policy="no_input_audio"
fi

actual_duration="$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$temporary_output")"
if ! awk -v actual="$actual_duration" -v target="$target_duration" 'BEGIN { delta=actual-target; if (delta < 0) delta=-delta; exit !(delta <= 0.080) }'; then
  printf 'Extended output duration %s differs from target %s by more than 0.080 seconds.\n' "$actual_duration" "$target_duration" >&2
  exit 1
fi

input_sha256="$(sha256sum "$input" | awk '{print $1}')"
output_sha256="$(sha256sum "$temporary_output" | awk '{print $1}')"
created_at="$(date --iso-8601=seconds)"

jq -n \
  --arg input "$input" \
  --arg output "$output" \
  --arg input_sha256 "$input_sha256" \
  --arg output_sha256 "$output_sha256" \
  --arg audio_policy "$audio_policy" \
  --arg created_at "$created_at" \
  --argjson input_duration "$input_duration" \
  --argjson hold_seconds "$hold_seconds" \
  --argjson maximum_hold_seconds "$max_hold_seconds" \
  --argjson target_duration "$target_duration" \
  --argjson actual_duration "$actual_duration" \
  '{
    schema_version: "1.0",
    operation: "freeze_last_frame",
    input: {path: $input, sha256: $input_sha256, duration_seconds: $input_duration},
    output: {path: $output, sha256: $output_sha256, duration_seconds: $actual_duration},
    hold_seconds: $hold_seconds,
    maximum_hold_seconds: $maximum_hold_seconds,
    target_duration_seconds: $target_duration,
    video_filter: "tpad=stop_mode=clone",
    audio_policy: $audio_policy,
    overwrite: false,
    created_at: $created_at
  }' > "$temporary_sidecar"

mv "$temporary_output" "$output"
mv "$temporary_sidecar" "$sidecar"
printf 'Extended final frame by %s seconds: %s\n' "$hold_seconds" "$output"
printf 'Provenance: %s\n' "$sidecar"
