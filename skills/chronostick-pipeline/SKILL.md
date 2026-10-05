---
name: chronostick-pipeline
description: Inspect, resume, and orchestrate a ChronoStick YouTube Short from reference-video or title/source intake through analysis, scenario, neutral storyboard, real voice timing, references, H3 generation, review, assembly, upscale, and YouTube packaging. Use for end-to-end work or when the next valid production stage is unclear.
---

# Chronostick Pipeline

Treat the repository as the production memory; never rely on chat history as the only record.

## Resume protocol

1. Read the repository `AGENTS.md`, active production docs, episode `README.md`, and `pipeline-state.json`.
2. Inspect actual artifacts and Git state. Preserve unrelated and uncommitted work.
3. Validate claimed outputs before trusting a stage status. Existing files do not imply approval.
4. Skip a stage only when its required artifacts exist, pass its gate, and the state is `approved`.
5. If a stage is `draft`, `needs_review`, or `rejected`, continue that stage rather than advancing.
6. Update `pipeline-state.json` with paths, status, decision, timestamp, and next action after each handoff.

Read [references/stage-contracts.md](references/stage-contracts.md) for dependencies, outputs, and gates.

## Reference-first default

For a new supplied-video Short, read `docs/reference-first-shorts.md` and use semantic state v2. Route intake → `chronostick-transcribe` → `chronostick-reference-video` → `chronostick-script` → `chronostick-storyboard`. User review of both scenario and actual neutral rough sketches gates production references. Then reference design and final Spanish writing/user voice can progress independently. Before Google Vids voice handoff, route the clean narration through `chronostick-voice-direction` for its required registered-tag paste copy and text validation; track this substage within `voice`. Ingest accepted voice, run Ajil again in voice mode, and reconcile final timing/direction before prompts/jobs. Use 20–30 seconds (choose and record target), 4–7-second editorial clips, 16 steps and sparse isolated diegetic SFX. Preserve raw source bytes and provider timing. Never use neutral storyboard panels as H3 references.

## Legacy text-first routing

- Title/source to narration: `$chronostick-script`
- After narration review and before voice generation, use `chronostick-voice-direction` for the required tagged paste input when Google Vids is selected; record used/skipped and artifact paths in the manifest. Audition the actual voice before timing.
- Approved narration plus word timestamps: `$chronostick-timestamps`
- Timing to directing plan, continuity ledger, and reference requirements: `$chronostick-shot-plan`
- Full-frame stick-world reference prompts/assets: `$chronostick-references`
- Five-second H3 prompts: `$chronostick-clip-prompts`
- Deterministic 14-step job JSON: `$chronostick-generation-jobs`
- Local preflight and operator-authorized generation: `$chronostick-batch`
- Render QC and replacements: `$chronostick-review`
- Prefer reviewed clean native SFX; after an actual music/sound failure, route
  the independent physical-cue fallback through `$chronostick-sfx` without
  altering accepted picture frames.
- Selection, concat, framewise 1080×1920 upscale and local narration/active-word
  captions/supplied sound layers: `$chronostick-finish`; `docs/postproduction.md`
- Thumbnail and upload metadata: `$chronostick-youtube`

## Invariants

- New reference-first Shorts target 20–30 seconds in vertical 9:16, with accepted voice-led 4–7-second clip allocation and 16 steps. Existing text-first episodes retain their named duration/step profile.
- Generated references are full-frame, single-scene, and entirely inside the approved stick-world style—never contact sheets or multi-panel boards.
- Story state moves forward. A hard cut may change framing, never chronology, identity, prop state, or event phase without cause.
- Generated clips contain brief isolated synchronized diegetic SFX with silence between cues but no music, speech, narration, lip sync, or readable text.
- Text is Git-versioned; media uses immutable `-rNNN` revisions. Never infer approval from a revision number.
- Preparation never authorizes an expensive batch, an upload, publication, deletion, or overwrite. Require explicit operator intent at that boundary.

## Completion

An episode closes only when the distribution master, thumbnail package, metadata, provenance, review decisions, and final state are recorded. External voice/subtitle work may remain a documented Google Vids stage; do not claim it was completed locally.
