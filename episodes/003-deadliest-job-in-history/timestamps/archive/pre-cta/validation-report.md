# Timestamp validation report

## Lifecycle notice

This timing set was valid for the approved 45.500-second narration body, but it was superseded on 2026-09-27 when the user requested a new subscription CTA. Preserve it for provenance; do not use it for the current shot plan. A new timing set from the revised voice is required.

## Decision

- status: superseded
- operator confirmation: the user supplied this CSV as the episode timestamps and confirmed that the first line of `script/narration-es.md` is the non-spoken title
- approved timing scope: the 116-word spoken narration body
- title handling: `¿El trabajo más mortal de la historia?` remains unchanged in the script and is excluded from spoken timing coverage

## Source preservation

- supplied file: `/home/mhr/Downloads/Untitled video (1)-timestamps-2026-09-27T19-54-50.csv`
- archived file: `timestamps/archive/pre-cta/word-timestamps-source.csv`
- SHA-256: `089b42d16943e71348634e5ae2c90ad44d17845533074c0ac2129d3ab733704c`
- source preservation: byte-for-byte identical
- encoding: UTF-8 with BOM
- columns: `index,word,start,end,duration,probability`

## Structural validation

- data rows / tokens: 116
- index sequence: continuous from 1 through 116
- empty word tokens: 0
- duplicate indices: 0
- duplicate rows: 0
- negative timestamps: 0
- end-before-start rows: 0
- duration arithmetic errors above 0.001 seconds: 0
- probability values: absent in all 116 rows; not required for timing use
- first spoken word starts: 0.360 seconds
- final spoken word ends: 45.500 seconds
- spoken span: 45.140 seconds

## Text coverage

After Unicode, case, and punctuation-only normalization, all 116 CSV tokens match the approved Spanish narration body in order. There are no missing, added, or changed spoken words. The only excluded text is the user-confirmed non-spoken title on the first line of the script.

Non-lexical transcription differences are:

- the script writes `8,9 %,` while the CSV token is `8,9%,`
- the script capitalizes `Guerra Civil`; the CSV uses `guerra civil`
- the script uses em dashes around `sorpresa, sorpresa`; the CSV represents the phrase without dashes
- the script ends with an ellipsis; the CSV ends the final token with a period

## Source timing overlaps and gaps

The original CSV contains five overlaps. They remain unchanged:

| Previous / current token | Previous end | Current start | Overlap |
| --- | ---: | ---: | ---: |
| 18 / 19 | 7.020 | 6.860 | 0.160 s |
| 35 / 36 | 14.580 | 14.100 | 0.480 s |
| 54 / 55 | 20.500 | 20.380 | 0.120 s |
| 97 / 98 | 37.360 | 36.900 | 0.460 s |
| 110 / 111 | 42.880 | 42.760 | 0.120 s |

There are two positive inter-word gaps: 0.200 seconds between tokens 70 and 71, and 0.060 seconds between tokens 83 and 84. The timeline also has 0.360 seconds of leading silence.

No normalized CSV was created. The shot-planning timing map computes slot membership directly from source interval overlap, so destructive or cosmetic normalization is unnecessary.

## Editorial derivation

- slot duration: 5.000 seconds
- clip count: `ceil(45.500 / 5) = 10`
- editorial duration: 50.000 seconds
- narration tail hold: 45.500–50.000 seconds, totaling 4.500 seconds
- derived map: `timestamps/timing-map.json`
