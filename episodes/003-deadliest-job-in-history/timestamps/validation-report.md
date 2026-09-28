# Timestamp validation report

## Decision

- status: approved
- operator confirmation: the user supplied this CSV as the revised voice timestamps and requested a freeze-frame tail instead of a tenth generated clip
- approved timing scope: the 119-word spoken narration body
- title handling: `¿El trabajo más mortal de la historia?` remains unchanged in the script and is excluded from spoken timing coverage

## Source preservation

- supplied file: `/home/mhr/Downloads/Untitled video (2)-timestamps-2026-09-27T20-09-30.csv`
- archived file: `timestamps/word-timestamps-source.csv`
- SHA-256: `bed0bbe65781ee315e1e760c0994c60a7790dc5fca396264e78537dd1e85a69d`
- source preservation: byte-for-byte identical
- encoding: UTF-8 with BOM
- columns: `index,word,start,end,duration,probability`

## Structural validation

- data rows / tokens: 119
- index sequence: continuous from 1 through 119
- empty word tokens: 0
- duplicate indices: 0
- duplicate rows: 0
- negative timestamps: 0
- end-before-start rows: 0
- duration arithmetic errors above 0.001 seconds: 0
- probability values: absent in all 119 rows; not required for timing use
- first spoken word starts: 0.320 seconds
- final spoken word ends: 45.640 seconds
- spoken span: 45.320 seconds

## Text coverage

After Unicode, case, and punctuation-only normalization, all 119 CSV tokens match the approved Spanish narration body in order. There are no missing, added, or changed spoken words. The user-confirmed non-spoken title is the only excluded script text.

Non-lexical transcription differences include punctuation spacing, transcript lowercasing of `Guerra Civil`, removal of the script's em dashes around `sorpresa, sorpresa`, and the CSV's emphatic `¡Suscríbete!` punctuation for script text `Suscríbete.`

## Source timing overlaps and gaps

The original CSV contains four overlaps. They remain unchanged:

| Previous / current token | Previous end | Current start | Overlap |
| --- | ---: | ---: | ---: |
| 18 / 19 | 7.200 | 6.780 | 0.420 s |
| 35 / 36 | 14.200 | 14.020 | 0.180 s |
| 97 / 98 | 35.500 | 35.020 | 0.480 s |
| 110 / 111 | 40.960 | 40.860 | 0.100 s |

There are three positive inter-word gaps: 0.780 seconds between tokens 53 and 54, 0.600 seconds between tokens 70 and 71, and 0.260 seconds between tokens 83 and 84. The timeline also has 0.320 seconds of leading silence.

No normalized CSV was created. Shot-planning slot membership is computed directly from the preserved source intervals.

## Editorial derivation

- default ceiling rule: `ceil(45.640 / 5) = 10` generated clips
- approved short-tail exception: enabled because the overhang is no more than 1.000 second and contains only the end of the CTA
- generated clips: 9 × 5.000 seconds = 45.000 seconds
- freeze-last-frame extension: 45.000–45.640 seconds = 0.640 seconds
- final editorial duration: 45.640 seconds
- generated SFX during extension: silence
- external narration: continues normally through 45.640 seconds
- derived map: `timestamps/timing-map.json`

The final shot plan must resolve Clip 09 before 45.000 seconds and hold a freeze-safe final composition. No tenth generated clip is required.
