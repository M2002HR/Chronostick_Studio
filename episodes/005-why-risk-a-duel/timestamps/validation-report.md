# Timestamp validation report

## Decision

- status: approved
- operator context: the user pasted these timestamps for Episode 005 and asked that they be converted to the same CSV format used by earlier videos
- narration timing: 0.080–52.520 seconds
- duration variance: the intake target was 40–49 seconds, but this voice ends 3.520 seconds beyond that ceiling
- operator decision: on 2026-09-29 the user explicitly confirmed the 52.520-second timing and authorized shot planning for the resulting 11-clip, 55-second picture timeline

## Source preservation

- supplied form: structured token/start/end text pasted into chat; no provider CSV file was supplied
- archived conversion: `timestamps/word-timestamps-source.csv`
- SHA-256: `b712a2fb72b549eb1225c8b4de5992d8fc94ce22012c2e6d7806c120b2968718`
- encoding: UTF-8
- columns: `index,word,start,end,duration,probability`
- conversion: token spellings, capitalization, punctuation escapes, indices, starts, and ends were retained; duration was derived as `end - start`; probability is blank because it was not supplied
- byte-for-byte provider preservation: unavailable because the source was pasted as structured text rather than uploaded as a CSV file

## Structural validation

- data rows / source tokens: 129
- index sequence: continuous from 1 through 129
- empty word tokens: 0
- duplicate indices: 0
- duplicate rows: 0
- negative timestamps: 0
- end-before-start rows: 0
- duration arithmetic errors above 0.001 seconds: 0
- overlaps: 0
- first spoken word starts: 0.080 seconds
- final spoken word ends: 52.520 seconds
- spoken span: 52.440 seconds
- leading silence: 0.080 seconds
- positive inter-word gaps: one 0.150-second gap between source tokens 68 and 69

## Text coverage

The source contains 129 recognized tokens while the approved narration contains 127 written words. Timing order covers the complete narration, but the recognition text is not a literal match. The source CSV intentionally preserves these differences:

- likely inflection recognition: `podía` / `podías`, `daba` / `daban`
- split words: `a` + `Drede` for `adrede`, `se` + `obtimo` for `séptimo`, `he` + `rido` for `herido`, and `a` + `punto` for `apuntó`
- fused words: `perdiomas` for `perdió más`
- number transcription: `100 de los` for `cien duelos`, `4.000` for `cuatro mil`, and `20` for `veinte`
- likely name truncation: `Urue` for `Uruguay`
- possible omitted reflexive pronoun: source has `Políticos enfrentaban`; the script has `Políticos se enfrentaban`
- punctuation-only differences include commas versus periods/colons and the escaped token `1992\.`

No normalized CSV was created because the time intervals themselves are already monotonic and usable. The corrected approved narration text is carried in the beat and slot labels of `timing-map.json`; the recognition source remains immutable.

## Editorial derivation

- default ceiling rule: `ceil(52.520 / 5) = 11` clips
- generated timeline: 11 × 5.000 seconds = 55.000 seconds
- resolved post-narration hold: 2.480 seconds
- ten-clip alternative: narration would overhang 50.000 seconds by 2.520 seconds
- short-tail exception: unavailable because 2.520 seconds exceeds the 1.000-second maximum
- requested maximum: 49.000 seconds
- contract variance: +3.520 seconds of narration, or +6.000 seconds of 5-second picture slots

The timing is approved for the 11-clip rapid-cut shot plan. Any later narration or voice change invalidates this map and all downstream timing artifacts.
