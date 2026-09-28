---
name: chronostick-clip-prompts
description: Author pure, creatively directed ultra-fast five-second MiniMax H3 prompts from an approved ChronoStick shot plan and reference manifest. Use when clip timing, continuity, and generation-safe references are ready.
---

# Chronostick Clip Prompts

Create one English generator prompt per clip under `episodes/<episode>/prompts/`. Prompt files contain no metadata, rationale, approval notes, or checklists.

## Required structure

1. Declare exactly one 5.00-second vertical 9:16 sequence and its pacing intent. ChronoStick's default rapid profile contains exactly eight materially distinct shots joined by instantaneous hard cuts unless the approved plan records an explicit exception.
2. Map every ordered `<Picture N>` exactly once. Picture 1 or the named style authority controls every rendered pixel; other references provide only scene, identity, vehicle, or prop content.
3. Lock the entire frame to the detailed cinematic stick-world: people, architecture, food, sky, smoke, vehicles, shadows, and debris. Explicitly ban photorealism, live action, realistic anatomy, glossy 3D, anime, panels, grids, and mixed style.
4. State inherited start state, exact subject/object count, screen placement, current event phase, and resolved end state.
5. Give contiguous local timestamps from `0.00` to `5.00`. For the rapid profile, write all eight shot intervals explicitly, typically about 0.35–0.80 seconds each. Every shot names its story purpose, framing, composition, main action, simple camera behavior, lighting, emotion, transition, and synchronized SFX.
6. Use instantaneous hard cuts unless the approved plan deliberately records a slower exception. State every cut time explicitly. Ban dissolves, temporal morphs, whip-pan masking, speed-ramped blur, or continuous camera motion that merely imitates editing. Camera motion must settle before the end hold.
7. Describe emotion with dot-eye focus, eyebrow angle, closed mouth line, head angle, shoulders, hands, stance, and movement speed. Never request dialogue or lip sync.
8. Describe the current state positively. Do not name a later high-salience event merely to negate it; that can cause premature story events.
9. End with specific visual failure constraints and this exact final sentence: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

## Professional directing standard

- Make the eight shots feel designed, not mechanically divided. Build a miniature setup–escalation–payoff arc and give each cut a new piece of visual information.
- Use purposeful coverage: establishing geometry, portrait reaction, extreme prop insert, silhouette, foreground reveal, low/high angle, environmental clue, or symbolic payoff. Avoid eight near-identical medium shots.
- Direct lens feeling, camera height, subject scale, negative space, depth layering, key-light direction, practical sources, palette, and contrast only where they make the story more readable or exciting.
- Keep motion generation-safe: one primary action and at most one camera move per shot. Editorial speed comes from hard-cut contrast; subject and camera motion remain controlled.
- Use match concepts and motivated visual rhymes across cuts—shape, direction, color, prop, or light—without blending frames or compromising chronology.
- Reserve a stable resolved hold at the end of the clip. If post-production will extend the final frame, lock every subject, camera, light, shadow, and environmental motion for the exact approved tail interval.

## Historical identity lock

For named real people, treat the approved portrait-grounded identity or scene anchor as binding. Repeat the compact distinguishing cues needed in the current shots—silhouette, hair, facial hair, costume, proportions, and signature accessory—and explicitly forbid averaging, swapping, duplication, or identity morphing. Use the stylized scene anchor for video continuity; do not ask H3 to reconcile raw photographs with the stick-world.

## Audio lock

Request many literal, synchronized Foley/ambience cues where visible: fabric, footsteps, paper, ceramics, doors, wind, water, engines, birds, debris, and room tone. Explicitly forbid melody, harmony, beat, percussion, rhythm bed, tonal drone/pad/pulse, score, soundtrack, riser, sting, singing, speech, narration, whispers, and musicalized ambience.

## Gate

Reject prompts with gaps/overlaps in timing, fewer than eight distinct shots without an approved exception, fake speed created only by camera motion, repetitive coverage, unmapped references, contradictory actions, too many simultaneous movements, chronology leakage, portrait-grounded identity ambiguity, vague audio, unresolved ending, generated text, or more visual complexity than the reference can control.
