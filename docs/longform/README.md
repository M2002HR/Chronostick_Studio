# Long-form production

Use this route for 10–15 minute, Spanish-narrated, landscape historical videos. `docs/workflow.md` and the existing `chronostick-*` production skills describe Shorts unless they explicitly say otherwise. Shared authority remains `AGENTS.md`, `docs/production-rules.md`, `docs/style-rules.md`, `docs/reference-and-prompt-continuity.md`, `docs/audio-rules.md`, and `docs/versioning.md`. This directory defines the long-form decisions that differ. Existing Shorts profiles and episodes are unchanged.

Read [workflow.md](workflow.md), [format-contract.md](format-contract.md), and [artifact-contract.md](artifact-contract.md) before creating a long episode. Use [ledger-schemas.md](ledger-schemas.md) while writing structured handoffs. Use `chronostick-longform-pipeline` to inspect or resume work. Each phase has a dedicated skill in `skills/CATALOG.md`.

When the user supplies an example video, transcript or selected frames, follow [reference-video-workflow.md](reference-video-workflow.md). It carries the example through intake, visual direction, shot planning, anchors and prompts without treating it as historical evidence.

A long episode may start with a title and a supplied example video plus transcript when no separate historical source has arrived. Record `reference_transcript_only`, complete the Stage 00 joint video/transcript intake review, and verify every historical claim independently in Stage 01 before approving a script. The example video and screenshots are creative research, not historical evidence or a script to reproduce. Do not claim a voice, timestamps, approval, rendered clip, or completed distribution master until the artifact and review record exist.

An explicit user instruction can waive Stage 01 independent verification for a named episode. Record the scope and source assumption in `source/research-waiver.json`, mark research `skipped`, and label the Spanish script as a source-assumption draft. The waiver does not certify historical accuracy or approve the script or later artifacts.

Create a workspace with `python scripts/new-longform-episode.py NNN-slug --title "Title"`. Follow the [operator runbook](operator-runbook.md) for job generation, dry-run, selection and finishing. Validate it at any point with `python scripts/validate-longform.py episodes/NNN-slug`; validation is stage-aware and is also included in `./scripts/validate-repo.sh`. Run `./scripts/validate-skills.sh` and `git diff --check` before handoff.
