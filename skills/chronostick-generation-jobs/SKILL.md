---
name: chronostick-generation-jobs
description: Build deterministic MiniMax H3 generation-job JSON and batch settings from approved ChronoStick prompts and references. Use when preparing a batch-ready episode package; default new reference-first Shorts to 16 sampling steps and approved dynamic durations; preserve existing profiles.
---

# Chronostick Generation Jobs

Inspect the current `comfy-video-automation` Pydantic models and service capabilities before emitting JSON; repository examples may lag behind code.

## Reference-first default

Use `docs/reference-first-shorts.md` and the named `h3-short-dynamic-16step-20-30s` episode profile: 16 steps, Lightning off, `res_multistep`, `beta`, SFX only. Preserve each approved 4–7-second editorial slot separately from the service-supported frame-grid request. Inspect live models and pilot raw-tail normalization; do not assume arbitrary duration support. Store exact duration/frame count and normalization strategy in `automation/job-plan.json`. One immutable raw take and one exact editorial-duration derivative per slot, without time stretching. Run complete dry-run before submission. Do not silently emit legacy five-second/14-step jobs for this route.

Check the resolver's actual `frame_count` and appended audio suffix. Record the resulting 17-frame grid separately from the requested seconds. For editorial slots shorter than five seconds, request five and resolve all actions before the earlier editorial endpoint. Set an explicit non-tonal, silence-separated `audio.prompt_suffix` that does not repeat the exact required policy sentence already in the pure prompt; verify that the resolved generator text contains it once. Bind prompt/reference/timing hashes in the job plan so a later change invalidates preflight. Never certify a four-step draft as a sixteen-step result.

## Legacy defaults

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

For the reviewed reference-first route, use `scripts/build-short-jobs.py EPISODE --service-root SERVICE_ROOT` to package the explicit timing/direction/reference contract. It preserves fixed seeds and refuses existing package/media targets. Then use `scripts/preflight-short-batch.py EPISODE --service-root SERVICE_ROOT` to archive actual live resolved configurations and the complete CLI dry-run. This verifies bound hashes, scene order, raw frames, 16 steps and exactly one audio-policy sentence in the final engine text; it never submits generation. Preserve failed validation evidence and use a new `--revision rNNN` for a corrected check.

- `automation/jobs/clip-NN-slug.json` per clip
- `automation/jobs/defaults.json` only for fields genuinely shared and supported by CLI merge
- `automation/batch-settings.json` with reviewed retry/failure policy; default first pass does not concat/upscale
- one revision-safe output prefix matching `job_identity`

References remain in authoritative array order and the prompt must mention exactly `<Picture 1>` through `<Picture N>`. Resolve paths beneath the service input root. Confirm every prompt path/reference exists, all seeds differ, all output targets are absent, and all job files parse against the live service.

## Gate

Run repository validation and `comfy-video batch --dry-run`. Do not submit generation as part of preparation; actual launch belongs to `$chronostick-batch` and requires explicit operator intent.
