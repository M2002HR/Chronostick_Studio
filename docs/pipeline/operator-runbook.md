# Local operator runbook

This runbook covers executable local operations. Replace `EPISODE_ROOT`, job/output paths, and service config with the reviewed episode paths.

## 1. Start and check services

Preferred persistent units, when installed:

```bash
systemctl --user start comfyui.service comfy-video.service
systemctl --user status comfyui.service comfy-video.service --no-pager
curl --fail --silent http://127.0.0.1:8090/v1/ready | python -m json.tool
```

Manual fallback in two terminals:

```bash
cd /home/mhr/AI/ComfyUI
uv run python main.py --listen 127.0.0.1 --port 8188
```

```bash
cd /home/mhr/AI/comfy-video-automation
uv run comfy-video service serve --config EPISODE_ROOT/automation/service-config.json
```

Local interfaces:

- ComfyUI: `http://127.0.0.1:8188`
- automation OpenAPI UI: `http://127.0.0.1:8090/docs`

## 2. Validate without generation

```bash
cd /home/mhr/Code/chronostick-studio
./scripts/validate-repo.sh

cd /home/mhr/AI/comfy-video-automation
uv run comfy-video batch \
  --folder EPISODE_ROOT/automation/jobs \
  --settings EPISODE_ROOT/automation/batch-settings.json \
  --dry-run
```

This dry-run may upload/cache reference files and compile graphs, but it must not create a batch or queue expensive generation.

## 3. Launch only after explicit approval

```bash
cd /home/mhr/AI/comfy-video-automation
uv run comfy-video batch \
  --folder EPISODE_ROOT/automation/jobs \
  --settings EPISODE_ROOT/automation/batch-settings.json \
  --watch
```

Record the returned batch ID. Reconnect after detaching:

```bash
uv run comfy-video status --batch BATCH_ID --watch
```

Do not submit a second batch because a watcher disconnected. Inspect persisted state first.

## 4. Review and stage selections

Keep every attempt immutable in `renders/raw/` and `renders/editorial/`. Copy one approved editorial file per number into `renders/final-selected/`; do not move or overwrite source attempts.

## 5. Concatenate

Use an episode wrapper when present. Generic fallback:

```bash
cd /home/mhr/AI/comfy-video-automation
uv run comfy-video concat \
  --directory EPISODE_ROOT/renders/final-selected \
  --output EPISODE_ROOT/final/episode-slug-concat-r001.mp4 \
  --missing-audio fail \
  --watch
```

## 6. Default framewise 1080×1920 upscale

Use the declared Spandrel model and cover-fit every frame to the exact vertical delivery canvas:

```bash
/home/mhr/AI/comfy-video-automation/scripts/upscale-framewise-video.sh \
  EPISODE_ROOT/final/episode-slug-concat-r001.mp4 \
  --output EPISODE_ROOT/final/episode-slug-picture-master-1080x1920-r001.mp4 \
  --model /home/mhr/AI/ComfyUI/models/upscale_models/RealESRGAN_x4plus_anime_6B.pth \
  --width 1080 \
  --height 1920 \
  --fit cover
```

Keep the adjacent `*.framewise-upscale.json` report until the upscaled master passes QC.

## 7. Reports and recovery

- service state: configured `state_dir`
- job/batch reports: `state_dir/run-reports/`
- render provenance: adjacent `*.run.json`
- framewise-upscale provenance: adjacent `*.framewise-upscale.json`

Generation, concat, and upscale are separate authorization boundaries. Never run them concurrently on one GPU.
