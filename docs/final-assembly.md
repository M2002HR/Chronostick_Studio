# Final clip selection and assembly

Final assembly is a separate deterministic stage after clip review. Generation attempts remain immutable under `renders/raw/` and `renders/editorial/`; selected copies are staged under `renders/final-selected/`.

## Selection contract

- copy one reviewed video for every timeline slot into `renders/final-selected/`
- preserve filenames beginning with `clip-NN-`
- keep exactly one file per clip number
- use editorial five-second versions unless a documented exception is required
- do not copy `.run.json` sidecars into the selection folder
- do not rename or overwrite the source render

For Episode 002 the selection folder must contain exactly 17 videos numbered 01 through 17. Different revisions may be mixed intentionally; the selected filename records the source revision.

## Assembly behavior

The service accepts a directory, naturally sorts supported video filenames, verifies media streams, preserves audio, normalizes incompatible codec/dimension/frame-rate inputs when needed, concatenates them, validates total duration, and writes a provenance `.run.json` sidecar.

The Episode 002 wrapper additionally validates exact clip numbering and automatically selects the next unused final revision:

```bash
/home/mhr/Code/chronostick-studio/episodes/002-hiroshima-final-minute/automation/assemble-final-selected.sh
```

Outputs are written under `episodes/002-hiroshima-final-minute/final/` as `episode-002-hiroshima-final-minute-rNNN.mp4`. Existing outputs are never overwritten.

The generic service command is:

```bash
cd /home/mhr/AI/comfy-video-automation
uv run comfy-video concat \
  --directory /absolute/path/to/selected-clips \
  --output /absolute/path/to/final/output-r001.mp4 \
  --missing-audio fail \
  --watch
```

## Future stages

Caption rendering, typography, narration mixing, branding, loudness normalization, and any music policy belong after deterministic clip concatenation. They should be explicit configurable stages rather than implicit behavior in folder concat. The current production policy forbids background music; introducing it later requires an intentional policy decision and audio-mix specification.
