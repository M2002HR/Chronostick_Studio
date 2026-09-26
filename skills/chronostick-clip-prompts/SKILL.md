---
name: chronostick-clip-prompts
description: Author pure, tightly controlled five-second MiniMax H3 prompts from an approved ChronoStick shot plan and reference manifest. Use when clip timing, continuity, and generation-safe references are ready.
---

# Chronostick Clip Prompts

Create one English generator prompt per clip under `episodes/<episode>/prompts/`. Prompt files contain no metadata, rationale, approval notes, or checklists.

## Required structure

1. Declare exactly one 5.00-second vertical 9:16 sequence and its pacing intent.
2. Map every ordered `<Picture N>` exactly once. Picture 1 or the named style authority controls every rendered pixel; other references provide only scene, identity, vehicle, or prop content.
3. Lock the entire frame to the detailed cinematic stick-world: people, architecture, food, sky, smoke, vehicles, shadows, and debris. Explicitly ban photorealism, live action, realistic anatomy, glossy 3D, anime, panels, grids, and mixed style.
4. State inherited start state, exact subject/object count, screen placement, current event phase, and resolved end state.
5. Give contiguous local timestamps from `0.00` to `5.00`. Every shot names framing, composition, main action, simple camera behavior, lighting, emotion, transition, and synchronized SFX.
6. Use instantaneous hard cuts unless the approved plan deliberately calls for a continuous emotional/terminal shot. Camera motion must settle before the end hold.
7. Describe emotion with dot-eye focus, eyebrow angle, closed mouth line, head angle, shoulders, hands, stance, and movement speed. Never request dialogue or lip sync.
8. Describe the current state positively. Do not name a later high-salience event merely to negate it; that can cause premature story events.
9. End with specific visual failure constraints and this exact final sentence: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

## Audio lock

Request many literal, synchronized Foley/ambience cues where visible: fabric, footsteps, paper, ceramics, doors, wind, water, engines, birds, debris, and room tone. Explicitly forbid melody, harmony, beat, percussion, rhythm bed, tonal drone/pad/pulse, score, soundtrack, riser, sting, singing, speech, narration, whispers, and musicalized ambience.

## Gate

Reject prompts with gaps/overlaps in timing, unmapped references, contradictory actions, too many simultaneous movements, chronology leakage, identity ambiguity, vague audio, unresolved ending, generated text, or more visual complexity than the reference can control.
