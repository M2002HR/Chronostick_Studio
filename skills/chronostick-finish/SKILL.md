---
name: chronostick-finish
description: Validate selected ChronoStick clips, concatenate the picture master, and upscale it frame by frame to 1080×1920 with the local Spandrel wrapper. Use only after every timeline slot is approved.
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

Use the framewise wrapper with a declared model, an exact 1080×1920 target, and cover fitting:

```bash
/home/mhr/AI/comfy-video-automation/scripts/upscale-framewise-video.sh CONCAT_RNNN.mp4 \
  --output PICTURE_MASTER_1080X1920_RNNN.mp4 \
  --model /home/mhr/AI/ComfyUI/models/upscale_models/RealESRGAN_x4plus_anime_6B.pth \
  --width 1080 \
  --height 1920 \
  --fit cover
```

Keep concurrency one and retain the adjacent `*.framewise-upscale.json` provenance report until final QC. Never run generation and upscaling concurrently on the same GPU. The model path is the project default; replace it explicitly when testing another approved model.

## Gate

Review the upscaled result for geometry, crop, temporal stability, seams, flicker, color shift, over-sharpening, audio sync, and complete duration. This output is the picture/SFX master. When voice and subtitles are added externally in Google Vids, document the uploaded revision and archive the returned distribution master separately.
