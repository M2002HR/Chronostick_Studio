# Production profiles

An episode manifest names one profile. Do not mix profile defaults implicitly.

## `h3-short-dynamic-16step-20-30s`

The 2026-10-05 reference-first Shorts default; existing profiles remain scoped
to their episodes. Spanish 9:16, chosen 20–30-second target, 480×864 at 24 fps,
MiniMax H3 `h3_ref2va`, 16 steps, `res_multistep`, `beta`, Lightning off and
`ref_image_size: match`. Editorial slots vary from 4 to 7 seconds; raw engine
frame counts and editorial durations are recorded separately, with immutable
normalization and no time stretch. A 4-second editorial slot may request 5
seconds to remain inside the service's documented trained frame range, settle
before 4 seconds and hold through the raw tail; actual quality requires a pilot.

Reference-first video/transcript analysis and a reviewed neutral sketch
storyboard precede production reference generation. Production identities and
anchors are single-person/single-scene full-frame stick-world images, never
grids or multi-pose sheets. Prefer one or two ordered references per clip;
larger allocations require explicit shot coverage and capability validation.
Cut density is chosen for the actual slot and narration rather than a fixed
eight-shot quota. Maintain one action and at most one camera move per shot.
Only isolated, short natural SFX with silence; no generated speech or music.
Every video prompt contains the exact mandatory no-music sentence once.

Follow `docs/reference-first-shorts.md`. Dynamic job/selection checks and render
quality are exercised when the real episode reaches those stages; this profile
does not claim those stages have already passed a pilot.

An accepted user voice can have an explicit episode-only runtime exception.
Keep the original working target, exact decision evidence and voice SHA-256 in
`episode.json.duration_override`; the selected picture endpoint is the first
24-fps frame that covers the complete audio. This changes that episode's total
runtime only, never the 4–7-second clip contract or future 20–30-second default.
Episode 007 follows the user's continuation of the proposed full-voice route:
33.365333 seconds of unchanged narration and 801 frames / 33.375 seconds of picture.

Long-form profile `h3-long-5s-14step-16x9` is defined in `docs/longform/format-contract.md`; service request profile names are separate from project production-profile names.

For Episode 006, the user explicitly authorized a 12-step full batch. Its named episode override is `h3-long-5s-12step-16x9`, recorded in that episode's `episode.json` as `generation_steps: 12`. All other 16:9 parameters remain the long-form profile values. The job builder and validator read this episode-level choice; the 14-step profile remains the default for later episodes.

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

## `h3-short-5s-14step-rapid-cut-65s`

Episode 004's user-authorized duration and rapid-edit profile:

- MiniMax H3 `h3_ref2va`, vertical 480×864 at 24 fps; preserve the immutable 124-frame raw output and normalize each editorial clip to exactly 5.000 seconds
- 13 independent generated clips, producing a 65.000-second picture timeline for narration ending at 62.120 seconds
- 14 sampling steps, `res_multistep`, `beta`, Lightning off; fixed unique seeds
- one approved full-frame single-scene reference normally, two only for an explicitly mapped scene handoff; no multi-panel board or multi-pose identity sheet passed directly to H3
- Clips 01–12 use eight simple, materially distinct hard-cut shots each. The original Clip 13 plan uses four shots; after r001 review, the r002 replacement uses three compositions with the final frame and exact `SUBSCRIBE` button visible from frame 21 and held still after narration ends. The r002 exception is recorded in `plan/retry-direction-r002.md`.
- one primary action and at most one simple camera move per shot; low background motion; no cross-generation match move
- native natural SFX only, with no generated narration, speech, voices, or music; the only readable-text exception is the exact white `SUBSCRIBE` lettering on one red button in Clip 13, explicitly requested by the user
- sequential batch after complete preflight; immutable media revisions and no overwrite

The user accepted the supplied 62.120-second voice despite the normal 40–60-second default. The narration extends 2.120 seconds beyond 60.000, so the one-second final-frame-extension exception does not apply. Every generator prompt defines its ordered `<Picture N>` references and contains exactly: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

## `h3-short-5s-14step-rapid-cut-55s`

Episode 005's user-authorized rapid-edit profile:

- MiniMax H3 `h3_ref2va`, vertical 480×864 at 24 fps; retain the immutable 124-frame raw output and normalize every editorial clip to exactly 5.000 seconds
- 11 independent generated clips, producing a 55.000-second picture timeline for narration ending at 52.520 seconds
- 14 sampling steps, `res_multistep`, `beta`, Lightning off; fixed unique seeds
- exactly eight materially distinct hard-cut shots in every clip; Clip 11 completes seven fast shots by local 2.300 and holds its eighth resolved handshake tableau unchanged through local 5.000
- one primary action and at most one simple camera move per shot; zero to two low-amplitude secondary movements; no cross-generation match dependency
- one approved full-frame single-scene reference normally; two only for an explicitly mapped subject or scene handoff; no multi-panel board or multi-pose identity sheet passed directly to H3
- native isolated natural SFX only, with no generated narration, speech, voices, sustained ambience, tonal bed, or music
- no generated readable text; the spoken subscription CTA remains external narration and any CTA typography is added during editorial finishing
- sequential batch only after complete preflight; immutable media revisions and no overwrite

The user explicitly accepted the supplied 52.520-second voice and the resulting 55.000-second timeline despite the original 40–49-second target. Every generator prompt defines all ordered `<Picture N>` references and contains exactly: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

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
