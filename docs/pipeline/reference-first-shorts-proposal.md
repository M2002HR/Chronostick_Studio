# Reference-first Shorts: requirements and implementation plan

Captured from the user's instruction on 2026-10-05. The requirements below
describe the requested future route. This document records the design review;
it does not claim implementation, new skill installation, media generation or
production validation. Implementation will proceed against the supplied
example video, stage by stage.

## Requested defaults and scope

- Start the example Short from a downloaded reference video, rather than a
  separately supplied source text.
- Spanish is the default release language.
- Target 20–30 seconds, preferably near 30 when the material benefits from it.
  Record the episode's chosen target at intake; actual accepted voice and final
  picture must fit it. Compression must remove or rewrite content rather than
  make an unintelligible voice or omit necessary historical qualifications.
- Choose each final generation clip's editorial duration dynamically within
  4–7 seconds. Clip length and shot length are different: a clip contains fast,
  purposeful hard-cut shots.
- Use 16 sampling steps by default for the new Shorts route, with Lightning off
  and existing sampler/scheduler unless separately changed.
- Preserve detailed cinematic ChronoStick style across every production pixel;
  the deliberately neutral rough storyboard is a planning exception.
- No background music, generated speech or lip sync. Use small, isolated,
  action-synchronized natural SFX with silence between cues.
  Every video prompt retains exactly:
  `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`
- The generative engine supplies creative edits within clips. Final assembly
  joins reviewed clips, normalizes their duration, upscales and mixes the
  accepted voice; the plan must not depend on a separate manual editing pass to
  rescue impossible cuts, missing shots, maps or effects.
- Keep existing episodes and their accepted profiles unchanged. Shared modules
  may serve long-form; do not silently replace long-form's duration, pacing,
  landscape format or sampling profile with Shorts defaults.

## Stages and reviewable handoffs

| Stage | Work | Handoff and gate |
| --- | --- | --- |
| 1. Video intake | Preserve original downloaded video; record provenance when known, hash, duration, streams, dimensions, language and chosen target. | Original video and intake/probe record; unknown origin or missing audio recorded honestly. |
| 2. Ajil transcription | Extract a traceable audio derivative; use Ajil STT to obtain original-language text, word timestamps and segment timestamps. Preserve the returned body unchanged and derive separate readable/timing artifacts. | Transcript, timed words/segments, audio hash and provider/model provenance; review errors, omissions, names and apparent speech created from SFX/music. |
| 3. Director/editor analysis | Watch actual motion and listen alongside the transcript across the complete video, including every cut. Identify hook, story, people, props, emotion, actions, framing, pacing, visual explanations, payoff and replay/loop opportunity. | Timecoded analysis linking source shots and spoken beats to intended adaptations, with observed/inferred/unknown distinctions and feasibility decisions. |
| 4. Scenario and Spanish script | Preserve useful story architecture, character roles and visual mechanisms closely; write original, natural, compelling Spanish compressed to the chosen target. Verify historical claims separately where applicable. | Scenario/beat list and clean Spanish draft; source-to-adaptation trace and explicit omissions/qualifications. |
| 5. Neutral rough storyboard | Draw a simple sketch sequence for every intended shot, from the scenario and actual source video. Use only enough lines/forms to show composition, people, props, one action, camera and cut logic. | Actual reviewable sketch images plus shot IDs/notes; user reviews scenario and storyboard before production reference generation. |
| 6A. Production references | Derive identities, worlds, props and scene coverage from the approved storyboard and source analysis. Inspect reuse first; save exact pure prompts before creating and reviewing images. | Approved single-person identities and full-frame single-scene stick-world references; shot-to-anchor coverage and selected revisions/hashes. |
| 6B. Spanish narration and supplied voice | Finalize the exact creative Spanish wording; user supplies the generated voice. Listen for wording, pronunciation, intelligibility, performance and measured target duration. | Accepted immutable audio, script and review. This branch may proceed alongside reference production after scenario/storyboard review. |
| 7. Ajil voice timing | Transcribe the actual supplied Spanish voice through the same Ajil module; compare words against the accepted script and check timings against the sound. | Separate raw voice-response record, reviewed word/segment timings and validation report. Source-video timings cannot stand in for Spanish timing. |
| 8. Final timed direction | Reconcile voice timing with the approved scenario, sketches and references. Choose 4–7-second clip boundaries around semantic beats and achievable visual handoffs. | Final shot plan, variable-duration timing map, story-state ledger and complete reference coverage; review material creative changes. |
| 9. Pure video prompts | Write detailed generator text for each actual clip duration and its rapid internal shots. Ground inventory, identity, action, composition, camera, lighting, emotion, local cuts, SFX and resolved ending in reviewed references. | Pure prompts with contiguous shot times and exact audio sentence; no unresolved reference coverage or timing contradictions. |
| 10. Jobs and preflight | Build deterministic JSON with ordered references, fixed unique seeds, actual durations, 16 steps and immutable output revisions. Check paths, schemas, service capabilities, collisions and total timeline. | Passing repository checks and live dry-run; explicit batch execution state. |
| 11. Batch and review | Generate sequentially; inspect actual picture around every cut and listen to every clip. Replace only failed clips, preserving accepted work. | One reviewed editorial take per variable-duration slot, decision evidence and selection provenance. |
| 12. Finish and delivery | Concatenate in order, upscale, mix the accepted Spanish voice with restrained SFX and review complete playback and replay behavior. Prepare thumbnail and metadata. | Immutable picture/SFX and narrated distribution masters, review/probe records and truthful delivery status. |

Reference-video intake, Ajil transcription, joint video/transcript analysis,
neutral storyboard principles and shot-to-anchor coverage can serve long-form
with format-specific rhythm and planning. Scope numeric default changes
explicitly rather than infer them from module reuse.

## Directing and reference design

Keep adaptation close in narrative purpose and useful directing mechanisms,
while rewriting the language and translating imagery into the stick world.
Record what is retained, compressed, changed or dropped, and why. A reference
video is creative/source input, not independent proof of historical claims.
Avoid copying its exact wording or treating its frames as approved production
assets. Spoken transcription does not extract on-screen writing: inspect that
visually and record any required generated-text exception separately.

The rough storyboard establishes visual logic, not the production look. Use
plain monochrome sketches without rendering, palette, costume detail, locked
face design or ChronoStick style. Keep production character cues in a separate
brief. Never supply these neutral sketches directly as H3 style/identity
references. Their approval does not approve later identity designs.

Analyze source techniques for H3 feasibility before approving the storyboard:
retain achievable cuts/actions, adapt difficult ones, and document replacements
for speed ramps, multilayer overlays, complex choreography or exact match moves
that generation cannot reliably deliver. Each shot has one primary action and
at most one simple camera move. Use framing contrast, reactions, inserts,
reveals and escalation for rapid energy; do not turn speed into repeated images
or unreadable motion. Episodes 003/004 inform the energetic direction without
imposing exactly eight shots on every new variable-duration clip.

Reference count follows coverage, not a fixed episode-wide quota. For every
storyboard shot, map the required identity, visible counts, costume, prop,
location, camera view, light and story phase to an actual approved image.
Add distinct full-frame images for unsupported angles, scenes or states.
Each image has one scene/view/state; character identities show one person,
not sheets, turnarounds, grids or expression boards. Prefer one or two H3
inputs per clip when sufficient; settle any larger allocation or clip
repartitioning explicitly against the new profile and installed capability.

Reference production can begin before accepted voice timing because composition
and identities are already reviewed. Its shot IDs and timing remain provisional.
After voice timing, recheck every shot and affected reference instead of silently
using obsolete assets, cutting necessary speech or resetting the story state.

## Ajil implementation findings

The local gateway implements `POST /v1/audio/transcriptions` through Groq STT
in `ajil/unified_gateway/app/main.py` and `providers/groq_adapter.py`.
Its configuration currently defaults to `verbose_json` and segment timestamps.
The provider supports forwarding configured `word,segment` granularities.
The implementation must request both, validate the returned words and preserve
the raw response; endpoint existence is not proof of actual alignment quality.

The current route accepts an uploaded audio file and an optional language query
argument. Model and timestamp granularity come from gateway configuration rather
than per-request fields. Use source-language detection at intake and an explicit
Spanish language for accepted narration where supported. Review the actual
effective configuration safely without printing credentials; do not assume
the running service matches defaults in source code.

STT word timing is an estimate requiring review, not guaranteed exact forced
alignment to the supplied script. Correct mistaken text only in a derived
reviewed representation. If words or times are absent or inconsistent, resolve
the extraction/alignment issue before final timing; never fabricate exact times.
For long-form, audio-size chunking must preserve absolute offsets and check
seams. Keep the reference transcript and accepted-voice transcript in separate
artifact branches with their own audio hashes.

## Dynamic duration findings

The installed service already accepts floating-point generation duration and a
separate editorial duration. Its resolver rounds requested frames upward onto
the H3 `17n+5` grid. Inspection of the actual function at 24 fps gives:

| Requested duration | Raw frames | Raw nominal duration | Editorial frames |
| --- | --- | --- | --- |
| 4 s | 107 | 4.458333 s | 96 |
| 5 s | 124 | 5.166667 s | 120 |
| 6 s | 158 | 6.583333 s | 144 |
| 7 s | 175 | 7.291667 s | 168 |

The service documents 124–362 frames as H3's trained range and warns outside it.
A proposed 4-second editorial clip can request at least the supported 5-second
generation, resolve its action before 4 seconds and hold through the remaining
raw output. Automatic duration normalization trims picture/SFX to the planned
96-frame editorial copy without time-stretching or changing its creative edits.
This is a proposed strategy to pilot, not an observed quality result. Direct
4-second generation remains unproven by the inspected capability.

Record per clip: global start/end, editorial duration/frame count, generation
request duration, resolved raw frames, source word/beat coverage, local shot
intervals, final settled state and normalization provenance. Choose boundaries
on the 24-fps editorial grid; account for subframe STT times honestly. Sum actual
editorial durations for the master; remove fixed `ceil(end/5)` and fixed-five-
second normalization assumptions from the new route.

## Skill and code plan

Use focused modules rather than duplicate entire pipelines. Candidate new skill
names are proposals until implemented and installed:

| Module | Plan |
| --- | --- |
| `chronostick-transcribe` (new) | Shared Ajil extraction/transcription, raw-response preservation, separate reference/voice modes and timing QC; reusable audio helper. |
| `chronostick-reference-video` (new) | Joint actual-video/transcript directing analysis, adaptation trace and generation-feasibility decisions; reuse appropriate long-form intake guidance. |
| `chronostick-storyboard` (new) | Neutral sketch production/review from scenario and analysis; stable shot IDs and reference requirements. |
| `chronostick-pipeline` | Route the reference-first stages and parallel reference/voice branches; record dependencies, real approvals and downstream invalidation. |
| `chronostick-script` | Reference-derived Spanish narrative, 20–30-second chosen target, compression and source fidelity. |
| `chronostick-timestamps` / `chronostick-shot-plan` | Accepted-voice timing, variable boundaries and final reconciliation with storyboard/references. Keep extraction separate from creative timing decisions. |
| `chronostick-references` | Storyboard/source-driven single-person identities and enough reviewed single-scene anchors with explicit coverage. |
| `chronostick-clip-prompts` / `chronostick-generation-jobs` | Actual clip durations, fast purposeful shot timing, 16-step default, raw/editorial distinction and deterministic JSON. |
| `chronostick-batch` / `chronostick-review` / `chronostick-finish` | Variable-duration preflight, generation and QC, selected-take checks, complete narrated delivery. |

Add a new named profile, a Shorts scaffold and stage-aware validator. Update the
pipeline-state schema/template, production defaults, workflow, audio rules,
profile docs and skill catalog together with each exercised module. Update
long-form routing only for the shared capabilities selected for that format.
Do not relabel validation as creative approval or invalidate old approved media.

## Example-driven implementation order

1. With the supplied video, implement and verify intake plus Ajil transcription;
   retain the real extraction output and test preservation/timing contracts.
2. Implement video analysis, source fidelity and the compressed scenario/Spanish
   draft; produce and review actual neutral storyboard images.
3. Implement reference design and reviewed coverage while finalizing narration;
   then ingest the user's generated voice and derive its actual timings.
4. Reconcile the plan; pilot variable-duration H3 at 16 steps before the full
   example batch, including the proposed 4-second editorial strategy when used.
5. Implement prompt/job/preflight checks, generate and review the batch, finish
   the narrated Short and save the complete delivery evidence.

No reference video, storyboard, voice, new episode or production batch exists
for this example yet. No provider call or GPU generation was made during this
design review.

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
