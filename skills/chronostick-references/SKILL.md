---
name: chronostick-references
description: Design, prompt, generate, and review full-frame generation-safe stick-world references, including portrait-grounded historical identities. Use when the approved reference manifest identifies a missing scene, character, environment, vehicle, or prop anchor.
---

# Chronostick References

Reuse approved assets when they already control the needed identity and state. New reference generation is justified only by the approved manifest.

## Reference contract

- One full-frame image, normally vertical 9:16 and close to H3 composition.
- One scene, one time state, one camera viewpoint, and exactly the intended subject count.
- A concrete inventory of everything visible: exact people and animals, their screen positions and sizes, costume and face cues, hands, props, vehicles, flags, architecture, terrain, sky, and background extras. State the current phase and the physical state of each story-critical object. Leave no unnamed figure or ambiguous duplicate silhouette.
- A character reference shows one full-screen identity/pose or one scene anchor—not a turnaround, expression grid, sheet, collage, or multiple pose.
- Every visible pixel, including small background objects, empty landscapes, sea, sky, smoke, horses, hands, architecture, aircraft, shadows, and materials, is translated into the same approved detailed cinematic ChronoStick stick-world. Keep dark drawn contours and simplified anatomy/surfaces at full size and at phone size. The master style always overrides incidental realism in content references.
- No borders, labels, captions, typography, swatches, panels, duplicated subjects, alternate views, or future events.
- Preserve identity through an explicit, repeatable cue list: head/hair silhouette, face marks, costume cut/colors, proportions, signature props, and minimal expression language. Distinguish every other visible person's headwear and uniform from the named identity.
- Compose for the actual planned coverage: safe crop margins, fixed left/right placement, subject scale, clear silhouettes, stable background geometry, foreground/midground/background separation, controlled light direction and color, and low ambiguity. Show a vehicle's required masts/wheels/engines and a prop's required shape/count clearly enough to survive close crops.

## Shot-to-reference coverage

Before generating or approving an anchor, compare it with every shot that will cite it. Record in the episode manifest or shot plan which reference controls each shot's people, props, environment, event phase, and rendering style. A crop, insert, or camera angle must remain achievable from the anchor's one scene; do not expect the video model to invent an unanchored city, landscape, animal, hand, or vehicle and preserve style. If a planned shot needs a different state or location, revise the shot or create a separate approved single-scene anchor within the profile's reference limit. Resolve contradictions between references before writing video prompts.

Also check semantic coverage. A beautiful doorway is not a hospital anchor unless beds, patient/caregiver, or another period-appropriate care action makes its purpose clear. A negotiation table is not an Elba-condition anchor unless the island/mainland relationship is already legible. Approve the reference for the specific action and meaning required, not merely the right era, style, or location.

## Real historical character workflow

When a named real person recurs, do not invent a generic look from memory or generate the group scene first.

1. Research one or more authoritative real portraits from primary institutional collections such as national archives, libraries, museums, presidential sites, or park services. Preserve the source URL, downloaded portrait, attribution notes, and hash in the episode source folder.
2. Extract only the durable recognition cues that survive stick-world simplification: overall height/build, head and hair silhouette, facial-hair pattern, period costume shape, color signature, and one historically supported accessory when useful.
3. Generate one full-frame, single-person identity anchor using the approved ChronoStick style as rendering authority and the real portrait as identity/content authority. The result must remain unmistakably a stylized stick character, never a pasted or photoreal face.
4. Review the identity anchor against both authorities. Confirm recognizability, period accuracy, style purity, safe crop, and the absence of extra people, text, panels, or alternate poses.
5. For multiple real people, run a cross-character separation test at small scale. Each silhouette must remain distinguishable without names or captions. Fix identity anchors before building any group reference.
6. Derive group and event-scene anchors from the approved identity anchors plus the approved environment/state authority. H3 should normally receive these generation-safe scene anchors rather than raw historical photographs.

For a multi-person historical group, preserve the exact subject count and every individual's locked cues. Never average faces, swap hair or facial hair, repeat one identity, or let a shared dark suit erase the differences. Simplify the environment before simplifying the people.

## Prompt contents

State the style authority, real-portrait identity authority when applicable, approved identity-anchor mapping, exact visible inventory, positions and sizes, one action-ready shot state, geometry and depth layers, camera height/viewpoint, light source/direction, palette, expression, costume and anatomy, every story-critical prop's count/shape/color/location, exclusions, safe margins, and output aspect. Spell out obvious details when leaving them open could change identity, chronology, or the whole-frame style. Use concrete positive descriptions before a short failure list; avoid vague adjectives or contradictory instructions. Keep the paste-ready prompt separate from rationale.

Store prompts under `prompts/image/episodes/<episode>/` and immutable selected images under `assets/episodes/<episode>/references/` with `-rNNN`.

## Review

Inspect the full image and a phone-size crop before approval. Check the entire frame against the inventory and every intended shot crop, including corners, tiny extras, prop counts, light direction, and background materials. For a real person, compare the result to the archived portrait cues and to every other recurring identity. Reject realistic anatomy, photoreal surfaces anywhere, style mixing, hidden panel borders, repeated or averaged people, swapped identity cues, wrong costume, future-event contamination, unreadable silhouette, unsafe crop, or an anchor that leaves a planned shot unsupported. Do not mark an image approved merely because it exists.

Update `plan/reference-manifest.json` with selected path, hash, revision, role, clips, review status, and decision notes.
