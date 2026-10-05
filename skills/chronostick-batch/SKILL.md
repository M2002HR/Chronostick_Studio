---
name: chronostick-batch
description: Check local ComfyUI and comfy-video-automation readiness, preflight a complete ChronoStick batch, launch only when explicitly authorized, and monitor progress/resource reports. Use for generation operations rather than prompt authoring.
---

# Chronostick Batch

Preparation is not permission to spend GPU time. If the user asked only to prepare, validate, or explain, stop after dry-run and provide the launch command.

For reference-first Shorts, preflight the named 16-step profile and each declared service-supported request/frame grid against its 4–7-second editorial slot. Validate every reference-to-shot mapping, immutable output target and normalization plan; do not substitute legacy five-second/14-step defaults. Store preflight evidence in `automation/preflight.json`. A completed intake/storyboard check is insufficient for batch launch.

## Readiness

1. Confirm ComfyUI listens on `127.0.0.1:8188` and the automation API on `127.0.0.1:8090`.
2. Query `http://127.0.0.1:8090/v1/ready`; require `ready: true` and all required H3 models/nodes.
3. Confirm no conflicting GPU generation/upscale is running and sufficient disk space remains.
4. Run the ChronoStick repository validator.
5. Run the entire job folder through `uv run comfy-video batch --folder ... --settings ... --dry-run`. Preflight must pass for every child before launch.

## Launch

Only after an explicit `run`, `start`, or `launch` instruction, submit once with `--watch`. Record returned batch/job IDs immediately in episode runtime state. Never submit individual ad-hoc jobs when the reviewed batch package exists.

Honor an existing explicit instruction to execute the complete production workflow; a later continuation can resume that authorized work without a second permission request. Record the actual instruction and scope. For a native duration/cut pilot, split the reviewed package into a pilot batch and a remaining batch with unchanged JSON bytes. Review the pilot before submitting the remainder, and exclude its completed output targets from the next batch.

The watcher shows per-clip and overall progress. Ctrl+C detaches the CLI display; it does not authorize cancellation. To reconnect, use `comfy-video status --batch BATCH_ID --watch`.

## Failure handling

- Do not blindly resubmit after a connection interruption; inspect persisted batch/job state and ComfyUI history.
- Automatic retries are only for configured transient failures.
- Never overwrite an existing media revision.
- Cancellation is a separate explicit operation. Resolve exact job IDs before acting.

## Reports

Verify terminal state, output sidecars, media streams, and `state/.../run-reports/`. Preserve per-job elapsed time, queue wait, retries, CPU/RAM, GPU utilization, peak VRAM, temperature, power, estimated energy, outputs, and errors. Generation success is not creative approval.
