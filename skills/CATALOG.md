# ChronoStick modular skills

| Skill | Production responsibility |
| --- | --- |
| `chronostick-pipeline` | Inspect state, choose the next valid stage, and coordinate handoffs |
| `chronostick-transcribe` | Ajil extraction of actual reference/accepted-voice speech with preserved word and segment timing |
| `chronostick-voice-direction` | Required Google Vids paste input when selected; registered tags, expressive delivery and unchanged narration |
| `chronostick-reference-video` | Actual-footage and timed-transcript analysis, factual correction and engine-aware adaptation |
| `chronostick-storyboard` | Actual neutral rough sketches for user scenario/composition review before production design |
| `chronostick-script` | Original profile-sized narration and scenario; new reference Shorts default to Spanish and 20–30 seconds |
| `chronostick-longform-visual-direction` | Extract reusable ideas from historical-video examples and direct an original long-form visual blueprint |
| `chronostick-longform-pipeline` | Route and resume a full 10–15 minute episode with truthful gates |
| `chronostick-longform-script` | Verify claims, architect chapters, and write faithful Spanish narration |
| `chronostick-longform-timing` | Preserve accepted voice/timestamps and derive chapter/slot timing |
| `chronostick-longform-shot-plan` | Direct timed chapters, shots, continuity, maps, text and references |
| `chronostick-longform-assets` | Build landscape identities, worlds, maps and generation-safe anchors |
| `chronostick-longform-prompts` | Write pure five-second 16:9 H3 prompts from approved coverage |
| `chronostick-longform-jobs` | Prepare deterministic 14-step landscape jobs and full preflight |
| `chronostick-longform-review` | Review video/audio/maps/text and plan targeted replacements |
| `chronostick-longform-finish` | Assemble, upscale and finish reviewed landscape masters |
| `chronostick-longform-youtube` | Package accurate 16:9 thumbnail, chapters and metadata |
| `chronostick-timestamps` | Preserve and validate word timestamps; build the timing map |
| `chronostick-shot-plan` | Direct profile-sized clips and produce continuity/reference plans |
| `chronostick-references` | Create full-frame, single-scene stick-world reference prompts/assets |
| `chronostick-clip-prompts` | Write pure, controlled H3 prompts with timed cuts and SFX |
| `chronostick-generation-jobs` | Build deterministic job JSON; new reference-first Shorts use 16 steps and dynamic editorial durations |
| `chronostick-batch` | Readiness, atomic preflight, authorized launch, monitoring, reports |
| `chronostick-review` | Creative/technical QC and replacement planning |
| `chronostick-sfx` | Prefer clean engine SFX; review and synchronize recorded independent SFX only when native sound fails |
| `chronostick-finish` | Approved selection, concat, and framewise 1080×1920 upscale |
| `chronostick-youtube` | Prompt-first thumbnail design, optional authorized generation, metadata, and closeout |
| `chronostick-localize` | New-language script, cue-level voice, real timestamps, and fixed-picture release |

Each directory is a self-contained Codex skill with `SKILL.md` and optional UI metadata in `agents/openai.yaml`. The source of truth remains in this repository. Run `scripts/install-local-skills.sh` to link them into the local Codex skill directory and `scripts/validate-skills.sh` to validate all packages.
