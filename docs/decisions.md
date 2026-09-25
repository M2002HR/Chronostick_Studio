# Decision record

This file records durable production decisions and the evidence behind them. Active rules derived from these decisions live in the focused documents under `docs/`.

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

## 2026-09-22 — Separate internal specifications from generator prompts

### Decision

Files in prompt directories contain only paste-ready generator input. Metadata, design rationale, checklists, approvals, and generation logs live elsewhere.

### Reason

Long internal specifications are valuable to collaborators but add irrelevant identity and process language when sent directly to a generator. Separation keeps both layers precise.

## 2026-09-22 — Style and identity authority

### Decision

The approved master style reference controls rendering. Character sheets control identity only. World sheets control recurring environments and prop language. If complexity must be reduced, simplify backgrounds before characters.

### Reason

This prevents character-reference artifacts from overriding the studio style and prevents recurring people from being redesigned between shots.

## 2026-09-22 — Complete ten-second generations

### Decision

Every AI video generation is exactly 10 seconds, finishes its action, settles camera motion, and reaches a readable ending without depending on the next generated clip.

### Reason

Cross-generation motion and match-frame dependencies are unreliable. Editorial continuity comes from narration, story logic, and hard cuts.

### Historical scope

This remains the Episode 001 Omni contract. It is not a global duration rule for engines introduced later.

## 2026-09-25 — H3 short-clip production profile

### Decision

The `h3-short-5s` profile uses 17 independent 5.00-second editorial slots at 480×864, 24 fps, 12 steps, `res_multistep`, `beta`, Lightning disabled, and two to four ordered references per clip. MiniMax H3 emits 124 frames for the request, so the immutable raw result is retained and an exact 5.000-second editorial copy is created without time stretching.

All jobs are schema-, path-, collision-, reference-mapping-, and capability-validated before any batch child is queued. The batch is sequential on a single GPU, preserves seeds on retry, continues after non-transient clip failures when configured, and never overwrites a revision.

### Reason

Engine constraints and editorial timing are different contracts. Keeping them in a named profile preserves Episode 001 history while allowing repeatable H3 production without misleading global rules.

## 2026-09-22 — No background music

### Decision

ChronoStick uses no background music at generation or assembly time. Natural diegetic effects and separately recorded narration are allowed. Every video prompt includes the exact sentence: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

### Supersedes

Earlier Episode 001 working notes that mentioned a continuous music track.

## 2026-09-22 — Git and media revision strategy

### Decision

Git history versions text. Generated media uses immutable `-rNNN` revisions. Media is never overwritten, and filename suffixes such as `final2` are forbidden.

## 2026-09-22 — Missing Episode 001 prompts remain missing

### Decision

The owner confirmed that the final video was completed but the final prompts from Clip 03 onward were not saved. Clip 03–06 prompt files remain intentionally empty. They must not be reconstructed and represented as the original successful prompts.

### Reason

An explicit gap is more trustworthy than a plausible fabrication. Future prompts may be newly authored from the shot plan, but must be labeled as new drafts.
