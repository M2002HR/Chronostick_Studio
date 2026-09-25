#!/usr/bin/env bash

set -euo pipefail

episode_root="/home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute"
studio_root="/home/mhr/Code/chronostick-studio"
automation_root="${COMFY_VIDEO_AUTOMATION_ROOT:-/home/mhr/AI/comfy-video-automation}"
service_url="${COMFY_VIDEO_SERVICE_URL:-http://127.0.0.1:8090}"

if [[ "${1:-}" != "" && "${1:-}" != "--preflight-only" ]]; then
  printf 'Usage: %s [--preflight-only]\n' "$0" >&2
  exit 2
fi

cd "$studio_root"
./scripts/validate-repo.sh

cd "$automation_root"
curl --fail --silent --show-error "$service_url/v1/ready" >/dev/null

uv run comfy-video batch \
  --service-url "$service_url" \
  --folder "$episode_root/automation/jobs" \
  --settings "$episode_root/automation/batch-settings.json" \
  --dry-run

if [[ "${1:-}" == "--preflight-only" ]]; then
  printf 'Preflight passed. No generation was queued.\n'
  exit 0
fi

printf 'Preflight passed. Starting the r002 batch; press Ctrl+C only to detach the progress display.\n'
uv run comfy-video batch \
  --service-url "$service_url" \
  --folder "$episode_root/automation/jobs" \
  --settings "$episode_root/automation/batch-settings.json" \
  --watch
