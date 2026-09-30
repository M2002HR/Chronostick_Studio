# Episode 005 two-seed generation queue

The persistent queue submits two complete 11-clip MiniMax H3 batches sequentially: `r001`, then `r002`. Prompt text, reference order, generation settings, and output geometry are identical across both variants. Only the deterministic fixed seed differs. Each job uses 14 steps, produces an immutable raw render plus an exact 5.000-second editorial copy, requests SFX-only audio, and disables automatic concatenation and upscaling.

Runtime state is stored in `automation/queue-state.json`. Each submitted variant records its batch ID and submission marker inside `automation/variants/<revision>/`. The queue refuses duplicate submission when a marker exists.

Generation success is a technical result only. Every candidate still requires frame, motion, continuity, audio, and stream review before any final selection.
