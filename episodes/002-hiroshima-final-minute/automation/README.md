# Episode 002 automation

The first r001 batch (`45b01a15-f702-468f-9697-a677057b5957`) was deliberately stopped. Clips 01–02 are rejected and clips 03–17 were cancelled. There is no active r002 batch.

Start ComfyUI on `127.0.0.1:8188`, then start the automation service from `/home/mhr/AI/comfy-video-automation`:

```bash
uv run comfy-video service serve --config /home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute/automation/service-config.json
```

Open the local panels at `http://127.0.0.1:8188` (ComfyUI) and `http://127.0.0.1:8090/docs` (automation API).

Validate all 17 jobs, including their actual uploaded references and compiled workflows, without generation:

```bash
/home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute/automation/run-batch.sh --preflight-only
```

When ready, run the exact same script without the flag. It repeats preflight, submits the naturally ordered sequential batch, and stays attached with one progress bar per clip plus an overall bar:

```bash
/home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute/automation/run-batch.sh
```

To reconnect to an already submitted batch:

```bash
uv run comfy-video status --batch BATCH_ID --watch
```

The service state is persistent under `/home/mhr/AI/comfy-video-automation/state/chronostick-episode-002`. Per-job resource reports and the final aggregate batch report are written to its `run-reports/` directory. Each output `.run.json` sidecar also receives elapsed time and CPU, RAM, GPU utilization, peak VRAM, temperature, power, estimated energy, disk, retry, and queue-wait metrics. Restarting both local services resumes incomplete jobs without blindly resubmitting an existing ComfyUI prompt.
