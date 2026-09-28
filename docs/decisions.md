# Decision record

This file records durable production decisions and the evidence behind them. Active rules derived from these decisions live in the focused documents under `docs/`.

## 2026-09-27 — Sub-second final-frame extension

### Decision

When approved narration ends no more than 1.000 second after the last complete five-second H3 slot, a future episode may omit the otherwise-empty extra generation and extend the concatenated picture by cloning the final frame for the exact overhang. The last generated clip must intentionally reach a resolved, freeze-safe state before its boundary. Native generated audio is padded with silence while separately recorded narration continues.

The timing map records the normal ceiling count, the reduced generated count, and the exact extension. `scripts/extend-last-frame.sh` performs the immutable post-concat, pre-upscale operation and writes provenance. Longer overhangs or any overhang containing a new visual event still require another generated clip.

### Reason

Episode 003 narration ends at 45.640 seconds. Generating a tenth five-second clip solely for the last 0.640 seconds would add cost and a visually unnecessary scene. A controlled freeze preserves the complete narration, keeps the resolved ending stable, and avoids time stretching or silent truncation.

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

## 2026-09-26 — Episode 002 r003 continuity references

### Decision

Episode 002 r003 uses the `h3-short-5s-16step-continuity` profile. It increases sampling from 12 to 16 steps and replaces the multi-panel style, world, character, and vehicle inputs at generation time with nine episode-scoped single-scene anchors. Most clips use one anchor; Clip 12 uses two because it must show both the recurring couple and the separate airborne object.

Each five-second prompt uses three to four precisely timed beats and declares a resolved end state. Recurring-character prompts inherit the prior character state explicitly, particularly across Clips 12–15. Pre-event aircraft and falling-object prompts state only the current physical state and unchanged intact environment; later consequence concepts are omitted from those prompts.

### Reason

The r002 results showed three coupled failure modes: contact-sheet imagery copied into video frames, duplicate recurring characters from multi-pose identity sheets, and narrative completion occurring earlier than the narration. Single-scene anchors reduce compositional ambiguity, while fewer timed actions and explicit start/end states improve identity tracking and narrative order. More sampling steps may improve refinement but are not treated as the mechanism that fixes continuity.

## 2026-09-26 — Selected-clip master assembly

### Decision

Each episode keeps a `renders/final-selected/` staging directory containing exactly one human-approved video for every numbered clip. Filenames retain both the two-digit clip number and immutable render revision. Final assembly validates a complete, duplicate-free number sequence, sorts naturally by filename, concatenates through the automation service, waits for a terminal result, and writes the next unused master revision under the episode's `final/` directory.

Captions, narration mix, and background audio are not implicit parts of concatenation. If those stages are approved later, they must be explicit and independently reviewable post-production stages.

### Reason

The best take can differ per clip across render revisions. A dedicated selection layer makes that choice visible, prevents accidental ordering or omission, preserves provenance in filenames, and keeps future finishing work separate from lossless assembly.

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

## 2026-09-28 — Episode 003 rapid-cut profile and symbolic presidential identities

### Decision

Episode 003 uses `h3-short-5s-16step-rapid-cut`: nine five-second H3 clips at 16 steps, each directed as eight short hard-cut shots. The user explicitly selected 16 steps as an episode override of the 14-step future default. Cut frequency, inserts, framing changes, and silhouette contrast create speed; the one-action/one-camera-move motion budget remains unchanged. Clip 09 locks its final memorial frame at local 4.20 seconds so the approved 0.640-second external tail freeze contains no new visual event.

The four assassinated presidents each receive a reusable, full-frame, single-person ChronoStick identity anchor. Their distinguishing cues are Lincoln's extreme height, stovepipe hat, and chin beard without mustache; Garfield's broader silhouette and full beard with mustache; McKinley's clean-shaven receding hair and scarlet lapel carnation; and Kennedy's youthful swept hair and modern navy suit. Six episode-scoped single-scene anchors combine those identities with the required historical worlds. H3 receives no more than two scene anchors per clip and does not receive the identity anchors directly under normal operation.

### Reason

The user explicitly prioritized a pace faster than prior episodes while requiring all four figures to remain recognizable in the symbolic stick-figure language. A named profile prevents this episode-specific density from silently changing global H3 behavior. Separating four identity authorities from six generation-safe scene anchors keeps the four people distinct without exposing H3 to multi-pose sheets, repeated identities, or unnecessary references.
