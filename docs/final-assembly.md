# Final clip selection and assembly

For the new reference-first Short profile, use `docs/reference-first-shorts.md`: chosen 20–30-second output, 4–7-second editorial slots, adaptive fast purposeful cuts and 16 steps. Fixed-five-second slot/count guidance below belongs to older profiles. Each selected editorial clip is checked against its own approved duration/frame count; raw engine output and normalization stay separate. Neutral storyboard grids are internal planning only and are never production references.

This document describes the existing Shorts assembly route. Long-form selection, chapter assembly and landscape finishing use `docs/longform/workflow.md` and `chronostick-longform-finish` while preserving the same immutable revision principle.

Final assembly is a separate deterministic stage after clip review. Generation attempts remain immutable under `renders/raw/` and `renders/editorial/`; selected copies are staged under `renders/final-selected/`.

## Selection contract

- copy one reviewed video for every generated timeline slot declared by the approved timing map into `renders/final-selected/`; a documented freeze-frame tail is an assembly operation, not another selected clip
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

## Short narration overhang

The default clip count remains `ceil(narration_end / clip_seconds)`. A future H3 episode may avoid one otherwise-empty generation only when all of these conditions are documented in its approved timing map and shot plan:

- the narration crosses the final generated five-second boundary by no more than 1.000 second
- the final generated clip reaches a deliberately resolved, freeze-safe frame before that boundary
- no new visual event, action, camera move, or required diegetic sound occurs during the overhang
- the only continuing program element is external narration or caption timing

In that case, generate the complete five-second slots before the overhang, concatenate them, then clone the final frame for the exact remaining narration duration. Pad generated SFX audio with silence; do not stretch it. Apply the extension after concat and before framewise upscale:

```bash
./scripts/extend-last-frame.sh \
  EPISODE_ROOT/final/episode-slug-concat-r001.mp4 \
  EPISODE_ROOT/final/episode-slug-tail-extended-r001.mp4 \
  0.640
```

The script refuses overwrites, enforces the one-second default maximum, validates output duration, and writes an adjacent `*.freeze-tail.json` provenance report. The extended output, not the shorter concat input, becomes the upscale input.

## Local finishing

Caption rendering, typography, narration mixing and loudness normalization now
use the repeatable local stage in [`postproduction.md`](postproduction.md), via
`scripts/postproduce-episode.py` and `postproduction/edit.json`. They remain
explicit stages after concat/upscale. Keep the clean picture master; create an
immutable separate distribution master with format-specific active-word captions:
Montserrat Bold and larger, shorter, raised phrases for Shorts; Arial Bold for
long-form. The exact defaults and licensed installation are in `postproduction.md`.
Supplied music, ambience and SFX are configurable external stems under the
2026-10-05 user decision; generator no-music wording is unchanged.

Each released language is an independent post-picture branch. See
[`localization-workflow.md`](localization-workflow.md): it replaces the
narration/caption program track while retaining the approved picture timeline
and natural SFX. Do not overwrite a source-language distribution master when
making a localized export.
