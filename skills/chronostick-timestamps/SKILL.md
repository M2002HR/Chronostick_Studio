---
name: chronostick-timestamps
description: Validate and archive word-level narration timestamps, preserve the original timing source, and derive clip-aligned timing maps for ChronoStick production. Use after the narration and voice delivery are approved.
---

# Chronostick Timestamps

Use timestamps from the approved voice, not estimated reading speed.

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
