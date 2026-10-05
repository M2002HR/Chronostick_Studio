---
name: chronostick-longform-script
description: Turn a supplied historical title and full source into a faithful, sourced, compelling Spanish narration for a 10–15 minute ChronoStick video. Use at long-form intake or when the script needs revision, before user voice and word timing.
---

# ChronoStick long-form script

Read `AGENTS.md`, `docs/longform/workflow.md`, the original historical source if supplied, the Stage 00 reference-video intake review and transcript when present, and existing research. Preserve the user's source verbatim. If the example transcript is the only story input, use it to inventory candidate claims and story beats, then verify claims independently before writing accepted Spanish narration; do not promote the transcript to historical evidence. Search reliable historical sources for disputed, niche, causal, numerical, map and identity claims; record citations and uncertainty in `source/`, never in prompts. A noisy transcript is not an authority. An explicit user instruction may waive independent verification for a named episode: record the decision as `source/research-waiver.json`, mark Stage 01 `skipped`, and label the resulting script a source-assumption draft. Do not claim verification or erase earlier research.

## Before Spanish prose

Build `source/claims.json`: one record per material assertion with source span, supporting citation, status (`supported`, `qualified`, `contested`, `unverified`), and required wording. Separate actual quotations from invented dialogue. Flag any omission or proposed addition. Build `script/story-architecture.md`: title/thumbnail promise, central question, chapter questions, first proof of the promise, escalation, reveal, human consequence, final answer and the default tiny subscribe CTA (`Suscríbete.` in Spanish), with delivery matching the ending. Say only subscribe; an explicit user override may omit/change it. A ten-minute target does not justify invented facts or padded repetition; state if the supplied material is insufficient.

## Spanish narration

Write original, natural spoken Spanish with accurate names, diacritics, dates, numbers, relationships and qualifications. Preserve the supplied content and causal meaning; rearrange only to improve comprehension and retention. The opening needs a concrete hook, a quick confirmation that the video will deliver the title/thumbnail promise, and an *earned* reason to keep watching. Give each chapter a new question or change of stakes. Make the narration exciting and inventive through sharp contrasts, surprising but true turns, concrete images and occasional situational humor. Vary sentence length and emotional intensity; make geography and succession easy to follow without turning victims into punchlines. Do not import music, jokes, artwork, or dramatized conversations from a reference video. Do not frame colonial self-justification as neutral fact. Put proposed new material outside the narration until sourced and accepted.

Maintain `script/fidelity-ledger.json` mapping every source claim to the Spanish passage or an explained omission. Audit the reverse direction: each Spanish factual claim must map to the supplied text or an approved, cited addition. Read aloud for rhythm, pronunciation, referent clarity, and the actual title payoff. Estimate duration only until the user's accepted voice exists. Save the review decision in the manifest; no self-declared script approval.
