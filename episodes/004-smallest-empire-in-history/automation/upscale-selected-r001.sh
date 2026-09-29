#!/usr/bin/env bash
set -Eeuo pipefail
EPISODE_ROOT=/home/mhr/Code/chronostick-studio/episodes/004-smallest-empire-in-history
INPUT="$EPISODE_ROOT/final/episode-004-smallest-empire-in-history-concat-r001.mp4"
OUTPUT="$EPISODE_ROOT/final/episode-004-smallest-empire-in-history-picture-master-1080x1920-r001.mp4"
MODEL=/home/mhr/AI/ComfyUI/models/upscale_models/RealESRGAN_x4plus_anime_6B.pth
STATE="$EPISODE_ROOT/final/upscale-r001-state.json"
LOG="$EPISODE_ROOT/final/upscale-r001.log"
exec >>"$LOG" 2>&1
write_state() {
  python - "$STATE" "$1" "$INPUT" "$OUTPUT" "$MODEL" <<'PY'
import json,sys,datetime,os
from pathlib import Path
p=Path(sys.argv[1]);d={'schema_version':'1.0','status':sys.argv[2],'input':sys.argv[3],'output':sys.argv[4],'model':sys.argv[5],'updated_at':datetime.datetime.now().astimezone().isoformat()};q=p.with_suffix('.tmp');q.write_text(json.dumps(d,indent=2)+'\n');os.replace(q,p)
PY
}
restore_comfyui() {
  code=$?
  if [[ "$code" -eq 0 ]]; then write_state succeeded; else write_state failed; fi
  systemctl --user start comfyui.service || true
  printf '%s upscale exit=%s; ComfyUI restart requested\n' "$(date --iso-8601=seconds)" "$code"
}
trap restore_comfyui EXIT
[[ -f "$INPUT" && -f "$MODEL" && ! -e "$OUTPUT" ]]
write_state running
printf '%s stopping idle ComfyUI to free GPU memory\n' "$(date --iso-8601=seconds)"
systemctl --user stop comfyui.service
printf '%s framewise upscale started\n' "$(date --iso-8601=seconds)"
/home/mhr/AI/comfy-video-automation/scripts/upscale-framewise-video.sh "$INPUT" \
  --output "$OUTPUT" \
  --model "$MODEL" \
  --width 1080 \
  --height 1920 \
  --fit cover
ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate,nb_frames -of json "$OUTPUT" > "$EPISODE_ROOT/final/upscale-r001-ffprobe.json"
printf '%s framewise upscale finished\n' "$(date --iso-8601=seconds)"
