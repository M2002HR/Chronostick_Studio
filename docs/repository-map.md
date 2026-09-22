# Repository map

## Active documentation

`AGENTS.md` is the entry point for AI collaborators. `README.md` is the human overview. Files directly under `docs/` are active rules. `docs/specs/` contains detailed internal design specifications. `docs/archive/` contains historical briefs and must not override active rules.

## Prompt boundary

Only these locations contain paste-ready generation input:

- `prompts/image/` for shared style, character, and world image prompts
- `episodes/<episode>/prompts/` for final video prompts

An empty prompt file means the final text is unavailable. It is not a request to infer or regenerate an approved prompt.

## Asset boundary

`assets/` holds reusable approved or candidate reference media. Episode outputs belong in the episode's `renders/` and `final/` directories. `assets/episodes/` is reserved for episode-specific reusable reference media, not final exports.

## Episode contract

Every episode directory contains:

- `README.md`: manifest, state, dependencies, missing material
- `source/`: input story, evidence, citations
- `script/`: approved narration text
- `audio/`: voice assets or a local manifest
- `timestamps/`: timing derived from approved audio
- `plan/`: production and shot plans
- `prompts/`: final generator-facing prompts only
- `renders/`: generated clip revisions
- `final/`: assembled exports

## Internal specification boundary

Detailed design rationale, metadata, approval fields, review checklists, and historical notes belong in `docs/specs/`. They may be long. Their corresponding files in `prompts/image/` must contain only the extracted generation prompt.
