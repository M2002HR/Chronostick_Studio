---
name: chronostick-longform-finish
description: Assemble selected long-form ChronoStick clips, upscale to 1920×1080, and finish a separate distribution master locally with accepted narration, active-word captions and explicit sound layers. Also use for post-production on an already completed landscape master.
---

# ChronoStick long-form finishing

Read the accepted timing map, selection manifest and per-clip reviews. Verify exactly one selected five-second editorial video per slot, numeric order including slots 100+, correct frame rate/dimensions, audio stream and no missing or duplicate numbers. Assemble chapters deterministically and then the full picture/SFX timeline into an unused `-rNNN` path. Preserve original clips and `.run.json` provenance; no overwrite. Confirm full duration, chapter seams, resolved last frame and no silent truncation of accepted voice.

Use the landscape-capable framewise upscale path with explicit `--width 1920 --height 1080`; do not run the Shorts-only `1080×1920` wrapper. Measure actual source and output frame count, fps, dimensions, audio stream, aspect, temporal stability, crop, seam/flicker and text/map integrity. A final-setting pilot should show whether the chosen upscale preserves illustrated outlines and exact generated lettering before processing ten minutes.

The picture/SFX and distribution masters are separate immutable outputs. For
voice, subtitles or supplied music/background/SFX on an existing picture, read
`docs/postproduction.md` and use `scripts/postproduce-episode.py` with the
episode's `postproduction/edit.json`. Do not regenerate, re-concatenate or
upscale a completed picture merely to change finishing layers. Record actual
picture approval or the already authorized episode-specific selection policy;
a technical render does not approve the underlying picture.

Choose native-audio mute/preserve explicitly. Honor a complete-mute request by
excluding its stream, then use only the accepted continuous narration and
actual supplied tracks. Generated clips remain music-free; external finishing
music is an explicit configurable stem. Default captions are simple Arial Bold,
white text with only the current word yellow, no cumulative highlight, safe
bottom placement and measured width. Require the exact font and actual voice
timings; preserve raw timing and record measured export drift separately.

Review the actual rendered text at word changes, pauses, inserts, long lines,
light/dark backgrounds and phone size; verify fixed frame count, full decode,
encoded loudness and timing. In-engine text remains in the picture and ordinary
subtitles remain a separate finishing layer. Archive captions, stems, mix/QC
provenance and truthful review status. Music/SFX without supplied assets stay
pending. External finishing remains an optional documented route. Localization
uses its own real voice/timing branch on the fixed picture timeline.
