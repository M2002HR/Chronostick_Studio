#!/usr/bin/env bash
set -Eeuo pipefail
REPO_ROOT=/home/mhr/Code/chronostick-studio
EPISODE_ROOT="$REPO_ROOT/episodes/004-smallest-empire-in-history"
QUEUE_ROOT="$EPISODE_ROOT/automation/retries/r003"
AUTOMATION_ROOT=/home/mhr/AI/comfy-video-automation
SERVICE_URL=http://127.0.0.1:8091
PRIOR_BATCH=9bd1ba96-3686-462b-96b9-65b3c4437501
STATE="$QUEUE_ROOT/queue-state.json"
exec 9>"$QUEUE_ROOT/queue.lock"
flock -n 9 || exit 0
exec >>"$QUEUE_ROOT/queue.log" 2>&1
log() { printf '%s %s\n' "$(date --iso-8601=seconds)" "$*"; }
update_state() {
  python - "$STATE" "$1" "$2" "$3" <<'PY'
import json,sys,tempfile,os
from pathlib import Path
p=Path(sys.argv[1]);rev,key,val=sys.argv[2:];d=json.loads(p.read_text());d['variants'][rev][key]=val;d['last_updated']=__import__('datetime').datetime.now().astimezone().isoformat();q=p.with_suffix('.tmp');q.write_text(json.dumps(d,indent=2)+'\n');os.replace(q,p)
PY
}
batch_state() {
  curl --fail --silent --show-error --max-time 20 "$SERVICE_URL/v1/batches/$1" | jq -r '[.status,([.jobs[] | select(.status=="queued" or .status=="running" or .status=="pending")]|length)]|@tsv'
}
wait_terminal() {
  local id="$1" result status unfinished
  while true; do
    result=$(batch_state "$id") || { log "Cannot query batch $id; retrying"; sleep 20; continue; }
    IFS=$'\t' read -r status unfinished <<<"$result"
    if [[ "$unfinished" == 0 && "$status" != running && "$status" != queued ]]; then
      printf '%s\n' "$status"
      return 0
    fi
    sleep 20
  done
}
log 'Three-seed queue started; waiting for r002 to be terminal.'
prior_status=$(wait_terminal "$PRIOR_BATCH")
log "r002 terminal status=$prior_status; queue may start"
for revision in r003 r004 r005; do
  variant_root="$EPISODE_ROOT/automation/retries/$revision"
  marker="$variant_root/submitted.marker"
  watch_log="$variant_root/batch-watch.log"
  if [[ -e "$marker" ]]; then
    log "Refusing duplicate submission of $revision: marker already exists"
    exit 2
  fi
  log "Preflight $revision"
  curl --fail --silent --show-error "$SERVICE_URL/v1/ready" | jq -e '.ready == true' >/dev/null
  for n in $(seq -w 1 13); do
    test ! -e "$EPISODE_ROOT/renders/raw/clip-$n-episode-004-$revision.mp4"
    test ! -e "$EPISODE_ROOT/renders/editorial/clip-$n-episode-004-$revision.mp4"
  done
  cd "$REPO_ROOT"
  ./scripts/validate-repo.sh
  cd "$AUTOMATION_ROOT"
  /home/mhr/.local/bin/uv run comfy-video batch --service-url "$SERVICE_URL" --folder "$variant_root/jobs" --settings "$variant_root/batch-settings.json" --dry-run > "$variant_root/queue-dry-run.log" 2>&1
  test "$(rg -c 'VALID clip-' "$variant_root/queue-dry-run.log")" -eq 13
  update_state "$revision" status submitting
  printf '%s\n' "$(date --iso-8601=seconds)" > "$marker"
  log "Submitting $revision as one 13-job batch"
  PYTHONUNBUFFERED=1 /home/mhr/.local/bin/uv run comfy-video batch --service-url "$SERVICE_URL" --folder "$variant_root/jobs" --settings "$variant_root/batch-settings.json" --watch --poll-interval 15 > "$watch_log" 2>&1 &
  watcher_pid=$!
  batch_id=''
  for poll in $(seq 1 120); do
    batch_id=$(python - "$watch_log" <<'PY'
import re,sys
s=open(sys.argv[1],errors='replace').read()
m=re.search(r'Batch ([0-9a-f]{8}-[0-9a-f-]{27,})\s+status=',s)
print(m.group(1) if m else '')
PY
)
    [[ -n "$batch_id" ]] && break
    if ! kill -0 "$watcher_pid" 2>/dev/null; then break; fi
    sleep 2
  done
  if [[ -z "$batch_id" ]]; then
    log "No batch ID for $revision; inspect $watch_log before any retry"
    update_state "$revision" status submission_uncertain
    exit 3
  fi
  printf '%s\n' "$batch_id" > "$variant_root/batch-id.txt"
  update_state "$revision" batch_id "$batch_id"
  update_state "$revision" status running
  log "$revision batch_id=$batch_id"
  wait "$watcher_pid" || log "$revision watcher exited nonzero; checking persisted service state"
  terminal=$(wait_terminal "$batch_id")
  update_state "$revision" status "$terminal"
  log "$revision terminal status=$terminal"
  # Continue to the next distinct-seed batch even if an individual candidate failed.
done
log 'All three queued seed variants reached terminal batch states.'
