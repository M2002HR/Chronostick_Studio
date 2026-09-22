# Instructions for AI collaborators

This repository is the production source of truth for ChronoStick Studio. Before creating or changing an episode, read these files in order:

1. `README.md`
2. `docs/workflow.md`
3. `docs/production-rules.md`
4. `docs/style-rules.md`
5. `docs/video-rules.md`
6. `docs/audio-rules.md`
7. `docs/versioning.md`
8. `docs/decisions.md`
9. the target episode's `README.md` and `plan/shot-plan.md`
10. only the relevant locked files in `docs/specs/`

## Source-of-truth priority

When instructions conflict, use this order:

1. the user's current explicit instruction
2. this file and the active rules in `docs/`
3. locked, approved specifications in `docs/specs/`
4. the episode manifest and shot plan
5. archived material in `docs/archive/`

Archived files explain history; they are not active instructions.

## Non-negotiable rules

- Files under `prompts/` and `episodes/*/prompts/` contain only text that is ready to paste into a generation model.
- Never put YAML metadata, explanations, review checklists, logs, or approval notes in a prompt file.
- Never invent or reconstruct a missing "approved" prompt. Leave it empty and record the gap in the episode manifest.
- Preserve approved character identity, style, world, and asset references. Simplify backgrounds before characters.
- Every video generation is exactly 10 seconds, vertical 9:16, self-contained, and ends on a resolved frame.
- Use fast editing with moderate motion: one primary action and at most one camera move per shot.
- Every video prompt must contain exactly this policy sentence: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`
- Do not generate narration, dialogue, lip sync, subtitles, labels, or other readable text unless an episode explicitly requires an approved exception.
- Do not overwrite generated media. Add `-r001`, `-r002`, and so on.
- Use Git history for text versions. Never create names such as `final2` or `final-final`.
- Do not mark an artifact approved or locked without an actual review decision.

## Working method

Start from source material, then script, voice, timestamps, shot plan, asset-reuse decision, missing asset generation, final prompts, renders, review, and assembly. Do not skip a stage silently. If an input is unavailable, record it as unavailable instead of fabricating it.

For historical claims, distinguish documented fact from popular anecdote. Verify claims against reliable sources when research is part of the task, preserve citations in the episode source notes, and carry qualifications into the narration and visuals.

Before handing off changes, validate paths, prompt purity, required audio wording, reference limits, empty/missing artifacts, and `git diff --check`.
