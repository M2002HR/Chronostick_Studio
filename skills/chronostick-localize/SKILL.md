---
name: chronostick-localize
description: Adapt a finished ChronoStick picture master into another language with natural narration, immutable cue-level TTS, real target-language timestamps, and reviewed sync; use for dubbing existing Shorts or long videos without regenerating scenes.
---

# ChronoStick localization

Use the finished visual timeline as a fixed authority. The task is to make a
new language branch, not to remake its shots. Read the repository `AGENTS.md`,
active production docs, target episode README/shot plan, and
`docs/localization-workflow.md` before creating or changing an episode. For
Ajil setup, request schema, and commands, read `docs/ajil-integration.md`.
If working outside this repository, locate equivalent source script, picture
master, and cue map; ask for missing media rather than inventing it.

## Intake and editorial adaptation

1. Inspect the exact final picture and audio streams. Require an approved
   picture/SFX-only master or separable SFX stem; a mixed source voice cannot
   be cleanly replaced merely by overlaying another voice. Record its path,
   SHA-256, duration, frame rate, scene boundaries, and approval state.
2. Read the original narration, actual source timing, shot plan, and sources.
   If any are unavailable, mark them unavailable and derive visual cues by
   watching the picture. Source-language word times are evidence for semantic
   beats, never target-language word timestamps.
3. Write a new script in natural, everyday target-language speech. For
   Persian, use ordinary conversational storytelling; avoid literal
   English/Spanish syntax, bookish synonyms, filler, exaggerated sentiment,
   and factual embellishment. Keep historical qualifications and align names,
   numbers, reveals, and actions with what viewers see. Read aloud before TTS.
4. Make `timing/visual-timing-map.json` and `timing/segments.json` with cue ID,
   visual intent, window, tolerance, localized text, and optional delivery
   style. Segment at complete thoughts/natural breaths, not automatically at
   every source word or five-second render boundary. Use more cues for long
   videos but keep the same fixed-picture rule.

## Voice and cue rendering

Ask for the target voice when it has not been selected; provide a small
audition set. Do not silently switch an approved voice. For Gemini Persian,
voice names and live support are documented at the official [speech generation
guide](https://ai.google.dev/gemini-api/docs/speech-generation). Keep style
instructions short and restrained. Gemini Developer API does not guarantee
utterance duration or return word timestamps.

When synthesis is authorized, check `ajil/` and root `.env`, initialize its
submodules if needed, start the gateway if `/health` is down, and verify
`POST /v1/audio/speech` with a short probe. Do not display secrets. Use
`scripts/ajil-tts-synthesize.py` for one immutable WAV + JSON provenance per
cue. Check rate limits and quotas before a batch; key rotation does not imply
free capacity. Never overwrite a take. Use an unused `rNNN` suffix and record
voice, model, text hash, WAV hash, duration, and safe key-slot headers.

Review each take at normal speed for colloquial delivery, pronunciation,
emotion, drift, and whether it fits its visual window. Fix overlength first
by rewriting that cue naturally, then render only that cue with `--cue-id`
and a new revision. Do not edit or regenerate the other cue WAVs. A short
quiet hold or documented subsecond pause may help; do not globally stretch
speech or change picture timing just to force a fit.

## Assembly and release gate

Make a new assembly plan referencing the selected take for each cue. For a
single-cue revision, change only that cue in a new plan. Build a new immutable
complete narration with `scripts/assemble-localized-narration.py`; verify
sample rate/channel count, duration, peaks, neighboring cues, and the final
hold. Preserve the raw provider audio and the raw target-language STT/alignment
response unchanged. Derive reviewed target word timestamps from **accepted
target audio**, then generate RTL captions from those times. Never copy source
word timestamps.

Mix against the approved picture/SFX master without source-language voice or
background music. Review the whole release on a phone at normal speed:
factual meaning, all semantic cue onsets, native-sounding narration, audio
gaps/overlaps/clipping, pronunciation, SFX, caption joining/reading order,
safe areas, and video duration. Record reviewer decisions in the language
manifest; file existence or a technical pass is not approval. Keep the
picture unchanged and save each output as a new `-rNNN` revision.

Do not publish or regenerate video without explicit authorization. If only a
voice choice or workflow is requested, stop before a full synthesis run.
