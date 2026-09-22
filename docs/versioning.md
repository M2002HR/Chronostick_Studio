# Naming and versioning

## Text files

Git history is the version system. Use stable semantic names and do not add `final`, `final2`, `new`, or dates solely to simulate versions.

For specs with explicit lifecycle metadata:

- `0.x.y`: draft or actively changing
- `1.0.0`: first approved locked definition
- major: intentional compatibility-breaking identity or design change
- minor: compatible production addition
- patch: clarification that does not alter the intended output

## Generated media

Use monotonically increasing three-digit revisions and never overwrite:

```text
character-name-sheet-r001.png
clip-01-hook-r001.mp4
episode-001-master-r001.mp4
```

A revision number identifies an attempt, not approval. Record approval separately in the relevant spec, episode manifest, or generation log.

## IDs and paths

- episode directory: `NNN-lowercase-hyphenated-slug`
- clip prompt: `clip-NN-lowercase-hyphenated-purpose.md`
- shared assets: descriptive lowercase names ending in `-rNNN.ext`
- no duplicated extensions
- no repeated path segments such as `assets/worlds/assets/worlds`

## Commit intent

Prefer one coherent production decision per commit. Useful prefixes include `feat`, `refactor`, `docs`, `fix`, `lock`, and `chore`. Do not amend or rewrite shared history unless explicitly requested.
