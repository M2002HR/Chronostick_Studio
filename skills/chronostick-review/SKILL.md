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

Record timecodes and evidence in `renders/review-rNNN.md`. Decisions are `approved`, `retry`, `revise_prompt`, `revise_reference`, or `reject`; never infer approval.

## Replacement policy

- Isolated stochastic defect with a sound specification: keep the prompt/reference contract, use a new explicit fixed seed, and advance output revision.
- Specification defect: revise the prompt or reference first, revalidate all mappings, use a new seed, and advance revision.
- Chronology/continuity defect: correct the state ledger and every downstream affected prompt/job, not only the visible symptom.
- Music or speech: reject; stronger prompt wording may reduce recurrence but human audio review remains mandatory.

Create replacement jobs under `automation/retries/` and run only the affected clips after preflight and explicit authorization. Keep prior outputs immutable.

## Approval gate

Stage exactly one reviewed editorial video for every clip number under `renders/final-selected/`. Verify no duplicate/missing numbers and preserve source revision in each filename.
