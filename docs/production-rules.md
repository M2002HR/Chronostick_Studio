# Permanent production rules

These rules apply to every ChronoStick episode unless a documented, approved decision explicitly supersedes one of them.

## Content and historical integrity

- Preserve the story's factual meaning while optimizing narration for a Spanish-language YouTube Short.
- Separate documented history from folklore, legend, or uncertain claims. Use qualifying language such as “según la historia popular” when needed.
- Do not imply causation when the source only establishes chronology or correlation.
- Store research, citations, and fact-check notes under the episode's `source/` directory; never place them in generator prompts.
- Do not invent missing source material, timestamps, approved prompts, render results, or review decisions.

## Narration

- Rewrite the English source into natural spoken Spanish, not literal translation.
- Optimize the hook, retention, pacing, payoff, ending, and CTA without changing the historical claim.
- Read the Spanish aloud or otherwise review it for natural rhythm before voice generation.
- Keep production instructions in English unless a generator performs better with another language.

## Asset reuse

Evaluate assets in this order: master style, existing world, recurring character, episode-specific prop, then new asset.

- Reuse a locked asset if its identity and period fit.
- Create only what the shot plan truly needs.
- A reference sheet represents one exact character; different views, poses, and expressions are not different people.
- Preserve head shape, hair silhouette, costume silhouette, colors, proportions, and signature accessories.
- When complexity must be reduced, simplify background detail before character identity.

## Prompt separation

Generator-facing prompt files contain only the final paste-ready prompt. Put rationale and rules in `docs/`, planning in `plan/`, status in the episode `README.md`, and attempts/results in `logs/`.

## Review gates

An artifact may move from `draft` to `locked` or `approved` only after review. Check:

- historical meaning and qualification
- narrative timing and clarity
- character and style consistency
- reference count and correct paths
- profile-defined framing and clip boundaries
- readable ending state
- absence of generated text and background music
- stable output at Shorts viewing size

Random model failure does not automatically require a prompt revision. Retry the same prompt when the specification is still correct; revise text only when the instruction itself is deficient.
