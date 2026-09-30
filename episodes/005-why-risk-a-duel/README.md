# Episode 005 — Why Risk a Duel?

## Status

- lifecycle: picture/SFX master complete and technically checked; distribution finishing and channel decisions pending
- source: user-supplied English text captured verbatim; independent historical verification intentionally not performed at the user's request
- narration: Spanish, 127 words; treated as approved because the user generated and supplied its voice timestamps
- voice: external; supplied timing ends at 52.520 seconds
- timestamps: approved; the user accepted the 52.520-second voice and 55.000-second picture timeline
- shot plan: approved; 11 clips and 88 hard-cut shots
- references: approved; one Andrew Jackson identity and nine generation-safe scene anchors reviewed at full and phone size
- final prompts: approved; 11 pure H3 prompts with eight materially distinct shots each
- generation jobs: r001/r002 completed but rejected after user review; corrected r003/r004 contain 22 new unique fixed seeds at 14 steps
- preflight: repository validation and both 11/11 live-service dry-runs passed
- renders: r001 and r002 were rejected for music, short duel distance, and incorrect muzzle direction; corrected r003 and r004 batches both succeeded, and the user placed one selected clip in each of the 11 timeline slots
- final video: `final/episode-005-why-risk-a-duel-r001.mp4` assembles the 11 user-selected clips; `final/episode-005-why-risk-a-duel-picture-sfx-1080x1920-r001.mp4` is the completed 55-second, 1080×1920, 24-fps picture/SFX master enhanced frame by frame with `RealESRGAN_x4plus_anime_6B`; technical checks passed, but neither picture master nor distribution master has a final editorial approval
- thumbnail: `delivery/youtube/thumbnail-episode-005-r001.png` generated with integrated Spanish headline and passed assistant full-size/phone-size visual QC; channel approval pending
- YouTube metadata: primary and alternative titles, Spanish description, thumbnail provenance, and upload checklist prepared under `delivery/youtube/`; upload and publication not authorized
- distribution master: unavailable; Spanish voice is external, and the finished narrated/captioned export has not been supplied or reviewed

## Production contract

- target: 55.000-second vertical Short, as approved for the 11 five-second clip timeline
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
- `automation/retries/r003-r004-queue-state.json`: completed corrected two-seed batch state
- `final/episode-005-why-risk-a-duel-picture-sfx-1080x1920-r001.framewise-upscale.json`: immutable model, settings, timing, resource, and stream provenance
- `delivery/youtube/thumbnail-prompt-r001.md`: selected thumbnail direction and approved generation prompt
- `delivery/youtube/thumbnail-episode-005-r001-source.png` and `thumbnail-episode-005-r001.png`: generated source and 2160×3840 delivery image
- `delivery/youtube/thumbnail-provenance-r001.json` and `thumbnail-review-r001.md`: image hashes and assistant review
- `delivery/youtube/metadata.json` and `metadata.md`: provisional Spanish upload package

## Next action

Finish and review the Spanish-voice/caption distribution export against the 55-second picture timeline; get editorial/channel approval of the picture, thumbnail, and required YouTube operator settings. Only then upload or publish. The current picture/SFX master must not be mistaken for that distribution export.
