---
name: chronostick-longform-shot-plan
description: Direct a timed 10–15 minute ChronoStick video from approved Spanish voice timing and visual direction into five-second slots, detailed shots, continuity states, maps, text events, and reference requirements. Use before asset creation and H3 prompts.
---

# ChronoStick long-form shot plan

Start from accepted narration, actual word/cue timing, approved chapter architecture, visual-direction blueprint, reference-video analysis when supplied, and project profile. Follow `docs/longform/format-contract.md` and shared `docs/reference-and-prompt-continuity.md`.

## Two levels of direction

First assign every chapter/sequence a purpose, unanswered question, factual turning point, emotional register, visual mode, color/light progression, map scale and exit handoff. Then cover each five-second generation slot with exact local and global shot times. Each shot needs narration overlap, purpose, source claim, selected reference-analysis ID when applicable, subjects/props and count, start state, allowed change, framing, camera height, light, one action, at most one camera move, brief SFX, cut and resolved end. State the concrete adaptation of a reference technique, including an earned visual joke or reaction where useful. A rapid cut is a choice, not an eight-shot quota. Use close detail, wider orientation, geographic explanation, surprise, reaction and readable holds in a rhythm that prevents fatigue.

Write `plan/story-state-ledger.json` for every recurring person, animal, vessel, place and critical object; states move forward in time. A clean cut may change viewpoint but may not resurrect a prop, reverse injury or emotional state, or reveal a future event before the narration. Make named historical identities recognizable at small size from approved cues, and maintain exact count and screen placement. Treat maps as story-state scenes: date, territory/status, scale, route, arrow direction, label and political ownership must be consistent with researched facts.

Create `plan/text-events.json` for each exact in-engine Spanish word, date, number or time. A text event defines one clip, exact string, citation/claim ID, onset/hold/exit, style/position and frame-level failure conditions. Unlisted readable text is forbidden. Create `plan/map-manifest.json` and `plan/reference-manifest.json` with a shot-to-anchor coverage matrix. If an anchor cannot support a hand, animal, shore, map label or viewpoint, revise the shot or request a new anchor; negative prompting cannot supply missing evidence.

Finish `plan/shot-plan.md` only when all actual narration words have purposeful coverage, chapters build and pay off the premise, every generated slot resolves, sensitive history is contextualized, and no planned text/map claim is unverified. Run a voice-and-still animatic review before bulk prompts; revise the plan on observed boredom or confusion, not on an arbitrary cut count.
