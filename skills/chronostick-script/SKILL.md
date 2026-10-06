---
name: chronostick-script
description: Adapt a reviewed reference-video story or supplied source into an original, high-retention Spanish narration and scenario for a profile-sized vertical Short in the requested target language. Use at episode intake or when an unapproved script needs revision.
---

# Chronostick Script

## Inputs

Require a title and preserved source text. For reference-first intake, also require actual-video analysis and its Ajil transcript; use the source architecture closely while writing original Spanish. Resolve from the episode manifest when available: target language, audience, factual vs fictional mode, desired duration, CTA policy, pronunciation notes, and whether the user explicitly requested fact-checking. If target language is omitted, use the project default and record the assumption.

Preserve the source verbatim under `source/`; never replace it with the rewrite.

For supplied-source adaptation, default to `fact_check_requested: false`. Preserve its claims, numbers, dates, causal links and payoff; do not research, correct, omit or substitute content without the user's explicit request. Making a video, translating it or fitting a shorter duration does not request fact-checking. Change wording and pacing while preserving meaning. Track supplied claims as source claims in internal provenance, without representing them as independently verified. Prior unsolicited research is not permission to alter the script. If verification is explicitly requested, present any proposed corrections separately before changing the chosen content.

## Rewrite

- For new reference-first Shorts target 20–30 seconds, preferably near 30; record the selected duration before writing. Existing legacy episodes retain their 40–60-second contract. Compress to hook, causal escalation and payoff without dropping factual qualifications.
- Open with the strongest source-grounded image, contradiction, danger, question, or consequence in the first sentence. Do not start with greetings or setup.
- Use surprise, vivid action and occasional situational wit when supported by the source; keep suffering and victims outside the joke.
- Establish a clear open loop, then deliver a new visual/narrative beat every few seconds.
- Use short spoken sentences, concrete verbs, escalating stakes, clean chronology, and one payoff.
- Remove filler and repeated context without removing user-retained claims or changing the source's degree of certainty.
- Preserve qualifications already in the source. Research historical claims only when the user explicitly requests verification; store citations outside the narration.
- Write natural speech in the target language, not a literal translation.
- End with payoff first, then always add a tiny spoken subscribe CTA by default: Spanish `Suscríbete.` or the equally brief equivalent in the target language. Say only "subscribe"—no like/share/bell request, channel pitch or extra sentence. Fit its delivery to the scene and include it in the duration budget. Omit or change it only when the user explicitly overrides this default; record that choice. This is narration, not permission for in-picture text or a subscribe-button scene.
- Create original phrasing and directing opportunities. Do not mimic a named living creator or copy source wording unnecessarily.

Estimate duration using the target language and intended energetic delivery. Word count is a diagnostic, not the timing source of truth.

## Outputs

- `source/intake.json`: title, source path/hash, language, audience, duration range, factual mode, assumptions.
- `script/narration-<lang>.md`: narration only.
- `script/script-analysis.json`: estimated duration, word count, hook, open loop, beat list, payoff, CTA, `fact_check_requested`, source-claim provenance, and pronunciation notes.
- For reference-first, also write `plan/scenario.md` with adaptation, roles and engine feasibility; update semantic `scenario-script` to `needs_review`. Legacy route uses stage 01. Only a real review may mark either approved.
- Immediately after writing or revising the clean script, use `chronostick-voice-direction` to also deliver `script/voiceover-google-vids-<lang>.md`, notes and text validation with many fitting emotion/style tags throughout. This default includes drafts: do not wait for storyboard review or another voice-formatting request. Only an explicit user/provider override skips Google Vids preparation. Changes to clean wording invalidate the old tagged copy and require regenerating it before handoff.

## Gate

Immediately after script creation, when Google Vids is the selected voice provider, hand the clean text to
`chronostick-voice-direction` before voice generation. Deliver the separately
tagged paste input and validation report as part of the workflow, using the
registered account tags, many emotional cues and fast expressive Short performance. Do not
silently hand off only untagged narration. Keep actual voice acceptance separate.

Reject a script that is slow before the hook, chronologically confusing, outside its selected profile duration without a documented change, deceptive, difficult to say aloud, visually repetitive, or factually stronger than its source.
