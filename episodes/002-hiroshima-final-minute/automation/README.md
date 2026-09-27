# Episode 002 automation

## Completed r003 batch

- batch ID: `2ad1371c-ff73-45e2-82cd-8c3b81be66f7`
- revision: r003
- profile: 5-second H3, 480×864, 24 fps, 16 steps, fixed seeds
- jobs: 17, sequential GPU concurrency 1
- background unit used for submission: `chronostick-episode-002-r003.service`
- launched: 2026-09-26 00:38 Asia/Tehran
- raw outputs: `episodes/002-hiroshima-final-minute/renders/raw/*-r003.mp4`
- editorial outputs: `episodes/002-hiroshima-final-minute/renders/editorial/*-r003.mp4`

Check structured batch status:

```bash
cd /home/mhr/AI/comfy-video-automation
uv run comfy-video status --batch 2ad1371c-ff73-45e2-82cd-8c3b81be66f7 --watch
```

Check the detached launcher journal:

```bash
journalctl --user -u chronostick-episode-002-r003.service -f
```

Check both persistent services:

```bash
systemctl --user status comfyui.service comfy-video.service
```

The launcher first runs repository validation and service-side dry-run validation for all 17 jobs, then submits the real batch. Closing a terminal does not cancel the server-side batch. If ComfyUI or the automation API restarts, the configured persistent service state resumes incomplete work.

All 17 r003 jobs completed successfully. Clip 17 r003 was rejected in visual review because it returned to an earlier story state and generated another explosive event near the end. The targeted replacement is:

- job ID: `dd6d58e4-5d11-4cf5-bee9-0f4a81178942`
- retry specification: `automation/retries/clip-17-aftermath-r004.json`
- selected candidate: `renders/editorial/clip-17-aftermath-r004.mp4`
- review result: accepted; a single continuous post-event aftermath view with no replay, flash, or new explosive event

## Assemble the selected master

Copy exactly one approved video for every clip number into `renders/final-selected/`. Keep the original revision in each filename and use names beginning with `clip-01-` through `clip-17-`. Then run:

```bash
/home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute/automation/assemble-final-selected.sh
```

The script rejects missing numbers, duplicates, extra videos, and invalid filenames. It checks that the automation API is ready, submits the directory to the media-concat service in natural filename order, waits for completion, and writes the next unused master revision to `episodes/002-hiroshima-final-minute/final/`.

## Re-run commands

Validate without queueing generation:

```bash
/home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute/automation/run-batch.sh --preflight-only
```

Start a future revision only after changing every job identity and output prefix to a new unused `rNNN` value:

```bash
/home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute/automation/run-batch.sh
```

Do not run the current r003 job set again because outputs are immutable and overwrite is disabled.
