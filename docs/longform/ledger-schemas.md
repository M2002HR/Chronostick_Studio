# Long-form ledger fields

Use UTF-8 JSON, `schema_version: "1.0"`, stable IDs and repository-relative paths. These are minimum records, not an exhaustive schema. Keep actual supplied voice/timestamp files unchanged; derived ledgers are separate. A status of `approved` always includes `approved_by` and a recorded decision.

## Claims and script fidelity

`source/claims.json` has `claims[]` with `id`, `source_span`, `claim`, `kind` (fact, quotation, estimate, allegation, interpretation), `status` (supported, qualified, contested, unverified), `citations[]` (direct URLs and what each supports), `required_qualification`, and `visual_implication`. Exact quotations need the original language and provenance. A reference-video transcript is never a citation by itself.

`script/fidelity-ledger.json` has `mappings[]` with `claim_id`, `source_span`, `spanish_passage`, `treatment` (retained, qualified, omitted, sourced_addition), and `reason`. Audit both directions: no supplied claim silently dropped, no new Spanish claim without an approved source.

## Reference-video evidence and adaptation

When example material exists, `source/reference-video/manifest.json` has `schema_version: "1.0"`, `items[]`, and the user's stated influence goal. Each item has `id`, `kind` (`video`, `transcript`, `frame`, `screenshot`), local `path` or external `url`, `sha256` for a local file, and `timecode` when known; leave unknown fields null rather than estimating them. Preserve supplied local files byte-for-byte. When video and transcript are supplied together, Stage 00 also writes `source/reference-video/intake-review.md` from sampled video frames and time-aligned transcript text, with sampling limits and disputed claims. Stage 04 revisits selected video moments and writes `plan/reference-video-analysis.md`, mapping item IDs and observations to storytelling techniques and original ChronoStick adaptations. The sequence and shot plan identify selected analysis IDs and the concrete adapted directing choice. The prompt describes the approved scene itself, not the example video. See [`reference-video-workflow.md`](reference-video-workflow.md).

## Voice, cues and slots

`timestamps/timing-map.json` has `narration_end` in seconds, `clip_seconds: 5`, `slot_count: ceil(narration_end / 5)`, `slots[]` numbered from 1 with exact numeric `start` and `end`, overlapping word IDs, visual cue IDs and chapter ID, plus `chapters[]` with actual start/end and a semantic promise/payoff. The user-supplied `word,start,end` CSV remains unchanged. The final slot's silent tail is documented rather than filled with an invented event.

## Character, object and scene state

`plan/story-state-ledger.json` has `states[]` indexed by clip/shot with subject ID, phase, inherited state, allowed change, resolved state, count, screen position and travel direction, costume/prop ownership, injury/emotion, light and environment. A recurring subject points to its identity authority and to the next shot inheriting it. Named people use sourced recognizability cues; anonymous roles use a stable designed identity.

`plan/reference-manifest.json` has `assets[]` with stable ID, type (identity, world, animal, vessel, map, text, scene), authority sources, revisioned path, SHA-256, status/reviewer, exact subject inventory, aspect, story phase, and supported shot IDs. `coverage[]` maps every planned shot to approved assets and names unsupported elements. A reference is not approved merely because an image exists.

## Maps and exact in-engine text

`plan/map-manifest.json` has `maps[]` with ID, depicted date/interval, extent, scale, geopolitical status definitions, source URLs, coastline/border authority, palette/legend, route and arrows, allowed labels, zoom/handoff sequence, supported shots and frame-level failure conditions. State uncertainty in disputed borders. Keep geography stable between map shots.

`plan/text-events.json` is `{"schema_version":"1.0","events":[]}` until a specific exception is approved. Each event has `clip` (integer), `exact_text` (Spanish string), `claim_id`, `source` (citation), `onset_seconds`, `hold_until_seconds`, `exit_seconds`, `placement`, `reference_asset`, `status`, `approved_by`, and `failure_conditions`. Times are local to the five-second clip. Only these strings may be readable in H3 output. Even approved exceptions require final-frame review; a status approves the request, not the rendered spelling.

## Preflight, review, selection and finish

`automation/job-plan.json` is `{"schema_version":"1.0","project_seed":123456,"slots":[...]}`. Its `slots[]` contains exactly one ordered entry per five-second slot, each with `number`, `revision`, and `references[]` of one or two existing repository-relative full-frame scene anchor paths. A `seed` override is allowed only when recorded for a targeted retry. The job builder derives unique fixed seeds from the project seed and slot otherwise. See the [operator runbook](operator-runbook.md) for commands.

`automation/preflight.json` records `job_count`, `expected_slot_count`, job/prompt/reference hashes, service capability result, live-service dry-run command/result and `live_dry_run_passed`, estimated GPU time/space, `output_collision_count`, reviewer and `passed`. It does not authorize launch.

`renders/review-rNNN.md` records every clip decision, evidence timecode, image/identity/map/text/audio findings and any retry dependency. `renders/selection-manifest.json` has `selections[]` in slot order with `number`, repository-relative `path`, `sha256`, source revision, `approved_by` and `decision: "approved"`. `final/distribution-review.md` records technical probe, full-playback QC, voice/caption sync, SFX/no-music check, aspect and output hashes. A finished picture/SFX master is not automatically a narrated distribution master.
