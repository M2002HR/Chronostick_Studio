---
name: chronostick-batch
description: Check local ComfyUI and comfy-video-automation readiness, preflight a complete ChronoStick batch, launch only when explicitly authorized, and monitor progress/resource reports. Use for generation operations rather than prompt authoring.
---

# Chronostick Batch

Preparation is not permission to spend GPU time. If the user asked only to prepare, validate, or explain, stop after dry-run and provide the launch command.

## Readiness

1. Confirm ComfyUI listens on `127.0.0.1:8188` and the automation API on `127.0.0.1:8090`.
2. Query `http://127.0.0.1:8090/v1/ready`; require `ready: true` and all required H3 models/nodes.
3. Confirm no conflicting GPU generation/upscale is running and sufficient disk space remains.
4. Run the ChronoStick repository validator.
5. Run the entire job folder through `uv run comfy-video batch --folder ... --settings ... --dry-run`. Preflight must pass for every child before launch.

## Launch

Only after an explicit `run`, `start`, or `launch` instruction, submit once with `--watch`. Record returned batch/job IDs immediately in episode runtime state. Never submit individual ad-hoc jobs when the reviewed batch package exists.

The watcher shows per-clip and overall progress. Ctrl+C detaches the CLI display; it does not authorize cancellation. To reconnect, use `comfy-video status --batch BATCH_ID --watch`.

## Failure handling

- Do not blindly resubmit after a connection interruption; inspect persisted batch/job state and ComfyUI history.
- Automatic retries are only for configured transient failures.
- Never overwrite an existing media revision.
- Cancellation is a separate explicit operation. Resolve exact job IDs before acting.

## Reports

Verify terminal state, output sidecars, media streams, and `state/.../run-reports/`. Preserve per-job elapsed time, queue wait, retries, CPU/RAM, GPU utilization, peak VRAM, temperature, power, estimated energy, outputs, and errors. Generation success is not creative approval.
