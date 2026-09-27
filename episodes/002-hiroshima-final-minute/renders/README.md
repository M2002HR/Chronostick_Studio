# Render layout

- `raw/`: immutable 124-frame H3 outputs and provenance sidecars
- `editorial/`: exact 5.000-second normalized copies and provenance sidecars
- `final-selected/`: exactly one human-selected video for each clip number 01–17; no sidecars are required here

Generated media and runtime sidecars remain local and are ignored by Git. Never overwrite a revision; advance `-rNNN` after a reviewed prompt change or when an existing target is present.

Natural filename order controls final assembly. Keep selected filenames in the form `clip-NN-description-rNNN.ext`, with exactly one file for every number 01–17. Run `automation/assemble-final-selected.sh`; it rejects missing or duplicate numbers and writes the next unused final revision under `final/` without overwriting an earlier master.

Revision r001 clips 01–02 are rejected diagnostic artifacts. Revision r002 and r003 remain immutable review sources. Clip 17 r004 is the reviewed and accepted targeted correction; use it instead of Clip 17 r003 in `final-selected/`.
