# Workflow review for the next episode

Reviewed on 2026-10-05. This is an inspection record and a working agenda,
not an approved change to production rules.

## Requested working method

The user wants to revise the production workflow while producing a new example
video through completion. Carry each selected change into the relevant code,
repository skill and active documentation as the affected stage is exercised.
Preserve existing episode work and uncommitted changes.

The user subsequently selected a Short and supplied the reference-first design
requirements. They are captured in
[reference-first-shorts-proposal.md](reference-first-shorts-proposal.md).
The reference video and example title have not yet been supplied. No new
episode or generation batch has been created for this review.

## Current routes

- Shorts: `docs/workflow.md`, `docs/pipeline/`, and `chronostick-*` skills.
- Long-form: `docs/longform/workflow.md` and `chronostick-longform-*` skills.
- Shared sequence: source, script, accepted voice, actual timestamps, direction,
  reference coverage, pure prompts, deterministic jobs, generation, review,
  selection, finishing and delivery.
- Long-form additionally specifies reference-video intake when supplied,
  visual direction, map/text ledgers, a complete animatic and a risk pilot.
- Repository skills are exposed through local skill-directory symlinks;
  changing their repository source changes the installed skill source.

## Findings to resolve during the example

| Finding | Evidence | Effect on future work |
| --- | --- | --- |
| Generated sound rules disagree about continuous ambience. | `docs/audio-rules.md` permits room tone, wind and restrained crowd ambience; `docs/video-rules.md` and the long-form contract prohibit continuous ambience and require isolated cues with silence. | Make the accepted SFX behavior consistent across rules, prompts and review. |
| The Shorts state contract omits a separate accepted-voice stage. | `docs/workflow.md` has voice generation/review before timestamps; `skills/chronostick-pipeline/references/stage-contracts.md` and the state template move directly from script to timestamps. | Ensure a resumed run can identify the actual accepted voice and its review before deriving timing. |
| Optional voice direction is documented but absent from the Shorts state schema/template. | Stage contracts describe `01a`; `docs/pipeline/pipeline-state.schema.json` permits only numeric IDs `01`–`10` and has no `skipped` status. | Represent used/skipped voice direction consistently, with an explicit compatibility decision for existing states. |
| General automation checks retain episode-specific assumptions. | `scripts/validate-repo.sh` hard-codes Episode 002's 17 jobs, seed range and r003 settings. Long-form has a separate stage-aware validator; `scripts/new-longform-episode.py` provides its scaffold. | Extend checks for the selected format so the new episode is checked against its own declared profile, timing and reference map. Preserve legacy checks where needed. |

These findings do not authorize choosing the user's creative changes or marking
new artifacts approved. Episode-specific historical overrides remain scoped to
their existing episodes.

## Iteration record

For each selected change, record the intended behavior, affected stage and
files, actual example artifact, validation result and review decision here or
in the episode's planning/state files. Promote the resulting rule into active
documentation when its scope and review are established. Keep production notes
out of generator-facing prompt files.

## Checks

- Repository skills passed `scripts/validate-skills.sh` during this inspection.
- `scripts/validate-repo.sh` passed, including Episode 006's long-form checks.
  Its four empty-prompt warnings concern the intentionally missing Episode 001
  prompts; they remain documented gaps.
- `git diff --check` passed; it does not include newly untracked files.
- No existing production rule, skill, episode or media was changed by this review.

## Example implementation update — 2026-10-05

The earlier intake/design statements above describe the initial audit. The real
example now lives in `episodes/007-guy-fawkes-mask/`: original reference moved
with hash verification, actual Ajil extraction retained, joint frame/transcript
analysis and claim corrections recorded, Spanish scenario drafted and neutral
rough boards generated/reviewed as r002. Three new installed skills, a Short
scaffold, transcription helper, state v2 schema and stage-aware validator are
implemented. Active routing/defaults now specify 20–30-second Shorts, dynamic
4–7-second editorial clips and 16 steps. See `docs/reference-first-shorts.md`.

Scenario/storyboard await user review; production references, user voice, final
timing, duration pilot, generation jobs/renders and masters remain unavailable.
No H3 batch was launched. Later modules must be exercised against this example
as inputs and actual reviews arrive. Native-video/audio machine review failed;
frame inspection limitations are explicit in the episode intake review.
