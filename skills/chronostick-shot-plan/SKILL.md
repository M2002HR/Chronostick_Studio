---
name: chronostick-shot-plan
description: Turn approved word timing into a directed five-second clip plan, continuity ledger, and full-frame reference requirements. Use before reference creation or final H3 prompt writing.
---

# Chronostick Shot Plan

Work from `timing-map.json`, approved narration, current style authority, and existing assets.

## Directing method

- Allocate one independent 5.000-second clip per timing slot. Every clip must start after a hard editorial boundary and end in a resolved state.
- Map exact narration words and dramatic purpose to every slot. Do not move discoveries, reactions, props, damage, or consequences earlier than the narration.
- Build `plan/story-state-ledger.json` first: inherited start state, allowed change, resolved end state, character/object counts, screen positions/directions, prop state, emotion, environment, light, and event phase.
- Design an original visual idea for each clip: hook, reveal, contrast, match concept, reaction, scale change, symbolic insert, or payoff. Avoid merely illustrating nouns.
- Fast rhythm is default, but clarity controls shot density:
  - hook/action: 6–8 short shots;
  - standard exposition: 5–7;
  - identity-heavy or precise physics: 3–5;
  - intimate emotion or settled aftermath: 2–4 phases/shots.
- Each shot has one primary action, at most one simple camera move, and no more than two low-amplitude secondary motions.
- Specify framing, lens feeling, camera height, composition, light, palette, motion, emotion performance, hard-cut point, diegetic SFX, and stable end frame.

## Reference planning

Inventory approved assets before requesting new ones. Prefer full-frame, single-scene, vertical generation anchors. Do not plan contact sheets, grids, multiple poses, repeated identities, annotations, or future story states. Each required reference entry declares content authority, style authority, exact subject count, intended clips, and whether a new asset is necessary.

## Outputs

- `plan/shot-plan.md`
- `plan/story-state-ledger.json`
- `plan/reference-manifest.json`
- update stage 03 to `needs_review`

## Gate

Every narration token is covered once, shot times fit their local five seconds, chronology never regresses, character/prop continuity is explicit, references are achievable, SFX are motivated, and no clip depends on the next generation to finish its action.
