---
name: chronostick-references
description: Design, prompt, generate, and review full-frame generation-safe stick-world references for ChronoStick clips. Use when the approved reference manifest identifies a missing scene, character, environment, vehicle, or prop anchor.
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

## Prompt contents

State the style authority, content/identity authority, exact count, shot state, composition, environment, lighting, emotion, costume, prop state, exclusions, and output aspect. Keep the paste-ready prompt separate from rationale.

Store prompts under `prompts/image/episodes/<episode>/` and immutable selected images under `assets/episodes/<episode>/references/` with `-rNNN`.

## Review

Inspect the full image before approval. Reject realistic anatomy, photoreal surfaces, style mixing, hidden panel borders, repeated people, wrong costume, future-event contamination, unreadable silhouette, or unsafe crop. Do not mark an image approved merely because it exists.

Update `plan/reference-manifest.json` with selected path, hash, revision, role, clips, review status, and decision notes.
