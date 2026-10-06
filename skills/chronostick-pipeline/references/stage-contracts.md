# Stage contracts

New reference-first Shorts use semantic schema v2 and the fifteen stages in `docs/reference-first-shorts.md`. `validated` denotes a technical check; creative decisions require recorded review, and production references require user-approved scenario and storyboard. Voice and reference branches may progress independently after that gate. When Google Vids is selected, the `voice` branch includes a required `chronostick-voice-direction` substage with tagged script, notes, validation and source/tagged hashes; a prepared paste copy is not an accepted voice. The numbered table below is the preserved legacy route, not the new default.

The tagged-copy preparation runs immediately after every script creation/revision,
including drafts, before storyboard review and without a separate request. Deliver
clean/tagged versions together with many fitting emotion/style cues throughout.
Record early preparation under `voice`; its audio-acceptance status remains missing.

For this route, both reference design/review and timed shot direction must inspect the actual selected storyboard pages. Every reference entry and directed shot records `storyboard_panel_ids`; omitted/combined/retimed panels require a separate rationale, and material creative changes reopen the relevant review. Sketches control composition/action while locked production style and researched identities control rendering/appearance. They are never H3 reference images.

Allowed legacy stage states: `missing`, `draft`, `needs_review`, `approved`, `rejected`, `blocked`, `superseded`.

| Stage | Skill | Requires | Required outputs before approval |
| --- | --- | --- | --- |
| 01 intake/script | `chronostick-script` | title, source text, target language | `source/intake.json`, source copy, narration, script analysis |
| 01a voice direction (immediate post-script preparation) | `chronostick-voice-direction` | clean narration draft/revision and Google Vids as voice provider | densely emotional tagged script, notes, text validation and hashes delivered with clean narration; final delivery gate remains actual audio acceptance |
| 02 timestamps | `chronostick-timestamps` | approved narration, word timestamps from approved voice | preserved source CSV, optional normalized CSV, `timing-map.json` |
| 03 direction | `chronostick-shot-plan` | approved timing map | shot plan, story-state ledger, reference manifest |
| 04 references | `chronostick-references` | approved reference manifest and style authority | paste-ready image prompts, immutable full-frame assets, review status |
| 05 clip prompts | `chronostick-clip-prompts` | approved plan and references | one pure generator prompt per slot |
| 06 jobs | `chronostick-generation-jobs` | approved prompts and reference paths | one job JSON per slot, batch settings, unique fixed seeds |
| 07 generation | `chronostick-batch` | complete preflight and explicit run instruction | renders, sidecars, batch/run reports |
| 08 review | `chronostick-review` | terminal batch | per-clip decisions and exactly one approved take per slot |
| 09 assembly/upscale | `chronostick-finish` | selected complete sequence | concat master, 1080×1920 upscale, technical QC |
| 10 YouTube package | `chronostick-youtube` | approved final content | thumbnail prompt/asset decision, metadata, upload checklist, closeout |

## Dependency rules

- Later drafts may be prepared in parallel only when they do not pretend an upstream draft is approved.
- A changed approved narration invalidates timestamps and every downstream timing artifact.
- A changed voice-direction tag requires a new voice audition; a changed accepted voice invalidates timestamps and downstream timing artifacts.
- Changed timestamps invalidate shot timing, prompts, and jobs but not necessarily approved visual identities.
- Changed reference order invalidates prompt `<Picture N>` mapping and all affected jobs.
- Changed clip prompt, reference, generation settings, or seed requires a new immutable render revision.
- Replacement of one approved clip invalidates only final selection and downstream masters, not unrelated clips.

## State record

Every stage entry records `status`, `inputs`, `outputs`, `validated_at`, `approved_at`, `approved_by`, `decision_notes`, and `next_action`. Use `null` for unknown values. Do not fabricate names or approvals.
