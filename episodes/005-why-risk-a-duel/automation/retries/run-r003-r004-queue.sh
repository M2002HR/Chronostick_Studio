#!/usr/bin/env bash
set -Eeuo pipefail
REPO_ROOT=/home/mhr/Code/chronostick-studio
EPISODE_ROOT="$REPO_ROOT/episodes/005-why-risk-a-duel"
AUTOMATION_ROOT=/home/mhr/AI/comfy-video-automation
QUEUE_ROOT="$EPISODE_ROOT/automation/retries"
SERVICE_URL=http://127.0.0.1:8092
STATE="$QUEUE_ROOT/r003-r004-queue-state.json"
exec 9>"$QUEUE_ROOT/r003-r004-queue.lock"
flock -n 9 || exit 0
exec >>"$QUEUE_ROOT/r003-r004-queue.log" 2>&1
log() { printf '%s %s\n' "$(date --iso-8601=seconds)" "$*"; }
update_state() {
  python - "$STATE" "$1" "$2" "$3" <<'PY'
import datetime,json,os,sys
from pathlib import Path
p=Path(sys.argv[1]); rev,key,val=sys.argv[2:]
d=json.loads(p.read_text())
if rev == 'queue': d[key]=val
else: d['variants'][rev][key]=val
d['last_updated']=datetime.datetime.now().astimezone().isoformat()
q=p.with_suffix('.tmp'); q.write_text(json.dumps(d,indent=2)+'\n'); os.replace(q,p)
PY
}
batch_state() {
  curl --fail --silent --show-error --max-time 20 "$SERVICE_URL/v1/batches/$1" |
    jq -r '[.status,([.jobs[]|select(.status=="created" or .status=="validated" or .status=="queued" or .status=="preparing" or .status=="submitted" or .status=="running" or .status=="postprocessing")]|length)]|@tsv'
}
wait_terminal() {
  local result status unfinished
  while true; do
    result=$(batch_state "$1") || { log "Cannot query $1; retrying"; sleep 20; continue; }
    IFS=$'\t' read -r status unfinished <<<"$result"
    if [[ "$unfinished" == 0 && "$status" != running && "$status" != queued ]]; then printf '%s\n' "$status"; return; fi
    sleep 20
  done
}
extract_batch_id() {
  python - "$1" <<'PY'
import re,sys
s=open(sys.argv[1],errors='replace').read(); m=re.search(r'Batch ([0-9a-f]{8}-[0-9a-f-]{27,})\s+status=',s)
print(m.group(1) if m else '')
PY
}
update_state queue status running
log 'Corrected two-seed queue started'
for revision in r003 r004; do
  root="$QUEUE_ROOT/$revision"; marker="$root/submitted.marker"; id_file="$root/batch-id.txt"; watch="$root/batch-watch.log"
  if [[ -e "$marker" ]]; then
    test -s "$id_file" || { update_state "$revision" status submission_uncertain; exit 3; }
    batch_id=$(<"$id_file"); terminal=$(wait_terminal "$batch_id"); update_state "$revision" status "$terminal"; continue
  fi
  curl --fail --silent "$SERVICE_URL/v1/ready" | jq -e '.ready == true and .h3_available == true' >/dev/null
  for n in $(seq -w 1 11); do
    test ! -e "$EPISODE_ROOT/renders/raw/clip-$n-episode-005-$revision.mp4"
    test ! -e "$EPISODE_ROOT/renders/editorial/clip-$n-episode-005-$revision.mp4"
  done
  cd "$REPO_ROOT"; ./scripts/validate-repo.sh
  cd "$AUTOMATION_ROOT"
  /home/mhr/.local/bin/uv run comfy-video batch --service-url "$SERVICE_URL" --folder "$root/jobs" --settings "$root/batch-settings.json" --dry-run >"$root/dry-run.log" 2>&1
  test "$(rg -c 'VALID clip-' "$root/dry-run.log")" -eq 11
  update_state "$revision" status submitting; date --iso-8601=seconds >"$marker"
  PYTHONUNBUFFERED=1 /home/mhr/.local/bin/uv run comfy-video batch --service-url "$SERVICE_URL" --folder "$root/jobs" --settings "$root/batch-settings.json" --watch --poll-interval 15 >"$watch" 2>&1 &
  pid=$!; batch_id=''
  for poll in $(seq 1 120); do batch_id=$(extract_batch_id "$watch"); [[ -n "$batch_id" ]] && break; kill -0 "$pid" 2>/dev/null || break; sleep 2; done
  [[ -n "$batch_id" ]] || { update_state "$revision" status submission_uncertain; exit 4; }
  printf '%s\n' "$batch_id" >"$id_file"; update_state "$revision" batch_id "$batch_id"; update_state "$revision" status running; log "$revision batch_id=$batch_id"
  wait "$pid" || true; terminal=$(wait_terminal "$batch_id"); update_state "$revision" status "$terminal"; log "$revision terminal=$terminal"
done
update_state queue status complete
log 'Corrected r003 and r004 reached terminal states'
