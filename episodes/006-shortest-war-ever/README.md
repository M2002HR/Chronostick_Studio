# 006 — The Shortest War EVER

## Current production state

The complete **131-clip twelve-step H3 batch** is running in the persistent background service. Batch ID: `f2ed5f96-6091-458b-bcab-9a2315ccd83c`. All children use12 sampling steps,Lightning disabled,1024×576 landscape,24fps and immutable revision004 output prefixes. The first child was verified running in ComfyUI; no generation success is treated as picture approval.

The user explicitly stopped the four-step preview and requested full12-step production without waiting for preview review. The previous preview batch `019625ab-2084-4483-babb-dc5be22281d7` is terminal: two clips completed; the remaining children were cancelled/interrupted. Its existing media and cancellation evidence remain preserved. It will not resume automatically.

The current frozen package is `automation/batches/production-12step-r004/`. All131 children passed complete live-service dry-run without warnings. The batch was submitted once with a detached CLI watcher. Its ID, all child IDs and actual engine-start evidence are recorded in `automation/run-state.json`, the batch manifest,submission.json andstart-verification.json. Native SFX are retained; automatic concatenation and upscale are disabled.

The accepted Spanish narration remains unchanged at651.389 seconds, with131 five-second picture slots and655 seconds of planned picture. The reviewed plan uses57 full-frame image anchors and215 shots. Four harbour references were corrected and thirteen new references added. Maximum anchor reuse is6, with at most two consecutive identical-reference slots; complete minutes contain7–12 distinct anchors. Ordinary scenes use two simple shots per five seconds; geography, clocks and respectful human-cost passages stay continuous.

`plan/beat-cards.tsv`, `plan/clip-direction.json`, `plan/shot-plan.md`, state/map/text ledgers and131 pure prompts form the current direction. See `plan/preview-revision-review.md` for the repaired count, prefire, token, refuge and damage-state issues. `plan/animatic-r006.mp4` is a655-second still planning guide; all production picture remains H3-generated.

The supplied English example and transcript remain under `source/reference-video/`. Independent verification was explicitly waived for the source-assumption episode; see `source/research-waiver.json`. Earlier pilots, rejected references and planning previews remain preserved. No actual final picture selection is approved yet.

## Monitor and next action

```bash
cd /home/mhr/AI/comfy-video-automation
uv run comfy-video status f2ed5f96-6091-458b-bcab-9a2315ccd83c --batch --watch
```

Ctrl+C closes the watcher display; it does not stop generation. The detached watcher logs to `automation/batches/production-12step-r004/watcher.log`. Closing this chat does not cancel the service batch.

After completion, review all131 editorial candidates under `renders/editorial/` with `clip-NNN-shot-r004` prefixes. Check meaning, identity, motion, continuity, every exact-text/map frame and native audio, then replace only necessary failures in immutable revisions before selecting the picture timeline. Changes and launch provenance are committed locally; videos remain local and ignored by Git.
