# Video generation rules

## Format and boundaries

- use the named production profile for requested duration, engine resolution, frame rate, and reference limit
- use vertical 9:16 unless the profile explicitly says otherwise
- a complete visual idea within each clip
- final action and camera movement settled before the profile boundary
- a new clip begins with a clean hard cut, not a cross-generation match move

## Pacing

- for 10-second Omni clips: hook 6–8 beats, body 4–6 beats, ending 3–5 beats
- for 5-second H3 clips: approximately 2–4 readable micro-beats; reduce density before sacrificing clarity
- reserve a short resolved hold when useful

Permanent principle: FAST EDITING + MODERATE MOTION.

Energy comes from hard cuts, inserts, reaction shots, close-ups, and framing changes. Do not create energy through unstable camera work or complex simultaneous animation.

## Per-shot budget

- one main action
- no more than one simple camera move
- zero to two subtle secondary movements
- low background motion

Split a shot with a hard cut if it exceeds this budget.

## References

Use the profile-specific maximum. State what every reference controls and keep JSON array order identical to `<Picture N>` order. Do not let multiple views on one character sheet become multiple characters.

## Generated content restrictions

- no narration, character dialogue, speech, or lip sync
- no subtitles, CTA text, labels, legal copy, or other readable generated text
- no background music
- only controlled natural ambience and Foley

Every video prompt must include: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

## Review failures

Reject or retry outputs with identity drift, style drift, extra foreground characters, historical anachronisms, unreadable action, excessive motion, unfinished endings, generated text, speech, or music.
