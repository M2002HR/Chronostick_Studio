---
name: chronostick-script
description: Convert a supplied title and source text into an original, high-retention narration for a 40–60 second vertical Short in the requested target language. Use at episode intake or when an unapproved script needs revision.
---

# Chronostick Script

## Inputs

Require a title and source text. Resolve from the episode manifest when available: target language, audience, factual vs fictional mode, desired duration, CTA policy, pronunciation notes, and cited sources. If target language is omitted, use the project default and record the assumption.

Preserve the source verbatim under `source/`; never replace it with the rewrite.

## Rewrite

- Target 40–60 seconds; default to roughly 50–55 seconds unless the source demands otherwise.
- Open with the strongest truthful image, contradiction, danger, question, or consequence in the first sentence. Do not start with greetings or setup.
- Establish a clear open loop, then deliver a new visual/narrative beat every few seconds.
- Use short spoken sentences, concrete verbs, escalating stakes, clean chronology, and one payoff.
- Remove filler, repeated context, generic superlatives, and unsupported certainty.
- Preserve factual qualifications. Research unstable or high-stakes claims when research is in scope; store citations outside the narration.
- Write natural speech in the target language, not a literal translation.
- End with payoff first; add a concise CTA only when the episode contract requests one.
- Create original phrasing and directing opportunities. Do not mimic a named living creator or copy source wording unnecessarily.

Estimate duration using the target language and intended energetic delivery. Word count is a diagnostic, not the timing source of truth.

## Outputs

- `source/intake.json`: title, source path/hash, language, audience, duration range, factual mode, assumptions.
- `script/narration-<lang>.md`: narration only.
- `script/script-analysis.json`: estimated duration, word count, hook, open loop, beat list, payoff, CTA, factual claims needing verification, and pronunciation notes.
- update stage 01 to `needs_review`; only a real review may mark it `approved`.

## Gate

Reject a script that is slow before the hook, chronologically confusing, over 60 seconds without approval, deceptive, difficult to say aloud, visually repetitive, or factually stronger than its source.
