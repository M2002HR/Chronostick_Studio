# Episode 002 automation

Start ComfyUI on `127.0.0.1:8188`, then start the service from `/home/mhr/AI/comfy-video-automation`:

```bash
uv run comfy-video service serve --config /home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute/automation/service-config.json
```

Validate one job without generation:

```bash
uv run comfy-video validate-config /home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute/automation/jobs/clip-01-sixty-seconds-before.json
```

Submit the naturally ordered sequential batch:

```bash
uv run comfy-video batch \
  --folder /home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute/automation/jobs \
  --settings /home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute/automation/batch-settings.json
```

Monitor the active production batch:

```bash
uv run comfy-video status --batch 45b01a15-f702-468f-9697-a677057b5957
```

The service state is persistent under `/home/mhr/AI/comfy-video-automation/state/chronostick-episode-002`. Restarting both local services resumes incomplete jobs without blindly resubmitting an existing ComfyUI prompt.
