---
name: chronostick-shot-plan
description: Turn approved word timing into a creatively directed, ultra-fast five-second clip plan, continuity ledger, and full-frame reference requirements. Use before reference creation or final H3 prompt writing.
---

# Chronostick Shot Plan

Work from `timing-map.json`, approved narration, current style authority, and existing assets.

## Directing method

- Allocate one independent 5.000-second clip per timing slot. Every clip must start after a hard editorial boundary and end in a resolved state.
- Map exact narration words and dramatic purpose to every slot. Do not move discoveries, reactions, props, damage, or consequences earlier than the narration.
- Build `plan/story-state-ledger.json` first: inherited start state, allowed change, resolved end state, character/object counts, screen positions/directions, prop state, emotion, environment, light, and event phase.
- Design an original visual idea for each clip: hook, reveal, contrast, match concept, reaction, scale change, symbolic insert, or payoff. Avoid merely illustrating nouns.
- Ultra-fast editorial rhythm is the ChronoStick default: plan exactly eight materially distinct hard-cut shots inside each 5.000-second clip unless the user or approved profile explicitly requires a slower exception. Typical shot spans are about 0.35–0.80 seconds. Document any lower-density exception in the shot plan instead of silently slowing the episode.
- Create speed through editorial contrast—not frantic motion. Each cut should change the visual question through framing, subject, scale, prop, silhouette, environment, or event phase while action inside the shot remains moderate and controlled.
- Each shot has one primary action, at most one simple camera move, and no more than two low-amplitude secondary motions.
- Specify framing, lens feeling, camera height, composition, light, palette, motion, emotion performance, hard-cut point, diegetic SFX, and stable end frame.

## Creative direction standard

- Give every five-second clip a miniature dramatic arc: immediate setup, escalation or discovery, then a resolved payoff or handoff.
- Include at least one non-obvious but truthful visual beat per clip, such as a macro prop insert, silhouette reveal, negative-space composition, environmental clue, match cut, visual metaphor, or scale reversal.
- Vary coverage deliberately across the episode: wides, close portraits, extreme inserts, low/high angles, architectural geometry, foreground occlusion, and controlled camera moves. Do not repeat the same centered medium composition across adjacent shots.
- Plan light and color as story information. Use changes in key direction, contrast, practical sources, and palette to clarify era, threat, discovery, or payoff without breaking world continuity.
- Design cross-clip visual handoffs when useful, but keep every generated clip self-contained and resolved so assembly never depends on a model completing an action in the next file.

## Reference planning

Inventory approved assets before requesting new ones. Prefer full-frame, single-scene, vertical generation anchors. Do not plan contact sheets, grids, multiple poses, repeated identities, annotations, or future story states. Each required reference entry declares content authority, style authority, exact subject count, intended clips, and whether a new asset is necessary.

For named real historical people, plan identity work before scene work. Require one portrait-grounded single-person ChronoStick identity anchor per recurring person, then build group and event-scene anchors from those approved identities. Record the few silhouette, hair, facial-hair, costume, proportion, and signature-prop cues that keep every person distinguishable at thumbnail scale. Never ask a group scene to invent several real identities from text alone.

## Outputs

- `plan/shot-plan.md`
- `plan/story-state-ledger.json`
- `plan/reference-manifest.json`
- update stage 03 to `needs_review`

## Gate

Every narration token is covered once, the default eight-shot cadence fits the local five seconds without gaps or overlaps, chronology never regresses, every cut has a distinct purpose, character/prop continuity is explicit, historical identities have achievable portrait-grounded anchors, SFX are motivated, and no clip depends on the next generation to finish its action.
