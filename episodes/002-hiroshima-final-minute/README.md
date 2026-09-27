# Episode 002 — Hiroshima: Final Minute

## Status

- lifecycle: production
- production profile: `h3-short-5s-16step-continuity`
- source verification: complete for the stated time and casualty estimate
- supplied Spanish narration: preserved
- voice file: external/not supplied
- word timestamps: archived, 122 tokens, 00:00.460–01:24.520
- shot plan: rebuilt around explicit cross-clip story states
- image prompts: nine exact generator-ready single-scene anchor prompts
- generated references: nine visually reviewed single-scene r001 anchors
- video prompts: 17 generator-ready, precisely timed files
- automation jobs: 17 sequential r003 jobs using fixed seeds and 16 sampling steps
- completed r003 batch: `2ad1371c-ff73-45e2-82cd-8c3b81be66f7`; all 17 jobs succeeded
- targeted Clip 17 correction: r004 job `dd6d58e4-5d11-4cf5-bee9-0f4a81178942`, visually reviewed and accepted
- prior renders: r001 rejected/incomplete; r002 retained for diagnosis and not approved
- final master: not produced; `renders/final-selected/` is ready for one approved take per clip

## Production contract

- timeline: 85.000 seconds, 17 × 5.000-second editorial slots
- narration language: Spanish
- generator language: English
- generator: MiniMax H3 `h3_ref2va`
- source render: 480×864, 24 fps, 124 raw frames, native audio
- editorial render: exactly 5.000 seconds, no time stretch
- sampling: 16 steps, `res_multistep`, `beta`, Lightning disabled
- references: one generation-safe single-scene anchor normally; two only for Clip 12
- execution: sequential GPU concurrency 1; continue safely after clip failure; transient retry maximum 2
- first pass: no concat, no FlashVSR, no final master
- content: restrained non-graphic historical depiction; no generated text, narration, dialogue, or music
- edit grammar: three to four readable timed shots per clip, one primary action per shot, resolved ending frame
- continuity grammar: recurring-character clips declare the exact inherited start state and the end state passed to the next character clip

## Generation-safe r003 references

1. `assets/episodes/002-hiroshima-final-minute/references/city-morning-anchor-r001.png`
2. `assets/episodes/002-hiroshima-final-minute/references/breakfast-couple-anchor-r001.png`
3. `assets/episodes/002-hiroshima-final-minute/references/couple-window-anchor-r001.png`
4. `assets/episodes/002-hiroshima-final-minute/references/b29-crossing-anchor-r001.png`
5. `assets/episodes/002-hiroshima-final-minute/references/bomb-release-anchor-r001.png`
6. `assets/episodes/002-hiroshima-final-minute/references/falling-object-anchor-r001.png`
7. `assets/episodes/002-hiroshima-final-minute/references/couple-departure-anchor-r001.png`
8. `assets/episodes/002-hiroshima-final-minute/references/couple-flash-anchor-r001.png`
9. `assets/episodes/002-hiroshima-final-minute/references/aftermath-anchor-r001.png`

The original shared style, world, character, and vehicle sheets remain design sources. They are deliberately not sent directly to H3 in r003 because their multi-panel layouts caused sheet copying, repeated characters, and narrative leakage. `<Picture N>` always maps exactly to array item N in the corresponding job JSON.

## Artifact inventory

- supplied timing source: `timestamps/word-timestamps.csv`
- exact narration reconstruction: `script/narration-es.md`
- verification and scope: `source/research-notes.md`
- continuity plan: `plan/shot-plan.md`
- exact image prompts: `../../prompts/image/episodes/002-hiroshima-final-minute/*.md`
- video prompts: `prompts/clip-01-*.md` through `prompts/clip-17-*.md`
- service settings: `automation/service-config.json`
- independent jobs: `automation/jobs/clip-01-*.json` through `clip-17-*.json`
- targeted retry: `automation/retries/clip-17-aftermath-r004.json`
- selection and assembly: `renders/final-selected/` and `automation/assemble-final-selected.sh`
- targeted render review: `renders/review-r003.md`

## Review gate

Review every r003 source clip for story state, character count, identity, aircraft physics, timing, text, audio, and final-frame stability before final selection. Use the accepted r004 replacement for Clip 17 instead of r003. After placing exactly one approved take for every number 01–17 in `renders/final-selected/`, run `automation/assemble-final-selected.sh`. Generated references are selected production inputs, not locked shared assets.
