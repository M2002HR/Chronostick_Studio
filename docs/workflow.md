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

Gate: timestamps cover the complete narration. Preserve the source file exactly; document transcription overlaps and derive a separate normalized representation only if downstream tooling requires one.

## 6. Build the shot plan

Create `plan/shot-plan.md` from the timestamps. Divide the video using the episode's named production profile. For every clip define narrative purpose, timing, visual beats, framing, main action, camera movement, references, final resolved frame, and failure conditions.

Gate: every narration beat has visual coverage; no clip depends visually on the next clip; the final action settles before the profile boundary.

For a narration overhang of no more than 1.000 second beyond the last complete five-second H3 slot, the approved timing map may replace an otherwise-empty final generation with a documented `freeze_last_frame` tail. The preceding clip must resolve before its boundary and remain visually valid through the frozen extension.

## 7. Decide asset reuse

Create an asset/reference map in the shot plan. Check locked style, world, and character assets first. Use the reference limit defined by the production profile.

Priority: required recurring character identities, then another necessary character, then style or world. When a visual reference slot is unavailable, enforce the relevant locked spec in text.

Gate: every recurring identity and environment has an explicit source, and only necessary new assets are proposed.

## 8. Create and approve missing assets

Write internal design detail in `docs/specs/` and place only the paste-ready prompt under `prompts/image/`. Generate media into the correct `assets/` area using `-rNNN`, review it, then record the approved revision in the spec and generation log.

Gate: an approved reference exists before it is treated as locked.

## 9. Write final video prompts

Create one file per generation clip in the episode `prompts/` directory. Each file contains only the generator-facing text. It must explicitly describe reference roles, visible identity constraints, environment, shot timing, edits, action, camera, end frame, negative constraints, and audio policy.

Build a continuity ledger before finalizing prompts. For every clip, record the inherited start state, allowed state change, resolved end state, character count and placement, prop state, emotional state, environment state, and event phase. Describe the current desired state positively. Avoid naming later high-salience events in earlier prompts merely to forbid them; this can activate the unwanted concept.

Avoid internal IDs, historical metadata, and explanatory prose that the generator does not need. For historical people, use the approved character reference as the visual identity source rather than asking for realistic facial imitation.

Gate: prompt-purity validation passes and the prompt includes `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

## 10. Generate and review clips

Store immutable engine outputs under `renders/raw/` and timeline-normalized copies under `renders/editorial/` when the profile requires normalization. Name both `clip-NN-slug-rNNN.ext` and never overwrite a render. Evaluate against the shot plan and record each attempt in `logs/generation-log.md`.

Retry the same prompt version for random generation defects. Change the prompt only for a specification defect, and commit that text change.

Gate: identity, style, pacing, framing, sound, and final frame are approved.

## 11. Assemble the final episode

Copy exactly one approved editorial clip per timeline slot into the episode's `renders/final-selected/` directory. Preserve a sortable `clip-NN-...` filename for every selection. Run the episode assembly command to validate numbering, sort naturally, concatenate picture and existing audio, and write an immutable revision under `final/`.

Use the continuous Spanish narration, approved clips, optional natural Foley, captions, CTA typography, and branding in later explicit stages. Add text in editing rather than asking the generator to render it. Do not add background music under the current production policy.

When the timing map declares a sub-second tail extension, concatenate only the approved generated slots, run `scripts/extend-last-frame.sh` for the exact overhang, pad native SFX with silence, and use that immutable extended revision as the upscale input.

Gate: complete timing, clean cuts, readable captions, factual integrity, audio compliance, and correct vertical export.

## 12. Localize an approved picture/SFX master (optional, once per target language)

Do this only after the visual timeline has been selected and assembled. Create
`localizations/<bcp47-language>/` inside the episode and follow
[`localization-workflow.md`](localization-workflow.md).

- use the approved picture/SFX master as an immutable timing authority
- translate and adapt the narration to *semantic visual-cue windows*, not to
  Spanish words one-for-one
- generate the target-language voice, preserve the provider timing source, and
  derive a new word-timing map from the accepted target-language audio
- revise target-language wording or controlled delivery before considering any
  audio time-stretch; never regenerate visual clips to accommodate a routine
  translation-length difference
- create target-language captions from the accepted target-language timings and
  review RTL shaping/line breaks for Arabic-script languages

Gate: the localized narration covers the approved meaning, lands on the fixed
visual cues, ends within the approved picture duration, contains no leaked
source-language voice, and has its own reviewed immutable distribution master.

## 13. Archive and close

Store final exports under `final/` with revision naming. Update the episode manifest with what is present, what is external, what is missing, and which revisions are approved. Commit documentation, prompt, and manifest changes together when they describe one production decision.

## New-episode completion checklist

- source and citations present
- Spanish narration approved
- voice revision identified
- actual word timestamps present
- the profile-defined clip count and duration are planned
- reuse/new-asset decisions recorded
- reference count and mapping satisfy the named profile
- prompt files contain only generator text
- every video prompt has the exact no-music sentence
- renders use `-rNNN` and are never overwritten
- approvals and missing items are truthful
- final export and handoff status documented
- every released localization has its own script, real timings, captions,
  review decision, and immutable distribution master
