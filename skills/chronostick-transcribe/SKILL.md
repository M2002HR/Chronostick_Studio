---
name: chronostick-transcribe
description: Extract a reference video's speech or an accepted narration's real word and segment timestamps through Ajil, with immutable raw responses and timing validation. Use before reference analysis or final voice-led direction; do not generate a voice or estimate timestamps.
---

# ChronoStick Transcribe

Read `docs/ajil-integration.md` and the selected episode workflow. Keep reference-video timing and accepted-voice timing in separate artifact branches.

## Execute

Use the repository helper, not a direct provider bypass:

When the user's voice arrives in a video export, first run
`scripts/ingest-narration.py --input INPUT --episode EPISODE --language es --revision r001`.
It archives original bytes, extracts the complete native-rate/channel 24-bit
PCM WAV for final assembly and, for AAC, a stream-copy M4A. Keep these separately
from the mono 16 kHz STT derivative. Record their hashes and the selected
assembly voice path. Ingestion does not trim, resample, normalize or time-stretch
the narration; any duration discrepancy or delivery review remains explicit.

```bash
python3 scripts/ajil-transcribe.py --input INPUT --output-dir OUTPUT_DIR \
  --purpose reference --revision r001
```

For a supplied Spanish voice, use `--purpose voice --language es --expected-script EPISODE/script/narration-es.md`. Preserve the accepted input unchanged and verify its actual delivery first. The helper creates a mono audio derivative, archives the Ajil response bytes and provenance, and derives word CSV, segment JSON, readable transcript and validation report. FLAC is the default to reduce upload size; WAV can be selected explicitly.

Ajil's running STT configuration must enable `verbose_json` and `word,segment`. The current API gets granularity from gateway configuration and language from a query parameter. Start a local gateway using root `.env` and explicit `UAG_GROQ_STT_TIMESTAMP_GRANULARITIES=word,segment` overrides when needed; do not print credentials or overwrite an unrelated running service. A successful HTTP response alone does not establish usable timestamps.

## Review and failure

Read the actual returned transcript and timing report. Inspect difficult names, numbers, speech over music, omissions and hallucinations against the original audio. Word times are STT estimates, not guaranteed forced alignment. Preserve raw bytes and overlapping intervals; put corrections in a derived reviewed file with reasons. For voice mode, resolve token differences against the approved script before downstream timing.

Do not overwrite a partial or failed revision. Inspect its saved provenance, then fix the cause and choose the next unused revision. Bound retries to diagnosed transient failures; record unavailable extraction honestly. The helper rejects derivatives over 24 MiB; for larger long-form inputs, implement verified chunk offsets and seam reconciliation before use rather than silently truncating audio. An upstream script or voice change invalidates its timing and affected downstream direction.

## Handoff

Record input/audio/response hashes, model and requested/detected language, actual word/segment coverage, validation issues and review decision in the episode state. Reference outputs feed `chronostick-reference-video`; accepted voice outputs feed `chronostick-timestamps` and final timed direction. Neither a returned file nor a validator pass is creative approval.
