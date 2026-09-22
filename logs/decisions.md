## 2026-09-22 — Omni prompt complexity and pacing

### Decision

Generator-facing Omni prompts must remain operational and visually specific, but should avoid unnecessary historical-person naming, identity discussion, metadata-like language, or other information that the video generator does not need in order to render the scene.

Internal ChronoStick files may retain full historical names, research context, and production mapping.

Generator-facing prompts should primarily describe:

- reference usage
- visible character design
- environment
- shot timing
- camera
- action
- cuts
- motion
- ending frame
- visual prohibitions

### Confirmed Test

Episode 001 Clip 02 initially failed before generation when using the longer identity-heavy prompt.

A simplified generator-facing prompt using the same visual character reference successfully generated the intended video.

Therefore, future generator-facing prompts should prefer direct visual instructions over unnecessary identity exposition.

### Pacing Rule

Controlled motion must NOT result in slow videos.

ChronoStick pacing target:

- Hook clips: 6–8 visual beats per 10 seconds
- Standard body clips: 4–6 visual beats per 10 seconds
- Final clips: 4–5 beats, slowing only near the final resolved frame

Typical shot duration:

- Hook: approximately 0.6–1.8 seconds
- Body: approximately 1.0–2.5 seconds
- Ending hold: approximately 0.5–1.5 seconds

Fast pacing should come primarily from:

- hard cuts
- framing changes
- reaction shots
- inserts
- close-ups

Individual shots should still use moderate, controlled motion.

Permanent principle:

FAST EDITING + MODERATE MOTION.

Never interpret motion control as static or slow storytelling.