#!/usr/bin/env bash
set -Eeuo pipefail

EPISODE_ROOT=/home/mhr/Code/chronostick-studio/episodes/004-smallest-empire-in-history
PICTURE="$EPISODE_ROOT/final/episode-004-smallest-empire-in-history-picture-master-1080x1920-r001.mp4"
VOICE="$EPISODE_ROOT/audio/narration-es-candidate-r001.m4a"
OUTPUT="$EPISODE_ROOT/final/episode-004-smallest-empire-in-history-narrated-preview-r001.mp4"

[[ -s "$PICTURE" && -s "$VOICE" && ! -e "$OUTPUT" ]]

# Immutable review preview only. Keep the approved picture bitstream and mix
# the candidate voice at timeline zero over subdued native SFX; no music.
ffmpeg -hide_banner -nostdin -n \
  -i "$PICTURE" -i "$VOICE" \
  -filter_complex '[0:a:0]aresample=48000,volume=-10dB[sfx];[1:a:0]aresample=48000,volume=1.5dB[voice];[sfx][voice]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,alimiter=limit=0.95:level=false,atrim=duration=65,asetpts=PTS-STARTPTS[mix]' \
  -map 0:v:0 -map '[mix]' -c:v copy -c:a aac -b:a 256k \
  -movflags +faststart "$OUTPUT"
