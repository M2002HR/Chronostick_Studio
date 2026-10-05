---
name: chronostick-longform-visual-direction
description: Analyze historical-video transcripts and frame references, then design an original ChronoStick visual language and sequence plan for a 10–15 minute episode. Use before detailed long-form shot planning; do not treat a reference video's script or artwork as historical authority or generator-ready material.
---

# ChronoStick long-form visual direction

Turn supplied examples into reusable storytelling methods and a specific visual blueprint. This skill owns the bridge between an episode's researched narrative and its detailed timed shot plan. It does not approve historical claims, generate media, write H3 jobs, or replace the short-form skills.

## Inputs and authority

Read the repository `AGENTS.md`, `docs/longform/workflow.md`, `docs/longform/format-contract.md`, `docs/longform/reference-video-workflow.md` and active shared rules before changing an episode. Gather the supplied title/source, actual reference video, its Stage 00 intake review and manifest, transcript and screenshots, approved Spanish narration if present, accepted voice and word timing if present, existing ChronoStick style and identity authorities, and the named production profile. Record missing inputs explicitly. Reinspect selected video moments more densely than the intake sample before relying on exact motion, framing or cuts. Treat a video transcript as a noisy *example*, not evidence: correct names and claims against independent sources before proposing them as narration, map content, screen text, or character identity.

If the user supplied only examples, produce an analysis and reusable direction; do not fabricate a locked episode plan or word timings. If the script is not yet approved, keep shot times and narration synchronization provisional.

For episode 006, prefer its inspected `source/reference-video/intake-review.md` and video over the earlier screenshot-only [reference-example-analysis.md](references/reference-example-analysis.md). For other examples, apply the same analysis method to their actual evidence.

## Extract the mechanism, then adapt it

For each useful example moment, record: manifest item ID, visible or audible observation and timestamp; the narrative job it performs; the viewer question before and after; the *mechanism* (such as a scale change, map reveal, visual contradiction, word card, or time compression); the historical claim it may imply; and an original ChronoStick adaptation. Distinguish what the screenshot proves from motion, sound, or timing that cannot be inferred from a still. Match useful directing principles closely enough to give the episode the intended energy and clarity, while creating new ChronoStick staging. Do not trace frames, copy the other creator's character design, map art, wording, jokes, palette, or exact shot sequence. Never carry over the reference's music or generated dialogue. An acted cold open can instead be directed as silent action under separately approved narration when that serves the story.

Select visual ideas by their explanatory value and viewer effect. A cut should reveal a new fact, consequence, location, scale, point of view, or earned visual punchline. Alternate scene action, spatial explanation, evidence, surprise, reaction, and resolved holds according to the narration; do not impose the Shorts eight-cuts-per-five-seconds rule on a long video. Aim for lively, inventive direction and situational wit without making documented suffering a gag. Keep each generated shot within the repository's one-primary-action and at-most-one-camera-move budget. Default independent H3 generations to the episode's five-second profile unless the user names a different one; an editorial sequence can use fewer or more cuts than one generation contains.

## Historical visual contracts

- **Identity:** Inventory every recurring named person, anonymous role, animal, vessel, and prop. For a documented individual, research institutional portraits or period sources and extract recognizable stick-world cues; archive provenance. For an undocumented role, create one deliberately consistent episode design without implying an authentic likeness. Preserve approved identity across ages or costume changes by recording exactly what changes and why. Build single-scene generation anchors from approved identities instead of feeding multi-pose boards directly to H3.
- **Maps:** Define the date, geographic extent, source, political/status terminology, coastline and border authority, symbols, route order, labels, and zoom levels *before* drawing. Distinguish state, colony, protectorate, sphere of influence, and trade route. Use the same map grammar across world, region, island, and tactical scales; label changes of time or scale. A modern political map cannot silently stand in for a historical map. Verify each visible border, movement, flag, ship position, and label against the claim it is meant to teach. Make the map itself an approved full-frame illustrated asset or scene anchor, then test whether motion preserves its geography.
- **Visible text inside H3:** The user's default is to generate selected dates, times, numbers, names, and short terms *inside the five-second video*. Treat each as a named, clip-specific exception to the repository's general no-readable-text rule. Record the exact Spanish string, source and certainty, punctuation/diacritics, position, onset, hold, disappearance, and other text that must be absent. Prefer one short message per composition. Supply an approved text-bearing anchor when exact typography matters; ask H3 to preserve it without morphing. Inspect spelling and stability frame by frame at full size and at phone size. A good reference or prompt cannot guarantee correct generated text; a failed result stays unapproved. Do not silently replace the user's in-engine choice with an editorial overlay.
- **Sensitive history:** Frame colonial rule, enslavement, mass injury, and contested allegations with the actual evidence and human consequences. A visual joke may explain a power imbalance; it must not turn victims into a gag or imply that one side's self-description is the whole history. Mark dramatized conversations and uncertain causes so the finished narration and image do not present them as documented dialogue or fact.

## Build the episode direction

Produce `plan/reference-video-analysis.md` for supplied examples and a reviewable visual blueprint under the target episode's `plan/` once that episode exists. Use a concept document plus structured ledgers or tables; do not put planning notes in `prompts/`. It should contain:

1. The title/thumbnail promise and the first visual proof of that promise; central question, chapter questions, revealing payoff, and what the viewer learns in each chapter.
2. An ordered sequence list with narrative purpose, provisional or accepted time range, visual mode, shot-density rationale, transitions, any selected reference-analysis IDs, humor/emotional register, and a deliberate change of scale or viewpoint where useful. Make a complete voice-and-image animatic before bulk H3 generation.
3. An identity/world ledger and a map/graphic grammar: recurring cues, chronological states, palette and lighting logic, map scales, symbol legend, and provenance/uncertainty notes.
4. A text-event ledger for every intended in-engine word or number and an explicit default of no other readable text.
5. A reference-coverage matrix: every proposed shot's people, animals, props, terrain, viewpoint, event phase, typography, and map detail must be achievable from named approved anchors. Mark missing anchors instead of pretending coverage exists.
6. A risk and test order. Prototype expensive or fragile motifs early: historical likenesses, crowded groups, maps, exact text, physical interactions, and SFX-only audio. A low-step preview can reject a bad concept but cannot approve a final-step clip; compare selected paired renders at the final settings before trusting it as a predictor. Budget and queue only after reference coverage and prompt/job validation.

## Handoff gate

Pass the approved blueprint, actual narration timing, reference requirements, text/map exceptions, and continuity states to a dedicated long-form shot-plan stage. Every proposed historical image or displayed claim must have a source or an explicit unresolved flag. Every repeated figure must have a stable identity authority. Every map or text insert must have an exact content contract. The plan must remain original to ChronoStick, preserve the no-background-music rule, and identify where the existing 9:16 Shorts tools need a separate landscape profile before generation.
