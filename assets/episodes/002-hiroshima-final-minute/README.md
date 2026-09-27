# Episode 002 asset map

The shared multi-panel style, world, character, and vehicle assets remain the design source of truth. For r003, nine single-scene references were generated from exact prompts and visually checked before being assigned to H3 jobs:

- city morning: `references/city-morning-anchor-r001.png`
- breakfast couple: `references/breakfast-couple-anchor-r001.png`
- couple at window: `references/couple-window-anchor-r001.png`
- B-29 crossing: `references/b29-crossing-anchor-r001.png`
- bomb release: `references/bomb-release-anchor-r001.png`
- falling object: `references/falling-object-anchor-r001.png`
- couple departure: `references/couple-departure-anchor-r001.png`
- couple and first white light: `references/couple-flash-anchor-r001.png`
- restrained aftermath: `references/aftermath-anchor-r001.png`

The exact generation prompts are stored under `prompts/image/episodes/002-hiroshima-final-minute/`. Each image is a 941×1672 vertical PNG, contains one continuous composition, and was selected only after checking for panel borders, duplicated foreground subjects, identity separation, relevant historical content, and absence of readable generated text.

These are episode production inputs and are not marked as shared locked assets. Existing files were not overwritten; every new image uses revision `r001` in its own episode-scoped path.
