---
name: chronostick-timestamps
description: Validate and archive word-level narration timestamps, preserve the original timing source, and derive clip-aligned timing maps for ChronoStick production. Use after the narration and voice delivery are approved.
---

# Chronostick Timestamps

Use timestamps from the approved voice, not estimated reading speed.

For reference-first Shorts, first use `chronostick-transcribe` on the actual accepted Spanish voice with `--language es --expected-script`. Preserve provider response bytes as the primary timing source and the emitted CSV as a traceable derivative. Keep original-reference timing separate. For the new profile, allocate 4–7-second slots from actual speech/beat boundaries and frame grid; do not use `ceil(end/5)` or pad to a five-second multiple. Check total target, complete word coverage and overlaps. The fixed-five-second procedure below applies to legacy profiles only.

Use `scripts/build-short-timing.py` with a reviewed `plan/clip-slot-decisions.json`: integer frame boundaries, actual voice/source/response hashes and any text aliases. It preserves the original CSV bytes and records normalized intervals separately. Clamping an overlapping start to the preceding derived end is an explicit visual/caption adjustment, not a new measurement; reject a nested overlap that leaves no positive supported interval. Keep number tokens such as `1605` or `36` as aggregate provider intervals rather than inventing timings for expanded spoken words. Assign each token exactly one clip owner and record boundary-spanning overlap separately. Round the complete audio endpoint up to the next picture frame, never to an extra whole clip. An out-of-default runtime requires a hash-bound episode-only user voice decision; future default targets stay unchanged.

## Procedure

1. Preserve the original CSV byte-for-byte as `timestamps/word-timestamps-source.csv`; record its SHA-256 hash.
2. Detect columns, encoding, empty tokens, negative times, end-before-start rows, duplicates, overlaps, gaps, and coverage.
3. Reconstruct token text and compare it with the approved narration. Report punctuation/tokenization differences separately from missing or changed words.
4. Never modify the source file to hide overlaps. If downstream logic needs monotonic intervals, write `word-timestamps-normalized.csv` and document the deterministic normalization.
5. Create `timing-map.json` with narration start/end, duration, five-second global slots, words overlapping each slot, sentence/beat boundaries, and any tail hold.
6. Use `ceil(narration_end / 5)` for the default clip count. The editorial duration is `clip_count × 5`; document silence/hold after narration ends.

## Gate

Approval requires complete narration coverage, usable numeric times, traceability to the preserved source, and no unexplained mismatch with the approved script. A changed voice or narration invalidates this stage.

## Outputs

Store a validation report beside the timing files, including hash, row count, token count, first/last timestamp, overlap count, normalization method, and unresolved issues. Advance to `approved` only after the operator confirms the timing belongs to the approved voice.
