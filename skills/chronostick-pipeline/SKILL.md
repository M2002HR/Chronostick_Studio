---
name: chronostick-pipeline
description: Inspect, resume, and orchestrate a ChronoStick YouTube Short from title/source intake through script, timing, references, H3 generation, review, assembly, upscale, and YouTube packaging. Use for end-to-end work or when the next valid production stage is unclear.
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

## Routing

- Title/source to narration: `$chronostick-script`
- Approved narration plus word timestamps: `$chronostick-timestamps`
- Timing to directing plan, continuity ledger, and reference requirements: `$chronostick-shot-plan`
- Full-frame stick-world reference prompts/assets: `$chronostick-references`
- Five-second H3 prompts: `$chronostick-clip-prompts`
- Deterministic 14-step job JSON: `$chronostick-generation-jobs`
- Local preflight and operator-authorized generation: `$chronostick-batch`
- Render QC and replacements: `$chronostick-review`
- Selection, concat, and 480-tile FlashVSR upscale: `$chronostick-finish`
- Thumbnail and upload metadata: `$chronostick-youtube`

## Invariants

- Default target is a 40–60 second, vertical 9:16 Short; narration and timestamps determine the final five-second slot count.
- Generated references are full-frame, single-scene, and entirely inside the approved stick-world style—never contact sheets or multi-panel boards.
- Story state moves forward. A hard cut may change framing, never chronology, identity, prop state, or event phase without cause.
- Generated clips contain rich synchronized diegetic SFX but no music, speech, narration, lip sync, or readable text.
- Text is Git-versioned; media uses immutable `-rNNN` revisions. Never infer approval from a revision number.
- Preparation never authorizes an expensive batch, an upload, publication, deletion, or overwrite. Require explicit operator intent at that boundary.

## Completion

An episode closes only when the distribution master, thumbnail package, metadata, provenance, review decisions, and final state are recorded. External voice/subtitle work may remain a documented Google Vids stage; do not claim it was completed locally.
