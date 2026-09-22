# Final export status

Final-video binaries in this directory are intentionally ignored by Git. Keep
revisioned exports here, but record their provenance and review status in the
episode manifest.

## Present artifact

- `papa_2_erasio.mp4`: externally supplied H.264/AAC export, 1080×1920,
  30 fps, 56.587 seconds. It is present locally but has not been reviewed or
  approved in this repository.

For a real 720×1280 source, run
`scripts/upscale-final-video.py`. It uses the locally installed FlashVSR 1.1
model through ComfyUI, produces a revisioned 1080×1920 export here, and leaves
the input untouched.
