---
name: chronostick-review
description: Perform frame, motion, continuity, audio, and technical QC on ChronoStick renders; classify failures and prepare only necessary immutable replacements. Use after generation and before final clip selection.
---

# Chronostick Review

Review the actual video with sound and representative frames around every cut. A successful job is only a candidate render.

## Per-clip checks

- story phase and chronology match the narration window
- whole frame remains in the approved stick-world style
- exact recurring identity, costume, count, placement, prop state, and emotion
- readable action, controlled physics, intended camera, rapid but comprehensible cuts
- no sheet panels, clones, anatomical failures, generated labels, captions, or logos
- synchronized natural SFX; no melody, beat, tonal ambience, speech, narration, singing, or vocal reactions
- correct resolution/frame rate, valid audio/video streams, editorial duration, stable final frame

## Rapid-cut and directing audit

- Build a dense contact sheet or inspect representative frames immediately before and after every planned cut. Count materially distinct shot states; a rapid-profile clip must show the planned eight hard-cut shots unless an approved exception exists.
- Do not accept a long take, whip pan, speed ramp, zoom blur, or morph as a substitute for editing. The pace must come from discrete readable compositions while motion inside each shot remains controlled.
- Confirm every cut contributes new story information and the clip still reads as setup–escalation–payoff. Flag repetitive medium coverage, arbitrary camera moves, weak visual hierarchy, flat lighting, or technically correct but uncreative direction.
- Review the intended camera height, lens feeling, subject scale, depth layers, light direction, palette, negative space, and final resolved hold—not only anatomy and continuity.

## Historical identity audit

For every named real person, compare multiple frames to the approved portrait-grounded identity and scene anchors. Check the locked silhouette, hair, facial hair, costume, proportions, and signature prop. Also compare recurring people against one another: reject averaged faces, swapped cues, duplication, identity morphing, or a generic stick figure that is no longer recognizable without a label.

Record timecodes and evidence in `renders/review-rNNN.md`. Decisions are `approved`, `retry`, `revise_prompt`, `revise_reference`, or `reject`; never infer approval.

## Replacement policy

- Isolated stochastic defect with a sound specification: keep the prompt/reference contract, use a new explicit fixed seed, and advance output revision.
- Specification defect: revise the prompt or reference first, revalidate all mappings, use a new seed, and advance revision.
- Chronology/continuity defect: correct the state ledger and every downstream affected prompt/job, not only the visible symptom.
- Music or speech: reject; stronger prompt wording may reduce recurrence but human audio review remains mandatory.

Create replacement jobs under `automation/retries/` and run only the affected clips after preflight and explicit authorization. Keep prior outputs immutable.

## Approval gate

Stage exactly one reviewed editorial video for every clip number under `renders/final-selected/`. Verify no duplicate/missing numbers and preserve source revision in each filename.
