---
name: chronostick-clip-prompts
description: Author pure, creatively directed ultra-fast five-second MiniMax H3 prompts from an approved ChronoStick shot plan and reference manifest. Use when clip timing, continuity, and generation-safe references are ready.
---

# Chronostick Clip Prompts

Create one English generator prompt per clip under `episodes/<episode>/prompts/`. Prompt files contain no metadata, rationale, approval notes, or checklists.

Before writing, inspect the actual approved images and the shot-to-reference coverage in the episode plan. Resolve any unanchored person, hand, animal, prop, location, or camera view by changing the shot or reference first. More adjectives in a prompt cannot supply missing visual authority.

## Required structure

1. Declare exactly one 5.00-second vertical 9:16 sequence and its pacing intent. ChronoStick's default rapid profile contains exactly eight materially distinct shots joined by instantaneous hard cuts unless the approved plan records an explicit exception.
2. Map every ordered `<Picture N>` exactly once. Picture 1 or the named style authority controls every rendered pixel; other references provide only scene, identity, vehicle, or prop content.
3. Lock every pixel of every shot to the detailed illustrated stick-world: people, hands, animals, architecture, maps, food, sea, sky, smoke, vehicles, shadows, and debris all have the same clean dark drawn outlines, simplified geometry, and non-photographic shading. Empty landscape and prop inserts are not exceptions. Explicitly ban photorealism, live action, realistic skin or fingers, realistic anatomy, photographic backgrounds or textures, glossy 3D, anime, panels, grids, and mixed style.
4. State a binding continuity contract before the shots: inherited start state; exact count and identity of every visible subject; each subject's head, face, costume, hands, size, screen position and gaze; prop count, shape, color, location and ownership; environment geometry and depth layers; current event phase; permitted changes; and resolved end state. Explicitly state zero when an easily hallucinated person or object must be absent.
5. Give contiguous local timestamps from `0.00` to `5.00`, and frame numbers when frame-accurate cuts matter. For the rapid profile, write all eight shot intervals explicitly, typically about 0.35–0.80 seconds each. In **each** shot, name the approved anchor scene/phase supplying its setting and subjects without repeating the `<Picture N>` mapping; specify exact visible inventory and screen placement, framing/camera height/lens feeling, lighting and palette, one action with a clear start and end, expression or posture, camera behavior, hard-cut boundary, and one short synchronized SFX. Repeat critical invariants at the point of risk instead of relying only on a global style sentence.
6. Use instantaneous hard cuts unless the approved plan deliberately records a slower exception. State every cut time explicitly. Ban dissolves, temporal morphs, whip-pan masking, speed-ramped blur, or continuous camera motion that merely imitates editing. Camera motion must settle before the end hold.
7. Describe emotion with dot-eye focus, eyebrow angle, closed mouth line, head angle, shoulders, hands, stance, and movement speed. Never request dialogue or lip sync.
8. Describe the current state positively. Do not name a later high-salience event merely to negate it; that can cause premature story events.
9. End with specific visual failure constraints and this exact final sentence: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

## Professional directing standard

- Make the eight shots feel designed, not mechanically divided. Build a miniature setup–escalation–payoff arc and give each cut a new piece of visual information.
- Check every shot against the spoken claim with a cause → action → result test. A viewer seeing the shot for under one second must identify the subject and the meaningful change. Avoid arbitrary prop macros, repeated opening frames, or symbolic counters that resemble unrelated objects. When the reference cannot show the actual narrated thing, revise the anchor or use a legible action already in it.
- A dense continuity contract must not crowd out the story. Put the positive action and visual payoff before compact exclusions; shorten shot count through a recorded exception when eight specified states repeatedly become duplicates.
- Use purposeful coverage: establishing geometry, portrait reaction, extreme prop insert, silhouette, foreground reveal, low/high angle, environmental clue, or symbolic payoff. Avoid eight near-identical medium shots.
- Direct lens feeling, camera height, subject scale, negative space, depth layering, key-light direction, practical sources, palette, and contrast only where they make the story more readable or exciting.
- Keep motion generation-safe: one primary action and at most one camera move per shot. Editorial speed comes from hard-cut contrast; subject and camera motion remain controlled.
- Keep each cut within the locations, props, and illustrated visual language actually controlled by its approved single-scene anchors. When a prior render turns an unanchored landscape, animal, hand, or object photographic, replace that coverage with a grounded illustrated composition or revise the anchor before retrying. Stronger negative wording alone is not a reliable repair.
- Treat continuity as a frame-by-frame constraint: named people never duplicate or swap costume, hats, proportions, hands, or positions without an explicit action; props never teleport, multiply, change color, or advance to a later story state; architecture and light do not silently change within a scene. Specify the few stable visual facts that could plausibly drift, including seemingly obvious ones. Keep the wording concrete and consistent rather than repeating long generic ban lists.
- Use match concepts and motivated visual rhymes across cuts—shape, direction, color, prop, or light—without blending frames or compromising chronology.
- Reserve a stable resolved hold at the end of the clip. If post-production will extend the final frame, lock every subject, camera, light, shadow, and environmental motion for the exact approved tail interval.
- For an approved text exception such as a CTA button, prefer a reference containing the finished exact lettering and cut directly to that stable image. Review generated spelling frame by frame; a prompt cannot guarantee exact text.

## Historical identity lock

For named real people, treat the approved portrait-grounded identity or scene anchor as binding. Repeat the compact distinguishing cues needed in the current shots—silhouette, hair, facial hair, costume, proportions, and signature accessory—and explicitly forbid averaging, swapping, duplication, or identity morphing. Use the stylized scene anchor for video continuity; do not ask H3 to reconcile raw photographs with the stick-world.

## Audio lock

Request only brief, isolated, non-tonal diegetic SFX synchronized to visible actions: a footstep, cloth movement, paper snap, door click, short wind gust, or single water splash. Keep each cue short and dry, let it end promptly, and leave silence between cues so the creator can add background music later without competition or masking. Do not request continuous ambience or room tone, sustained natural sounds, long echoes or ringing tails, repeated rhythmic effects, musical notes, even a short melody, or any sound bed. Explicitly forbid melody, harmony, beat, percussion, rhythm bed, tonal drone/pad/pulse, score, soundtrack, riser, sting, singing, speech, narration, whispers, and musicalized ambience. Retain the exact required final sentence above.

## Gate

Reject prompts with gaps/overlaps in timing, fewer than eight distinct shots without an approved exception, fake speed created only by camera motion, repetitive coverage, unmapped or insufficient references, an unlisted visible subject/prop/location, contradictory actions or states, too many simultaneous movements, chronology leakage, portrait-grounded identity ambiguity, any photographic or mixed-style element anywhere in the frame, vague or sustained audio, overlapping SFX that mask later music, unresolved ending, generated text, or more visual complexity than the reference can control. Prompt completeness reduces drift; it never substitutes for inspecting the generated frames and rejecting failures.
