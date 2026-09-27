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

## `h3-short-5s-16step-continuity`

Episode 002 r003 continuity-focused variant of `h3-short-5s`:

- engine/template, dimensions, frame rate, raw duration, editorial normalization, sampler, scheduler, Lightning, audio, execution, and retry behavior are unchanged
- sampling: 16 steps
- reference images: one generation-safe single-scene anchor normally; two only when a separate subject/state anchor is necessary
- multi-panel master sheets remain design inputs and are not passed directly to H3
- pacing: three to four precisely timed shots per five-second clip
- continuity: each recurring-character prompt declares its start state and resolved end state; adjacent clips may make a clean editorial cut but must not regress the story state

Every generator prompt defines all ordered `<Picture N>` references and contains exactly: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`
