---
name: chronostick-longform-timing
description: Preserve and validate the user's accepted Spanish voice and word timestamps, then derive chapter cues and five-second picture slots for a long ChronoStick episode. Use only after script and voice review.
---

# ChronoStick long-form timing

Read the approved spoken script, the accepted audio file or recorded external location, and the original timing response. Keep the supplied audio and `timestamps/word-timestamps-source.csv` byte-for-byte; derived corrections belong in a new timing map. Do not infer timing from a text transcript or reuse another language's timestamps.

Validate every spoken token against the Spanish text, start/end order, gaps, overlaps, missing words, punctuation handling, true narration end and media duration. Record any transcription mismatch without altering the source. If the accepted voice is unavailable, stop derived timing at `missing` and hand the user the exact gap. If source length is outside the 10–15 minute target, report it; never stretch or truncate narration to hit a round number.

Derive `timestamps/timing-map.json` with accepted audio hash/location, narration end, semantic visual-cue windows, chapter boundaries, and complete five-second slot coverage from 0 through `ceil(narration_end/5)*5`. The last slot may have a resolved hold after speech; never invent a new historical action merely to fill it. Record exact words overlapping every slot and the planned picture duration. Review timestamp alignment by listening at chapter turns and high-salience dates/names. Mark `approved` only after an actual timing review decision.
