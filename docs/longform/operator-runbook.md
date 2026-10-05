# Long-form operator runbook

This is the executable route for one reviewed 16:9 episode. Replace `EPISODE` with `episodes/NNN-slug`. Every command that creates media uses a new `-rNNN` path. Running a validator or dry-run does not approve a stage or authorize a paid/GPU batch.

## 1. Workspace and source

```bash
python scripts/new-longform-episode.py NNN-slug --title "Original title" --source /path/to/supplied-source.txt
python scripts/validate-longform.py episodes/NNN-slug
```

When the user starts from a reference video and its transcript, use:

```bash
python scripts/new-longform-episode.py NNN-slug --title "Original title" \
  --reference-video /path/to/reference.mp4 \
  --reference-transcript /path/to/transcript.txt \
  --reference-influence-goal "Desired rhythm, framing and tone"
```

The scaffold copies supplied inputs byte-for-byte, records their hashes and leaves unsupplied artifacts missing. It records the optional Google Vids direction stage as `skipped` until chosen. The video/transcript route marks the historical source `reference_transcript_only` when no separate source is supplied; it does **not** mark Stage 00 reviewed. Inspect the actual video alongside the transcript and write `source/reference-video/intake-review.md` before advancing Stage 00. When later frames or screenshots arrive, append them to the manifest with hashes and timecodes. Follow [`reference-video-workflow.md`](reference-video-workflow.md). Do not merge example material into the verified historical source. Advance `pipeline-state.json` only after the actual stage handoff and reviewer decision.

## 2. Timing, plans, references and pilot

Complete stages 01–06 in [workflow.md](workflow.md). Keep the supplied accepted voice and word timing immutable. Build the full 120–180-slot timing map, state ledger, dated maps, exact text exceptions and reviewed reference coverage before batch preparation. Review the complete voice-led animatic. Run a *representative* final-setting 16:9 H3 pilot before relying on the profile, and save actual quality and resource results in `plan/pilot-review.md`. Four-step previews are concept filters; a paired final-setting comparison is required before treating them as useful for a risk category.

## 3. Deterministic job JSON

After approving all clip prompts, write `EPISODE/automation/job-plan.json`:

```json
{
  "schema_version": "1.0",
  "project_seed": 123456,
  "slots": [
    {
      "number": 1,
      "revision": 1,
      "references": ["assets/episodes/NNN-slug/references/opening-scene-r001.png"]
    }
  ]
}
```

The displayed array is only the first entry; supply **every** numbered slot in order. Each prompt explicitly names `<Picture 1>` (and `<Picture 2>` if used). Use stable approved full-frame anchors. Generate the JSON only into an empty `automation/jobs/` directory; revise JSON through Git and render output through a new numbered media revision.

```bash
python scripts/build-longform-jobs.py EPISODE --dry-run
python scripts/build-longform-jobs.py EPISODE
python scripts/validate-longform.py EPISODE
./scripts/validate-repo.sh
```

Create `automation/batch-settings.json` with reviewed `continue_on_error`, `stop_on_error`, `max_retries`, `concat_on_complete: false`, and `upscale_on_complete: false`. Stage 09 becomes `approved` only after a passing *live-service* dry-run, capabilities/paths/output-collision check, resource estimate and explicit review recorded in `automation/preflight.json`.

```bash
cd /home/mhr/AI/comfy-video-automation
uv run comfy-video batch --folder /home/mhr/Code/chronostick-studio/EPISODE/automation/jobs --settings /home/mhr/Code/chronostick-studio/EPISODE/automation/batch-settings.json --dry-run
```

This dry-run may cache/upload references or compile graphs, but does not queue generation. The service must be running and its `output_root` must include this repository. Check `docs/pipeline/operator-runbook.md` for service startup/status. Record the returned report and whether the 1024×576 override is truly accepted.

## 4. Generation and selection

Stage a reviewed chapter's contiguous slot range into an immutable batch folder:

```bash
python scripts/stage-longform-chapter.py EPISODE chapter-01 --first 1 --last 24
```

Its `manifest.json` records source job hashes and starts with `launch_status: not_submitted`. Check chapter boundaries against the accepted timing map; the numbers above are only an example. Submit that folder only after explicit authorization, with the reviewed global settings. Never retry an entire approved chapter to repair one clip. Preserve job IDs, raw 124-frame files, editorial 120-frame files and service reports. Review critical identity/map/text/physics frames and every audio track before choosing one editorial take for each slot. Place exact copies under `EPISODE/renders/final-selected/`, preserving `clip-NNN-...-rNNN.mp4` names. Update `renders/selection-manifest.json` with hashes and decisions. Validate the complete numbered sequence before assembly.

## 5. Landscape finishing

```bash
cd /home/mhr/AI/comfy-video-automation
uv run comfy-video concat --directory /home/mhr/Code/chronostick-studio/EPISODE/renders/final-selected --output /home/mhr/Code/chronostick-studio/EPISODE/final/picture-sfx-1024x576-r001.mp4 --missing-audio fail --watch
```

Verify order, 24 fps, 16:9, 5.000 seconds per selected clip, total duration, chapter seams and audio streams. Then upscale with explicit landscape dimensions:

```bash
/home/mhr/AI/comfy-video-automation/scripts/upscale-framewise-video.sh /home/mhr/Code/chronostick-studio/EPISODE/final/picture-sfx-1024x576-r001.mp4 --output /home/mhr/Code/chronostick-studio/EPISODE/final/picture-sfx-1920x1080-r001.mp4 --model /home/mhr/AI/ComfyUI/models/upscale_models/RealESRGAN_x4plus_anime_6B.pth --width 1920 --height 1080 --fit cover
```

Probe the output and inspect illustrated outlines, historical maps and in-engine text before accepting the upscale. Mix the **accepted** Spanish narration separately with the selected SFX; no music. Preserve both picture/SFX and narrated distribution masters. Captions, thumbnail and metadata are separate reviewed outputs. Upload/publish is a separate explicit decision.
