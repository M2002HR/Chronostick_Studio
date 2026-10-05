# Local post-production

From 2026-10-05, ChronoStick finishes narration, ordinary captions and separate
sound layers locally after the picture master. This shared stage supports
Shorts and long-form without changing either generation profile or its fixed
picture timeline. External Google Vids finishing remains optional. Generation
continues to forbid music and generated voices; supplied music can be added as
an explicit finishing track. No music is selected or generated implicitly.

## Inputs and repeatable commands

Use the completed clean picture master, accepted narration and its real
word-level CSV (`word,start,end`). Preserve all originals. A new voice export
must match the timing's audio authority: actual measured alignment evidence is
required for export-only drift; different speech needs new actual transcription.
Do not reuse another language's words or timings. Localizations retain their
own immutable post-picture branch.

Dependencies: Python with Pillow (plus fontTools for the Shorts font installer), FFmpeg/FFprobe with libass, loudnorm and
sidechaincompress, fontconfig and the exact selected bold font. New Shorts use
Montserrat Bold, installed from the official Google Fonts source with its OFL
license and source hashes:

```bash
python scripts/install-shorts-font.py
```

Long-form uses genuine Arial Bold. The Arial Core Fonts package was extracted
locally without executing its Windows installer. On another machine:

```bash
python scripts/install-arial-font.py
```

The font helper requires `7z` (Ubuntu package `7zip`). Fonts stay under the
user's local font directory, outside Git. An unavailable Arial font is an error;
do not silently replace it with Liberation Sans. See the
[original font package](https://sourceforge.net/projects/corefonts/files/the%20fonts/final/).

Initialize an episode once, using matching accepted inputs:

```bash
python scripts/postproduce-episode.py episodes/NNN-slug --init \
  --picture final/picture-sfx-1920x1080-r001.mp4 \
  --narration audio/narration-es-r001.wav \
  --words timestamps/word-timestamps-source.csv --audio-language spa
```

This writes `postproduction/edit.json` with actual input hashes, dimensions,
format-scaled typography, narration-only sound and no external tracks. Review
and edit that stable configuration; text versions belong in Git. Check then
render:

```bash
python scripts/postproduce-episode.py episodes/NNN-slug --check
python scripts/postproduce-episode.py episodes/NNN-slug
```

For a long render launched from this chat or another short-lived runner, use
`--background` and monitor `postproduction/run-state.json` plus the recorded
`render-rNNN.log`. The detached export survives the caller's session timeout;
keep monitoring until the final manifest/full-decode check exists. A started
process is not a completed export.

The renderer chooses the next unused distribution revision, preserves every
picture frame, and refuses overwrites. A failed attempt retains its package
and logs; fix the configuration and use the next revision. A finishing-only
change creates a new distribution master and does not regenerate clips or
upscale the picture again. `--revision N` explicitly selects an unused number.

## Captions

Both format profiles keep all words white; only the currently spoken word
yellow (`#FFD700`). Already spoken and future words remain white. There is no
cumulative karaoke fill, bounce, glow or progressive letter animation. A short
dark outline/shadow keeps text readable on light pictures. The highlight returns
to white during an actual gap and captions disappear after the final spoken word.

New portrait Shorts use **Montserrat Bold**,104px at1080×1920,80% safe width,
300px bottom inset and one line. Use short2–4-word phrases (maximum4 words or
1.8seconds, with a300ms gap break), further shortened when measured width
requires it. This places larger, heavier text near the lower-middle region,
above channel/player overlays, approximating the user's2026-10-05 screenshot.
The screenshot's original font is unknown; Montserrat Bold is a selected visual
approximation, not an asserted font identification. A restrained2px dark
outline and2px shadow preserve readability without a thick sticker border.

Landscape 1920×1080 keeps Arial Bold64px,88px bottom inset,80% width and its
existing12-word/four-second grouping,2.5px outline and1px shadow. Scale each
format's own geometry with frame size. Existing saved configurations remain
explicit and are not silently migrated. Size, width, position and color are
configuration values. Break at sentence ends, useful commas and pauses; measure with the
actual font and keep one line by shortening each caption phrase when it reaches the width limit. Long tokens outside the safe width
fail instead of spilling outside the image. For RTL languages, separately
review shaping and breaks; the Episode 006 pilot verifies Spanish only.

ASS provides the baked-in active-word colors. Plain SRT and WebVTT are separate
upload/edit assets and do not retain those colors. Display boundaries snap to the nearest picture frame and are stored in ASS
at 10ms resolution, floored so the chosen frame can display even a 40ms word.
Unquantized boundaries remain in the derived map; source CSV times are unchanged. When provider
word ends overlap the next start, the later-starting word wins; never highlight
two words or reactivate an earlier one. The original CSV stays unchanged. The
derived caption map records original and adjusted times and every active event.
For near-duplicate provider starts separated by only 1ms, an explicit
`timing.start_boundary_repairs` entry may use `previous_source_word_end` as the
next display start. It preserves the supplied end boundary and records the
reason; it is display normalization, not a new measured timestamp. If supplied
ends cannot resolve the collision, re-align the actual audio. Verify that every
word has a visible highlight interval.

## Separate audio tracks

`native_audio.mode` is explicitly `mute` or `preserve`. In `mute`, only the
picture's video stream is mapped: its original audio contributes zero samples
to the mix. In `preserve`, its audio becomes a separate track at the configured
gain. This setting affects the new distribution only; retain the picture/SFX
master and earlier exports. Episode 006 explicitly uses `mute`.

Narration is a continuous separate FLAC stem. Its offset defaults to zero;
captions use the same offset. Never trim silence, time-stretch narration or
truncate it to fit the picture. Refuse an overlong narration. Pad the resolved
picture tail with audio silence without extending or dropping picture frames.

`tracks` is initially empty. Add user-supplied audio under `audio/` and specify
role (`music`, `ambience`, `sfx`), path, SHA-256, placement, source in-point,
length and gain. Each cue is self-contained. For example:

```json
{
  "role": "music",
  "path": "audio/music-bed-r001.wav",
  "sha256": "ACTUAL_FILE_SHA256",
  "start_seconds": 0,
  "source_start_seconds": 0,
  "duration_seconds": 655,
  "gain_db": -24,
  "loop": true,
  "fade_in_seconds": 1,
  "fade_out_seconds": 3,
  "duck_under_narration": true
}
```

This is a schema example, not a present or approved asset. The actual file hash
is required. Music also requires `external_music_allowed: true` in the edit.
Start with conservative gains and audition them. Ducking lowers a background
bed while narration is present; isolated SFX may remain unducked. Loop only
when explicitly configured, and review audible loop seams. No invented or
missing audio layer is marked complete.

Use two-pass narration and final-mix normalization, initially -16 LUFS,
-1.5 dBTP, LRA 11, stereo 48kHz AAC at 192kbps. Measure the encoded output, since
AAC can change true peaks. Normalize to the explicit mix specification rather
than claiming a platform mandates these values. FFmpeg's
[filter documentation](https://ffmpeg.org/ffmpeg-filters.html#loudnorm)
defines the loudness measurement and
[sidechain compression](https://ffmpeg.org/ffmpeg-filters.html#sidechaincompress).

## Artifacts and review

Each distribution revision has a package under `postproduction/exports/rNNN/`:
configuration snapshot, input/output hashes, ASS/SRT/VTT, derived caption map,
lossless voice/mix stem, measurement JSON, command and logs, probe and manifest.
The final video lives under `final/` with adjacent `*.postproduction.json`.
Lossless stems and copied local fonts remain outside Git; timing, settings,
provenance and review evidence are retained. Record the actual source font and
hash. Technical success is `validated_needs_user_review`, never implicit approval.

Require complete frame count/duration/dimensions/fps, one output audio stream,
full decode without errors, encoded loudness/peak check and source hashes.
Inspect actual rendered subtitles at the beginning, word changes, pauses,
long lines, light/dark backgrounds, clock/map inserts, export seams and final
hold, including a phone-sized preview. Audition voice/mix intelligibility and
timing; full human playback/release approval stays separate from sampled QC.
Music, ambience and SFX remain pending until actual assets and reviewed mix
exist. `python -m pytest -q tests/test_postproduction.py` exercises active-word
timing, safe line width, immutable inputs, track scheduling and a real FFmpeg
render that proves the native source tone is absent.
