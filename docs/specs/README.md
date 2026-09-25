# Specification registry

Specifications contain internal design knowledge, metadata, historical notes, review criteria, and approval state. They are not pasted into generation models. Use the corresponding file under `prompts/image/` for generation.

## Locked shared specifications

| ID | Specification | Approved reference | Generator prompt |
|---|---|---|---|
| CST-STYLE-001@1.0.0 | `styles/style-detailed-cinematic-stick-history.md` | `assets/styles/style-detailed-cinematic-stick-history-r001.png` | `prompts/image/styles/style-detailed-cinematic-stick-history.md` |
| CST-WORLD-001@1.0.0 | `worlds/world-france-late-18c.md` | `assets/worlds/world-france-late-18c-r001.png` | `prompts/image/worlds/world-france-late-18c.md` |
| CST-CHAR-001@1.0.0 | `characters/character-french-villager-male.md` | `assets/characters/french-villager-male/character-french-villager-male-sheet-r001.png` | `prompts/image/characters/character-french-villager-male.md` |
| CST-CHAR-002@1.0.0 | `characters/character-french-villager-female.md` | `assets/characters/french-villager-female/character-french-villager-female-sheet-r001.png` | `prompts/image/characters/character-french-villager-female.md` |
| CST-CHAR-003@1.0.0 | `characters/character-antoine-parmentier.md` | `assets/characters/antoine-parmentier/character-antoine-parmentier-sheet-r001.png` | `prompts/image/characters/character-antoine-parmentier.md` |
| CST-CHAR-004@1.0.0 | `characters/character-french-guard.md` | `assets/characters/french-guard/character-french-guard-sheet-r001.png` | `prompts/image/characters/character-french-guard.md` |
| CST-WORLD-002@1.0.0 | `worlds/world-hiroshima-summer-1945.md` | `assets/worlds/world-hiroshima-summer-1945-r001.png` | supplied reference; no image prompt |
| CST-CHAR-005@1.0.0 | `characters/character-hiroshima-elder-female.md` | `assets/characters/hiroshima-elder-female/character-hiroshima-elder-female-sheet-r001.png` | supplied reference; no image prompt |
| CST-CHAR-006@1.0.0 | `characters/character-hiroshima-elder-male.md` | `assets/characters/hiroshima-elder-male/character-hiroshima-elder-male-sheet-r001.png` | supplied reference; no image prompt |
| CST-VEHICLE-001@1.0.0 | `vehicles/vehicle-b29-hiroshima.md` | `assets/vehicles/vehicle-b29-hiroshima-r001.png` | supplied reference; no image prompt |

All paths in this table are relative to the repository root.

## Episode working specifications

`episodes/001-potato-france/` contains the historical internal working specifications for Clips 01 and 02. Their metadata and checklists are retained for learning; the clean generator prompts live in the episode prompt directory.

Before modifying a locked shared specification, create a deliberate versioned design decision. Do not casually edit identity-defining features after downstream episodes depend on them.
