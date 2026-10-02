# Episode 006 resume audit — 2026-10-02

Recorded at 14:24 Asia/Tehran. This audit reconciles local artifacts, service state, Git and sampled actual frames. It is not a complete motion/audio or every-frame review. Machine-readable evidence and batch metrics are in `resume-audit.json`.

## Verified state

- Accepted voice exists: `audio/narration-es-google-vids-r001.mp4`, 651.389388 seconds. Accepted voice and corrected working timestamp hashes match the timing map. Provider originals remain separate. Word alignment includes documented corrections/interpolation; final sync review is still required.
- Picture plan: 131 five-second slots, 655 seconds, landscape 16:9. H3 settings are 1024×576, 24 fps, 12 steps, Lightning disabled. The final 3.68-second hold is measured from the last timed word; the hold after the audio container ends is approximately 3.611 seconds.
- There are 44 selected still anchors, 131 pure prompts and 131 current revision-003 jobs. All 44 recorded image hashes and execution-plan job hashes match actual files. An intact hash proves provenance, not visual correctness.
- Integrated pilot batch `a8fd33bf-eb25-4f44-b36f-b18b6c8e0a7b` succeeded for clips 013, 064, 075, 099 and 124. It ran from 09:52:29 to 10:27:04 Asia/Tehran, taking 2,074.81 seconds (34 minutes 35 seconds). Each editorial candidate is 1024×576, 24 fps, exactly 120 frames/5.000 seconds, with an audio stream.
- ComfyUI and the automation service are reachable. ComfyUI's running/pending queues are empty; service job listing contains no active jobs. No main batch is running. The five pilot renders are not selected or approved. `renders/final-selected/`, `final/` and YouTube delivery are empty.

## Findings that prevent bulk launch

| Artifact | Observed evidence | Required continuation |
| --- | --- | --- |
| Clip 013 r003 | At 0.000 seconds there are full-size people and a red cloth; at sampled 1–4.958 seconds several people surround/reveal the map. The contract requires zero people and fixed chart composition. | Correct the world-map prompt family and rerender this candidate immutably. Inspect related map slots; do not infer acceptance from a successful job. |
| Four harbour references | Full-resolution inspection of prebattle, early-battle, aftermath and refuge anchors counts **six navy British ship tokens plus one ochre Glasgow**, against the required five plus one. | Previous approval is revoked in the manifest. Correct the four still anchors with new media revisions before rebuilding dependent jobs. |
| Clip 064 r003 | Six-plus-one ship count is inherited from the bad reference. Between sampled frames the ships and Rawson token move despite their fixed-position contract. | Correct reference and motion locks; rerender. |
| Clip 075 r003 | `08:59` is readable in the sampled frames, but new dark harbour smoke appears by 1.000 seconds and persists through 4.958 seconds during the final prefire minute. | Correct this chronology failure in the clock/prefire family and rerender. The boilerplate naming possible smoke is a prompt-review candidate, not a proven cause. |
| Clip 099 r003 | Inherits the six-plus-one reference failure. Prompt fixes token positions while also directing Khalid to move; sampled motion toward the lower/right coast does not demonstrate arrival at the consulate. | Resolve fixed-versus-moving token instructions and a clear consulate destination, correct the anchor, then rerender. |
| Clip 124 r003 | `09:38` and the recurring shoe-searcher are recognizable in the samples. | Keep as an unapproved candidate pending whole-motion/audio, every text frame and terminal-hold review. |

The four rejected harbour anchors support slots **007, 055, 064, 073, 076, 085, 088, 093, 094, 096, 099, 101, 105 and 127**. Repair those 14 slots' reference mapping without discarding unrelated work. Stages 05–10 now say `needs_review`; previous decisions are preserved in each stage's `previous_review`. Still animatic r004 remains an accepted planning preview, but is not approval of H3 motion.

Sampling used the source anchor plus frames at 0, 1, 2, 3, 4 and 4.958 seconds for each current pilot. Obvious failures are enough to reopen the gate; no clean candidate receives final approval from this sampling. Full audio listening was not performed.

## Document and automation recovery

- `graphics-method-decision.md`, current episode manifest and execution plan require **all picture through H3**. The deterministic graphics proposal in the earlier `pilot-review.md` is superseded. Its historical log names `renders/graphics/`, but that directory is currently absent; those outputs are neither selected nor recovered artifacts.
- `automation/batches/scene-12step-r001/` contains 86 old jobs; none matches current active JSON. It is not the current remaining-job batch. `pilot-integrated-r001/` is also old; `pilot-integrated-r003/` matches the submitted current pilot.
- Active jobs for 013, 064, 075, 099 and 124 collide with existing output paths. Do not submit `automation/jobs/` wholesale. There are 126 unrendered active slots, plus whatever immutable replacements pilot review requires. Preserve completed candidates and sidecars.
- Historical full preflight passed before those outputs existed. Rebuild only changed jobs at new media revisions and freshly stage/dry-run the intended remaining queue after corrective review.
- `build-episode-006-production.py` rewrites prompts, ledgers, the reference manifest and job plan, including generated approval fields and a project-seed value different from the current job plan. Review and reconcile the builder before rerunning it; do not let it overwrite this audit's decisions or silently change seeds.
- Old stage notes describing voice auditions or independent research as next actions are historical notes. Accepted voice/timing are already present. Research was explicitly waived for this episode; it was skipped rather than passed.

## Git and local media

At the start of the audit, `master` was `63b9440`; live `origin/master` returned the same commit. There were 19 modified tracked files and 791 untracked files, approximately 152.56 MiB of untracked content. Episode 006 had no tracked files. The pending work mixes shared long-form infrastructure, voice-direction rules, scripts/skills, assets and episode production records. No commit or push was performed during this audit.

Video formats are excluded by `.gitignore`, and render sidecars are also local. Committing episode text will not back up the voice, reference video, animatics or H3 renders. Preserve a separate media backup alongside Git.

After reviewing changes, use coherent commits for shared long-form infrastructure/rules, episode assets/prompts, and episode production/audit records. Inspect the old batch/experiment files before staging them so they cannot be mistaken for active production.

## Checks and next action

Before and after audit reconciliation, repository validation, long-form validation, skill validation and `git diff --check` passed. The repository warnings were only the four documented missing Episode 001 prompts. These checks did not detect the visual count/chronology failures above. Rerun them after repairs; a static pass does not close the reopened creative gates.

Continue with corrected harbour references and pilot-family instructions, review immutable replacement H3 candidates in full, then preflight/stage the remaining authorized generation. At the observed pilot average of about 6.92 minutes per clip, 126 remaining clips would take roughly **14.5 hours** on the same machine, before replacements, review and finishing; this is an extrapolation, not a scheduling guarantee. After generation, review every slot, select one approved take per slot, concatenate, upscale to 1920×1080, mix accepted Spanish voice/SFX, and prepare YouTube delivery.
