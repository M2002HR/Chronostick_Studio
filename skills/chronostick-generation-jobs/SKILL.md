---
name: chronostick-generation-jobs
description: Build deterministic MiniMax H3 generation-job JSON and batch settings from approved ChronoStick prompts and references. Use when preparing a batch-ready episode package; default future jobs to 14 sampling steps unless explicitly overridden.
---

# Chronostick Generation Jobs

Inspect the current `comfy-video-automation` Pydantic models and service capabilities before emitting JSON; repository examples may lag behind code.

## Defaults

- schema/template/profile: `1.0`, `h3_ref2va`, `youtube_shorts_hq`
- 480×864, 0.4 MP, 9:16, 5 seconds, 24 fps
- 14 steps, `res_multistep`, `beta`, Lightning off, `ref_image_size: match`
- explicit unique fixed seed per clip
- audio enabled, `sfx_only`, music/dialogue/narration false, audio stream required
- immutable raw output plus exact 5.000-second editorial copy
- overwrite false; no automatic concat or upscale during first generation

If an episode explicitly chooses another profile, record the override in its manifest rather than silently mixing defaults.

## Seed contract

Persist one `project_seed` in `source/intake.json`. Derive each clip seed deterministically from episode ID, render revision, clip number, and project seed with `scripts/derive_clip_seeds.py`; then store the resulting integer directly with `seed_mode: fixed`. Seeds must be unique within the batch and remain unchanged for retries intended to reproduce the same attempt.

## Package

- `automation/jobs/clip-NN-slug.json` per clip
- `automation/jobs/defaults.json` only for fields genuinely shared and supported by CLI merge
- `automation/batch-settings.json` with reviewed retry/failure policy; default first pass does not concat/upscale
- one revision-safe output prefix matching `job_identity`

References remain in authoritative array order and the prompt must mention exactly `<Picture 1>` through `<Picture N>`. Resolve paths beneath the service input root. Confirm every prompt path/reference exists, all seeds differ, all output targets are absent, and all job files parse against the live service.

## Gate

Run repository validation and `comfy-video batch --dry-run`. Do not submit generation as part of preparation; actual launch belongs to `$chronostick-batch` and requires explicit operator intent.
