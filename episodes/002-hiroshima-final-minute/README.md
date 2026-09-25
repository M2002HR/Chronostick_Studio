# Episode 002 — Hiroshima: Final Minute

## Status

- lifecycle: production
- production profile: `h3-short-5s`
- source verification: complete for the stated time and casualty estimate
- supplied Spanish narration: preserved
- voice file: external/not supplied
- word timestamps: archived, 122 tokens, 00:00.460–01:24.520
- shot plan: complete
- prompts: 17 generator-ready files
- automation jobs: 17 independently runnable JSON files plus batch defaults
- renders: batch pending/running; inspect `automation/run-state.json` when present
- final master: intentionally not produced in this pass

## Production contract

- timeline: 85.000 seconds, 17 × 5.000-second editorial slots
- narration language: Spanish
- generator language: English
- generator: MiniMax H3 `h3_ref2va`
- source render: 480×864, 24 fps, 124 raw frames, native audio
- editorial render: exactly 5.000 seconds, no time stretch
- sampling: 12 steps, `res_multistep`, `beta`, Lightning disabled
- execution: sequential GPU concurrency 1; continue safely after clip failure; transient retry maximum 2
- first pass: no concat, no FlashVSR, no final master
- content: restrained non-graphic historical depiction; no generated text, narration, dialogue, or music

## Canonical assets

1. `assets/styles/style-detailed-cinematic-stick-history-r001.png`
2. `assets/worlds/world-hiroshima-summer-1945-r001.png`
3. `assets/characters/hiroshima-elder-female/character-hiroshima-elder-female-sheet-r001.png`
4. `assets/characters/hiroshima-elder-male/character-hiroshima-elder-male-sheet-r001.png`
5. `assets/vehicles/vehicle-b29-hiroshima-r001.png`

The ordered reference list is clip-specific. `<Picture N>` always means array item N in the corresponding job JSON.

## Artifact inventory

- supplied timing source: `timestamps/word-timestamps.csv`
- exact narration reconstruction: `script/narration-es.md`
- verification and scope: `source/research-notes.md`
- production plan: `plan/shot-plan.md`
- generator prompts: `prompts/clip-01-*.md` through `prompts/clip-17-*.md`
- service settings: `automation/service-config.json`
- batch defaults: `automation/jobs/defaults.json`
- independent jobs: `automation/jobs/clip-01-*.json` through `clip-17-*.json`

## Review gate

Approve the 0.4 MP source clips individually before any concat, upscale, captioning, narration mix, or final export.
