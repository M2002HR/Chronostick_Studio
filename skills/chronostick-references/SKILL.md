---
name: chronostick-references
description: Design, prompt, generate, and review full-frame generation-safe stick-world references, including portrait-grounded historical identities. Use when the approved reference manifest identifies a missing scene, character, environment, vehicle, or prop anchor.
---

# Chronostick References

Reuse approved assets when they already control the needed identity and state. New reference generation is justified only by the approved manifest.

## Reference-first prerequisites

For reference-first Shorts, production design begins only after the user's actual scenario/storyboard review. Derive the required identities, places, props and action states from both reviewed storyboard and reference-video analysis. Use as many separate single images as needed for shot coverage; per-job reference limits remain profile-specific. Neutral rough storyboard grids are planning only and must not become generation inputs. Prepare pure image prompts before generating. Preserve the approved ChronoStick style while adapting source character recognition and staging into stick-world.

Open and visually inspect the selected storyboard pages alongside `plan/storyboard/shot-list.json` before planning references or writing their prompts. Use the panels to preserve framing, composition, subject count, screen placement, action, prop state and narrative purpose; translate their neutral figures into the approved stick-world style without treating sketch faces or costumes as identity authority. Each reference-manifest entry must name its supporting `storyboard_panel_ids` and source-analysis IDs, then explain which panel views/actions it covers. Check each generated image against those actual panels during review. If engine feasibility or real voice timing requires a change, record the affected panels and rationale in a separate reconciliation record; reopen material story/composition changes for user review instead of silently replacing the storyboard.

## Reference contract

- One full-frame image, normally vertical 9:16 and close to H3 composition.
- One scene, one time state, one camera viewpoint, and exactly the intended subject count.
- A concrete inventory of everything visible: exact people and animals, their screen positions and sizes, costume and face cues, hands, props, vehicles, flags, architecture, terrain, sky, and background extras. State the current phase and the physical state of each story-critical object. Leave no unnamed figure or ambiguous duplicate silhouette.
- A character reference shows one full-screen identity/pose or one scene anchor—not a turnaround, expression grid, sheet, collage, or multiple pose.
- Every visible pixel, including small background objects, empty landscapes, sea, sky, smoke, horses, hands, architecture, aircraft, shadows, and materials, is translated into the same approved detailed cinematic ChronoStick stick-world. Keep dark drawn contours and simplified anatomy/surfaces at full size and at phone size. The master style always overrides incidental realism in content references.
- No borders, labels, captions, typography, swatches, panels, duplicated subjects, alternate views, or future events.
- Preserve identity through an explicit, repeatable cue list: head/hair silhouette, face marks, costume cut/colors, proportions, signature props, and minimal expression language. Distinguish every other visible person's headwear and uniform from the named identity.
- Check body proportions against the locked style before scene derivation: the standard figure is roughly 5.0–5.8 round-head units with narrow shoulders and limbs. Detailed clothing must follow the simplified stick anatomy; a round face on a broad 7–8-head human body is insufficient. Use the actual master image and locked proportion guidance when an initial identity drifts.
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

## Reproducible image requests

Use `scripts/reference-artifacts.py freeze` before a reference-first image call. Supply the episode, known reference IDs, request-group name, new `rNNN` revision and master-style path. This records the exact pure prompt, storyboard panel IDs, ordered image roles and hashes, and the intended immutable asset path. Dependencies must already have actual review decisions and unchanged selected bytes. Use `verify --request <snapshot>` immediately before generation, then call the built-in image tool with that snapshot's prompt and ordered local image paths. Archive its returned PNG unchanged with `ingest`; ingestion creates a candidate/result record and never selects or approves art. Keep failed candidates and request snapshots, update the pure prompt in Git, and freeze a new revision for corrections. An old snapshot stays historical even when its current prompt has changed.

The built-in image tool accepts at most five input paths including the style image. Inherit already-reviewed identities from a scene anchor when that preserves coverage; do not remove the style or a necessary prop/state authority merely to fit. This limit is separate from the video engine's per-job limit. When collecting independent image calls, await every outcome, including failures, so a rejected call cannot discard another generated result's provenance.

Keep the style input's role separate from scene content: architecture, era, people and props pictured on the master style board must not leak into a new setting. Specify a sparse period-appropriate background positively. Check pre-action states explicitly: a closed door and an opened threshold, or a mask held below a face and a worn mask, can require separate single-image anchors. Match their physical geometry and identity cues across state changes.

## Review

Inspect the full image and a phone-size crop before approval. Check the entire frame against the inventory and every intended shot crop, including corners, tiny extras, prop counts, light direction, and background materials. Phone-size derivatives are review evidence only; keep the original production PNG unchanged. Inspect drawings within props too: a blank-text plan can still depict an anachronistic building. For a real person, compare the result to the archived portrait cues and to every other recurring identity. Reject realistic anatomy, photoreal surfaces anywhere, style mixing, hidden panel borders, repeated or averaged people, swapped identity cues, wrong costume, future-event contamination, unreadable silhouette, unsafe crop, or an anchor that leaves a planned shot unsupported. Do not mark an image approved merely because it exists.

Update `plan/reference-manifest.json` with selected path, hash, revision, role, clips, review status, and decision notes.
