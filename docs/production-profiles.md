# Production profiles

An episode manifest names one profile. Do not mix profile defaults implicitly.

## `omni-10s`

Historical Episode 001 contract: vertical 9:16, exact 10-second generations, at most three references, complete independent clips, hard cuts between clips.

## `h3-short-5s`

- engine/template: MiniMax H3 `h3_ref2va`
- editorial slot: 5.000 seconds
- raw engine request: 5 seconds at 24 fps; H3-valid output is 124 frames (about 5.167 seconds)
- resolution: 480×864, 0.4 MP, 9:16
- sampling: 14 steps, `res_multistep`, `beta`, Lightning off
- reference images: two to four normally; dynamic service maximum nine
- `ref_image_size`: `match`
- audio: native SFX-only stream required; no music, dialogue, narration, or voices
- media: immutable raw plus exact 5.000-second editorial normalization; no time stretch
- execution: validate the complete batch first, then sequential GPU concurrency one
- retries: transient connection/time-out failures only; preserve fixed seed
- first pass: no concat and no upscale

Every generator prompt defines all ordered `<Picture N>` references and contains exactly: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`
