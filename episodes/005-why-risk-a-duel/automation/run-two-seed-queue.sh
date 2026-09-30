#!/usr/bin/env bash
set -Eeuo pipefail

REPO_ROOT=/home/mhr/Code/chronostick-studio
EPISODE_ROOT="$REPO_ROOT/episodes/005-why-risk-a-duel"
AUTOMATION_ROOT=/home/mhr/AI/comfy-video-automation
QUEUE_ROOT="$EPISODE_ROOT/automation"
SERVICE_URL=http://127.0.0.1:8092
STATE="$QUEUE_ROOT/queue-state.json"

exec 9>"$QUEUE_ROOT/queue.lock"
flock -n 9 || exit 0
exec >>"$QUEUE_ROOT/queue.log" 2>&1

log() { printf '%s %s\n' "$(date --iso-8601=seconds)" "$*"; }

update_state() {
  python - "$STATE" "$1" "$2" "$3" <<'PY'
import datetime
import json
import os
import sys
from pathlib import Path

path = Path(sys.argv[1])
revision, key, value = sys.argv[2:]
data = json.loads(path.read_text())
if revision == "queue":
    data[key] = value
else:
    data["variants"][revision][key] = value
data["last_updated"] = datetime.datetime.now().astimezone().isoformat()
temporary = path.with_suffix(".tmp")
temporary.write_text(json.dumps(data, indent=2) + "\n")
os.replace(temporary, path)
PY
}

batch_state() {
  curl --fail --silent --show-error --max-time 20 "$SERVICE_URL/v1/batches/$1" |
    jq -r '[.status, ([.jobs[] | select(.status=="created" or .status=="validated" or .status=="queued" or .status=="preparing" or .status=="submitted" or .status=="running" or .status=="postprocessing")] | length)] | @tsv'
}

wait_terminal() {
  local batch_id="$1" result status unfinished
  while true; do
    result=$(batch_state "$batch_id") || {
      log "Cannot query batch $batch_id; retrying in 20 seconds"
      sleep 20
      continue
    }
    IFS=$'\t' read -r status unfinished <<<"$result"
    if [[ "$unfinished" == 0 && "$status" != "running" && "$status" != "queued" ]]; then
      printf '%s\n' "$status"
      return 0
    fi
    sleep 20
  done
}

extract_batch_id() {
  python - "$1" <<'PY'
import re
import sys

text = open(sys.argv[1], errors="replace").read()
match = re.search(r"Batch ([0-9a-f]{8}-[0-9a-f-]{27,})\s+status=", text)
print(match.group(1) if match else "")
PY
}

update_state queue status running
log "Two-seed queue started"

for revision in r001 r002; do
  variant_root="$QUEUE_ROOT/variants/$revision"
  marker="$variant_root/submitted.marker"
  batch_file="$variant_root/batch-id.txt"
  watch_log="$variant_root/batch-watch.log"

  if [[ -e "$marker" ]]; then
    if [[ ! -s "$batch_file" ]]; then
      log "$revision has a submission marker but no batch ID; refusing duplicate submission"
      update_state "$revision" status submission_uncertain
      update_state queue status submission_uncertain
      exit 3
    fi
    batch_id=$(<"$batch_file")
    log "$revision already submitted as $batch_id; reconnecting"
    terminal=$(wait_terminal "$batch_id")
    update_state "$revision" status "$terminal"
    continue
  fi

  log "Preflight $revision"
  curl --fail --silent --show-error "$SERVICE_URL/v1/ready" | jq -e '.ready == true' >/dev/null
  for n in $(seq -w 1 11); do
    test ! -e "$EPISODE_ROOT/renders/raw/clip-$n-episode-005-$revision.mp4"
    test ! -e "$EPISODE_ROOT/renders/editorial/clip-$n-episode-005-$revision.mp4"
  done
  cd "$REPO_ROOT"
  ./scripts/validate-repo.sh
  cd "$AUTOMATION_ROOT"
  /home/mhr/.local/bin/uv run comfy-video batch \
    --service-url "$SERVICE_URL" \
    --folder "$variant_root/jobs" \
    --settings "$variant_root/batch-settings.json" \
    --dry-run >"$variant_root/dry-run.log" 2>&1
  test "$(rg -c 'VALID clip-' "$variant_root/dry-run.log")" -eq 11

  update_state "$revision" status submitting
  printf '%s\n' "$(date --iso-8601=seconds)" >"$marker"
  log "Submitting $revision as one 11-job batch"
  PYTHONUNBUFFERED=1 /home/mhr/.local/bin/uv run comfy-video batch \
    --service-url "$SERVICE_URL" \
    --folder "$variant_root/jobs" \
    --settings "$variant_root/batch-settings.json" \
    --watch --poll-interval 15 >"$watch_log" 2>&1 &
  watcher_pid=$!

  batch_id=''
  for poll in $(seq 1 120); do
    batch_id=$(extract_batch_id "$watch_log")
    [[ -n "$batch_id" ]] && break
    if ! kill -0 "$watcher_pid" 2>/dev/null; then
      break
    fi
    sleep 2
  done
  if [[ -z "$batch_id" ]]; then
    log "No batch ID captured for $revision; inspect $watch_log before any retry"
    update_state "$revision" status submission_uncertain
    update_state queue status submission_uncertain
    exit 4
  fi

  printf '%s\n' "$batch_id" >"$batch_file"
  update_state "$revision" batch_id "$batch_id"
  update_state "$revision" status running
  log "$revision batch_id=$batch_id"

  wait "$watcher_pid" || log "$revision watcher exited nonzero; checking persisted service state"
  terminal=$(wait_terminal "$batch_id")
  update_state "$revision" status "$terminal"
  log "$revision terminal status=$terminal"
done

update_state queue status complete
log "Both seed variants reached terminal batch states"
