# Episode 001 — Potato France

This episode is the historical reference project for the ChronoStick workflow.

## Status

- lifecycle: completed externally; repository archive is partial
- final video: `final/papa_2_erasio.mp4` is present locally as an externally supplied 1080×1920 H.264/AAC export; it has not been reviewed or approved in this repository
- English source: unavailable; `source/source-en.md` is intentionally empty
- Spanish narration: recovered from the shot plan and stored in `script/narration-es.md`
- voice audio: unavailable in the repository
- word-level timestamps: unavailable; `timestamps/word-timestamps.csv` is intentionally empty
- shot plan: detailed archived working plan, not formally locked
- Clip 01 prompt: available
- Clip 02 prompt: available
- Clip 03–06 prompts: unavailable and intentionally empty
- generated clip renders: unavailable in the repository
- YouTube thumbnail: r002 candidate at `delivery/youtube/thumbnail-r002.png`; assistant QC passed, user approval pending; r001 retained immutably
- YouTube metadata: `delivery/youtube/metadata.json` and `metadata.md` prepared provisionally; audience, age restriction, related video, and final-master approval remain operator decisions
- YouTube upload/publication: not authorized and not performed

## YouTube delivery status

- thumbnail prompt revision: `delivery/youtube/thumbnail-prompt-r002.md`
- thumbnail generation authorization: authorized by the user's 2026-09-27 request to regenerate Episodes 001 and 002
- generated source: `delivery/youtube/thumbnail-source-r002.png` (`sha256:58898f625d052db8230ba918c1a3405b478761047db3a7ba1899aafb517acac9`)
- thumbnail delivery master: `delivery/youtube/thumbnail-r002.png`, 2160×3840 (`sha256:830cb6e4ae79558fec7a1413cb3e8f4c90af205026722160cf136f9807c93e2b`)
- typography: locked channel lettering system derived from Episode 002; generated inside the artwork with no separate overlay
- thumbnail review: assistant QC passed; user approval pending; not locked
- metadata revision: stable files `delivery/youtube/metadata.json` and `metadata.md`; assistant technical validation passed, operator review pending
- distribution-master candidate: `final/papa_2_erasio.mp4` (`sha256:f3921736e351517cd09a1b4db02d57b892fc0d732699bd715ef9c06c1dede2c1`); review/approval pending
- external Google Vids finishing: no Google Vids finishing artifact or status is recorded; not treated as complete
- publication status: not uploaded; no visibility or publication action authorized

Do not infer that an empty file is approved content. Do not reconstruct missing prompts and call them the originals.

## Production contract

- format: 60-second YouTube Short
- frame: vertical 9:16
- generation: six independent 10-second Omni clips
- narration language: Spanish
- production/prompt language: English
- maximum references per generation: 3
- inherited visual system: `CST-STYLE-001@1.0.0`
- inherited world: `CST-WORLD-001@1.0.0`

## Approved reusable references

- style: `assets/styles/style-detailed-cinematic-stick-history-r001.png`
- world: `assets/worlds/world-france-late-18c-r001.png`
- male villager: `assets/characters/french-villager-male/character-french-villager-male-sheet-r001.png`
- female villager: `assets/characters/french-villager-female/character-french-villager-female-sheet-r001.png`
- Parmentier character: `assets/characters/antoine-parmentier/character-antoine-parmentier-sheet-r001.png`
- guard: `assets/characters/french-guard/character-french-guard-sheet-r001.png`

## Prompt inventory

| Clip | Purpose | Prompt status |
|---|---|---|
| 01 | Hook: hunger and potato rejection | Preserved generator prompt |
| 02 | Restriction and researcher | Preserved generator prompt |
| 03 | Field and armed guards | Missing; empty by design |
| 04 | Night theft | Missing; empty by design |
| 05 | Tasting and acceptance | Missing; empty by design |
| 06 | Revolution transition and ending | Missing; empty by design |

The full internal working specifications for Clips 01 and 02 are retained under `docs/specs/episodes/001-potato-france/`. The files in this episode's `prompts/` directory contain generator-facing text only.

## Historical guardrail

The revolutionary sequence is a chronological transition. It must never imply that potatoes caused the French Revolution. The nighttime theft is presented as popular history and therefore uses explicit qualifying language.

## Audio policy

No background music. The final assembly uses separately recorded narration and may use natural diegetic effects only.

## If this archive is resumed

Treat any Clip 03–06 prompt as a newly authored draft derived from `plan/shot-plan.md`, not as a recovered final prompt. Add missing source, citations, audio, timestamps, renders, and final exports only when the actual artifacts are available.
