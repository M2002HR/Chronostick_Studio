---
name: chronostick-longform-pipeline
description: Inspect, start, resume, and route a 10–15 minute ChronoStick historical episode through research, Spanish narration, timing, direction, references, H3 production, review, finishing, and YouTube packaging. Use for end-to-end long-form work or when the next valid gate is unclear.
---

# ChronoStick long-form pipeline

Read `AGENTS.md`, `docs/longform/README.md`, `docs/longform/workflow.md`, `docs/longform/format-contract.md`, `docs/longform/artifact-contract.md`, the target manifest and state file. Existing `docs/workflow.md` and `chronostick-*` script/timing/direction/finish skills are Shorts-specific. Shared style, audio, continuity and versioning rules still apply.

## Resume and route

1. Inspect actual files and `git status` before trusting the manifest. Protect unrelated/uncommitted work. A file or successful batch is not an approval. When the user supplies a reference video and transcript, preserve and inventory both and complete the Stage 00 joint video/transcript `intake-review.md` using `docs/longform/reference-video-workflow.md`. Do not defer first viewing of the video until visual direction.
2. Identify the earliest incomplete gate from `docs/longform/workflow.md`. Record missing evidence; do not synthesize a missing user voice, word timings, approved source, historical portrait, or render.
   If a user explicitly waives independent historical verification for a named episode, use the recorded `source/research-waiver.json`, mark Stage 01 `skipped`, and route to a source-assumption script draft. Keep that distinction visible in every downstream handoff.
   After Stage 02 script review, route `chronostick-voice-direction` and `docs/google-vids-voice-direction.md` when Vids is the voice provider; tagging is required for that provider. Record its `02a` state and manifest choice; do not mark voice/timing complete until the actual audio is accepted.
3. Route to `chronostick-longform-script`, `chronostick-longform-timing`, `chronostick-longform-visual-direction`, `chronostick-longform-shot-plan`, `chronostick-longform-assets`, `chronostick-longform-prompts`, `chronostick-longform-jobs`, `chronostick-longform-review`, `chronostick-longform-finish`, or `chronostick-longform-youtube`. `chronostick-batch` can handle only the authorized launch and monitoring after long-form preflight.
4. Update `pipeline-state.json` with real inputs, output paths, status, reviewer/decision if approved, and next action. If a fact, accepted voice, reference, or picture timeline changes, invalidate affected later gates and jobs.

For local voice, captions or sound work on an existing master, route directly
to `chronostick-longform-finish` and `docs/postproduction.md`. Preserve its
picture timeline and current authorization; changing finishing layers does not
reopen generation. Record explicit native mute/preserve, real voice/timing,
active-word Arial Bold captions, supplied tracks and immutable output review.

## Production control

Complete the whole-video outline and animatic before mass H3 generation. Test final-setting 16:9 H3 on representative hard cases and record time/resource cost. Prepare every job and dry-run the service before requesting a chapter batch. Run sequentially, review per chapter, replace only failed slots with immutable revisions. No generation launch, upload, publication, overwrite or deletion is inferred from planning. Authorization to build the studio or prepare a batch is not authorization for expensive generation.

Close only when the full distribution master, source-linked metadata, actual thumbnail, chapters, provenance and final human review are recorded. If external finishing is used, record exactly what remains external. Run `python scripts/validate-longform.py EPISODE`, `./scripts/validate-repo.sh`, `./scripts/validate-skills.sh`, and `git diff --check` at handoff.
