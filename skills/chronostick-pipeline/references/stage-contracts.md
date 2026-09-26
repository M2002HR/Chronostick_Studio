# Stage contracts

Allowed stage states: `missing`, `draft`, `needs_review`, `approved`, `rejected`, `blocked`, `superseded`.

| Stage | Skill | Requires | Required outputs before approval |
| --- | --- | --- | --- |
| 01 intake/script | `chronostick-script` | title, source text, target language | `source/intake.json`, source copy, narration, script analysis |
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
- Changed timestamps invalidate shot timing, prompts, and jobs but not necessarily approved visual identities.
- Changed reference order invalidates prompt `<Picture N>` mapping and all affected jobs.
- Changed clip prompt, reference, generation settings, or seed requires a new immutable render revision.
- Replacement of one approved clip invalidates only final selection and downstream masters, not unrelated clips.

## State record

Every stage entry records `status`, `inputs`, `outputs`, `validated_at`, `approved_at`, `approved_by`, `decision_notes`, and `next_action`. Use `null` for unknown values. Do not fabricate names or approvals.
