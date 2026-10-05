# Long-form episode artifact contract

Use `episodes/NNN-slug/` and stable text filenames. Revision generated media with `-rNNN`; never overwrite. `source/source-en.md` (or another clearly named original) is the supplied material, preserved verbatim. A reference video's transcript is stored or linked separately as *example material*, never merged into the verified source.

```text
README.md                         honest current status and next gate
pipeline-state.json               per-stage status and actual approvals
source/intake.json                 original title/source provenance and desired format
source/claims.json                 claim-to-evidence ledger
source/research-notes.md           citations, uncertainties, map/portrait provenance
source/research-waiver.json         explicit episode-specific user decision if Stage 01 research is skipped
source/reference-video/manifest.json  supplied video/transcript/frame inventory and provenance, when present
source/reference-video/           unchanged supplied video, transcript and frames, when present
source/reference-video/intake-review.md  first joint video/transcript review and evidence gaps
script/story-architecture.md      chapter promise, questions, reveal, payoff
script/narration-es.md             accepted/draft Spanish spoken text
script/voiceover-google-vids-es.md optional tagged copy for Vids, only when used
script/voiceover-google-vids-scenes/scene-NN.txt  ordered per-scene paste inputs under Vids' character limit
script/voice-direction-notes.md    optional tag tests, scene order and voice review
script/fidelity-ledger.json        supplied-claim to Spanish passage mapping
audio/                              immutable accepted voice or location manifest
timestamps/word-timestamps-source.csv  exact supplied timings
timestamps/timing-map.json         derived words, cues, chapters, five-second slots
plan/visual-direction.md           aesthetic and editorial grammar
plan/reference-video-analysis.md   source-moment to adapted-direction trace, when example material exists
plan/shot-plan.md                  exact local/global timed shots
plan/story-state-ledger.json       forward chronology/identity/object state
plan/reference-manifest.json       required and selected anchors/shot coverage
plan/map-manifest.json             dated source, scale, geometry, symbols, labels
plan/text-events.json              exact in-engine readable-text exceptions
plan/animatic-review.md            whole-video pacing test
plan/pilot-review.md               landscape H3 and draft/final test results
prompts/clip-NNN.md                generator text only; NNN supports >99 slots
automation/jobs/clip-NNN.json      live-service request JSON
automation/job-plan.json           ordered per-slot references, project seed, revision
automation/batch-settings.json    execution policy
renders/raw/                      immutable engine output
renders/editorial/                exact five-second normalized clips
renders/final-selected/           one reviewed take per slot
renders/review-rNNN.md            timecoded picture/audio decisions
final/                            immutable picture/SFX and distribution masters
postproduction/edit.json          local finishing configuration and exact input hashes
postproduction/exports/rNNN/      captions, derived word map, stems, loudness and QC provenance
delivery/youtube/                 metadata, thumbnail prompt/revisions, chapters
```

The episode manifest must name its project profile, language, actual source and audio status, planned and accepted duration, style authority, inherited identities, last reviewed stage, active revision, exact missing artifacts and next action. A status of `approved` requires a recorded reviewer/decision and a real artifact; an automated validation pass alone is `validated`.

Reference-video materials follow [`reference-video-workflow.md`](reference-video-workflow.md). Their manifest and analysis are planning/evidence artifacts, never image or video generator prompts. The optional Google Vids direction step is represented by `02a` in `pipeline-state.json`: `skipped` until selected, then `draft`/`needs_review`/`approved` as the actual tagged script and review progress. Stage 03 cannot rely on a draft or rejected tagged script.
When a Stage `02a` tagged script exists, validation removes bracket tags and requires the remaining spoken text to match `script/narration-es.md` exactly apart from whitespace. For long narration, the ordered scene files must reconstruct the tagged master and each stay within Vids' 2,500-character input limit.

The structured ledgers may be expanded as production teaches us more. Do not allow a new field to obscure the minimum contract: traceable source, exact timing, identity and story state, map/text content, ordered reference-to-prompt mapping, revisioned output and explicit review. Keep generator-facing files free of YAML, citations, explanations and approval notes.
