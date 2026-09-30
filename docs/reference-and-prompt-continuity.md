# Generation-safe references and prompt continuity

This document captures the reusable production method learned from Episode 002. It applies whenever a reference-to-video model must preserve style, recurring identity, physical action, emotion, and narrative order across independently generated clips.

## Separate design sources from video inputs

Master style boards, world sheets, character sheets, and vehicle sheets remain valuable design authorities. Their multi-panel layouts are risky as direct video inputs because a model may copy borders, grids, repeated poses, alternate views, or later event states into the animation.

For video generation, derive episode-scoped generation-safe references:

- one continuous scene rather than a board or contact sheet
- one time state only
- one camera viewpoint
- exactly the intended number of foreground characters and objects
- no repeated pose or alternate view of the same identity
- no readable labels or annotations
- no future narrative event visible anywhere in the image
- vertical composition close to the generation aspect ratio
- stable background geometry and clear subject silhouettes

Keep the original master assets unchanged. Store the exact image-generation prompt before generation, generate from that exact text, visually inspect the result, and save the selected image with an immutable `-rNNN` filename.

## Reference allocation

Use the fewest references that fully control the shot:

1. Prefer one single-scene anchor that already combines style, world, identities, props, and current story state.
2. Add a second reference only when a separately controlled subject is essential, such as a distant falling object seen from a character's point of view.
3. Do not pass a multi-pose character sheet merely because an identity appears. A scene anchor with one instance of that character is safer.
4. Keep JSON reference order identical to `<Picture N>` order and describe each role exactly once.
5. Sampling steps refine a generation; they do not repair ambiguous identity, duplicated subjects, a contaminated reference, or a contradictory story state.

## Lock the shot-to-anchor contract

Before final video prompts, record for every timed shot which approved full-frame anchor controls its people, hands, animals, vehicles, story-critical props, architecture/landscape, light, event phase, and rendering style. Include exact visible counts, left/right placement, scale, distinguishing identity/costume cues, object ownership and physical state, camera crop, and the state carried through the next cut. State a deliberate absence as zero when the model could plausibly add an extra person, boat, flag, or word.

Check the real image at full resolution and at phone size. The intended shot must be achievable by reframing that single scene; an era-matched anchor cannot control a new aerial city, realistic horse, hand insert, or unseen coastline. If coverage is missing, change the shot or approve a new single-scene anchor within the profile limit. Resolve conflicting image details before generation. No amount of sampling or generic negative wording guarantees style or identity when the visual input is ambiguous.

## Build a story-state ledger first

Before writing generator prompts, create one row per clip with:

- global timeline range and narration overlap
- inherited start state
- allowed change during the clip
- resolved end state
- exact character and object count
- fixed screen placement and travel direction
- posture and prop state
- facial/emotional state
- environment and illumination state
- event phase

The next recurring-character clip must inherit the preceding relevant end state. A clean hard cut may change framing, but it must not reset a standing character to breakfast, restore a consumed action, move a prop backward in time, or reduce fear to an earlier emotional phase without narrative cause.

## Prompt at controllable density

For a standard five-second H3 clip, use roughly three to four readable timed beats. Reduce shot count before sacrificing identity or action clarity. Each shot should contain one primary action, no more than one simple camera move, and at most two subtle secondary motions.

A named rapid-cut profile may use six to eight hard-cut shots in five seconds when the narration and approved direction require it. This is an editorial-density exception, not a motion-complexity exception: each short shot still has one simple action, no more than one camera move, low background motion, a distinct silhouette or framing purpose, and an exact local time. Use single-scene references and strong identity locks so the extra cuts do not become character drift or contact-sheet imagery. If a historical identity cannot be read at thumbnail scale, reduce the cut density for that moment rather than adding labels.

For a terminal state such as a settled aftermath, a single continuous locked shot can be safer than multiple cuts. If timing validation requires phases, describe phases of the same shot rather than new compositions.

Every prompt should explicitly define:

- duration, aspect ratio, and frame rate
- reference roles
- start state
- exact time spans
- camera behavior and when it stops
- character/object count
- screen direction and simple physics
- expression changes through eyebrows, dot-eye focus, mouth state, shoulders, hands, stance, and movement speed
- resolved end state and final hold
- text, speech, and audio restrictions

For each short shot, repeat the critical local facts: exact visible subject and prop inventory, the anchor scene/phase, screen position, one action from start to settled end, camera height and move, light direction/palette, hard-cut frame, and brief isolated SFX. Keep the shared global lock for whole-frame illustrated style and recurring identity. Specify seemingly obvious facts when omission could let a person duplicate, a prop teleport, or an empty background turn photographic; keep the instructions mutually consistent and grounded in the image.

## Describe the present state positively

High-salience words can activate the very concept they are intended to forbid. In a pre-event clip, do not repeatedly name a later event in a negative list. Instead state the current state positively and completely:

- the object remains high and airborne
- the city geometry, sky color, cloud shape, and morning illumination remain intact and unchanged
- the only change is the object's downward position
- the clip begins and ends in the same event phase

Likewise, a settled-aftermath clip should say that the aftermath already exists before frame 1 and remains unchanged through the final frame. Avoid a reveal, before/after comparison, transition, new light source, focal plume, or large compositional change.

## Identity and emotion control

State exact count and differentiation before action:

- exactly one woman and one man
- fixed clothing colors and silhouettes
- stable left/right positions when continuity depends on them
- exactly two heads and the expected limb count
- one joined-hand pair when hands are the story action

Use a deliberate emotion ladder. For minimal ChronoStick faces, specify eyebrow angle, dot-eye direction/width, mouth line, head angle, shoulder tension, hand shape, weight shift, and speed. Keep mouths closed whenever narration is external and generated dialogue is forbidden.

## Vehicle and airborne-object control

Define physics rather than cinematic adjectives:

- one aircraft only
- a fixed screen direction
- level wings, constant altitude, constant orientation, rigid geometry
- all four engines attached and rotating steadily
- one release action only
- object moves downward and slightly rearward
- separation increases monotonically
- object remains below a maximum frame-size percentage
- rotation is limited to a few degrees

Avoid vague words such as “escalating” when they could imply a later causal event. Separate aircraft crossing, object release, isolated descent, human recognition, and later consequence into distinct references and prompts.

## Review and retry

Review a contact sheet at several frames per second and inspect the actual video around every cut. Check:

- correct story phase in every frame
- character/object count and identity
- absence of reference panels or sheet borders
- environment and light continuity
- physical travel direction
- facial/emotional progression
- generated text, dialogue, music, and audio stream
- stable final frame
- absence of photographic or mixed-style pixels in every shot, including hands, animals, sea, sky, and background inserts
- exact shot-to-anchor coverage and no unexplained subject, prop, costume, light, or setting change across cuts
- only short isolated SFX with silence between cues, leaving room for separately added background music

Retry the same prompt and seed for an isolated random defect when the specification is sound. Rewrite the prompt for a specification defect. When the generated motion follows an unwanted trajectory strongly, use a new immutable output revision and a new fixed seed after correcting the prompt. Never overwrite an earlier render.

## Episode 002 diagnostic examples

- Multi-panel style and world boards appeared inside Clips 06 and 10; single-scene anchors removed the board layout from H3 inputs.
- Multi-pose character sheets contributed to a cloned elderly man in Clip 13; one-instance couple anchors and exact count/placement rules reduced ambiguity.
- Clip 13 originally restarted from breakfast after Clip 12 had already placed the man at the window; explicit start/end states removed the regression.
- Clip 11 completed the causal story too early; present-state-only language and a single airborne-object anchor separated descent from consequence.
- Clip 17 r003 changed from a debris insert to a wide view and generated a new event at the end; the correction uses one locked aftermath composition with constant light and geometry.
