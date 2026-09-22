# Production workflow

This is the canonical path from a source story to a finished ChronoStick Short. Each stage has an input, output, and gate. Do not silently skip missing inputs.

## 1. Create the episode workspace

Choose the next zero-padded ID and a lowercase hyphenated slug, for example `002-sample-story`. Copy the structure described in `docs/templates/episode-readme-template.md`.

Gate: the episode manifest identifies its status, target duration, language, engine, inherited style, and known missing inputs.

## 2. Capture and verify the source

Store the English source story in `source/source-en.md`. Add citations and research notes beside it or in additional clearly named files under `source/`.

Check dates, names, places, causal claims, and whether a story is documented fact or popular anecdote.

Gate: factual claims are supported or explicitly qualified.

## 3. Write the Spanish narration

Create `script/narration-es.md`. Rewrite for natural speech and Shorts retention:

- immediate hook
- compact context
- escalating beats
- clear payoff
- concise CTA

Gate: natural Spanish, preserved historical meaning, and estimated duration within target.

## 4. Generate and archive the voice

Generate voice externally. Store the file in `audio/` using revision naming, or document its external location in the episode manifest. Do not add music.

Gate: approved delivery, pronunciation, pace, and clean voice file.

## 5. Obtain word-level timestamps

Store timestamps in `timestamps/word-timestamps.csv` with at least `word,start,end`. Use the actual approved voice, not estimated timings.

Gate: timestamps cover the complete narration and are monotonic.

## 6. Build the shot plan

Create `plan/shot-plan.md` from the timestamps. Divide the video into exact 10-second generation blocks. For every clip define narrative purpose, timing, visual beats, framing, main action, camera movement, references, final resolved frame, and failure conditions.

Gate: every narration beat has visual coverage; no clip depends visually on the next clip; the final action settles before 10.00 seconds.

## 7. Decide asset reuse

Create an asset/reference map in the shot plan. Check locked style, world, and character assets first. A generation may use no more than three references.

Priority: required recurring character identities, then another necessary character, then style or world. When a visual reference slot is unavailable, enforce the relevant locked spec in text.

Gate: every recurring identity and environment has an explicit source, and only necessary new assets are proposed.

## 8. Create and approve missing assets

Write internal design detail in `docs/specs/` and place only the paste-ready prompt under `prompts/image/`. Generate media into the correct `assets/` area using `-rNNN`, review it, then record the approved revision in the spec and generation log.

Gate: an approved reference exists before it is treated as locked.

## 9. Write final video prompts

Create one file per 10-second clip in the episode `prompts/` directory. Each file contains only the generator-facing text. It must explicitly describe reference roles, visible identity constraints, environment, shot timing, edits, action, camera, end frame, negative constraints, and audio policy.

Avoid internal IDs, historical metadata, and explanatory prose that the generator does not need. For historical people, use the approved character reference as the visual identity source rather than asking for realistic facial imitation.

Gate: prompt-purity validation passes and the prompt includes `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

## 10. Generate and review clips

Store renders under `renders/` as `clip-NN-slug-rNNN.ext`. Never overwrite a render. Evaluate against the shot plan and record each attempt in `logs/generation-log.md`.

Retry the same prompt version for random generation defects. Change the prompt only for a specification defect, and commit that text change.

Gate: identity, style, pacing, framing, sound, and final frame are approved.

## 11. Assemble the final episode

Use the continuous Spanish narration, approved clips, optional natural Foley, captions, CTA typography, and branding. Add text in editing rather than asking the generator to render it. Do not add background music.

Gate: complete timing, clean cuts, readable captions, factual integrity, audio compliance, and correct vertical export.

## 12. Archive and close

Store final exports under `final/` with revision naming. Update the episode manifest with what is present, what is external, what is missing, and which revisions are approved. Commit documentation, prompt, and manifest changes together when they describe one production decision.

## New-episode completion checklist

- source and citations present
- Spanish narration approved
- voice revision identified
- actual word timestamps present
- six or other required 10-second blocks planned
- reuse/new-asset decisions recorded
- reference count at most three per generation
- prompt files contain only generator text
- every video prompt has the exact no-music sentence
- renders use `-rNNN` and are never overwritten
- approvals and missing items are truthful
- final export and handoff status documented
