# Episode 002 — Master shot plan

## Production metadata

- status: r002 ready for operator-run H3 source generation; not launched
- profile: `h3-short-5s`
- timeline: 00:00.000–01:25.000
- narration: supplied Spanish, 00:00.460–01:24.520
- format: 17 independent vertical 480×864 clips, 5.000-second editorial slots, 24 fps
- H3 raw: 124 frames, expected about 5.167 seconds; preserve immutable
- sampling: 12 steps, `res_multistep`, `beta`, Lightning off, fixed per-clip seeds
- references: two to four ordered images per clip; dynamic mapping validated against `<Picture N>`
- audio: native synchronized SFX required; no generated speech, narration, voices, or music
- cut grammar: each 5-second prompt contains a first-frame hook and at least six explicit instantaneous hard cuts; no continuation or match-frame dependency

## Narrative and ethical guardrails

The verified facts are the 8:15 a.m. attack and Hiroshima City's approximate 140,000 deaths by the end of 1945. The elderly couple and exact countdown are dramatized narration devices, not identified historical people. Show ordinary civilian life and then respectful scale of loss. Never depict graphic injury, bodies, gore, screams, triumphant military imagery, weapon glamour, or spectacle-driven destruction. Generated footage contains no text or statistics; the later narration/caption layer carries those claims.

## Visual grammar

The style master controls every rendered pixel, never period/location. The Hiroshima world sheet controls architecture, atmosphere, domestic setting, skyline, flash, and aftermath content only and must be translated into the style master's illustrated stick language. Character sheets control identity only. The vehicle sheet controls the single B-29 and single bomb only; both are redrawn as outlined stick-world props. The `micro-shots` entries below summarize narrative beat groups; the generator-facing prompt files are authoritative for the expanded frame-accurate seven-to-nine-shot cut timing.

## Reference allocation

| Clips | Ordered references |
| --- | --- |
| 01, 04–06, 16–17 | Picture 1 style; Picture 2 Hiroshima world |
| 02–03, 09, 13–15 | Picture 1 style; Picture 2 world; Picture 3 elderly woman; Picture 4 elderly man |
| 07, 12 | Picture 1 style; Picture 2 world; Picture 3 elderly man; Picture 4 B-29/bomb |
| 08, 10–11 | Picture 1 style; Picture 2 world; Picture 3 B-29/bomb |

The couple is deliberately omitted when identity is not visible. The vehicle sheet is omitted from Clip 15–17 to prevent aircraft or weapon artifacts during the human beat, flash, and aftermath.

## Clip 01 — Sixty seconds before

- editorial range / seed: 00:00–00:05 / `1945080601`
- narration overlap: “60 segundos antes de la bomba atómica, Hiroshima parecía”
- purpose / emotion: immediate hook through serene normality; quiet unease comes only from context
- references: style, Hiroshima world
- micro-shots: leaves in sun 0.00–1.20; hard cut to high city wide 1.20–3.60; slow push and settle 3.60–5.00
- framing / camera: extreme detail to high wide; one restrained forward move
- action / environment / light: breeze in leaves over intact city; clear blue summer morning, warm dimensional sunlight
- SFX: leaves, birds, faint city ambience
- clean ending: stable complete peaceful city wide
- forbidden failures: aircraft, smoke, damage, countdown graphics, collage borders, ominous storm lighting
- files: `prompts/clip-01-sixty-seconds-before.md`; `automation/jobs/clip-01-sixty-seconds-before.json`; `clip-01-sixty-seconds-before-r002.mp4`

## Clip 02 — Breakfast

- editorial range / seed: 00:05–00:10 / `1945080602`
- narration overlap: “parecía una mañana normal. Una pareja anciana terminaba de desayunar. La”
- purpose / emotion: establish the recurring couple and warm domestic routine
- references: style, world, elderly woman, elderly man
- micro-shots: breakfast insert 0.00–1.30; medium two-shot clearing table 1.30–3.80; bowl placed and movement settles 3.80–5.00
- framing / camera: close insert to locked medium; no camera move after cut
- action / environment / light: she gathers a bowl, he folds a newspaper; tatami/shoji interior in warm sun
- SFX: ceramic clink, paper fold, cloth, birds outside
- clean ending: both at rest beside orderly table
- forbidden failures: duplicate characters, modern breakfast objects, animated conversation, panic, unreadable hands
- files: `prompts/clip-02-breakfast.md`; `automation/jobs/clip-02-breakfast.json`; `clip-02-breakfast-r002.mp4`

## Clip 03 — Alarm silenced

- editorial range / seed: 00:10–00:15 / `1945080603`
- narration overlap: “La alarma había sonado antes, pero ya se había”
- purpose / emotion: show that an earlier alert has passed; safety feels plausible
- references: style, world, elderly woman, elderly man
- micro-shots: silent period speaker detail 0.00–1.60; couple notices silence then relaxes 1.60–3.60; focus shifts to calm open window 3.60–5.00
- framing / camera: object close-up, medium couple, rack focus
- action / environment / light: minimal domestic clearing; still laundry and blue sky in soft morning light
- SFX: room tone, ceramic touch, breeze, distant birds; absolutely no siren
- clean ending: bright silent window in focus
- forbidden failures: active alarm, flashing indicator, visible text, panic, aircraft, identity drift
- files: `prompts/clip-03-alarm-silenced.md`; `automation/jobs/clip-03-alarm-silenced.json`; `clip-03-alarm-silenced-r002.mp4`

## Clip 04 — Forty seconds

- editorial range / seed: 00:15–00:20 / `1945080604`
- narration overlap: “había callado. 40 segundos. Afuera,”
- purpose / emotion: exterior reset; countdown tension against visible calm
- references: style, Hiroshima world
- micro-shots: curtain/leaves detail 0.00–1.20; centered normal street 1.20–3.80; short forward drift settles 3.80–5.00
- framing / camera: low detail to symmetrical wide; one restrained push
- action / environment / light: distant pedestrians only; intact wooden street under bright sun
- SFX: steps, bicycle chain far away, cicadas, birds; no alarm
- clean ending: centered quiet street
- forbidden failures: clock or digits, aircraft, panic, red lighting, modern street furniture, readable shop text
- files: `prompts/clip-04-forty-seconds.md`; `automation/jobs/clip-04-forty-seconds.json`; `clip-04-forty-seconds-r002.mp4`

## Clip 05 — Normal street

- editorial range / seed: 00:20–00:25 / `1945080605`
- narration overlap: “Afuera, niños pasan. Una bicicleta cruza. El sol”
- purpose / emotion: ordinary civilian life; make later loss personal without melodrama
- references: style, Hiroshima world
- micro-shots: children cross 0.00–1.60; bicycle crosses after hard cut 1.60–3.80; emptying street settles 3.80–5.00
- framing / camera: two medium-wide side views, locked camera
- action / environment / light: safe walking and cycling through intact residential street; clean morning shadows
- SFX: tires, chain, light footsteps, cicadas, birds
- clean ending: bicycle exits into an ordinary stable street
- forbidden failures: collision, frantic running, vocal children, modern bicycle/vehicles, aircraft, generated signage
- files: `prompts/clip-05-normal-street.md`; `automation/jobs/clip-05-normal-street.json`; `clip-05-normal-street-r002.mp4`

## Clip 06 — Thirty seconds

- editorial range / seed: 00:25–00:30 / `1945080606`
- narration overlap: “sol cae limpio sobre la calle. Treinta segundos. Un”
- purpose / emotion: peak visual serenity and contrast
- references: style, Hiroshima world
- micro-shots: sunlight/leaf detail 0.00–1.40; low wide sunlit street 1.40–3.70; slow tilt to empty sky 3.70–5.00
- framing / camera: macro to low wide; one upward tilt
- action / environment / light: one distant pedestrian; brilliant clean sun, blue sky, summer greenery
- SFX: cicadas, breeze, a few footsteps, neighborhood bed
- clean ending: empty blue sky before aircraft appears
- forbidden failures: early plane, time graphics, excessive flare, ominous clouds, damage, dreamy fantasy effects
- files: `prompts/clip-06-thirty-seconds.md`; `automation/jobs/clip-06-thirty-seconds.json`; `clip-06-thirty-seconds-r002.mp4`

## Clip 07 — Distant hum

- editorial range / seed: 00:30–00:35 / `1945080607`
- narration overlap: “Un zumbido rompe la mañana. El anciano levanta la vista. Un”
- purpose / emotion: first audible intrusion and human recognition
- references: style, world, elderly man, B-29/bomb sheet
- micro-shots: man pauses at window 0.00–1.60; lifts eyes as camera pushes 1.60–3.40; over-shoulder tiny plane 3.40–5.00
- framing / camera: medium profile to over-shoulder; one slow push
- action / environment / light: single restrained look upward; intact home and distant blue sky
- SFX: distant four-engine hum rising slightly, breeze, birds
- clean ending: man edge and tiny aircraft both readable
- forbidden failures: fear performance, close aircraft, bomb release, dialogue, duplicate man, malformed window geometry
- files: `prompts/clip-07-distant-hum.md`; `automation/jobs/clip-07-distant-hum.json`; `clip-07-distant-hum-r002.mp4`

## Clip 08 — B-29 crosses

- editorial range / seed: 00:35–00:40 / `1945080608`
- narration overlap: “Un B-29 atraviesa el cielo. Veinte segundos.”
- purpose / emotion: unambiguous aircraft reveal; scale becomes threatening
- references: style, Hiroshima world, B-29/bomb sheet
- micro-shots: roof-framed empty sky 0.00–1.00; one B-29 crosses 1.00–4.20; aircraft exits and camera settles 4.20–5.00
- framing / camera: medium-wide underside silhouette; one smooth pan
- action / environment / light: level flight over clear sky and dark roof edges
- SFX: steady distant four-engine drone, wind, birds fading
- clean ending: empty sky after exit
- forbidden failures: extra aircraft, bomb, contrail, dogfight, banking, modern jet geometry, copied sheet layout
- files: `prompts/clip-08-b29-crosses.md`; `automation/jobs/clip-08-b29-crosses.json`; `clip-08-b29-crosses-r002.mp4`

## Clip 09 — Silent alarm

- editorial range / seed: 00:40–00:45 / `1945080609`
- narration overlap: “—Si fuera peligro real, sonaría la alarma —dice su esposa.”
- purpose / emotion: communicate calm reassurance nonverbally while doubt remains
- references: style, world, elderly woman, elderly man
- micro-shots: couple by window 0.00–1.50; her small open-palm reassurance 1.50–3.60; his unresolved close reaction 3.60–5.00
- framing / camera: medium two-shot to close reaction; locked frames
- action / environment / light: gesture only, no mouth motion; quiet bright room
- SFX: distant aircraft hum, window breeze, cloth; siren silent
- clean ending: man still looking up
- forbidden failures: lip sync, speech, alarm tone, comic gesturing, panic, extra people, identity swap
- files: `prompts/clip-09-silent-alarm.md`; `automation/jobs/clip-09-silent-alarm.json`; `clip-09-silent-alarm-r002.mp4`

## Clip 10 — Object drops

- editorial range / seed: 00:45–00:50 / `1945080610`
- narration overlap: “Entonces, algo cae del avión. Pequeño.”
- purpose / emotion: make separation physically readable without weapon glamour
- references: style, Hiroshima world, B-29/bomb sheet
- micro-shots: track one aircraft 0.00–1.80; single bomb separates 1.80–3.20; gap increases in wide 3.20–5.00
- framing / camera: medium-long underside to wider hold; one tracking move that settles
- action / environment / light: one object drops against bright sky
- SFX: engine drone, wind, subtle release clunk
- clean ending: aircraft and object distinctly separated
- forbidden failures: multiple bombs/planes, detonation, dramatic spin, close weapon glamour, labels, contrails
- files: `prompts/clip-10-object-drops.md`; `automation/jobs/clip-10-object-drops.json`; `clip-10-object-drops-r002.mp4`

## Clip 11 — Small, dark, strange

- editorial range / seed: 00:50–00:55 / `1945080611`
- narration overlap: “Pequeño. Oscuro. Extraño. Diez”
- purpose / emotion: isolate the threat and compress attention
- references: style, Hiroshima world, B-29/bomb sheet
- micro-shots: tiny object in very wide 0.00–1.30; longer-lens cloud-edge descent 1.30–3.40; locked clear-sky hold 3.40–5.00
- framing / camera: extreme wide to telephoto medium-long; static after cut
- action / environment / light: single silhouette grows only slightly in clean blue sky
- SFX: high wind, distant fading engine; no exaggerated whistle
- clean ending: isolated object centered in stable sky
- forbidden failures: aircraft, duplication, explosion, spin, city destruction, countdown text, sheet border
- files: `prompts/clip-11-small-dark-strange.md`; `automation/jobs/clip-11-small-dark-strange.json`; `clip-11-small-dark-strange-r002.mp4`

## Clip 12 — Ten seconds

- editorial range / seed: 00:55–01:00 / `1945080612`
- narration overlap: “Diez segundos. El hombre entrecierra los ojos. Ahora cae”
- purpose / emotion: uncertainty becomes recognition
- references: style, world, elderly man, B-29/bomb sheet
- micro-shots: man's narrowed eyes 0.00–1.70; POV object crossing wire 1.70–3.70; recognition reaction 3.70–5.00
- framing / camera: tight face, telephoto POV, medium close profile; locked shots
- action / environment / light: one squint and subtle shoulder tension; bright home and sky
- SFX: fading engine, breeze, cloth, quiet room
- clean ending: man still, concern readable
- forbidden failures: spoken line, running, early flash, duplicate bomb/man, grotesque face or eyes, countdown graphic
- files: `prompts/clip-12-ten-seconds.md`; `automation/jobs/clip-12-ten-seconds.json`; `clip-12-ten-seconds-r002.mp4`

## Clip 13 — Five seconds

- editorial range / seed: 01:00–01:05 / `1945080613`
- narration overlap: “cae más rápido. Cinco segundos. Vámonos.”
- purpose / emotion: sudden controlled urgency
- references: style, world, elderly woman, elderly man
- micro-shots: man turns to wife 0.00–1.50; rises and guides 1.50–3.60; first shared step 3.60–5.00
- framing / camera: medium close to wider two-shot; one short lateral move
- action / environment / light: coordinated standing and departure; hard bright exterior light enters warm room
- SFX: cloth, table creak, two footsteps, low distant hum
- clean ending: both moving together but visually resolved
- forbidden failures: mouth movement, sprinting, falling, chaotic limbs, explosion, flash, duplicate couple
- files: `prompts/clip-13-five-seconds.md`; `automation/jobs/clip-13-five-seconds.json`; `clip-13-five-seconds-r002.mp4`

## Clip 14 — Two seconds, hands

- editorial range / seed: 01:05–01:10 / `1945080614`
- narration overlap: “Vámonos. Ahora. Dos segundos. Él busca su mano.”
- purpose / emotion: intimate human connection under pressure
- references: style, world, elderly woman, elderly man
- micro-shots: waist-level momentary separation 0.00–1.40; his hand reaches and hers turns 1.40–3.50; grip closes and holds 3.50–5.00
- framing / camera: medium detail to close hands; one gentle push
- action / environment / light: single reach and mutual clasp; warm interior with intense window edge light
- SFX: cloth, foot shift, quiet room, distant hum
- clean ending: joined hands centered and still
- forbidden failures: extra fingers/limbs, detached hands, wrong sleeves, speech, melodrama, flash, injury
- files: `prompts/clip-14-two-seconds-hands.md`; `automation/jobs/clip-14-two-seconds-hands.json`; `clip-14-two-seconds-hands-r002.mp4`

## Clip 15 — One second, flash begins

- editorial range / seed: 01:10–01:15 / `1945080615`
- narration overlap: “mano. Un segundo. A las ocho y quince. Un destello blanco”
- purpose / emotion: final human beat, then overwhelming light
- references: style, world, elderly woman, elderly man
- micro-shots: clasped hands 0.00–1.80; still couple notices brightness 1.80–3.60; white enters 3.60–4.60; almost-white hold 4.60–5.00
- framing / camera: close hands to medium two-shot; camera locked during light change
- action / environment / light: eyes turn without full body motion; warm color drains into white
- SFX: room hush and subtle pressure onset; no impact in this clip
- clean ending: stable near-white field with faint silhouette edge
- forbidden failures: fireball, visible injuries, screaming, explosive camera shake, captions/time display, duplicated couple
- files: `prompts/clip-15-one-second-flash.md`; `automation/jobs/clip-15-one-second-flash.json`; `clip-15-one-second-flash-r002.mp4`

## Clip 16 — White flash

- editorial range / seed: 01:15–01:20 / `1945080616`
- narration overlap: “blanco borra Hiroshima. Para finales de 1945,”
- purpose / emotion: visual erasure transitions directly into respectful consequence
- references: style, Hiroshima world
- micro-shots: warm white field 0.00–1.40; pale gray reveals distant damaged skyline 1.40–3.30; slow pullback and settle 3.30–5.00
- framing / camera: abstract full field to extreme wide; one slow pullback
- action / environment / light: smoke/dust resolves over ruined roofline; subdued desaturated daylight
- SFX: low rumble fading, settling debris, wind; never screams
- clean ending: stable non-graphic ruined-city wide
- forbidden failures: people/bodies, gore, fireball, glamorous mushroom cloud, orange spectacle, aircraft, victory imagery
- files: `prompts/clip-16-white-flash.md`; `automation/jobs/clip-16-white-flash.json`; `clip-16-white-flash-r002.mp4`

## Clip 17 — Aftermath

- editorial range / seed: 01:20–01:25 / `1945080617`
- narration overlap: “1945, unas 140.000 personas habrían muerto.” Narration ends at local 4.520; final 0.480 is visual hold.
- purpose / emotion: sober scale, remembrance, and closure
- references: style, Hiroshima world
- micro-shots: elevated aftermath wide 0.00–1.20; imperceptible push through smoke layers 1.20–3.80; settle with one ash/paper drift 3.80–4.52; complete hold 4.52–5.00
- framing / camera: wide elevated city view; one minimal push ending early
- action / environment / light: only haze and a small drifting fragment; subdued gray-brown daylight
- SFX: wind, distant settling debris, low rumble fading to near-silence
- clean ending: fully stable empty wide for at least 0.48 seconds
- forbidden failures: visible victims, injuries, screams, near flames, aircraft, flags, spectacle, mushroom cloud, casualty text
- files: `prompts/clip-17-aftermath.md`; `automation/jobs/clip-17-aftermath.json`; `clip-17-aftermath-r002.mp4`

## Final preflight and review

- narration coverage spans all 122 tokens and preserves boundary overlaps rather than duplicating words in the final voice track
- every clip is independent and ends cleanly
- every prompt defines every supplied reference exactly once by ordered Picture number
- all jobs request native audio and exact 5.000-second editorial normalization while retaining raw H3 output
- no concat, upscale, final assembly, or publication occurs before human clip review
