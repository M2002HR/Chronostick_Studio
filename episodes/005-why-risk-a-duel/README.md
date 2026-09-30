# Episode 005 — Why Risk a Duel?

## Status

- lifecycle: corrected two-seed batch generation running
- source: user-supplied English text captured verbatim; independent historical verification intentionally not performed at the user's request
- narration: Spanish, 127 words; treated as approved because the user generated and supplied its voice timestamps
- voice: external; supplied timing ends at 52.520 seconds
- timestamps: approved; the user accepted the 52.520-second voice and 55.000-second picture timeline
- shot plan: approved; 11 clips and 88 hard-cut shots
- references: approved; one Andrew Jackson identity and nine generation-safe scene anchors reviewed at full and phone size
- final prompts: approved; 11 pure H3 prompts with eight materially distinct shots each
- generation jobs: r001/r002 completed but rejected after user review; corrected r003/r004 contain 22 new unique fixed seeds at 14 steps
- preflight: repository validation and both 11/11 live-service dry-runs passed
- renders: r001 and r002 completed but were rejected for music, short duel distance, and incorrect muzzle direction; corrected `r003` is running as batch `f19517e9-d5b3-4f08-b5dd-5c7107f5271a`, with `r004` queued behind it
- final video: not produced

## Production contract

- target: 40–49-second vertical Short
- production profile: `h3-short-5s-14step-rapid-cut-55s`
- generation blocks: 11 × 5 seconds = 55.000 seconds
- narration language: Spanish
- production language: English
- pacing: rapid chronological storytelling with frequent simple visual changes and readable actions
- CTA: end the narration with `¡Suscríbete!`
- inherited style: `assets/styles/style-detailed-cinematic-stick-history-r001.png`
- world and characters: immutable approved references under `assets/episodes/005-why-risk-a-duel/references/`

## Artifact inventory

- `source/source-en.md`: supplied source preserved verbatim
- `source/intake.json`: intake contract and source hash
- `script/narration-es.md`: Spanish narration draft
- `script/script-analysis.json`: retention, duration, beat, and factual-status analysis
- `timestamps/word-timestamps-source.csv`: 129-row user-supplied timing conversion
- `timestamps/timing-map.json`: 11-slot derivation ending at 55.000 seconds
- `timestamps/validation-report.md`: structural, text-match, and duration review
- `plan/shot-plan.md`: 88-shot rapid-cut direction draft
- `plan/story-state-ledger.json`: clip-boundary continuity and state authority
- `plan/reference-manifest.json`: identity, scene-anchor, reuse, and coverage requirements
- voice audio: external and not present in the repository
- `plan/reference-review.md`: full-resolution and phone-size reference QC
- `prompts/clip-01.md` through `prompts/clip-11.md`: paste-ready H3 prompts
- `automation/variants/r001/jobs/` and `automation/variants/r002/jobs/`: two deterministic 11-job sets
- `automation/retries/r003/jobs/` and `automation/retries/r004/jobs/`: corrected full 11-job sets with absolute audio locks and wide direct-aim duel references
- `renders/review-r001-r002.md`: user-reported failure classification and replacement decision
- `automation/queue-state.json`: live two-seed queue state

## Next action

Run and monitor the persistent two-seed queue, then review all 22 resulting candidates before selecting one render per clip.
