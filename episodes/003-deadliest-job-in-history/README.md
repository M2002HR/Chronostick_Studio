# Episode 003 — The Deadliest Job in History?

## Status

- lifecycle: production
- current pipeline stage: `09-assembly-upscale`
- source: user-supplied English text preserved verbatim
- source verification: complete; qualifications recorded in `source/research-notes.md`
- Spanish narration: approved with the minimal subscription CTA
- voice: revised delivery approved externally; audio file not supplied or archived
- timestamps: approved; 119 spoken tokens from 00:00.320 through 00:45.640
- shot plan: approved by user; 72 shots across nine generated clips
- references: four portrait-grounded identity anchors and six scene anchors generated, reviewed, selected, and hash-locked
- final prompts: nine rapid-cut H3 prompts validated and approved under the user's unattended-production authorization
- generation jobs: nine deterministic 16-step jobs validated by the live-service dry run
- renders: all nine r001 editorial clips completed; user selected all nine for assembly
- assembly: 45-second concat and 0.640-second resolved-frame extension completed
- upscale: 1080×1920 framewise pass completed; 1095/1095 frames, technical probe and contact-sheet check passed
- YouTube package: updated 2026-10-03 with a 30-character Spanish hook title, two short alternatives, casual SEO description, grouped hashtags and smaller description subset, three pinned-comment candidates, five viewer-comment examples, and proposed revisioned upload filename; operator settings and upload checklist preserved
- thumbnail: `4 PRESIDENTES / ASESINADOS` r001 generated at 2160×3840; assistant QC passed, user approval pending
- final video: user supplied `/home/mhr/Downloads/historia_03.mp4`; requested 1.2× distribution export saved under `final/` at 1080×1920/30 fps, 38.133 seconds, with pitch-preserving audio and retimed embedded Spanish captions; technical QC passed, no new content approval recorded

## Production contract

- target: 40–60-second vertical YouTube Short; preferred duration 52 seconds
- production profile: `h3-short-5s-16step-rapid-cut`, an Episode 003 high-density variant with an explicit 16-step override
- generation engine: MiniMax H3 `h3_ref2va`, 5-second editorial clips, 16 sampling steps
- generation blocks: 9 × 5.000-second generated clips plus a 0.640-second final-frame freeze extension
- narration language: Spanish
- production language: English
- CTA: `¿Te sorprendió? Suscríbete.`
- inherited style: approved detailed cinematic ChronoStick stick world
- edit contract: exactly eight hard-cut shots per generated clip; one simple action and at most one camera move per shot
- identity contract: four reusable symbolic stick-figure anchors must keep Lincoln, Garfield, McKinley, and Kennedy recognizable without labels
- content constraint: preserve every supplied narrative claim and beat without additions or omissions, except the approved 45 / 8.9% correction and minimal subscription CTA

## Tail extension contract

- default ceiling result: 10 five-second clips
- approved generated count: 9 five-second clips, totaling 45.000 seconds
- narration end: 45.640 seconds
- post-concat extension: clone Clip 09's final frame for exactly 0.640 seconds
- audio during extension: generated SFX pad to silence; external narration continues
- execution order: select and concat 9 clips, run `scripts/extend-last-frame.sh`, then upscale the extended revision
- Clip 09 requirement: all motion and camera movement settle before 45.000 seconds on a resolved freeze-safe frame

## Artifact inventory

- verbatim supplied source: `source/source-en.md`
- intake record: `source/intake.json`
- factual verification and qualifications: `source/research-notes.md`
- approved Spanish narration: `script/narration-es.md`
- script analysis: `script/script-analysis.json`
- pipeline handoff state: `pipeline-state.json`
- preserved timing source: `timestamps/word-timestamps-source.csv`
- current timing source: `timestamps/word-timestamps-source.csv`
- approved timing validation: `timestamps/validation-report.md`
- approved clip-aligned timing map: `timestamps/timing-map.json`
- superseded pre-CTA timing set: `timestamps/archive/pre-cta/`
- visual identity research: `source/visual-research-notes.md`
- review-ready directed plan: `plan/shot-plan.md`
- review-ready continuity ledger: `plan/story-state-ledger.json`
- review-ready reference requirements: `plan/reference-manifest.json`
- completed renders and selected set: `renders/editorial/`, `renders/final-selected/`, and `renders/review-r001.md`
- assembly outputs: `final/episode-003-deadliest-job-in-history-concat-r001.mp4` and `final/episode-003-deadliest-job-in-history-tail-extended-r001.mp4`
- YouTube package: `delivery/youtube/thumbnail-prompt-r001.md`, `delivery/youtube/metadata.json`, and `delivery/youtube/metadata.md`
- generated thumbnail: `delivery/youtube/thumbnail-episode-003-r001.png` with source, provenance, and review record beside it
- user-requested final distribution export: `final/presidentes-eeuu-asesinados-historia-animada-es-003-r001.mp4` with adjacent `.speedup.json` provenance; original external finish remains in Downloads

## Next action

Review the generated thumbnail r001 and the user-requested 1.2× distribution export before choosing upload settings or publishing.
