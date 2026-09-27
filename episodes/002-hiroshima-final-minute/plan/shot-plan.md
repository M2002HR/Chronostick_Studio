# Episode 002 — r003 continuity shot plan

## Production metadata

- status: r003 configured for sequential H3 generation
- profile: `h3-short-5s-16step-continuity`
- timeline: 00:00.000–01:25.000
- narration: supplied Spanish, 00:00.460–01:24.520
- format: 17 vertical 480×864 clips, 5.000-second editorial slots, 24 fps
- H3 raw: 124 frames, approximately 5.167 seconds; retain immutable raw and normalize editorial copy to exactly 5.000 seconds
- sampling: 16 steps, `res_multistep`, `beta`, Lightning off, fixed per-clip seeds
- references: one single-scene image for Clips 01–11 and 13–17; two single-scene images for Clip 12
- pacing: three to four timed shots per clip; one primary action and at most one camera move per shot
- audio: synchronized natural SFX only; no generated speech, narration, voices, or music

## Narrative and ethical guardrails

The verified facts are the 8:15 a.m. attack and Hiroshima City's estimate of approximately 140,000 deaths by the end of 1945. The elderly couple and exact countdown are dramatized narration devices, not identified historical people. Ordinary civilian life, recognition, connection, white transition, and respectful scale of loss form the visual arc. No graphic injury, bodies, gore, screams, triumphal imagery, weapon glamour, generated text, or spectacle-driven destruction.

## Reference allocation

| Clips | Ordered references |
| --- | --- |
| 01, 04–06 | Picture 1 city-morning anchor |
| 02–03 | Picture 1 breakfast-couple anchor |
| 07, 09 | Picture 1 couple-window anchor |
| 08 | Picture 1 B-29-crossing anchor |
| 10 | Picture 1 bomb-release anchor |
| 11 | Picture 1 falling-object anchor |
| 12 | Picture 1 couple-window anchor; Picture 2 falling-object anchor |
| 13–14 | Picture 1 couple-departure anchor |
| 15 | Picture 1 couple-flash anchor |
| 16–17 | Picture 1 aftermath anchor |

The original multi-panel sheets are not supplied to H3. This prevents panel borders, style-board imagery, repeated poses, cloned characters, and later-story imagery from leaking into earlier clips.

## Continuity state map

| Clip | Global time | Narration overlap | Start state | Controlled change | Resolved end state |
| --- | --- | --- | --- | --- | --- |
| 01 | 00:00–00:05 | “60 segundos antes de la bomba atómica, Hiroshima parecía” | intact city, ordinary morning | leaf detail to city scale | stable peaceful city wide |
| 02 | 00:05–00:10 | “parecía una mañana normal. Una pareja anciana terminaba de desayunar. La” | couple seated at breakfast | bowl to tray; newspaper folds | woman seated left with tray; man seated right with folded paper |
| 03 | 00:10–00:15 | “La alarma había sonado antes, pero ya se había” | exact Clip 02 end state | both notice silence, then relax | both still seated; quiet window in focus |
| 04 | 00:15–00:20 | “había callado. 40 segundos. Afuera,” | intact exterior | calm residents and cart | ordinary empty foreground street |
| 05 | 00:20–00:25 | “Afuera, niños pasan. Una bicicleta cruza. El sol” | same normal street | three children and one bicycle cross safely | street clears normally |
| 06 | 00:25–00:30 | “sol cae limpio sobre la calle. Treinta segundos. Un” | normal sunlight | tilt from street to sky | stable empty blue sky; no engine yet |
| 07 | 00:30–00:35 | “Un zumbido rompe la mañana. El anciano levanta la vista. Un” | man seated near window; woman behind | hum; man lifts gaze and stands | man standing at window; woman behind; tiny distant plane |
| 08 | 00:35–00:40 | “Un B-29 atraviesa el cielo. Veinte segundos.” | one plane enters left | level left-to-right flight | aircraft exits right; unchanged sky |
| 09 | 00:40–00:45 | “—Si fuera peligro real, sonaría la alarma —dice su esposa.” | exact Clip 07 human end state | woman's calm open-palm reassurance | both standing; man's concern unresolved |
| 10 | 00:45–00:50 | “Entonces, algo cae del avión. Pequeño.” | one aircraft in level flight | one object separates once | aircraft high-right; one object lower; city intact |
| 11 | 00:50–00:55 | “Pequeño. Oscuro. Extraño. Diez” | one distant airborne object | continuous gravity-driven descent | object still high and airborne; world unchanged |
| 12 | 00:55–01:00 | “Diez segundos. El hombre entrecierra los ojos. Ahora cae” | man and woman already standing; object airborne | squint, recognition, torso turn | man turned toward wife; wife alert; object still airborne |
| 13 | 01:00–01:05 | “cae más rápido. Cinco segundos. Vámonos.” | exact Clip 12 human end state | beckon and two coordinated steps | both at doorway; hands centimeters apart |
| 14 | 01:05–01:10 | “Vámonos. Ahora. Dos segundos. Él busca su mano.” | exact Clip 13 end state | reach, fingertip contact, one clasp | joined hands centered and still; normal light |
| 15 | 01:10–01:15 | “mano. Un segundo. A las ocho y quince. Un destello blanco” | exact Clip 14 end state | notice brightness; white expands only after 3.20 | stable near-white field by 4.55 |
| 16 | 01:15–01:20 | “blanco borra Hiroshima. Para finales de 1945,” | near-white field | empty debris detail to elevated wide | stable non-graphic aftermath city |
| 17 | 01:20–01:25 | “1945, unas 140.000 personas habrían muerto.” | exact aftermath state | foreground, river, elevated scale | completely stable empty wide from 4.52–5.00 |

## Character and emotion continuity

- Woman: relaxed/content in Clips 02–03; calm reassurance in 09; alert attention in 12; worried but controlled movement in 13–14; quiet fear in 15.
- Man: relaxed in 02–03; mild attention in 07; unresolved concern in 09; focused recognition in 12; controlled alarm and protective urgency in 13–14; braced fear in 15.
- Both characters keep closed mouths throughout. Emotion is expressed through eyebrow angle, dot-eye focus, shoulder tension, head direction, hand gesture, stance, and movement speed.
- Woman remains visually identified by low gray-black bun, navy top, cream apron, loose dark trousers, and sandals. Man remains identified by gray-templed short hair, beige rolled-sleeve shirt, charcoal trousers, and dark shoes.
- Clips 12–15 prohibit spatial resets: no sitting, breakfast action, newspaper handling, tray handling, or return from doorway to table.

## Aircraft, falling-object, and light control

- Clip 08: one aircraft, four engines, level left-to-right path, constant orientation, no object release.
- Clip 10: one release only; aircraft stays level; object moves downward and slightly rearward; separation increases monotonically.
- Clip 11: one object only, always airborne, smaller than four percent of frame height, minimal rotation, normal sky/city/light unchanged.
- Clip 12: object remains airborne; recognition occurs indoors; no later visual state appears.
- Clip 15: normal room color through 3.20; white field expands from doorway only during 3.20–4.55; no impact sound.
- Clips 16–17: consequence only, with no people, aircraft, active near-camera flame, bodies, or spectacle-centered cloud.

## Preflight and review

- validate all prompt Picture tags against JSON order
- validate 16 steps, fixed seeds, r003 output prefixes, no overwrite, exact 5.000-second editorial normalization, and SFX-only audio
- reject any output with a reference layout, repeated foreground identity, narrative regression, early white/damage state, impossible aircraft motion, extra falling object, readable text, speech, music, unfinished action, or unstable final frame
- review each clip independently before concat or upscale
