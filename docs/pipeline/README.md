# Modular production pipeline

This package makes each production stage independently executable and resumable by Codex, another agent, or a human operator. The episode-local `pipeline-state.json` is the handoff record: a stage advances only when its artifacts exist, validation passes, and a real review marks it `approved`.

For new supplied-video Shorts use [`../reference-first-shorts.md`](../reference-first-shorts.md): Ajil source timing → actual video analysis → compressed Spanish scenario → neutral rough storyboard → user review → single-image stick-world references and accepted user voice → Ajil voice timing → dynamic 4–7-second direction → 16-step production. State v2 is created by `scripts/new-short-episode.py`; existing numbered state remains legacy.

## Legacy text-first stage order

1. title/source intake and high-retention 40–60 second target-language narration
1a. required tagged Google Vids paste input when Vids is selected, after the narration and before external voice generation; see [`../google-vids-voice-direction.md`](../google-vids-voice-direction.md)
2. approved voice word timestamps and five-second timing map
3. directing plan, story-state ledger, and reference requirements
4. full-frame, single-scene stick-world references—never sheets or panel grids
5. detailed five-second H3 prompts with adaptive fast cuts, emotion, light, camera, SFX, and a strict no-music lock
6. deterministic batch job JSON with unique fixed seeds and a 14-step default
7. atomic preflight, explicitly authorized generation, progress monitoring, and resource reports
8. frame/motion/audio review plus immutable replacements where required
9. selected-clip concat and framewise upscale to 1080×1920 with cover fitting
10. Shorts thumbnail and upload metadata package, followed by truthful closeout

After an approved picture/SFX master exists, an optional localization branch
can produce a distinct narrated/captioned distribution master for each target
language. It has independent script, voice, timing, caption, mix, and review
gates; it never sends an existing episode back through image/video generation.
See [`../localization-workflow.md`](../localization-workflow.md).

The master router and stage-specific instructions are catalogued in [`skills/`](../../skills/CATALOG.md). Preparation does not authorize GPU generation, cancellation, upload, publication, deletion, or overwrite.

Machine-readable contracts:

- [`production-defaults.json`](production-defaults.json): new reference-first Short defaults, including 16 H3 steps and the framewise 1080×1920 upscale route.
- [`pipeline-state-v2.schema.json`](pipeline-state-v2.schema.json): reference-first semantic handoff/status contract.
- [`pipeline-state.schema.json`](pipeline-state.schema.json): legacy numbered handoff/status contract.
- [`pipeline-state.template.json`](pipeline-state.template.json): legacy starting state; use the scaffold for new reference-first episodes.
- [`operator-runbook.md`](operator-runbook.md): local service, preflight, batch, assembly, and upscale commands.

The per-stage executable guidance is versioned under [`skills/`](../../skills/CATALOG.md). A collaborator resumes from repository artifacts and `pipeline-state.json`, not from chat history.
