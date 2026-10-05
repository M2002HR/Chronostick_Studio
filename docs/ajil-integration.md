# Ajil gateway in ChronoStick Studio

`ajil/` is a Git submodule. Its Gemini, Groq, and Pollinations providers are
nested submodules. Clone with `git submodule update --init --recursive` after
the Ajil commit containing the corrected provider pins is available. The
root ignored `.env` is the only local configuration/secret source; it was
copied from the existing sibling Ajil installation, retaining its values.
Never commit or paste the file. The Gemini TTS default voice is intentionally
empty pending editorial selection.

Start from the ChronoStick root:

```bash
PYTHONPATH=ajil UAG_ENV_FILE=.env python -m uvicorn unified_gateway.app.main:app \
  --host 127.0.0.1 --port 8080
```

`GET http://127.0.0.1:8080/health` checks readiness. Requests to
`POST /v1/audio/speech` require the root `.env`'s `UAG_AUTH_TOKEN` when auth is
enabled. See [Ajil's Gemini TTS guide](../ajil/docs/gemini-tts.md) for its
request schema, model, safe key-rotation headers, limits, and Worker-mode
behavior. The live integration test on 2026-09-28 returned a valid WAV and
showed key slot 1 of a 12-key pool; this is a functional test, not proof that
every key has available quota.

## Reference and accepted-voice transcription

The reference-first Short route uses `scripts/ajil-transcribe.py`, not TTS.
For word **and** segment timing, start an unused/local gateway with explicit
STT settings (leave any unrelated running service intact):

```bash
PYTHONPATH=ajil UAG_ENV_FILE=.env \
  UAG_GROQ_STT_TIMESTAMP_GRANULARITIES=word,segment \
  UAG_GROQ_STT_RESPONSE_FORMAT=verbose_json \
  python3 -m uvicorn unified_gateway.app.main:app --host 127.0.0.1 --port 8080
```

```bash
python3 scripts/ajil-transcribe.py --input EPISODE/source/reference-video/REFERENCE.mp4 \
  --output-dir EPISODE/source/reference-video/transcription --purpose reference --revision r001
python3 scripts/ajil-transcribe.py --input EPISODE/audio/ACCEPTED-VOICE.wav \
  --output-dir EPISODE/timestamps/ajil --purpose voice --language es \
  --expected-script EPISODE/script/narration-es.md --revision r001
```

Language goes in the gateway's query parameter. The helper defaults to mono
16 kHz s16 FLAC; `--audio-format mp3` is a documented lossy fallback for an
upload bottleneck. Keep original bytes, derivative hash, exact response bytes,
provider metadata, source CSV/segments and validation report. STT word times are
estimates; overlaps and changed words need review and never count as approval.
Do not overwrite a partial request revision or substitute source timing for
accepted Spanish timing. The helper's 24 MiB limit requires offset-preserving
chunking before larger long-form inputs can use this route.

If a valid response was saved but derivation failed, use `--from-response`,
`--audio-derivative`, `--source-provenance` and the matching `--audio-format`
with a new revision. This verifies all three hashes and makes **no** API call.
Episode 007's r004 was derived this way from the successful r003 response;
earlier timed-out/failed attempts remain archived.

`scripts/ajil-review-reference.py` is optional supplementary native-video
analysis, not STT or a replacement for actual frame inspection. It rejects
local fallback responses as evidence even when HTTP status is 200. Episode
007's machine-video reviews failed; source sound/motion claims remain unverified.

## Reusable cue synthesis

Create or review `timing/segments.json` first. Use the finished picture/SFX
master and its semantic visual cues for time windows; do not translate source
word timestamps. For a chosen voice, render all cues into unused revisions:

```bash
python scripts/ajil-tts-synthesize.py \
  --segments episodes/002-hiroshima-final-minute/localizations/fa/timing/segments.json \
  --output-dir episodes/002-hiroshima-final-minute/localizations/fa/synthesis/takes \
  --voice Charon --revision r003
```

Each cue gets a WAV with unchanged returned bytes and a JSON provenance file
containing text, voice, timing target, duration, SHA-256, and safe rotation
headers. Existing takes are never overwritten. To revise only one thought,
edit that cue's `localized_text` or `delivery_style`, then use `--cue-id
cue-08 --revision r004` (or a new revision for that cue). Only the selected
cue is sent and created; all other WAVs remain untouched. Update a new
`synthesis/assembly-rNNN.json` plan to point just that cue to the new file,
then run `scripts/assemble-localized-narration.py` to build a new immutable
narration master. Do not reuse an old output filename or change the source
picture timeline.

The script defaults to a 22-second request interval. Ajil itself rotates
keys on retryable upstream quota errors and exposes only key positions. Keys
on the same Google project may share a quota. In production, record actual
provider limits, monitor rate-limit failures, and do not treat multi-key
rotation as a promise of free capacity. The Gemini Developer API does not
return word timestamps; derive and preserve them from the accepted complete
audio in the language branch, then check every visual cue and caption.

For Episode 002, the existing Charon `r001`/`r002` takes were rendered before
Ajil integration and remain unchanged, draft, and unapproved. Do not relabel
them as Ajil output. A different selected voice requires new revisions of all
cues and a fresh human listening/timing review; it does not require any video
regeneration.
