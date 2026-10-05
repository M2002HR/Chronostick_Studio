---
name: chronostick-finish
description: Validate selected ChronoStick Shorts clips, concatenate and upscale the picture master, then finish accepted narration, active-word captions and explicit sound layers locally. Also use for post-production on a completed vertical master.
---

# Chronostick Finish

For reference-first Shorts, each approved editorial take has its own 4–7-second duration and frame count from the timing map. Verify those values instead of enforcing five seconds per file. Normalize raw terminal holds automatically with traceable derivatives before concat; preserve immutable raw takes. The accepted user Spanish voice is a separate track mixed against its actual timing. Assembly cannot repair missing creative cuts or failed generated actions.

## Selection and concat

If actual clip music was reported, use `chronostick-sfx` and
`docs/clean-sfx-workflow.md` to review an independent clean derivative before
selection. Keep the accepted picture unchanged and the contaminated original
archived/rejected for audio. Never preserve that native soundtrack under voice.

Require exactly one approved editorial clip for each consecutive clip number in `renders/final-selected/`. Preserve SFX audio, natural-sort filenames, probe every input, and reject duplicates, gaps, wrong duration, or incompatible unreviewed media.

Create the next unused immutable concat revision with the episode wrapper when present, otherwise use:

```bash
cd /home/mhr/AI/comfy-video-automation
uv run comfy-video concat --directory SELECTED_DIR --output CONCAT_RNNN.mp4 --missing-audio fail --watch
```

Probe duration, dimensions, frame rate, streams, cut order, audio continuity, and sidecar before upscale.

For dynamic Shorts, decode concat with frame passthrough when comparing the
ordered selected pictures: MP4/AAC stream-copy seams can shift presentation
timestamps even when all picture frames are retained. The framewise export
resets the picture to its declared fps. Build a separate selected-SFX stem
with each clip reset to zero and padded/trimmed to its exact editorial
48kHz sample count before audio concatenation (2000 samples per24fps frame).
Keep native and fallback choices unchanged; this removes mux-tail drift,
not creative sound. Bind source hashes and the actual command, and mix this
stem once at finishing instead of also mixing the old concatenated soundtrack.

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

Review the upscaled result for geometry, crop, temporal stability, seams,
flicker, color shift, over-sharpening, audio sync and complete duration. Keep
this picture/SFX master immutable. For local voice/caption/sound finishing,
read `docs/postproduction.md` and use `scripts/postproduce-episode.py` with
`postproduction/edit.json`. On an existing master, go directly to that stage.
Choose native-audio mute/preserve explicitly; fully exclude native sound when
requested. Use actual accepted narration/word timing. New portrait Shorts use
Montserrat Bold,104px at1080×1920, short2–4-word single-line phrases, and300px
bottom inset, approximating the user's supplied Short caption example. Install
the exact licensed font with `scripts/install-shorts-font.py`; never silently
substitute another family. Scale geometry with frame size and inspect phone
previews for similar visual weight and lower-middle placement. Keep all words
white and only the current spoken word yellow, with a restrained dark shadow.
Long-form retains its separate Arial Bold profile; existing edit configurations
and accepted exports change only under a requested finishing revision. Preserve source
timings, safe width and one line; review actual rendered frames and
phone size. Supplied music/ambience/SFX are separate configured tracks; generated
clips keep their music-free policy. Record unsupplied layers as pending.
Validate hashes, fixed picture frames, full decode and encoded loudness; write
the next immutable distribution revision and separate caption/stem provenance.
Technical validation does not imply human release approval. Google Vids remains
optional external finishing, documented with its actual returned master.
