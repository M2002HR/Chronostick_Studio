# ChronoStick Studio

ChronoStick Studio is a repeatable production system for short historical videos in a detailed cinematic stick-figure style. The repository separates permanent production knowledge, locked visual specifications, paste-ready prompts, episode work, media assets, and logs so a new collaborator can continue without relying on chat history.

## Start here

For a new human or AI collaborator:

1. Read [AGENTS.md](AGENTS.md).
2. Follow [the production workflow](docs/workflow.md).
3. Apply the [permanent production rules](docs/production-rules.md).
4. Read the target episode's `README.md` and shot plan.
5. Reuse approved assets before creating new ones.

## Repository layout

```text
assets/                         Approved and revisioned binary media
  styles/                       Master style references
  worlds/                       World/environment references
  characters/                   Character identity sheets
  vehicles/                     Vehicle and machine references
  episodes/                     Episode-specific reusable media
docs/                           Active rules and internal knowledge
  specs/                        Detailed locked style/world/character specs
  templates/                    Internal planning templates
  archive/                      Historical instructions; not active rules
prompts/image/                  Paste-ready image-generation prompts only
episodes/<id-slug>/             Complete episode workspace
  source/                       Source story and research
  script/                       Narration scripts
  audio/                        Voice inputs or manifests
  timestamps/                   Word-level timing data
  plan/                         Shot plan and production blueprint
  prompts/                      Paste-ready video prompts only
  automation/                   Service config, batch defaults, and job JSON
  renders/                      Revisioned generated clips
  final/                        Final assembled exports
logs/                           Cross-project generation records
```

## Current production state

Episode 001 is the reference implementation. Its final video was produced externally, but only the successful prompts for Clips 01 and 02 were retained. Clips 03–06 intentionally remain empty and must not be presented as recovered or approved prompts. See [Episode 001 status](episodes/001-potato-france/README.md).

## Core principles

- Documentation and generator-facing prompts are separate layers.
- The master style controls rendering; character sheets control identity.
- Clip duration, engine settings, and reference limits come from the episode's named production profile; every clip remains visually complete.
- Fast pacing comes from cuts and framing changes, not chaotic motion.
- No background music; only narration and natural diegetic sound effects.
- Git versions text; `-rNNN` versions generated media.

The migration brief that established this structure is preserved in `docs/archive/` for provenance and is not an active runbook.

## Validate before commit or push

Run:

```bash
./scripts/validate-repo.sh
```

The validator checks prompt purity, the mandatory audio sentence, malformed asset paths, referenced asset existence, automation JSON, prompt/reference mapping, profile settings, and whitespace errors. Empty archived prompts produce warnings because they are intentional documented gaps.
