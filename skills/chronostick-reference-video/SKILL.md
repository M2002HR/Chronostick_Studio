---
name: chronostick-reference-video
description: Review an actual supplied reference video alongside its timed transcript and derive a timecoded, generation-aware story and directing adaptation for ChronoStick. Use at reference-first intake or when new source footage changes direction.
---

# ChronoStick Reference Video

Read `docs/reference-first-shorts.md` for reference-first Shorts. Long-form retains its format and `docs/longform/reference-video-workflow.md`. Preserve original media/provenance and use `chronostick-transcribe` for actual text/timing before treating the review as complete.

## Observe, then direct

Probe and inspect the complete video alongside transcript timecodes. Sample the full timeline and revisit rapid/ambiguous cuts densely. Record the method: continuous viewing, extracted frames, audio access and any separate multimodal review. A still proves composition, not motion or sound; a provider's video review is machine evidence, not a fabricated personal listening claim. Record exact versus approximate cut times and unknowns.

Write `source/reference-video/intake-review.md` and `plan/reference-video-analysis.md`. Link each observed span to its spoken claim, hook/open loop, subject roles, physical action, framing, cut/transition, emotion/comedy, payoff and viewer effect. Carry useful mechanism IDs into the scenario/storyboard. Preserve the source's useful story structure closely while creating original Spanish wording and ChronoStick staging. Separate observed facts, interpretation and proposed adaptation.

For supplied-source adaptation, preserve the user's chosen content: claims, numbers, dates, causal links and payoff. Do not fact-check, research historical claims, or replace/remove them unless the user explicitly requests verification or content changes. A request to make, translate or shorten a video is not a verification request. Compression and original wording may change presentation, not meaning. Record `fact_check_requested: false` and distinguish source claims from independently verified findings in internal provenance; do not claim verification. Prior unsolicited research does not authorize rewriting the source. When verification is explicitly requested, preserve citations and propose corrections separately. Keep source music, branded joke labels and ordinary captions outside the production picture.

## Generation feasibility

For every retained mechanism choose keep/adapt/drop and give an achievable replacement where necessary. The engine supplies creative edits inside each generation: do not rely on later manual overlays, speed ramps, composite rescue or pixel-matched movement across clips. Give each shot one primary action and at most one simple camera move. Every clip must settle its own ending.

For Shorts, choose a 20–30-second working target at intake and compress by narrative value: immediate visual hook, short necessary context, fast consequence/reveal, clear payoff and an optional replay-friendly return. Source runtime is not output runtime. Match energetic Episodes 003/004 through purposeful cut contrast; do not impose a fixed shot count before accepted voice timing.

## Handoff

Produce a source-to-adaptation trace, character/world/prop inventory, feasibility decisions, uncertainties and a draft scenario brief. Pass these to `chronostick-script` and `chronostick-storyboard`. No image, scenario or timing becomes approved by inference.
