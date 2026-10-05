---
name: chronostick-clip-prompts
description: Author pure, creatively directed ultra-fast profile-sized MiniMax H3 prompts from an approved ChronoStick shot plan and reference manifest. Use when clip timing, continuity, and generation-safe references are ready.
---

# Chronostick Clip Prompts

For every clip, make the no-music lock prominent at the opening and ending,
and specify silence as the default between short isolated dry physical SFX.
Transitions and resolved holds do not receive music, tonal atmosphere or sound
beds. Include the exact required policy sentence once. A user report of audible
music rejects that take even when JSON says `music:false`; do not certify the
next render from stronger wording alone.

Create one English generator prompt per clip under `episodes/<episode>/prompts/`. Prompt files contain no metadata, rationale, approval notes, or checklists.

Before writing, inspect the actual approved images and the shot-to-reference coverage in the episode plan. Resolve any unanchored person, hand, animal, prop, location, or camera view by changing the shot or reference first. More adjectives in a prompt cannot supply missing visual authority.

## Reference-first timing

For `h3-short-dynamic-16step-20-30s`, use each approved 4–7-second editorial duration, not a fixed five seconds. State the supported engine request duration separately; resolve action by the editorial boundary and describe any remaining raw tail as a stable hold for automatic trimming. Write contiguous local shot intervals covering the actual requested duration and identify the editorial boundary. Shot count follows the approved fast, purposeful plan and generation feasibility; fixed eight-shot checks below belong only to legacy rapid-five-second profiles. Accepted voice drives meaning and cut allocation. References must cover every shot; neutral storyboard pages are never generation anchors.

## Required structure

1. Declare one vertical 9:16 sequence with the profile-approved request, output frame grid and editorial duration, and its pacing intent. Reference-first slots have their approved adaptive shot count; legacy five-second rapid profiles retain their eight-shot contract unless the approved plan records an exception.
2. Map every ordered `<Picture N>` exactly once. Picture 1 or the named style authority controls every rendered pixel; other references provide only scene, identity, vehicle, or prop content.
3. Lock every pixel of every shot to the detailed illustrated stick-world: people, hands, animals, architecture, maps, food, sea, sky, smoke, vehicles, shadows, and debris all have the same clean dark drawn outlines, simplified geometry, and non-photographic shading. Empty landscape and prop inserts are not exceptions. Explicitly ban photorealism, live action, realistic skin or fingers, realistic anatomy, photographic backgrounds or textures, glossy 3D, anime, panels, grids, and mixed style.
4. State a binding continuity contract before the shots: inherited start state; exact count and identity of every visible subject; each subject's head, face, costume, hands, size, screen position and gaze; prop count, shape, color, location and ownership; environment geometry and depth layers; current event phase; permitted changes; and resolved end state. Explicitly state zero when an easily hallucinated person or object must be absent.
5. Give contiguous local timestamps and frames from zero through the actual editorial endpoint, then the explicit resolved raw-tail hold. For legacy rapid-five-second profiles write all eight intervals explicitly. In **each** shot, name the approved anchor scene/phase supplying its setting and subjects without repeating the `<Picture N>` mapping; specify exact visible inventory and screen placement, framing/camera height/lens feeling, lighting and palette, one action with a clear start and end, expression or posture, camera behavior, hard-cut boundary, and a short synchronized SFX when physically motivated, otherwise silence. Repeat critical invariants at the point of risk instead of relying only on a global style sentence.
6. Use instantaneous hard cuts unless the approved plan deliberately records a slower exception. State every cut time explicitly. Ban dissolves, temporal morphs, whip-pan masking, speed-ramped blur, or continuous camera motion that merely imitates editing. Camera motion must settle before the end hold.
7. Describe emotion with dot-eye focus, eyebrow angle, closed mouth line, head angle, shoulders, hands, stance, and movement speed. Never request dialogue or lip sync.
8. Describe the current state positively. Do not name a later high-salience event merely to negate it; that can cause premature story events.
9. End with specific visual failure constraints and this exact final sentence: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

## Professional directing standard

- Make the approved shots feel designed, not mechanically divided. Build a miniature setup–escalation–payoff arc and give each cut a new piece of visual information.
- Carry any approved visual joke, ironic contrast or surprise through concrete staging and timing; keep it truthful, readable at phone size and consistent with the shot plan.
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

Request only brief, isolated, non-tonal diegetic SFX synchronized to visible actions: a footstep, cloth movement, paper snap, door click, short wind gust, or single water splash. Keep each cue short and dry, let it end promptly, and leave silence between cues for the external narration. Do not request continuous ambience or room tone, sustained natural sounds, long echoes or ringing tails, repeated rhythmic effects, musical notes, even a short melody, or any sound bed. Explicitly forbid melody, harmony, beat, percussion, rhythm bed, tonal drone/pad/pulse, score, soundtrack, riser, sting, singing, speech, narration, whispers, and musicalized ambience. Retain the exact required final sentence above.

`scripts/build-short-prompts.py` renders the explicitly reviewed `clip-direction.json` into pure model input for the reference-first route. It does not invent direction or approve prompts. Inspect the resulting text, exact picture mapping, frame-contiguous cuts and raw-tail/audio lock before recording prompt review.

## Gate

Reject prompts with timing gaps/overlaps or a shot count that does not match the approved profile/plan, fake speed created only by camera motion, repetitive coverage, unmapped or insufficient references, an unlisted visible subject/prop/location, contradictory actions or states, too many simultaneous movements, chronology leakage, portrait-grounded identity ambiguity, any photographic or mixed-style element anywhere in the frame, vague or sustained audio, overlapping SFX that mask narration, unresolved ending, generated text, or more visual complexity than the reference can control. Prompt completeness reduces drift; it never substitutes for inspecting the generated frames and rejecting failures.
