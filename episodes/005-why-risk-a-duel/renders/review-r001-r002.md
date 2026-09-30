# Review of episode 005 r001 and r002

User review on 2026-09-30 rejects both complete 11-clip variants as final selections.

## Shared failures

- `audio_music`: most clips contain audible background music. The `music:false` job field and earlier prompt wording did not prevent it.
- `duel_aim`: some duelists point pistols upward or away instead of directly toward the opposing chest.
- `duel_distance`: duelists frequently stand too close, especially in scenes that do not end with a handshake.

## Replacement decision

Decision for all 22 candidates: `revise_prompt`; duel clips additionally require `revise_reference`.

The r003 prompt set adds an absolute audio contract to all eleven clips. It permits only named dry sub-0.35-second Foley separated by silence and explicitly bans every musical, tonal, rhythmic, ambient, and vocal layer. Jobs add an independent `audio.prompt_suffix` with the same failure gate.

Four immutable r002 scene anchors replace close or lowered-weapon compositions: S01, S04, S06, and S09. Each locks at least 45 percent clear frame width between opponents and horizontal barrel aim directly at the opposing chest. Handshake approaches occur only after both weapons are safely lowered.
