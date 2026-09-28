---
name: chronostick-references
description: Design, prompt, generate, and review full-frame generation-safe stick-world references, including portrait-grounded historical identities. Use when the approved reference manifest identifies a missing scene, character, environment, vehicle, or prop anchor.
---

# Chronostick References

Reuse approved assets when they already control the needed identity and state. New reference generation is justified only by the approved manifest.

## Reference contract

- One full-frame image, normally vertical 9:16 and close to H3 composition.
- One scene, one time state, one camera viewpoint, and exactly the intended subject count.
- A character reference shows one full-screen identity/pose or one scene anchor—not a turnaround, expression grid, sheet, collage, or multiple pose.
- Every person, object, environment, aircraft, shadow, and material is translated into the approved detailed cinematic ChronoStick stick-world. The master style always overrides incidental realism in content references.
- No borders, labels, captions, typography, swatches, panels, duplicated subjects, alternate views, or future events.
- Preserve identity through head/hair silhouette, costume silhouette/colors, proportions, signature props, and minimal face language.
- Compose for safe crop, clear silhouettes, stable background geometry, controlled light direction, and low ambiguity.

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

State the style authority, real-portrait identity authority when applicable, approved identity-anchor mapping, exact count, shot state, composition, environment, lighting, emotion, costume, prop state, exclusions, and output aspect. Keep the paste-ready prompt separate from rationale.

Store prompts under `prompts/image/episodes/<episode>/` and immutable selected images under `assets/episodes/<episode>/references/` with `-rNNN`.

## Review

Inspect the full image before approval. For a real person, compare the result to the archived portrait cues and to every other recurring identity. Reject realistic anatomy, photoreal surfaces, style mixing, hidden panel borders, repeated or averaged people, swapped identity cues, wrong costume, future-event contamination, unreadable silhouette, or unsafe crop. Do not mark an image approved merely because it exists.

Update `plan/reference-manifest.json` with selected path, hash, revision, role, clips, review status, and decision notes.
