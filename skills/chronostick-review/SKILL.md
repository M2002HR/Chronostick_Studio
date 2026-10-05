---
name: chronostick-review
description: Perform frame, motion, continuity, audio, and technical QC on ChronoStick renders; classify failures and prepare only necessary immutable replacements. Use after generation and before final clip selection.
---

# Chronostick Review

Review the actual video with sound and representative frames around every cut. A successful job is only a candidate render.

`scripts/prepare-short-review.py EPISODE --clip clip-NN --media RENDER --revision rNNN`
archives all actual editorial frames, dense phone-size sheets, planned cut
inspection points, stream probes and an extracted actual audio/waveform.
It refuses existing evidence revisions and makes no creative/audio decision.

For reference-first Shorts, verify each 4–7-second editorial take against its own timing-map interval and planned cut count, not a fixed five-second/eight-shot quota. Check any raw terminal hold and immutable normalization before selection. Review all actual generated cuts, audio and accepted-voice sync. Source-video sketch review never certifies a produced clip.

Run `scripts/audit-short-render-timing.py EPISODE --revision rNNN` on an unused
audit revision. It compares job JSON to executed requests and compiled H3
frame counts/steps/seed, probes every raw/editorial frame PTS at the approved
fps, checks the exact editorial frame count and raw-tail trim, and verifies
decoded raw-prefix correspondence despite lossy normalization. Missing outputs
remain pending. Millisecond MP4 endpoint rounding is reported separately from
frame timing; never stretch the accepted voice to match a container duration.

A technical timing pass does not establish cut compliance. Record actual cut
start frames, match their visible story beats to the planned shots, and report
missing beats and frame/time drift. Inspect every raw-tail frame as well: if a
required final shot starts after the editorial endpoint, trimming discards
story, so revise the take instead of calling that section a resolved hold.
Keep an explicitly accepted actual-picture variant scoped to that clip and
retain its observed timing differences in the review record.

## Per-clip checks

- story phase and chronology match the narration window
- whole frame remains in the approved stick-world style
- compare every shot with its assigned approved scene anchor, including background, hands, animals, vehicles, sky, water, and prop inserts; even one brief photographic or mixed-style frame fails the style gate
- exact recurring identity, costume, count, placement, prop state, and emotion
- readable action, controlled physics, intended camera, rapid but comprehensible cuts
- semantic clarity at phone size: identify visible cause, action, and result without relying on narration to repair a misleading image; reject repeated crops or an ambiguous symbol even when style and identity pass
- no sheet panels, clones, anatomical failures, generated labels, captions, or logos
- synchronized natural SFX; no melody, beat, tonal ambience, speech, narration, singing, or vocal reactions
- correct resolution/frame rate, valid audio/video streams, editorial duration, stable final frame

## Rapid-cut and directing audit

- Build a dense contact sheet or inspect representative frames immediately before and after every planned cut. Count materially distinct shot states against the approved profile-sized plan; the legacy rapid profile requires eight shots, while reference-first dynamic clips use their individually reviewed shot counts.
- At each cut, audit the planned visible inventory and inherited state against actual frames: subject count, identity cues, hat/uniform, left/right placement, prop ownership and shape, environment geometry, light direction, and event phase. Record the first offending frame and the reference that should have controlled it.
- Do not accept a long take, whip pan, speed ramp, zoom blur, or morph as a substitute for editing. The pace must come from discrete readable compositions while motion inside each shot remains controlled.
- Confirm every cut contributes new story information and the clip still reads as setup–escalation–payoff. Flag repetitive medium coverage, arbitrary camera moves, weak visual hierarchy, flat lighting, or technically correct but uncreative direction.
- Compare the new attempt to the previous revision on separate axes: style purity, identity/physical logic, semantic clarity, cut rhythm, and audio. If style improves while story logic worsens, carry forward the stronger story coverage and strengthen its reference; do not accept a regression merely because the style improved.
- Review the intended camera height, lens feeling, subject scale, depth layers, light direction, palette, negative space, and final resolved hold—not only anatomy and continuity.

## Historical identity audit

For every named real person, compare multiple frames to the approved portrait-grounded identity and scene anchors. Check the locked silhouette, hair, facial hair, costume, proportions, and signature prop. Also compare recurring people against one another: reject averaged faces, swapped cues, duplication, identity morphing, or a generic stick figure that is no longer recognizable without a label.

Record timecodes and evidence in `renders/review-rNNN.md`. Decisions are `approved`, `retry`, `revise_prompt`, `revise_reference`, or `reject`; never infer approval.

## Replacement policy

- Aim for a convincingly usable result, not perfect obedience to every generated micro-detail. The user's approximate 95% quality target is a practical editorial judgment, not a measured score. Accept small cut drift, absorbed inserts or a brief non-disruptive detail when core story beats, identity, style, chronology and voice sync remain clear. Record the actual variant and its limitations. Do not retry solely to reach an ideal shot count or remove a tiny cosmetic defect. Missing essential meaning, obvious anatomy/identity failures, wrong chronology, significant timing mismatch and forbidden music still fail. Stop refinement once the take is usable; if a repair is already running, review it and select the stronger usable take without starting further cosmetic retries.
- Isolated stochastic defect with a sound specification: keep the prompt/reference contract, use a new explicit fixed seed, and advance output revision.
- Specification defect: revise the prompt or reference first, revalidate all mappings, use a new seed, and advance revision.
- If a required shot has no visual authority in its assigned anchor, classify it `revise_reference` or change the shot. Adding longer negative wording alone does not repair missing reference coverage.
- Chronology/continuity defect: correct the state ledger and every downstream affected prompt/job, not only the visible symptom.
- Music or speech: reject; stronger prompt wording may reduce recurrence but human audio review remains mandatory.
- A job's `music:false` setting and no-music prompt are constraints, not proof that music is absent. A reported audible music event fails review until a human listening check confirms a clean replacement or a separately reviewed isolated-SFX edit.

Keep supplementary machine listening separate from personal audition and user
listening. For a generated-media audit, do not feed the intended prompt/cut
timestamps as observations: use `scripts/ajil-review-reference.py --media-only`
with neutral actual-media questions. A provider can otherwise repeat the
planned cuts verbatim despite missing cuts visible in the real frames. Archive
that discrepancy and trust actual frames/user listening over its assertions.

Create replacement jobs under `automation/retries/` and run only the affected clips after preflight and explicit authorization. Keep prior outputs immutable.

## Approval gate

Stage exactly one reviewed editorial video for every clip number under `renders/final-selected/`. Verify no duplicate/missing numbers and preserve source revision in each filename.
