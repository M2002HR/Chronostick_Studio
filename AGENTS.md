# Instructions for AI collaborators

This repository is the production source of truth for ChronoStick Studio. Before creating or changing an episode, read these files in order:

1. `README.md`
2. `docs/workflow.md`
3. `docs/production-rules.md`
4. `docs/style-rules.md`
5. `docs/video-rules.md`
6. `docs/reference-and-prompt-continuity.md`
7. `docs/final-assembly.md`
8. `docs/audio-rules.md`
9. `docs/versioning.md`
10. `docs/decisions.md`
11. `docs/production-profiles.md`
12. `docs/localization-workflow.md` when creating a language version of an existing picture master
13. the target episode's `README.md` and `plan/shot-plan.md`
14. only the relevant locked files in `docs/specs/`

For a long-form episode, also read `docs/longform/README.md`, `docs/longform/workflow.md`, `docs/longform/format-contract.md`, and `docs/longform/artifact-contract.md` after the shared rules above. The existing `docs/workflow.md` describes Shorts; long-form stages and profile-specific exceptions are in `docs/longform/`. Read the target episode's manifest and shot plan once they exist.

When a long-form reference video and transcript are supplied, inspect the actual video alongside its transcript at intake and record a timecoded first-pass review before visual direction. Follow `docs/longform/reference-video-workflow.md`; preserve the original media and keep the example separate from historical evidence.

## Source-of-truth priority

When instructions conflict, use this order:

1. the user's current explicit instruction
2. this file and the active rules in `docs/`
3. locked, approved specifications in `docs/specs/`
4. the episode manifest and shot plan
5. archived material in `docs/archive/`

Archived files explain history; they are not active instructions.

## Non-negotiable rules

- Files under `prompts/` and `episodes/*/prompts/` contain only text that is ready to paste into a generation model.
- Never put YAML metadata, explanations, review checklists, logs, or approval notes in a prompt file.
- Never invent or reconstruct a missing "approved" prompt. Leave it empty and record the gap in the episode manifest.
- Preserve approved character identity, style, world, and asset references. Simplify backgrounds before characters.
- Every video generation follows the target episode's named production profile, is self-contained, and ends on a resolved frame.
- Use fast editing with moderate motion: one primary action and at most one camera move per shot.
- Every video prompt must contain exactly this policy sentence: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`
- Do not generate narration, dialogue, lip sync, subtitles, labels, or other readable text unless an episode explicitly requires an approved exception.
- Long-form dates, times, numbers, names, and short terms requested for in-engine display are allowed only as exact clip-specific exceptions recorded in `plan/text-events.json`, with frame-level review. This does not allow unlisted labels or ordinary subtitles.
- Do not overwrite generated media. Add `-r001`, `-r002`, and so on.
- Use Git history for text versions. Never create names such as `final2` or `final-final`.
- Do not mark an artifact approved or locked without an actual review decision.
- Treat each language version as an immutable post-picture branch under
  `episodes/<id>/localizations/<bcp47-language>/`. It may replace narration,
  captions, and language metadata, but never silently alter or regenerate the
  approved picture timeline.
- Derive localized word timestamps from the actual accepted localized audio.
  Preserve the provider response byte-for-byte, then record a separate
  localized visual-timing map. Do not recycle Spanish word timestamps for a
  different language.

## Working method

For post-picture voice, captions or sound work, read `docs/postproduction.md`
and the episode's `postproduction/edit.json`. Use the local repeatable finishing
script on the existing picture; choose native-audio mute/preserve explicitly.
New Shorts captions use Montserrat Bold104px at1080×1920 with a300px bottom
inset and short single-line phrases; landscape retains Arial Bold64px at1080p.
Use the configured safe width, white text and only the current spoken word
highlighted. Supplied music,
ambience and SFX are explicit finishing tracks, separate from the unchanged
generator no-music policy. Preserve actual timing sources, input hashes and
immutable distribution revisions; technical validation is not release approval.

Start from source material, then script, voice, timestamps, shot plan, asset-reuse decision, missing asset generation, final prompts, renders, review, and assembly. Do not skip a stage silently. If an input is unavailable, record it as unavailable instead of fabricating it.

Immediately after creating or revising any narration script, deliver both the clean text and a Google Vids paste-ready copy with many fitting emotion/style tags throughout, plus direction notes and text validation. Use `chronostick-voice-direction`; this includes drafts and does not wait for storyboard review or another request. Skip only on an explicit user/provider override. Keep spoken words unchanged and actual audio acceptance separate.

For historical claims, distinguish documented fact from popular anecdote. Verify claims against reliable sources when research is part of the task, preserve citations in the episode source notes, and carry qualifications into the narration and visuals.

For adaptation of user-supplied content, do not initiate fact-checking unless the user explicitly requests it. Preserve the selected source's claims, numbers, dates, causal links and payoff; shortening, translating or making a video does not authorize changing its content. Record `fact_check_requested: false` and internal source-claim provenance without asserting independent verification. This overrides automatic verification/correction language in the adaptation workflows; media validation and actual transcription remain required.

Before handing off changes, validate paths, prompt purity, required audio wording, profile-specific reference limits, automation JSON, empty/missing artifacts, and `git diff --check`.

## New reference-first Short route

When a downloaded reference is supplied for a new Short, follow
`docs/reference-first-shorts.md` and semantic pipeline state v2. The working
method above is the preserved text-first baseline: actual reference extraction
and analysis now precede original Spanish scenario and neutral rough storyboard.
The user reviews scenario and storyboard before production reference design;
references and accepted user voice can then progress independently. Use Ajil
for actual source and voice word/segment timing. New Shorts use the named
20–30-second, dynamic 4–7-second editorial, 16-step profile. Neutral storyboard
panels are internal planning only, not stick-world generation anchors. Shared
module reuse does not change long-form's existing format/profile contract.
