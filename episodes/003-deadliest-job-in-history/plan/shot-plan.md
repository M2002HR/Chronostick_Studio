# Episode 003 — The Deadliest Job in History? — Rapid-cut shot plan

## Production metadata

- status: `approved`
- profile: `h3-short-5s-16step-rapid-cut`
- timeline: 00:00.000–00:45.000 generated picture
- narration: approved Spanish delivery, 00:00.320–00:45.640
- finishing: freeze Clip 09's resolved final frame for 0.640 seconds after concat and before upscale
- format: 9 independent vertical 480×864 clips, 5.000-second editorial slots, 24 fps
- H3 raw: 124 frames, approximately 5.167 seconds; preserve raw and normalize an editorial copy to exactly 5.000 seconds
- sampling: 16 steps, `res_multistep`, `beta`, Lightning off, fixed per-clip seeds
- edit density: exactly 8 hard-cut shots per clip; 72 shots in 45 generated seconds; average shot length 0.625 seconds
- motion budget: one primary action, at most one simple camera move, and at most two low-amplitude secondary motions per shot
- audio: natural diegetic SFX only; external narration is added later; no generated speech, voices, or music

This episode deliberately exceeds the ordinary H3 micro-beat density. The speed comes from short, clean, precomposed hard cuts—not whip pans, morphs, unstable camera motion, or simultaneous choreography.

## Narrative guardrails

- The narration's “deadliest job” superlative is a rhetorical hook, not a proven occupational ranking.
- The four people shown are specifically the four assassinated U.S. presidents, not all presidents who died in office.
- Keep every attack non-graphic: one restrained flash or offscreen report, recoil or disappearance behind foreground geometry, no wound, blood, body, or suffering close-up.
- Lincoln's sequence may use a crumpled Confederate ribbon and theater symbolism to summarize Booth's motive, but must not invent dialogue or readable political copy.
- Garfield's attacker may be shown subdued and isolated; do not use monstrous features, manic animation, or a stigmatizing visual equation between mental illness and evil.
- McKinley's attacker is identified by period clothes and the concealed hand, not by ethnic caricature.
- Kennedy's shooter remains offscreen. The shot is conveyed with an offscreen report, startled birds, and a windshield reflection.
- No generated names, dates, numbers, subtitles, plaques, labels, newspaper text, title cards, CTA text, or other readable words.
- The four presidents remain stylized ChronoStick figures, never photorealistic portraits or exaggerated caricatures.

## Identity separation

| Identity | Locked silhouette and clothing cues |
| --- | --- |
| Abraham Lincoln | tallest and narrowest; black stovepipe hat; chin beard without mustache; black frock coat; black bow tie |
| James A. Garfield | broader; brushed-back side-parted dark hair; full brown-black beard and mustache; dark 1881 frock coat |
| William McKinley | compact and upright; clean-shaven; receding side-parted hair; black frock coat; high collar; one scarlet lapel carnation |
| John F. Kennedy | youngest; clean-shaven squared jaw; thick swept side-parted dark hair; navy early-1960s suit; slim blue tie |

These differences must read at thumbnail scale without text. The exact design authority is `source/visual-research-notes.md` and the four planned single-person identity anchors in `plan/reference-manifest.json`.

## Reference strategy

Only the approved master style already exists. Create four reusable single-person identity anchors, then use them to create six full-frame episode scene anchors. Identity anchors are design sources and normally stay out of H3; H3 receives one or two single-scene anchors only.

| Clip | Ordered H3 references |
| --- | --- |
| 01 | Picture 1 — presidential-danger office |
| 02 | Picture 1 — four-presidents memorial |
| 03 | Picture 1 — four-presidents memorial; Picture 2 — Lincoln theater |
| 04 | Picture 1 — Lincoln theater |
| 05 | Picture 1 — Garfield station |
| 06 | Picture 1 — Garfield station; Picture 2 — McKinley exposition |
| 07 | Picture 1 — McKinley exposition |
| 08 | Picture 1 — McKinley exposition; Picture 2 — JFK motorcade |
| 09 | Picture 1 — JFK motorcade; Picture 2 — four-presidents memorial |

No contact sheet, multi-panel board, alternate pose collection, or repeated identity is passed to H3.

## Camera and edit grammar

- Every listed boundary is a true hard cut; no dissolves and no cross-shot morphing.
- Alternate wide, medium, close, extreme close, and silhouette framings so the eye receives a new shape at nearly every cut.
- Push-ins last for only one listed shot and stop before that shot's cut.
- Background crowds are simplified silhouettes with low motion. The four presidents always remain the visual priority.
- Use graphic match cuts only across completed shots: chair circle to clock, station bars to exposition columns, exposition wheel to limousine wheel.
- Each clip finishes its own action and reaches a stable composition before 5.000 seconds.
- Clip 09 reaches its final locked memorial frame at local 4.200 and remains unchanged through local 5.000 and the external 0.640-second freeze.

## Narration timing master

| Global time | Narration event |
| --- | --- |
| 00.320–05.040 | dangerous-job hook and 8.9% |
| 05.040–08.500 | U.S. president |
| 08.500–12.400 | four of 45 did not survive the presidency |
| 12.400–18.960 | Lincoln, actor, Civil War outcome |
| 19.740–27.600 | Garfield, two shots, attacker with mental illness |
| 27.600–37.540 | McKinley, anarchist, revolver under handkerchief, public exposition |
| 37.540–43.200 | last president, Kennedy, shot |
| 43.200–45.640 | surprise question and subscription CTA |

## Clip 01 — The office nobody calls dangerous

- global time: 00:00.000–00:05.000
- narrative purpose: convert an ordinary “job” into a lethal-risk hook before explaining the office
- references: `<Picture 1>` presidential-danger office
- palette: midnight navy, parchment cream, muted brass, restrained crimson
- end state: empty chair centered beneath four still shadows

| Local time | Narration alignment | Framing and visible content | Primary action / camera / SFX / cut |
| --- | --- | --- | --- |
| 0.00–0.52 | pre-roll into “Uno” | Extreme low close-up of a closed formal office door; bright cream light leaks below it. | Door opens once toward camera; locked low camera; one hinge creak; hard cut. |
| 0.52–1.10 | “de los trabajos” | Low close-up of one polished black shoe and dark trouser entering the light. | One deliberate step lands; no camera move; heel click; hard cut on contact. |
| 1.10–1.68 | “más” | Tight frontal view of the empty presidential chair. | Very short straight push-in, stopping by 1.58; leather creak; hard cut. |
| 1.68–2.25 | “mortales” | One anonymous presidential stick silhouette stands behind the chair, face outside the crop. | Four long shadows slide into the wall behind the single figure; locked camera; low room tone; hard cut. |
| 2.25–2.85 | “con una” | Extreme insert of a brass desk clock with no readable numerals. | Second hand snaps one increment; static camera; sharp tick; hard cut. |
| 2.85–3.48 | “tasa de” | Overhead insert of one white-gloved oath hand above a closed blank book. | Hand lowers onto the blank cover; static camera; cloth tap; hard cut. |
| 3.48–4.20 | “mortalidad del” | Circular pool of red light closes around the empty chair, visually echoing a target without a crosshair. | Light aperture contracts once; locked camera; electrical click; hard cut. |
| 4.20–5.00 | “8,9%” | Wide symmetrical office: empty chair centered, four long distinct shadows behind it, no people or text. | Shadows stop by 4.72 and the frame settles; no camera movement; low clock tick; hard boundary at 5.00. |

Failure risks: generated seals or text, literal crosshair, visible weapon, more than four dominant shadows, moving final frame. Reject all of them.

## Clip 02 — Presidency, then four faces

- global time: 00:05.000–00:10.000
- narrative purpose: identify the U.S. presidency, then reveal the four symbolic identities exactly after “Cuatro”
- references: `<Picture 1>` four-presidents memorial
- palette: White House cream, navy, dark wood, controlled gold spotlights
- end state: Kennedy's clean portrait flash completes the four-person set

| Local time | Narration alignment | Framing and visible content | Primary action / camera / SFX / cut |
| --- | --- | --- | --- |
| 0.00–0.65 | tail of “8,9%” | Vertical exterior silhouette of the White House-inspired facade; no readable signage. | Flags lift once in a light gust; locked low camera; cloth flap; hard cut. |
| 0.65–1.35 | “es ser” | Medium symmetrical office desk and empty chair, one U.S.-color flag edge visible without a seal. | Chair turns a quarter turn and stops; static camera; wood swivel; hard cut. |
| 1.35–2.15 | “presidente de” | One anonymous president silhouette at a podium, framed from below; podium blank. | Figure places both hands on podium; tiny push-in stops before cut; room murmur; hard cut. |
| 2.15–3.50 | “Estados Unidos” into pre-“Cuatro” | Long corridor of unlettered oval portrait frames; four frames at the end remain dark. | Fast straight dolly ends at the four dark frames by 3.40; footsteps/whoosh; hard cut. |
| 3.50–3.88 | “Cuatro” | Lincoln identity close-up: tall hat brim, long face, chin beard without mustache. | Lincoln raises eyes to camera; locked camera; single spotlight click; hard cut. |
| 3.88–4.25 | “de los” | Garfield identity close-up: full beard and mustache, brushed-back hair, broader shoulders. | Garfield turns his head a few degrees; locked camera; spotlight click; hard cut. |
| 4.25–4.62 | “45” | McKinley identity close-up: clean-shaven receding hair and scarlet lapel carnation. | Carnation catches a restrained red glint; locked camera; spotlight click; hard cut. |
| 4.62–5.00 | start of “presidentes” | Kennedy identity close-up: swept dark hair, clean-shaven jaw, navy suit and slim tie. | Kennedy shifts gaze forward; locked camera; spotlight click; hard boundary at 5.00. |

Failure risks: trying to display 45 readable portraits, identity swaps, repeated faces, name captions, realistic portrait rendering. The number is carried by narration, not generated typography.

## Clip 03 — Four disappear; Lincoln steps out

- global time: 00:10.000–00:15.000
- narrative purpose: symbolize the mortality claim, then isolate the first named president
- references: `<Picture 1>` four-presidents memorial; `<Picture 2>` Lincoln theater
- palette: navy memorial darkness into gaslit theater red and gold
- end state: Lincoln alive and fully recognizable at the theater-box threshold; attack not begun

| Local time | Narration alignment | Framing and visible content | Primary action / camera / SFX / cut |
| --- | --- | --- | --- |
| 0.00–0.60 | “presidentes no” | Full memorial composition with exactly four presidents around the empty chair. | All four turn their eyes toward the empty chair; locked camera; low room tone; hard cut. |
| 0.60–1.20 | “sobrevivieron” | Same four silhouettes from behind, each with a separate overhead light. | The four lights extinguish together; no camera move; four tight electrical clicks; hard cut. |
| 1.20–1.80 | “a su” | Close on the now-empty chair with four distinct hat/hair shadows across it. | Shadows lengthen downward once; static camera; clock tick; hard cut. |
| 1.80–2.40 | “presidencia” | Four empty formal chairs in one receding diagonal, no plaques or people. | A narrow spotlight lands on the first chair only; locked camera; light click; hard cut. |
| 2.40–2.95 | “El primero” | Extreme close-up of Lincoln's black stovepipe hat against warm theater velvet. | One hand lifts the hat from a hook; static camera; felt brush; hard cut. |
| 2.95–3.60 | “en ser asesinado” | Tight Lincoln profile: elongated face, dark chin beard, no mustache. | Lincoln fastens his black bow tie once; no camera move; cloth rustle; hard cut. |
| 3.60–4.30 | “fue Abraham” | Low full-body view emphasizes Lincoln as the tallest, narrowest figure in black frock coat. | Lincoln takes one long step into gaslight; short upward tilt stops by 4.18; shoe step; hard cut. |
| 4.30–5.00 | “Lincoln” | Medium-wide presidential theater-box threshold; Lincoln enters alive, Booth only a distant dark actor shape in the rear doorway. | Lincoln rests one hand on the box rail and becomes still by 4.82; locked camera; audience murmur; hard boundary. |

Failure risks: attack before narration, multiple Lincolns, mustache, short body proportions, raised weapon, future fallen state, readable theater signage.

## Clip 04 — Actor, flash, curtain

- global time: 00:15.000–00:20.000
- narrative purpose: deliver Lincoln's assassination and Booth's theatrical/Confederate motive with fast non-graphic symbolism
- references: `<Picture 1>` Lincoln theater
- palette: warm gaslight, burgundy velvet, black formalwear, one restrained amber-white flash
- end state: closed still curtain and Lincoln's hat settled on carpet

| Local time | Narration alignment | Framing and visible content | Primary action / camera / SFX / cut |
| --- | --- | --- | --- |
| 0.00–0.55 | tail of “Lincoln” | Side medium shot of Lincoln seated alive in the theater box, stovepipe hat on the rail. | Lincoln leans forward slightly toward the unseen stage; locked camera; distant applause; hard cut. |
| 0.55–1.15 | “a quien disparó” | Tight doorway silhouette of Booth in dark actor's evening clothes, one theatrical makeup cloth in his free hand. | Booth steps through the door once; tiny push-in stops before cut; floor creak; hard cut. |
| 1.15–1.78 | end of “disparó” / “un actor” | Over-shoulder view: exactly Lincoln and Booth; one small period derringer rises behind Lincoln. | One restrained muzzle flash occurs at 1.42; camera locked; one sharp report; immediate hard cut. |
| 1.78–2.42 | “al que no le” | Empty stage wing insert with one plain comedy mask and folded actor's scarf, no readable playbill. | Mask drops once onto the scarf; static camera; hollow clack; hard cut. |
| 2.42–3.08 | “gustó el desenlace” | Close insert of Booth's black shoe beside a crumpled muted-gray Confederate ribbon, no emblem text. | Shoe presses the ribbon once; locked camera; fabric crush; hard cut. |
| 3.08–3.72 | “de la guerra” | Abstract period U.S. map silhouette split by a dark seam, without labels or arrows. | Seam closes into one intact silhouette; static camera; paper fold; hard cut. |
| 3.72–4.42 | “civil” | Lincoln's stovepipe hat falls alone through a dark burgundy frame; no body visible. | Hat completes one fall and lands brim-down; locked camera; soft thud; hard cut. |
| 4.42–5.00 | pause into “El siguiente” | Wide empty burgundy theater curtain with the settled hat at bottom foreground. | Curtain closes once and all motion stops by 4.82; no camera move; curtain sweep then silence; hard boundary. |

Failure risks: graphic wound, falling body, repeated discharge, modern handgun, Booth lip sync, readable flags or maps, moving curtain at boundary.

## Clip 05 — Garfield, twice

- global time: 00:20.000–00:25.000
- narrative purpose: reveal Garfield cleanly and punctuate “dos veces” with exactly two separated flashes
- references: `<Picture 1>` Garfield station
- palette: steam gray, dark walnut, aged brass, muted summer daylight
- end state: Garfield safely hidden by a bench; his hat settled in foreground

| Local time | Narration alignment | Framing and visible content | Primary action / camera / SFX / cut |
| --- | --- | --- | --- |
| 0.00–0.62 | “siguiente fue” | Extreme close-up of an 1881 steam locomotive wheel and station platform edge. | Wheel rolls half a turn and stops; low locked camera; steam hiss/metal clack; hard cut. |
| 0.62–1.25 | “el presidente James” | Station wide: exactly one Garfield foreground figure enters, recognizable full beard and dark frock coat. | Garfield walks one step rightward; short lateral track stops; footstep/steam; hard cut. |
| 1.25–1.90 | “A. Garfield” | Tight three-quarter Garfield portrait: high forehead, brushed-back hair, full beard and mustache. | Garfield adjusts one coat button; static camera; cloth snap; hard cut. |
| 1.90–2.55 | “a quien también” | Medium rear angle: Guiteau follows several steps behind Garfield, one hand inside dark coat. | Guiteau closes the distance by one step; locked camera; isolated shoe click; hard cut. |
| 2.55–3.18 | “dispararon” | Side medium shot with exactly Garfield and Guiteau; period revolver clears the coat. | First restrained flash occurs once at 2.88; static camera; first sharp report; hard cut. |
| 3.18–3.82 | “pero esta” | Tight Garfield reaction, non-graphic, station columns streaked behind by shallow depth. | Garfield turns sharply toward the sound; tiny handheld-free snap pan stops immediately; coat rustle; hard cut. |
| 3.82–4.45 | “vez dos” | Low silhouette view, bench obscuring bodies; Guiteau remains at distance. | Second and final restrained flash occurs at 4.25; locked camera; second sharp report; hard cut. |
| 4.45–5.00 | “veces” | Close foreground of Garfield's dark hat beside the bench; no person or wound visible. | Hat rocks once and settles by 4.82; static camera; felt scrape, steam ambience; hard boundary. |

Failure risks: one or three-plus flashes, modern station, duplicate Garfield, clean-shaven Garfield, blood, visible collapse, moving hat at boundary.

## Clip 06 — Custody bars to electric lights

- global time: 00:25.000–00:30.000
- narrative purpose: handle the mental-illness phrase without sensationalism, then launch McKinley's bright exposition world
- references: `<Picture 1>` Garfield station; `<Picture 2>` McKinley exposition
- palette: station gray to neutral custody gray to electric amber, cream, and burgundy
- end state: McKinley alive and composed at the receiving line, scarlet carnation clearly visible

| Local time | Narration alignment | Framing and visible content | Primary action / camera / SFX / cut |
| --- | --- | --- | --- |
| 0.00–0.55 | narration gap | Same still Garfield hat near station bench, preserving the prior resolved state. | One curl of steam crosses and clears; locked camera; soft steam hiss; hard cut. |
| 0.55–1.15 | “por un atacante” | Medium silhouette of Guiteau between two neutral officer silhouettes; no weapon visible. | Officers guide him one step forward; static camera; three footsteps; hard cut. |
| 1.15–1.78 | “con una enfermedad” | Sparse custody room; Guiteau sits alone, shoulders folded inward, face understated. | He lowers his gaze once; no camera move; room tone; hard cut. |
| 1.78–2.40 | “mental” | Close-up of Guiteau's relaxed empty hands clasped between his knees; no distorted anatomy. | Fingers tighten subtly once; locked camera; cloth rustle; hard cut. |
| 2.40–2.90 | pause into “El” | Vertical iron bars fill frame with neutral gray light behind. | One barred door closes; static camera; metal latch; hard cut on latch. |
| 2.90–3.50 | “tercer presidente” | Match-cut vertical columns of the 1901 exposition; electric bulbs ignite in sequence. | One row of bulbs turns on from bottom to top; short upward tilt stops; electrical buzz; hard cut. |
| 3.50–4.15 | continuation | Extreme lapel insert: black frock coat, high collar edge, one scarlet carnation. | McKinley's hand straightens the carnation once; static camera; cloth brush; hard cut. |
| 4.15–5.00 | “William McKinley” | Full McKinley identity in the public receiving line, clean-shaven, receding hair, upright posture; attacker not foregrounded. | McKinley extends one open greeting hand and holds still by 4.80; locked camera; polite crowd murmur; hard boundary. |

Failure risks: grotesque “madness” imagery, weapon retained in custody, McKinley with beard, missing carnation, attacker moving early into attack state, unreadable crowded staging.

## Clip 07 — Surprise, covered hand, flash

- global time: 00:30.000–00:35.000
- narrative purpose: accelerate through “sorpresa sorpresa,” depict the attack once, and end on the concealed-revolver idea
- references: `<Picture 1>` McKinley exposition
- palette: electric gold, cream stone, burgundy drapery, pale handkerchief, scarlet carnation
- end state: one revolver remains visibly shaped but fully covered beneath the pale cloth

| Local time | Narration alignment | Framing and visible content | Primary action / camera / SFX / cut |
| --- | --- | --- | --- |
| 0.00–0.60 | tail of “McKinley, fue” | Tight frontal McKinley portrait, clean-shaven face and scarlet carnation centered. | McKinley looks from left to right once; locked camera; crowd murmur; hard cut. |
| 0.60–1.25 | first “sorpresa” | Symmetrical wide of the bright public receiving line with McKinley centered. | One guest exits frame after greeting; static camera; shoes and room echo; hard cut. |
| 1.25–1.90 | second “sorpresa” | Reverse medium angle from behind McKinley; Czolgosz advances with one cloth-covered hand. | Czolgosz takes one measured step; no camera move; single shoe click; hard cut. |
| 1.90–2.55 | “también tiroteado” | Tight two-hand greeting composition: McKinley's bare hand approaches the pale covered hand. | One restrained flash blooms from beneath the cloth at 2.36; camera locked; one sharp report; hard cut. |
| 2.55–3.20 | end of “tiroteado” | McKinley medium close-up, no wound; carnation still fixed. | McKinley recoils one half-step behind a foreground shoulder; static camera; crowd gasp only; hard cut. |
| 3.20–3.85 | “esta vez por un” | Czolgosz in dark period coat and cap, seen as a controlled side silhouette, mouth closed. | He draws the covered hand back toward his torso; no camera move; cloth rustle; hard cut. |
| 3.85–4.45 | “anarquista que ocultó” | Close-up of the pale handkerchief tightly wrapped around the right hand. | Cloth edge lifts a few millimeters, revealing only a hard object outline; tiny push-in stops; cloth scrape; hard cut. |
| 4.45–5.00 | “el revólver” | Extreme insert of the single revolver silhouette completely under the handkerchief; no fingers duplicated. | Covered shape becomes still by 4.78; locked camera; faint metal click; hard boundary. |

Failure risks: exposed weapon before the final insert, multiple shots, carnation disappearance, graphic injury, anarchist symbols or readable slogans, attacker caricature, extra hands.

## Clip 08 — Handkerchief to motorcade

- global time: 00:35.000–00:40.000
- narrative purpose: complete the concealed-weapon and exposition context, then introduce the final president without beginning his attack
- references: `<Picture 1>` McKinley exposition; `<Picture 2>` JFK motorcade
- palette: exposition amber/gold transitioning sharply to clear Dallas blue, concrete gray, and Kennedy navy
- end state: Kennedy alive in the moving open limousine, identifiable from behind; no weapon or attack visible

| Local time | Narration alignment | Framing and visible content | Primary action / camera / SFX / cut |
| --- | --- | --- | --- |
| 0.00–0.62 | “revólver bajo” | Extreme insert continues the covered revolver shape from Clip 07. | Cloth peels back once enough to reveal the period revolver; static camera; cloth pull/metal click; hard cut. |
| 0.62–1.25 | “un pañuelo” | Low close-up of the pale handkerchief above ornate tile. | Handkerchief falls once and lands flat; locked camera; soft fabric slap; hard cut. |
| 1.25–1.90 | “durante una exposición” | Wide public receiving hall with exactly three dominant foreground silhouettes and an abstract background crowd. | The three silhouettes step backward together from the center; no camera move; crowd gasp/foot shuffle; hard cut. |
| 1.90–2.55 | “pública” | Vertical exterior of the exposition's Temple of Music-inspired facade, electric bulbs glowing; no signage. | Bulbs ripple off once from top to bottom; short tilt down stops; electrical buzz; hard cut. |
| 2.55–3.15 | “El último presidente” | Dark presidential portrait corridor; one final unlit oval frame at the end. | Final frame light clicks on but remains a silhouette; straight push stops; light click; hard cut. |
| 3.15–3.75 | “asesinado” | Graphic match: exposition wheel becomes a 1963 limousine wheel on sunlit Dallas pavement. | Limousine wheel completes one clean rotation; low lateral track; tire/road sound; hard cut. |
| 3.75–4.40 | “durante” | Wide open motorcade traveling left-to-right; exactly four simplified occupants, Kennedy rear-right; crowd remains background shapes. | Car advances steadily through frame; locked curb-height camera; engine/crowd ambience; hard cut. |
| 4.40–5.00 | end of “durante” | Medium rear three-quarter Kennedy: swept dark hair, navy shoulder, slim blue tie edge; fully alive. | Kennedy turns his head slightly toward the crowd and settles by 4.82; no camera move; crowd cheer; hard boundary. |

Failure risks: attack occurring early, visible rifle or shooter, modern vehicle, duplicated occupants, JFK hairstyle drift, readable signs, exposition and Dallas blended into one location.

## Clip 09 — Kennedy, then the four-person lockup

- global time: 00:40.000–00:45.000
- narration continues through 00:45.640 over the frozen final frame
- narrative purpose: identify Kennedy, show the final attack non-graphically, and land on a memorable four-person symbolic payoff for the CTA
- references: `<Picture 1>` JFK motorcade; `<Picture 2>` four-presidents memorial
- palette: clear Dallas daylight, then solemn navy, muted gold, cream, four restrained identity accents
- end state: exact freeze-safe memorial portrait locked from 4.20 through 5.00 and externally extended 0.64 seconds

| Local time | Narration alignment | Framing and visible content | Primary action / camera / SFX / cut |
| --- | --- | --- | --- |
| 0.00–0.55 | “durante su mandato” | Wide motorcade continues left-to-right from a new clean angle; exactly four occupants. | Limousine crosses one lane marker; locked camera; engine/road ambience; hard cut. |
| 0.55–1.15 | “John” | Rear close-up of Kennedy's distinctive swept hair and navy collar, crowd bokeh behind. | Kennedy begins one head turn toward camera side; no camera move; crowd murmur; hard cut. |
| 1.15–1.75 | “F. Kennedy” | Tight three-quarter Kennedy portrait: clean-shaven squared jaw, swept hair, white shirt, slim blue tie. | Head turn completes and eyes face the crowd; static camera; light wind; hard cut. |
| 1.75–2.35 | “también” | Kennedy's calm point of view toward waving abstract crowd and upper building windows; no shooter. | One small flag edge waves; very short push toward the windows stops; crowd cheer; hard cut. |
| 2.35–2.95 | “fue tiroteado” | Empty sky/building reflection above the limousine; one flock of birds at rest. | One offscreen report at 2.70 startles the birds upward; locked camera; single report/wing burst; hard cut. |
| 2.95–3.45 | end of “tiroteado” / start CTA | Side medium, windshield and seat obscure bodies; no wound or impact shown. | Kennedy lowers below the windshield as the limousine accelerates once; camera remains locked; engine surge; hard cut. |
| 3.45–4.20 | “¿Te sorprendió?” | Hard cut to exactly four presidents in the memorial composition around one empty chair, each identity immediately distinct. | Four overhead spotlights switch on together; camera locked; four light clicks; hard cut at 4.20. |
| 4.20–5.00 | lead-in to “¡Suscríbete!” | Final balanced frontal portrait: Lincoln tallest with hat and chin beard; Garfield full-bearded; McKinley clean-shaven with red carnation; Kennedy youthful with swept hair and navy suit; empty chair centered below them; no text. | Absolutely no character, camera, light, cloth, or background movement. Hold unchanged through 5.00; quiet room tone only. This exact frame is frozen externally through 5.64. |

Failure risks: visible shooter, multiple reports, graphic impact, duplicate occupants, smiling or waving memorial figures, text CTA, identity swaps, any motion or lighting change after 4.20.

## Continuity handoff summary

| Boundary | Required story-state handoff |
| --- | --- |
| 01→02 | symbolic danger established; no named person harmed |
| 02→03 | all four identities introduced; mortality statement can now become symbolic |
| 03→04 | Lincoln alive in theater; Booth has not raised weapon |
| 04→05 | Lincoln sequence fully closed; new station world begins with hard cut |
| 05→06 | Garfield attack completed; still hat provides one brief continuity insert; attacker in custody |
| 06→07 | McKinley alive, greeting hand extended; covered hand not yet touching him |
| 07→08 | McKinley attack completed; covered revolver established; public setting still visible |
| 08→09 | Kennedy alive in moving motorcade; no attack has begun |
| 09→tail | all action finished; four-person memorial frame remains unchanged for 0.640 seconds |

## Final pre-reference review gate

- all 119 narration tokens map to their original approved time; no script change
- nine independent 5.000-second clips; 72 hard-cut shots; every local table is contiguous from 0.00 to 5.00
- speed is created by cuts, scale changes, inserts, and angle changes; individual motion remains moderate and controllable
- all four presidents have explicit thumbnail-readable stick-figure identity locks
- exactly 10 missing reference assets: four identity anchors plus six single-scene anchors
- every H3 clip uses one or two ordered scene anchors, never a contact sheet or multi-pose identity sheet
- historical worlds stay separate; no blended eras or regressed event states
- attack count is controlled: Lincoln one flash, Garfield exactly two, McKinley one, Kennedy one offscreen report
- no generated dialogue, narration, lip sync, readable text, graphic injury, or background music
- every clip resolves before its boundary; Clip 09 is fully freeze-safe from local 4.20

The user approved this shot plan and authorized reference generation, prompt authoring, deterministic 16-step jobs, and full batch execution on 2026-09-28.
