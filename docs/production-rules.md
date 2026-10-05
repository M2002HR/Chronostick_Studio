# Permanent production rules

These rules apply to every ChronoStick episode unless a documented, approved decision explicitly supersedes one of them.

## Content and historical integrity

- Preserve the story's factual meaning while optimizing narration for the episode's named Spanish-language format.
- Separate documented history from folklore, legend, or uncertain claims. Use qualifying language such as “según la historia popular” when needed.
- Do not imply causation when the source only establishes chronology or correlation.
- Store research, citations, and fact-check notes under the episode's `source/` directory; never place them in generator prompts.
- Do not invent missing source material, timestamps, approved prompts, render results, or review decisions.

## Narration

- Rewrite the English source into natural spoken Spanish, not literal translation.
- Optimize the hook, retention, pacing, payoff, ending, and CTA without changing the historical claim.
- For new narration, append a tiny spoken subscribe CTA after the payoff by default: Spanish `Suscríbete.` or the brief target-language equivalent. Say only subscribe; match its delivery to the story's mood and fit it within the duration target. An explicit user opt-out overrides this default. This does not authorize a generated text/button scene or change existing approved masters.
- Aim for a vivid, surprising and emotionally engaging delivery in both Shorts and long-form. Use wit, irony and occasional visual humor when the documented situation supports them; let a joke clarify a fact or character choice. Do not invent events or dialogue for a punchline, make victims or suffering the joke, or let a gag obscure a qualification or human consequence.
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
- absence of unapproved generated text and generated background music; external
  finishing tracks follow the explicit mix in `docs/postproduction.md`
- stable output at the target format's viewing sizes

Random model failure does not automatically require a prompt revision. Retry the same prompt when the specification is still correct; revise text only when the instruction itself is deficient.

## YouTube delivery copy (from Episode 003 onward)

- Shorts titles aim for roughly 30 characters, normally 25–35 including spaces and punctuation: a few words and a truthful immediate hook. Record counts for the primary and two alternative titles. Long-form does not inherit this length target.
- Prepare about 15 relevant, unique Studio tags (default 15; normally 12–18), covering topic, people/places, useful spelling variants, related search phrases, niche and channel identity. Save the JSON array and a comma-separated Markdown copy; verify count and current field length limit. Avoid unrelated filler.
- All title variants stay free of hashtags, appended tags, and keyword lists. Studio tags remain a separate field. Review every variant for an explicit subject, truthful emotion/curiosity, and immediately understandable wording; preserve enough context to identify the topic.
- Use a focused main hashtag pool grouped by episode topic, history/animation niche, and format-appropriate broad discovery. The description ends with a smaller exact subset, usually 3–5 covering the three groups. Shorts may use `#Shorts`, `#YouTubeShorts`, and `#ViralShorts`; long-form uses relevant long-form terms.
- Write public descriptions and comments casually in the release language. Weave relevant search terms into sentences. Claim current trend status only with dated, locale-specific evidence; otherwise record them as SEO candidates. Preserve historical qualifications and citations. Put the main exact search phrase and relevant supporting phrases/names inside the first 200 characters of the actual description; count spaces and punctuation, verify complete phrase matches, and record the excerpt/matches in `description_opening_check`. Choose an explicit `seo_target_keyword` and verify the complete same phrase in the title, a Studio tag and the first 200 characters; related-word matches alone are insufficient. Compare Unicode NFC/casefold without changing accents or word forms. Keep JSON, Markdown and a public-copy-only `delivery/youtube/description.txt` identical. Record local phrase matches separately from the external vidIQ result; do not mark that external check passed unless observed.
- Every Shorts and long-form package includes three pinned-comment candidates and 3–5 suggested viewer-comment examples (default five), explicitly labeled as examples. No posting is implied.
- Save a descriptive lowercase ASCII upload filename with hyphens, topic, language/episode identity, immutable revision and actual extension in JSON and Markdown. Do not rename existing masters or promise a filename ranking benefit.
- Apply this policy to future delivery work. Only Episode 003 is retrofitted under the 2026-10-03 request; leave other existing episode packages untouched.

- Thumbnail headlines placed at the top require a ≥12% full-height inset for every visible letter effect, accent and punctuation mark; target 13%. Record requested and observed bounds and review full-size, phone-size and upper-12%-hidden previews. Middle-position headlines retain their layout; this upper-band rule does not move them. See `assets/branding/youtube-shorts/README.md` and delivery skills.
