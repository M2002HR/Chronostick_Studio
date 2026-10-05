---
name: chronostick-sfx
description: Select, archive, time and review short independent physical SFX for ChronoStick picture clips, including full native-audio replacement after a music-contaminated render. Use during render review or finishing; preserve the picture and accepted external voice.
---

# Chronostick SFX

Read `docs/audio-rules.md` and `docs/clean-sfx-workflow.md`, then the episode's
actual render review, shot plan and audio decision. Strong no-music prompts
remain mandatory; they do not certify actual generated sound.

Prefer clean, synchronized native engine SFX after actual sound review.
Independent cue replacement is a fallback for an actually contaminated or
failed soundtrack, not the default for every clip. A user acceptance of a
fallback preview does not approve unrelated effects or mandate replacement
of clean native audio.

## Choose actual physical events

Inspect the real clip and identify the contact/motion frame, visible material
and intensity. Use only motivated tiny dry cues: paper handling, cloth contact,
wood handling or a short metal click. An omitted action receives no effect.
Static inserts, transitions and terminal holds stay silent. Never place cues
mechanically on every planned cut or add a rhythm, riser, sting or tonal bed.

Prefer separately recorded physical effects with documented provenance and
usable license. Archive source bytes, actual source page/license, creator,
URL, download quality and hashes; original WAV and an HQ lossy preview are
different assets and must be named honestly. Review the sound itself rather
than accepting its title. Extract a brief natural transient, retain its timbre,
use small edge fades and restrained gain, and keep exact silence elsewhere.
Procedural clicks/noise are explicit preview alternatives, not recordings.

## Replace contaminated audio

Record a user music report as a render failure. If the sound contract calls
for replacement, exclude the **entire** native soundtrack; do not lower it under
narration or take snippets that might still contain music. Preserve raw takes.
Create a separate cue plan bound to the actual picture hash and observed action
times. `scripts/clean-short-sfx.py EPISODE --plan PLAN` stream-copies video and
maps only the new independent cue stem. It checks every decoded picture frame
and exact-zero PCM regions between cues. It never performs a creative picture
edit, narration synthesis, music separation or rhythmic cue loop.

For unreviewed source sounds, use `--preview` and a path outside final-selected.
Obtain actual sound feedback; only then mark the specific source/cue selection
reviewed. Do not treat elapsed time, JSON flags, waveforms or machine descriptions
as user approval. A separately reviewed clean derivative can be selected while
the music-contaminated original remains rejected for audio.

## Evidence and handoff

Bind source/picture/cue hashes, licenses, source in-points, processing, placements,
review decisions and native-audio exclusion in the cue plan and derivative
sidecar. Keep subjective sound quality separate from technical source exclusion.
Machine audition is supplementary: an output that invents cue times or reads
the intended prompt back is not evidence. Do not claim personal listening.
Hand the clean picture/SFX derivatives to `chronostick-finish`; mix the accepted
user narration separately, without any music or ambience track for this route.
