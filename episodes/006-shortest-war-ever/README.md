# 006 — The Shortest War EVER

## Current local finishing output

[The r008 distribution master](final/episode-006-shortest-war-ever-es-1920x1080-r008.mp4) is complete at 1920×1080, 24fps and 10:55. Native audio is completely muted; the root-supplied voice is a separate normalized track. Arial Bold 64px captions are single-line, white with only the current word yellow, within the unchanged 80% safe width and raised 20px (88px bottom inset). All 1772 words are present in 295 cues and visible on the actual frame grid.

Full technical decode and sampled actual subtitle/phone review passed. See [finishing settings](postproduction/edit.json), [review](postproduction/review.md) and [repeatable workflow](../../docs/postproduction.md). Full user playback/release approval and supplied music/background/SFX remain pending. Original high-quality picture and earlier voice/timing are unchanged. Production notes below preserve their original gates and authorization history.

The active r005 direction replaces26 map slots with physical period scenes and retains only two necessary geographic inserts,014/118, using controlled motion with zero people. Five newly generated scene anchors were inspected at full resolution. All240 frames of the two controlled map outputs were inspected; both clips are5.000 seconds at1024×576,24fps, with silent audio. See [the recorded method decision](plan/map-method-decision.md).

The **117 H3 clips at12steps** in the production batch have finished. All131 latest candidates were frozen and received sampled visual/reference review. **76 slots / 81 repair requests** are now persisted in an incremental background queue; replacements and unresolved native audio still need actual review. See [the review report](plan/review-r006.md), [ledger](renders/review-evidence-r006/review-ledger.json), and [live repair status](automation/retries/review-r006/status.json). No final picture selection is approved.

The accepted Spanish voice remains651.389 seconds; the picture plan remains655 seconds. There are52 active full-frame anchors and238 planned shots. At most two adjacent slots share their primary anchor; full minutes contain6–12 unique anchors. These are planning metrics; actual motion and pacing still require review. [animatic-r007.mp4](plan/animatic-r007.mp4) includes the actual controlled geography clips and planning stills for the other slots, with the accepted voice. It does not approve future H3 motion.

The earlier stopped batches are historical: four-step preview `019625ab-2084-4483-babb-dc5be22281d7`; twelve-step map batch `f2ed5f96-6091-458b-bcab-9a2315ccd83c` (21 succeeded,109 cancelled, one interrupted failure). All output is preserved. Nine completed map candidates are superseded by the revised method. The four-step pass will not resume.

Completed production batch ID: `c0a9da8a-56f6-40f9-89ff-649ec02c4d80`. GPU sampling of clip004-r005 was verified with all117 jobs persisted.

```bash
cd /home/mhr/AI/comfy-video-automation
uv run comfy-video status c0a9da8a-56f6-40f9-89ff-649ec02c4d80 --batch --watch
```

Ctrl+C closes only this progress display; generation continues.

Current runtime ID and status are in `automation/run-state.json` and the new batch manifest. Progress is persisted in its `progress.json` and `watcher.log`; the watcher records terminal state and reports when generation finishes. Closing this chat or a separate display does not cancel the persistent service batch.

The supplied reference video/transcript and the existing research waiver remain unchanged. No new historical verification is claimed; generic diplomatic dispatches illustrate interests without asserting a named meeting. Exact clock text remains H3-generated under the unchanged eight-event contract.

After generation, review actual editorial candidates for historical meaning, stick-world identity, motion, continuity, exact clock text and native SFX. Retained candidates are not already selected or approved. Select one approved artifact for each of131 slots before assembly; automatic concatenation and upscale are disabled.

## User-authorized overnight finish

The user explicitly authorized on2026-10-05(Asia/Tehran) correcting the14cases in `renders/step-comparison-r008/input-audit.json`, rebuilding them at20steps, selecting the latest completed numeric revision for every five-second slot, concatenating all131slots and finishing with RealESRGAN_x4plus_anime_6B at1920×1080. This specific instruction supersedes the earlier approval-only/automatic-finish-disabled route for this export. Latest-version selection is recorded as a user policy, not creative approval.

The reviewed input corrections and shot simplifications are in `plan/overnight-input-repairs.json`. Source references remain unchanged: their supported viewpoints, subject counts and poses are retained, and conflicting prompt requirements are removed. Frozen new prompts and complete live dry-run are under `automation/overnight-finish/`. Repairs use20steps, res_multistep/simple, Lightning off and new deterministic fixed seeds. The general12step episode default and previous experiment remain unchanged.

`automation/overnight-finish/status.json` and `pipeline.log` track generation, selection, concat, framewise anime6B upscale, accepted Spanish narration and final technical decode. Existing candidates are never overwritten. A technically failed new repair falls back to its latest existing complete candidate and is explicitly reported; every timeline slot remains required. Picture/native-SFX and narrated distribution masters are separate. The narrated output uses accepted Spanish voice only because generated native audio has not received full audio approval. Technical completion does not assert creative approval or guarantee first-pass model compliance.
