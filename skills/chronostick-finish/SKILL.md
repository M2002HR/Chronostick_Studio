---
name: chronostick-finish
description: Validate selected ChronoStick clips, concatenate the picture master, and upscale it through the local resumable FlashVSR workflow with the approved 480-pixel tile preset. Use only after every timeline slot is approved.
---

# Chronostick Finish

## Selection and concat

Require exactly one approved editorial clip for each consecutive clip number in `renders/final-selected/`. Preserve SFX audio, natural-sort filenames, probe every input, and reject duplicates, gaps, wrong duration, or incompatible unreviewed media.

Create the next unused immutable concat revision with the episode wrapper when present, otherwise use:

```bash
cd /home/mhr/AI/comfy-video-automation
uv run comfy-video concat --directory SELECTED_DIR --output CONCAT_RNNN.mp4 --missing-audio fail --watch
```

Probe duration, dimensions, frame rate, streams, cut order, audio continuity, and sidecar before upscale.

## Default upscale

Use the resumable long-video route, not a whole-timeline in-memory FlashVSR job. For the requested 480-pixel tile on the inspected 16 GB GPU, pair it with five-second chunks:

```bash
/home/mhr/AI/comfy-video-automation/scripts/upscale-long-video.sh CONCAT_RNNN.mp4 \
  --output PICTURE_MASTER_1080X1920_RNNN.mp4 \
  --width 1080 --height 1920 --fit cover \
  --chunk-seconds 5 \
  --settings /home/mhr/AI/comfy-video-automation/examples/flashvsr-quality-16gb-tile480.json
```

Keep concurrency one, resume state, chunks, manifests, and provenance until final QC. Never run generation and FlashVSR concurrently on the same GPU. A 480 tile is a project default, not a promise it fits another GPU/input; preflight and monitor VRAM.

## Gate

Review the upscaled result for geometry, crop, temporal stability, seams, flicker, color shift, over-sharpening, audio sync, and complete duration. This output is the picture/SFX master. When voice and subtitles are added externally in Google Vids, document the uploaded revision and archive the returned distribution master separately.
