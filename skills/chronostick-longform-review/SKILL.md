---
name: chronostick-longform-review
description: Review actual long-form ChronoStick H3 clips and chapter assemblies for historical meaning, stick-world style, identity, maps, in-engine text, timing, sound, and continuity; prepare only necessary immutable replacements.
---

# ChronoStick long-form review

A successful H3 job is a candidate, not an approval. Compare the actual raw and editorial video against accepted voice timing, exact prompt, approved reference, claim source, story-state ledger and adjoining slots. Inspect whole motion and listen with sound. Sample around every planned cut, and inspect **every frame** containing a map or exact generated writing. Log first/last bad timecodes and whether the defect is factual, reference, prompt, random sampling, normalization or audio.

Check full-frame illustrated style, recurring portrait-grounded identity, anonymous-role and animal stability, costume/prop counts, physical trajectory, screen direction, period material, chapter pace, story phase, resolved end, audio stream, correct 1024×576 raw and five-second editorial output. Evaluate legibility at desktop and phone size. No music, tonal bed, speech, generated narration or lip sync is acceptable even if `music:false` was set. Every map border, ship position, status color, route and label must remain correct throughout the clip. Every approved exact word/date/number must retain spelling, order, accents, placement and readable hold; reject extra text and accidental captions.

Review per chapter, then watch all chapter seams and the entire voice-led rough cut. A technically correct collection can still be repetitive, unclear, emotionally flat or misleading. Record decisions in `renders/review-rNNN.md` and the selection manifest: `approved`, `retry`, `revise_prompt`, `revise_reference`, or `reject`. A human review decision is distinct from automated checks.

For an isolated random defect, preserve the sound specification and retry only that slot with a recorded new seed/revision. For an unsupported view, text, map or identity defect, correct the plan/reference/prompt and invalidate affected downstream jobs. For chronology defects, fix all impacted later slots. Never overwrite media or silently switch to editorial typography when the selected in-engine text fails. Only copy one approved editorial render per slot to `renders/final-selected/`, preserving its revision provenance.
