# 006 — The Shortest War EVER

## Current production state

Spanish narration is accepted and unchanged: `audio/narration-es-google-vids-r001.mp4`, 651.389 seconds. Actual accepted timing covers 131 five-second picture slots, 655 seconds. All production picture remains MiniMax H3, including maps, clocks and approved exact text; still animatics are planning guides only.

The user explicitly requested a **full four-step Lightning concept preview**, followed by review and any needed corrections before a later **12-step production pass**. The preview keeps the final 1024×576 landscape resolution, 24 fps, ordered references and fixed per-slot seeds. Four-step results are not final-quality approvals. No automatic assembly, upscale or 12-step rerun is configured.

The revised plan uses **57 reviewed full-frame anchors and 215 shots** across 131 clips. Four harbour references now have exactly five British navy ships plus Glasgow; thirteen new references add trade cargo, market detail, messages, shore cannon, afloat/wreck Glasgow, refuge approach, civilian aftermath, shoe inserts and resolved map states. The busiest anchor is used six times, with at most two consecutive slots; each complete minute has seven to twelve distinct anchors. Ordinary scenes use two simple shots per five seconds; geography, exact clock text and quiet human-cost moments remain continuous. See `plan/visual-variety-audit.json` and `plan/preview-revision-review.md`.

`plan/beat-cards.tsv`, `plan/clip-direction.json`, `plan/shot-plan.md` and the state/map/text ledgers agree with 131 pure prompts. Revised 12-step jobs are revision004, prepared but unlaunched. The frozen preview package is `automation/batches/preview-4step-r001/`; every one of131 children passed a complete live-service dry-run without warnings. `plan/animatic-r006.mp4` is the655-second voice-led planning preview. Earlier animatics and rejected six-ship anchors are preserved.

The supplied English example and transcript remain under `source/reference-video/`. Independent historical verification was explicitly waived for this source-assumption episode; see `source/research-waiver.json`. No new independent verification is claimed.

The earlier five-job12-step pilot batch `a8fd33bf-eb25-4f44-b36f-b18b6c8e0a7b` remains preserved and unapproved. Its documented extra people, wrong ship counts, premature smoke and token-motion contradiction have been addressed in references and prompts; actual repair requires inspection of the new generated videos.

## Runtime and next action

Read `automation/batches/preview-4step-r001/manifest.json` for the current persisted batch ID and status, and `automation/batches/preview-4step-r001/start-verification.json` once processing starts. The API service owns queued work independently of the chat. The detached CLI watcher logs to `automation/batches/preview-4step-r001/watcher.log`.

After the preview completes, review all131 editorial outputs under `renders/preview-4step/editorial/`, record accepted/failed slots and correct only necessary failures in immutable revisions. A later12-step pass follows that review and user decision. No final clip is selected yet. Work is checkpointed locally in Git; video media stays local and ignored by Git.
