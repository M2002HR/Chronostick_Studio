# Production profiles

An episode manifest names one profile. Do not mix profile defaults implicitly.

## `omni-10s`

Historical Episode 001 contract: vertical 9:16, exact 10-second generations, at most three references, complete independent clips, hard cuts between clips.

## `h3-short-5s`

- engine/template: MiniMax H3 `h3_ref2va`
- editorial slot: 5.000 seconds
- raw engine request: 5 seconds at 24 fps; H3-valid output is 124 frames (about 5.167 seconds)
- resolution: 480×864, 0.4 MP, 9:16
- sampling: 12 steps, `res_multistep`, `beta`, Lightning off
- reference images: two to four normally; dynamic service maximum nine
- `ref_image_size`: `match`
- audio: native SFX-only stream required; no music, dialogue, narration, or voices
- media: immutable raw plus exact 5.000-second editorial normalization; no time stretch
- execution: validate the complete batch first, then sequential GPU concurrency one
- retries: transient connection/time-out failures only; preserve fixed seed
- first pass: no concat and no upscale

Every generator prompt defines all ordered `<Picture N>` references and contains exactly: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

## `h3-short-5s-16step-rapid-cut`

Episode 003 rapid-editorial variant for narration that changes historical subject several times within a short runtime:

- engine/template: MiniMax H3 `h3_ref2va`
- editorial slot: 5.000 seconds; immutable 124-frame raw plus exact 5.000-second normalized copy
- resolution and frame rate: 480×864, 24 fps, vertical 9:16
- sampling: 16 steps, `res_multistep`, `beta`, Lightning off; this is an explicit Episode 003 override of the 14-step future-episode default
- reference images: one generation-safe single-scene anchor normally; two only at a required subject or era handoff
- multi-panel boards and multi-pose identity sheets remain design inputs and are not passed directly to H3
- pacing: 6–8 explicit hard-cut shots per five-second clip; Episode 003 fixes all nine clips at eight shots
- typical shot length: approximately 0.38–0.85 seconds, with a longer resolved terminal hold when required
- motion: one primary action, no more than one simple camera move, and no more than two low-amplitude secondary movements per shot
- energy source: framing changes, inserts, reaction angles, silhouette changes, and hard cuts; never unstable camera motion or simultaneous complex choreography
- boundary: every action and camera move resolves before 5.000 seconds; a tail-freeze episode locks its final composition before the generated boundary
- audio: native SFX-only stream; no music, dialogue, narration, or voices
- execution: validate the complete batch first, then sequential GPU concurrency one; preserve fixed seeds on transient retry

This is a named high-density exception to the ordinary 2–4 H3 micro-beat guideline. Use it only when the approved shot plan demonstrates that every short shot remains visually simple and reference-achievable.

Every generator prompt defines all ordered `<Picture N>` references and contains exactly: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

## Optional sub-second tail extension

For future H3 episodes, a narration overhang of at most 1.000 second beyond the final complete five-second generated slot may use a post-concat `freeze_last_frame` extension instead of generating an otherwise-empty extra clip. The timing map must record both the default ceiling count and the reduced generated count, and the last prompt must end on a resolved freeze-safe frame. Generated SFX are padded with silence; the external narration continues normally. Use `scripts/extend-last-frame.sh` after concat and before upscale. This exception does not permit truncating narration, time-stretching media, or freezing through a new visual event.

## `h3-short-5s-16step-continuity`

Episode 002 r003 continuity-focused variant of `h3-short-5s`:

- engine/template, dimensions, frame rate, raw duration, editorial normalization, sampler, scheduler, Lightning, audio, execution, and retry behavior are unchanged
- sampling: 16 steps
- reference images: one generation-safe single-scene anchor normally; two only when a separate subject/state anchor is necessary
- multi-panel master sheets remain design inputs and are not passed directly to H3
- pacing: three to four precisely timed shots per five-second clip
- continuity: each recurring-character prompt declares its start state and resolved end state; adjacent clips may make a clean editorial cut but must not regress the story state

Every generator prompt defines all ordered `<Picture N>` references and contains exactly: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`
