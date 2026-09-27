# ChronoStick modular skills

| Skill | Production responsibility |
| --- | --- |
| `chronostick-pipeline` | Inspect state, choose the next valid stage, and coordinate handoffs |
| `chronostick-script` | Rewrite title/source into a high-retention 40–60 second narration |
| `chronostick-timestamps` | Preserve and validate word timestamps; build the timing map |
| `chronostick-shot-plan` | Direct five-second clips and produce continuity/reference plans |
| `chronostick-references` | Create full-frame, single-scene stick-world reference prompts/assets |
| `chronostick-clip-prompts` | Write pure, controlled H3 prompts with timed cuts and SFX |
| `chronostick-generation-jobs` | Build 14-step deterministic job JSON and batch settings |
| `chronostick-batch` | Readiness, atomic preflight, authorized launch, monitoring, reports |
| `chronostick-review` | Creative/technical QC and replacement planning |
| `chronostick-finish` | Approved selection, concat, and framewise 1080×1920 upscale |
| `chronostick-youtube` | Prompt-first thumbnail design, optional authorized generation, metadata, and closeout |

Each directory is a self-contained Codex skill with `SKILL.md` and `agents/openai.yaml`. The source of truth remains in this repository. Run `scripts/install-local-skills.sh` to link them into the local Codex skill directory and `scripts/validate-skills.sh` to validate all packages.
