---
id: CST-EP001-SHOTPLAN
title: Episode 001 — Potato France — Master Shot Plan
project: ChronoStick Studio
episode: 001
slug: potato-france
type: shot-plan
status: archived-working-plan
version: 0.1.0
created: 2026-09-22
updated: 2026-09-22
language_voice: es
language_production: en
format: youtube-shorts
aspect_ratio: "9:16"
target_duration: "60.00s"
narration_end: "55.98s"
video_engine: Omni
generation_segment_duration: "10.00s"
generation_segment_count: 6
max_reference_images_per_generation: 3
inherits:
  - CST-STYLE-001@1.0.0
  - CST-WORLD-001@1.0.0
  - CST-CHAR-001@1.0.0
  - CST-CHAR-002@1.0.0
  - CST-CHAR-003@1.0.0
  - CST-CHAR-004@1.0.0
approved: false
---

# Purpose

This file is the master visual-production blueprint for Episode 001.

It controls:

- exact visual pacing
- narration alignment
- internal cut rhythm
- character assignment
- environment assignment
- camera framing
- motion intensity
- reference-image allocation
- 10-second generation boundaries
- final-shot resolution
- transition logic
- drift prevention strategy

Individual Omni generation prompts must inherit from this file.

If an individual clip prompt conflicts with this shot plan, this shot plan has priority unless the shot plan itself is versioned and updated.

---

# Episode Concept

A short historical story about French distrust of potatoes and Antoine-Augustin Parmentier's campaign to increase their acceptance.

The visual narrative progresses through:

1. hunger + rejection
2. fear + restriction
3. Parmentier's intervention
4. guarded potato field
5. nighttime theft
6. tasting + acceptance
7. chronological transition to the French Revolution
8. CTA / visual resolution

---

# Narrative Guardrail

The final revolutionary sequence is a chronological transition.

The visuals must NOT imply:

"Potatoes caused the French Revolution."

The visual language must create a CLEAR EDITORIAL SEPARATION between:

- potato acceptance story

and

- later French revolutionary atmosphere

Do not visually connect them through causal arrows, transformation effects, or continuous potato-to-revolution imagery.

---

# Master Narration

Spanish narration:

En el siglo XVIII, muchos franceses preferían pasar hambre antes que comer papas.

Creían que causaban enfermedades, y el Parlamento de París llegó a prohibir su cultivo.

Antoine Parmentier sabía que eran nutritivas, pero muchos las veían como comida para animales.

Entonces plantó papas cerca de París y puso guardias armados.

La gente pensó: si está tan protegido, debe ser valioso.

Según la historia popular, por la noche los guardias se retiraban y la gente empezó a robarlas.

Funcionó.

Las probaron y comenzaron a aceptarlas.

Parmentier convirtió el rechazo en curiosidad usando psicología inversa.

Pocos años después comenzó la Revolución Francesa.

¿Te gustan estas historias? Suscríbete.

---

# Narration Timing Master

Important timing anchors:

| Time | Narration Event |
|---|---|
| 00.28 | Narration begins |
| 00.94–01.58 | "XVIII" |
| 01.58–03.12 | "muchos franceses" |
| 03.12–04.60 | "preferían pasar hambre" |
| 05.52–06.28 | "comer papas" |
| 06.28–09.20 | "Creían que causaban enfermedades" |
| 09.72–13.42 | Parliament / cultivation restriction |
| 13.42–17.00 | Parmentier / nutritional value |
| 17.00–19.90 | potatoes viewed as animal food |
| 19.90–23.64 | planting near Paris |
| 24.10–26.10 | armed guards |
| 26.10–30.48 | perceived value |
| 30.48–31.72 | narration pause |
| 31.72–33.48 | popular-history qualification |
| 33.78–35.42 | night / guards withdraw |
| 36.26–37.58 | people steal potatoes |
| 37.58–38.44 | narration pause |
| 38.44–39.60 | "Funcionó" |
| 39.60–42.34 | tasting / acceptance |
| 42.34–48.48 | Parmentier / rejection to curiosity / reverse psychology |
| 48.48–50.36 | "Pocos años después" |
| 50.36–52.80 | French Revolution |
| 52.80–53.48 | narration pause |
| 53.48–55.98 | CTA |
| 55.98–60.00 | no narration |

---

# Global Production Philosophy

This episode uses:

DETAILED CINEMATIC STICK-FIGURE HISTORICAL ANIMATION.

Visuals should feel:

- strongly art-directed
- historically grounded
- fast enough for Shorts
- readable
- controlled
- cinematic
- consistent

The goal is NOT maximum possible motion.

The goal is:

MAXIMUM VISUAL CONTROL WITH STRONG EDITORIAL RHYTHM.

---

# Motion Philosophy

Individual shots should generally contain:

ONE dominant action.

Optional secondary motion:

0–2 subtle movements.

Examples:

- small head turn
- hand adjustment
- slight cloth movement
- controlled camera push
- small background movement

Avoid simultaneous complex choreography.

---

# Editing Philosophy

IMPORTANT:

Internal cuts happen INSIDE the 10-second Omni generations.

We do NOT reduce each 10-second generation to one static shot.

However:

the number of cuts and motion complexity are controlled separately.

A clip may contain many cuts while each individual shot remains simple.

This is especially important for the opening hook.

---

# Hook Editing Rule

Clip 01 is intentionally faster than the rest.

Target:

6–8 visual beats within 10 seconds.

Typical shot duration:

0.6–1.8 seconds.

Preferred:

- hard cuts
- insert shots
- reaction cuts
- close-ups
- short controlled push-ins

Avoid:

- constant whip pans
- complex morphs
- chaotic camera motion
- multiple characters performing complicated actions simultaneously

The hook gets energy from CUT FREQUENCY, not from unstable animation.

---

# Body Editing Rule

Clips 02–05:

approximately 4–6 visual beats per 10 seconds.

Typical shot length:

1.2–2.8 seconds.

Use:

- clean hard cuts
- controlled camera reframing
- simple character actions
- reaction inserts

---

# Final Clip Editing Rule

Clip 06:

approximately 4–5 visual beats.

Allow slightly longer shots after narration ends.

The final 4 seconds can breathe more.

---

# 10-Second Boundary Rule

PERMANENT RULE:

Every Omni generation must reach a COMPLETE visual conclusion before the 10-second boundary.

At approximately:

09.20–10.00

the final shot must:

- finish its action
- stop any major camera motion
- settle into a readable composition

The next generation begins with a completely new hard-cut scene.

Do NOT attempt cross-generation:

- camera continuation
- matched character motion
- whip-pan continuation
- object movement continuation
- visual morph continuation

The separately recorded Spanish narration and deliberate hard cuts provide continuity.

---

# Reference Allocation Philosophy

Omni supports a maximum of 3 reference images.

Reference priority:

1. recurring character identity
2. second recurring character identity
3. master style or world reference

When three recurring characters are required in one generation:

use all three character references.

In that case:

- Style Bible must be enforced strongly in text
- World Bible must be enforced strongly in text

Do not sacrifice a necessary character reference merely to provide an environment reference.

---

# Reference IDs

## REF-STYLE-001

Approved ChronoStick master visual reference.

Asset:

assets/styles/style-detailed-cinematic-stick-history-r001.png

## REF-WORLD-001

Approved late-18th-century France world reference.

Asset:

assets/worlds/world-france-late-18c-r001.png

## REF-CHAR-001

French Working-Class Male Villager.

## REF-CHAR-002

French Working-Class Female Villager.

## REF-CHAR-003

Antoine-Augustin Parmentier.

## REF-CHAR-004

French Armed Guard.

---

# Clip Reference Map

| Clip | Reference 1 | Reference 2 | Reference 3 |
|---|---|---|---|
| 01 | Male Villager | Female Villager | Master Style |
| 02 | Parmentier | Male Villager | Master Style |
| 03 | Parmentier | Guard | World France |
| 04 | Male Villager | Female Villager | Guard |
| 05 | Male Villager | Female Villager | Parmentier |
| 06 | Parmentier | World France | Master Style |

If a later test shows a different reference combination gives better consistency, update this Shot Plan version before changing individual clip prompts.

---

# Global Camera Grammar

Preferred lenses / framing language:

- extreme close-up for hook inserts
- close-up
- medium close-up
- medium shot
- occasional wide establishing shot

Avoid:

- exaggerated fisheye
- extreme wide-angle facial distortion
- 360-degree orbit
- unstable handheld movement
- excessive crane motion

---

# Global Camera Motion

Allowed:

- subtle push-in
- subtle pull-back
- short lateral pan
- small vertical reveal
- static shot
- gentle rack-like reframing

Hook shots may use:

slightly faster push-in

but not unstable motion.

---

# Global Character Motion

Preferred:

- head turn
- glance
- lean
- reach
- push
- hold
- point
- walk 1–3 steps
- inspect
- taste
- carry
- exchange look

Avoid:

- running unless required
- jumping
- complicated group choreography
- exaggerated cartoon motion

---

# Global Environment Motion

Default:

LOW.

Allowed:

- subtle cloth motion
- light vegetation movement
- slight lantern flicker
- small crowd shift
- minimal paper movement

Do NOT animate entire environments aggressively.

---

# Global Text Rule

No readable generated text.

No subtitles.

No CTA text.

No generated legal sentences.

Text will be added later in Google Vids.

---

# Global Audio Rule

Omni clips:

NO narration.

NO character dialogue.

NO lip-sync speech.

Allowed:

- subtle environmental ambience
- simple Foley
- controlled natural SFX

Main Spanish narration exists separately as one continuous track.

NO BACKGROUND MUSIC at generation or edit time.

Natural diegetic sound effects only.

---

# ==========================================================
# CLIP 01 — HOOK
# ==========================================================

## Clip ID

CST-EP001-CLIP01

## Time

00.00–10.00

## Narrative Purpose

Immediately establish the central contradiction:

HUNGRY PEOPLE REFUSING POTATOES.

The viewer must understand the hook before the first 6–7 seconds are finished.

This is the FASTEST edited clip in the episode.

## Reference Allocation

1. REF-CHAR-001 — Male Villager
2. REF-CHAR-002 — Female Villager
3. REF-STYLE-001 — Master Style

## Primary Environment

Rural working-class interior.

Derived from CST-WORLD-001.

## Motion Level

Characters:

LOW–MEDIUM.

Camera:

MEDIUM.

Edit frequency:

HIGH.

## Target Visual Beat Count

7 beats.

---

## SHOT 01A

Time:

00.00–00.65

Duration:

0.65s

Framing:

EXTREME CLOSE-UP.

Subject:

empty rustic wooden bowl.

Composition:

bowl centered slightly below frame center.

Only a small amount of rough wooden table visible.

Lighting:

cool-neutral early daylight.

Action:

NONE except an extremely subtle camera push.

Motion:

VERY LOW.

Purpose:

instant visual signal of hunger / lack of food.

Cut:

HARD CUT.

---

## SHOT 01B

Time:

00.65–01.65

Duration:

1.00s

Framing:

CLOSE-UP.

Character:

CST-CHAR-001.

Expression:

hungry.

Composition:

male villager's head and upper torso.

Empty bowl blurred or partially visible at bottom edge.

Action:

he looks down toward the empty bowl.

A tiny head movement only.

Camera:

short controlled push-in.

Purpose:

connect hunger to a human character.

Cut:

HARD CUT.

---

## SHOT 01C

Time:

01.65–02.80

Duration:

1.15s

Framing:

MEDIUM SHOT.

Character:

CST-CHAR-001.

Environment:

same rural interior.

Action:

villager sits at the table with the empty bowl.

One hand rests near the bowl.

He appears tired but not dramatically sick.

Camera:

mostly static.

Purpose:

establish the contradiction setup.

Cut:

HARD CUT.

---

## SHOT 01D

Time:

02.80–04.25

Duration:

1.45s

Framing:

INSERT / CLOSE-UP.

Subject:

one brown potato.

Action:

a simplified hand places one potato onto the wooden table near the empty bowl.

The potato settles.

No complex hand movement.

Camera:

static.

Critical rule:

the hand must leave frame before the shot ends.

Purpose:

introduce the object.

Cut:

HARD CUT.

---

## SHOT 01E

Time:

04.25–06.30

Duration:

2.05s

Framing:

MEDIUM CLOSE-UP.

Character:

CST-CHAR-001.

Action sequence:

1. villager notices potato
2. eyebrows tighten
3. he slowly pushes the potato away with one hand

Only one clear arm movement.

Expression:

suspicious / rejecting.

Camera:

very subtle push-in.

Important narration alignment:

the visible rejection should peak around:

05.50–06.30

matching the phrase:

"comer papas."

Purpose:

deliver the main hook payoff.

Cut:

HARD CUT.

---

## SHOT 01F

Time:

06.30–07.60

Duration:

1.30s

Framing:

MEDIUM CLOSE-UP.

Character:

CST-CHAR-002.

Action:

female villager looks at the potato with skepticism and slightly leans away.

No large hand movement.

Expression:

skeptical / worried.

Environment:

same rural interior.

Purpose:

show the distrust is social, not just one man's behavior.

Cut:

HARD CUT.

---

## SHOT 01G

Time:

07.60–09.20

Duration:

1.60s

Framing:

OBJECT CLOSE-UP.

Subject:

potato centered.

Visual treatment:

simple stylized visual symbols suggesting fear of illness.

Possible controlled motifs:

- faint dark-green sickly aura
- two or three abstract warning-like marks
- villagers' silhouettes recoiling in background

Do NOT use:

- realistic disease imagery
- gore
- disgusting biological effects
- readable text

Camera:

slow small push toward potato.

Purpose:

align with:

"Creían que causaban enfermedades."

---

## SHOT 01H — ABSOLUTE END

Time:

09.20–10.00

Duration:

0.80s

Framing:

CLOSE-UP / INSERT.

Subject:

official parchment document on dark wooden surface.

Required visual cues:

- warm parchment
- dark formal desk
- wax seal
- potato placed beside document

Optional:

simple abstract prohibition mark without readable text.

Action:

NONE after approximately 09.55.

Camera:

static by final 0.4s.

Narration alignment:

"Parlamento de París..."

begins during this shot.

Purpose:

bridge conceptually into legal restriction while giving Clip 01 a COMPLETE visual ending.

Final frame:

stable official parchment + wax seal + potato.

No unfinished motion.

---

# Clip 01 Failure Conditions

Reject if:

- male villager changes outfit
- female villager changes outfit
- characters become realistic
- rejection action becomes slapstick
- potato becomes oversized comedy prop
- disease imagery becomes graphic
- cuts become morph transitions
- camera becomes chaotic
- official document contains large garbled text
- final shot is still moving at 10.00

---

# ==========================================================
# CLIP 02 — RESTRICTION + PARMENTIER
# ==========================================================

## Clip ID

CST-EP001-CLIP02

## Time

10.00–20.00

## Narrative Purpose

Move from public fear to official restriction, then introduce Parmentier as the calm informed counterpoint.

## Reference Allocation

1. REF-CHAR-003 — Parmentier
2. REF-CHAR-001 — Male Villager
3. REF-STYLE-001 — Master Style

## Edit Frequency

MEDIUM-HIGH.

Target:

5 shots.

---

## SHOT 02A

Time:

10.00–11.75

Duration:

1.75s

Framing:

close-up.

Subject:

official parchment.

Props:

- wax seal
- quill
- potato near edge of paper

Action:

an official-looking simplified hand presses or finishes placing the document.

No readable text.

Camera:

short push-in.

Purpose:

official restriction.

---

## SHOT 02B

Time:

11.75–13.45

Duration:

1.70s

Framing:

medium insert.

Subject:

potatoes / small basket near official setting.

Action:

simple hand closes or moves the basket away from the document.

Visual meaning:

cultivation / potato use under restriction.

No literal prison imagery.

No readable sign.

Final action resolves.

---

## SHOT 02C

Time:

13.45–16.90

Duration:

3.45s

Framing:

medium shot → medium close-up through internal cut.

Character:

CST-CHAR-003 Parmentier.

Environment:

pharmacist study / workroom.

Action:

Parmentier calmly examines a potato in one hand while comparing it with notes in the other.

Motion:

simple wrist turn + small eye/head movement.

Camera:

gentle push-in.

Expression:

analytical.

Purpose:

introduce Parmentier as knowledgeable and methodical.

---

## SHOT 02D

Time:

16.90–18.75

Duration:

1.85s

Framing:

medium shot.

Character:

CST-CHAR-001.

Environment:

rural edge / simple working area.

Action:

male villager dismissively places or tosses one potato into a simple low feed basket / trough area.

Optional:

one simplified livestock silhouette in background.

Do not make the animal visually dominant.

Purpose:

visualize:

"comida para animales."

---

## SHOT 02E — ABSOLUTE END

Time:

18.75–20.00

Duration:

1.25s

Framing:

medium close-up.

Character:

Parmentier.

Action:

he looks from the potato toward off-screen villagers.

Expression:

thoughtful / idea beginning.

One slight head turn.

Camera:

settles.

Final 0.5s:

stable.

Purpose:

finish the problem statement and prepare for his intervention.

No continuation required.

---

# ==========================================================
# CLIP 03 — FIELD + GUARDS + PERCEIVED VALUE
# ==========================================================

## Clip ID

CST-EP001-CLIP03

## Time

20.00–30.00

## Reference Allocation

1. REF-CHAR-003 — Parmentier
2. REF-CHAR-004 — Guard
3. REF-WORLD-001 — France World

## Primary Environment

Daytime potato field near Paris.

## Edit Frequency

MEDIUM.

Target:

5 shots.

---

## SHOT 03A

Time:

20.00–21.80

Duration:

1.80s

Framing:

wide establishing shot.

Environment:

organized potato field.

Elements:

- cultivated soil rows
- young green potato plants
- simple rural boundary
- distant muted urban/rural horizon

Character:

Parmentier small in midground.

Camera:

gentle lateral reveal or subtle push-in.

Purpose:

"Entonces plantó papas cerca de París."

---

## SHOT 03B

Time:

21.80–23.90

Duration:

2.10s

Framing:

medium shot.

Character:

Parmentier.

Action:

he checks a row of potato plants and looks at notes.

No digging choreography.

One simple bend / observation action.

Purpose:

reinforce intentional cultivation.

---

## SHOT 03C

Time:

23.90–26.20

Duration:

2.30s

Framing:

wide-medium shot.

Characters:

two instances of CST-CHAR-004 guard archetype.

Action:

guards take positions at opposite edges of the field.

Guard A:

musket vertical.

Guard B:

takes one controlled step and settles.

No aggressive weapon action.

Purpose:

"puso guardias armados."

---

## SHOT 03D

Time:

26.20–28.20

Duration:

2.00s

Framing:

medium-long shot.

Foreground:

one generic villager silhouette / partial body observing from outside boundary.

Midground:

guards.

Background:

field.

Action:

observer slightly leans forward.

One guard slowly turns head.

Purpose:

begin:

"si está tan protegido..."

---

## SHOT 03E — ABSOLUTE END

Time:

28.20–30.00

Duration:

1.80s

Framing:

close-medium reaction shot.

Subject:

curious villager reaction.

Use generic ChronoStick villager if no male reference is loaded.

Expression:

curiosity replacing skepticism.

Composition:

guarded potato field visible over shoulder.

Camera:

gentle push-in for first ~0.8s.

Then stop.

Final frame:

villager foreground + guarded field background.

Visual meaning:

"If it is protected, it must be valuable."

No readable text.

No unfinished movement.

---

# ==========================================================
# CLIP 04 — NIGHT + GUARDS LEAVE + THEFT
# ==========================================================

## Clip ID

CST-EP001-CLIP04

## Time

30.00–40.00

## Reference Allocation

1. REF-CHAR-001 — Male Villager
2. REF-CHAR-002 — Female Villager
3. REF-CHAR-004 — Guard

## Primary Environment

Same potato-field design at night.

## Edit Frequency

MEDIUM-HIGH.

Target:

6 shots.

## Historical Presentation Rule

Narration already qualifies this sequence as:

"Según la historia popular..."

Therefore visuals may dramatize the popular story.

Do NOT present the scene using documentary-style on-screen text claiming certainty.

---

## SHOT 04A

Time:

30.00–31.75

Duration:

1.75s

Framing:

wide establishing shot.

Environment:

potato field at night.

Required:

- deep muted navy sky
- readable soil rows
- two guards visible
- subtle lantern warmth if needed

Action:

almost none.

Small vegetation movement only.

Purpose:

use narration pause to establish night.

---

## SHOT 04B

Time:

31.75–33.50

Duration:

1.75s

Framing:

medium-wide.

Characters:

guards.

Action:

one guard exchanges a brief look with the other.

Minimal.

Then both orient toward exit direction.

Camera:

static.

Purpose:

build anticipation while narration says this is the popular account.

---

## SHOT 04C

Time:

33.50–35.55

Duration:

2.05s

Framing:

medium-long.

Action:

guards calmly leave their posts.

Movement:

each takes only a few controlled steps.

Muskets stay close to body.

No running.

No complex turn choreography.

Camera:

short lateral follow OR static composition.

Action must fully finish before cut.

---

## SHOT 04D

Time:

35.55–36.80

Duration:

1.25s

Framing:

medium.

Characters:

CST-CHAR-001 + CST-CHAR-002.

Environment:

edge of dark field.

Action:

they cautiously emerge from behind simple boundary / vegetation.

Male looks toward guard direction.

Female looks toward potatoes.

Subtle coordinated movement only.

---

## SHOT 04E

Time:

36.80–38.45

Duration:

1.65s

Framing:

close-medium / insert sequence.

Action:

male pulls one potato from soil.

Hard cut.

Female places one or two potatoes into cloth sack.

Keep hand actions simple.

Do NOT animate frantic digging.

Purpose:

align with:

"empezó a robarlas."

---

## SHOT 04F — ABSOLUTE END

Time:

38.45–40.00

Duration:

1.55s

Framing:

medium shot.

Characters:

male + female.

Prop:

partially filled cloth sack.

Action:

male lifts sack slightly.

Female gives a small pleased / excited glance.

No broad celebration.

Narration:

"Funcionó."

By approximately 39.40:

all major movement finishes.

Final composition:

two villagers + bag of potatoes.

Stable final frame.

---

# ==========================================================
# CLIP 05 — TASTE + ACCEPTANCE + REVERSE PSYCHOLOGY
# ==========================================================

## Clip ID

CST-EP001-CLIP05

## Time

40.00–50.00

## Reference Allocation

1. REF-CHAR-001 — Male Villager
2. REF-CHAR-002 — Female Villager
3. REF-CHAR-003 — Parmentier

## Edit Frequency

MEDIUM.

Target:

5 shots.

---

## SHOT 05A

Time:

40.00–41.45

Duration:

1.45s

Framing:

close-medium.

Character:

male villager.

Environment:

rustic kitchen.

Action:

he cautiously tastes a small prepared piece of potato.

One controlled hand movement.

Expression:

uncertain.

---

## SHOT 05B

Time:

41.45–42.70

Duration:

1.25s

Framing:

reaction cut.

Character:

male then female or two-character medium shot.

Male:

subtle positive surprise.

Female:

curious.

Female takes or holds another small potato piece.

No exaggerated smiles.

Purpose:

"comenzaron a aceptarlas."

---

## SHOT 05C

Time:

42.70–44.70

Duration:

2.00s

Framing:

medium shot.

Character:

Parmentier.

Environment:

simple study / edge of community setting.

Action:

Parmentier observes calmly while holding notebook.

He makes one small note or closes notebook.

Expression:

quietly satisfied.

Purpose:

reintroduce his role.

---

## SHOT 05D

Time:

44.70–48.45

Duration:

3.75s total with internal clean cuts.

Beat 1:

hand that previously pushed potato away now reaches toward potato.

Beat 2:

basket of potatoes passes from one villager to another.

Beat 3:

male and female inspect / accept potatoes at table.

Motion:

simple in each beat.

Purpose:

visually communicate:

rejection → curiosity → acceptance.

Do NOT use arrows or generated text.

Do NOT create surreal transformation.

---

## SHOT 05E — ABSOLUTE END

Time:

48.45–50.00

Duration:

1.55s

Narration:

"Pocos años después..."

Framing:

wide urban establishing shot.

Environment:

late-18th-century Paris street.

Important:

NO revolutionary crowd yet.

The street should feel:

calm,
historical,
slightly tense,
anticipatory.

Action:

minimal pedestrian motion.

Camera:

slow push-in for first second.

Then settle.

Final frame:

stable Paris street.

Purpose:

create a clean chronological transition.

No potato visible in this final shot.

This prevents causal visual linkage between potatoes and revolution.

---

# ==========================================================
# CLIP 06 — REVOLUTION + CTA + END
# ==========================================================

## Clip ID

CST-EP001-CLIP06

## Time

50.00–60.00

## Reference Allocation

1. REF-CHAR-003 — Parmentier
2. REF-WORLD-001 — France World
3. REF-STYLE-001 — Master Style

## Edit Frequency

MEDIUM → LOW.

Target:

5 beats.

---

## SHOT 06A

Time:

50.00–52.85

Duration:

2.85s

Framing:

wide / medium-wide.

Environment:

late-18th-century Paris revolutionary atmosphere.

Elements:

- controlled crowd
- papers
- urban architecture
- increased energy

Action:

crowd moves forward slightly.

A few arms or papers rise.

No complex riot choreography.

No graphic violence.

Camera:

controlled push-in.

Purpose:

"comenzó la Revolución Francesa."

---

## SHOT 06B

Time:

52.85–53.50

Duration:

0.65s

Framing:

wide still-impact frame.

Environment:

same Paris atmosphere.

Action:

movement largely settles.

Purpose:

brief visual punctuation during narration pause.

Hard cut afterward.

---

## SHOT 06C

Time:

53.50–55.95

Duration:

2.45s

Narration:

CTA.

Framing:

clean warm historical tableau.

Preferred composition:

Parmentier in background/side,
potato basket or rustic table in foreground,
one or two generic ChronoStick villagers.

No lip-sync.

No character speaks.

No generated CTA text.

Leave usable negative space for manual text overlay in Google Vids.

Motion:

very low.

Possible:

Parmentier small head turn,
villager places one potato into bowl.

Purpose:

keep visual interest while CTA plays.

---

## SHOT 06D

Time:

55.95–58.20

Duration:

2.25s

NO NARRATION.

Framing:

close-up.

Subject:

rustic wooden bowl.

Narrative callback to opening.

Difference from opening:

the bowl is now FILLED with several potatoes.

Lighting:

warmer than opening.

Action:

one final potato gently settles in bowl.

Simple controlled motion only.

Purpose:

visual story resolution.

Opening:

empty bowl.

Ending:

filled bowl.

---

## SHOT 06E — FINAL ABSOLUTE END

Time:

58.20–60.00

Duration:

1.80s

Framing:

same or slightly tighter bowl composition.

Action:

NONE.

Camera:

completely stable.

Composition:

filled wooden bowl centered slightly below middle.

Warm parchment / rustic background.

Optional:

very subtle ambient light movement only.

No text generated.

This creates:

- clean ending
- visual closure
- optional space for manual channel branding / subscribe overlay

Final frame must be completely resolved.

---

# Final Visual Motif

Opening motif:

EMPTY BOWL.

Ending motif:

BOWL FILLED WITH POTATOES.

This gives the Short a clear visual arc without requiring visual continuity between separate Omni generations.

---

# Internal Cut Summary

| Clip | Time | Target Beats | Pacing |
|---|---:|---:|---|
| 01 | 00–10 | 8 | Very Fast Hook |
| 02 | 10–20 | 5 | Fast |
| 03 | 20–30 | 5 | Medium-Fast |
| 04 | 30–40 | 6 | Suspense / Medium-Fast |
| 05 | 40–50 | 5 | Medium |
| 06 | 50–60 | 5 | Medium → Slow End |

---

# Motion Intensity Summary

Scale:

1 = nearly still

5 = highly active

| Clip | Character Motion | Camera Motion | Cut Frequency |
|---|---:|---:|---:|
| 01 | 2.5 | 3 | 5 |
| 02 | 2 | 2 | 4 |
| 03 | 2 | 2 | 3 |
| 04 | 2.5 | 1.5 | 4 |
| 05 | 2 | 1.5 | 3 |
| 06 | 2 | 2 → 0 | 3 → 1 |

Critical production principle:

FAST EDITING ≠ CHAOTIC CHARACTER MOTION.

---

# Complexity Budget

Within each individual shot:

Maximum:

- 1 main action
- 1 main camera movement
- 1–2 subtle secondary movements

If a shot needs more:

split it with a hard cut.

---

# Crowd Complexity

Crowd shots must use:

Foreground:

2–5 readable figures.

Midground:

small number of simplified figures.

Background:

silhouette clusters.

Never require Omni to animate dozens of individually detailed characters.

---

# Character Identity Priority

If a generation must simplify something, preserve in this order:

1. character identity
2. costume
3. silhouette
4. primary action
5. main prop
6. environment detail
7. background extras

Do not sacrifice recurring character identity for decorative environment complexity.

---

# Historical Figure Priority

Parmentier must remain:

- same pale period hair
- same deep-blue coat
- same cream waistcoat
- same neck cloth
- same ChronoStick head
- same proportions

No alternate interpretation is permitted inside this episode.

---

# Guard Priority

All guards must retain:

- same cocked hat
- same navy uniform
- same restrained burgundy accent
- same belt system
- same musket family

Do not generate a mixed-unit group.

---

# Color Continuity

Clip 01:
cooler / muted hunger interior.

Clip 02:
parchment + dark wood + blue Parmentier coat.

Clip 03:
muted daylight / earth / muted green.

Clip 04:
deep navy night + subtle warm lantern.

Clip 05:
warmer kitchen / acceptance.

Clip 06:
muted revolutionary urban tones → warm closing bowl.

The palette remains inside CST-STYLE-001 throughout.

---

# Audio / SFX Planning Notes

Suggested Omni SFX only:

Clip 01:
- subtle wooden bowl/table sound
- potato placement
- cloth movement

Clip 02:
- paper movement
- seal / desk sound
- subtle study ambience

Clip 03:
- light outdoor ambience
- footsteps
- subtle equipment movement

Clip 04:
- night ambience
- controlled footsteps
- soil / sack sound

Clip 05:
- rustic kitchen ambience
- food handling
- paper / notebook sound

Clip 06:
- controlled distant crowd ambience
- then significantly reduced ambience for final bowl shot

No dialogue.

No voices.

No loud cinematic impact sounds generated inside Omni unless specifically added later in editing.

---

# Manual Google Vids Layer Plan

Outside Omni:

1. continuous Spanish narration
2. optional natural editorial SFX
3. captions
4. CTA typography
5. final channel branding

Do not add a soundtrack, score, melody, beat, orchestral music, or musical ambience.

Omni-generated audio should remain secondary.

---

# File Dependency Map

This shot plan feeds:

episodes/001-potato-france/prompts/clip-01-hook.md

episodes/001-potato-france/prompts/clip-02-restriction.md

episodes/001-potato-france/prompts/clip-03-field-guards.md

episodes/001-potato-france/prompts/clip-04-night-theft.md

episodes/001-potato-france/prompts/clip-05-acceptance.md

episodes/001-potato-france/prompts/clip-06-ending.md

Each clip file will translate its shot section into one extremely explicit Omni generation prompt.

---

# Shot Plan Failure Conditions

Reject or revise this plan if:

1. the hook no longer feels fast
2. any 10-second generation depends on the following generation
3. too many complicated actions occur in one shot
4. character references exceed Omni's 3-reference limit
5. Parmentier identity is inconsistent
6. guards become visually inconsistent
7. visual storytelling implies potatoes caused the French Revolution
8. the final clip lacks clear visual resolution
9. generated text becomes necessary for basic story comprehension
10. the opening contradiction is not visually clear before approximately 6.5 seconds

---

# Approval Checklist

Before locking this Shot Plan:

- [ ] Six exactly 10-second generation blocks exist
- [ ] All narration beats are visually covered
- [ ] Hook is significantly faster than body
- [ ] Clip 01 has 6–8 visual beats
- [ ] Every other clip remains readable
- [ ] Motion remains moderate
- [ ] Internal cuts remain active
- [ ] All clips have absolute endings
- [ ] Reference allocation never exceeds 3 images
- [ ] Main characters have explicit reference assignments
- [ ] Night theft sequence remains simple enough for Omni
- [ ] Revolution is visually separated from potato causality
- [ ] CTA contains no generated speech/text requirement
- [ ] Final 4 seconds work without narration
- [ ] Final visual motif resolves opening empty-bowl motif

---

# Approval

Current status:

ARCHIVED WORKING PLAN

The episode was completed externally, but this plan was never formally reviewed and locked in the repository. It remains a detailed production reference with `approved: false`. Do not present it as an approved v1.0.0 artifact.
