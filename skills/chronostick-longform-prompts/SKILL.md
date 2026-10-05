---
name: chronostick-longform-prompts
description: Write detailed, paste-ready five-second MiniMax H3 prompts for an approved landscape ChronoStick long-form shot plan and reviewed references. Use after timing, continuity, map, identity, and text-event contracts are settled.
---

# ChronoStick long-form H3 prompts

Read the approved exact shot plan, voice timing, continuity ledger, reference images *visually*, manifest, map and text events, and `docs/longform/format-contract.md`. Use selected reference-video analysis through the approved shot plan; describe the adapted visual action and timing directly. Write one `prompts/clip-NNN.md` per five-second generation slot. Prompt files contain only generator-facing text, never citations, example-video links, review notes, YAML or internal state IDs.

## Every prompt

Specify 5.00 seconds, 16:9, 24 fps and exact `<Picture N>` roles in the same order as the job array. State the approved stick-world style across the whole frame. Declare current story phase, exact person/animal/vehicle/prop count, fixed identity cues, left/right placement and scale, costume, ownership and object condition, environment, light and palette. Give contiguous local shot intervals covering 0.00–5.00, each with visible action from start to stop, framing, camera behavior, cut point and a brief literal diegetic SFX or silence. Name the resolved end frame and settle motion before the boundary. Use one primary action and at most one simple camera move per shot.

Control actual physical mechanism when it matters: distance, screen direction, trajectory, contact, recoil, persistence and what remains intact. Describe the present state positively; avoid repeatedly naming a later event in pre-event negative text. State only necessary negative constraints—no extra identities, copies, panels, mixed realism, unsupported props, dialogue, narration, music, captions or unintended letters. A dense prompt must remain internally consistent and achievable from its anchor. If it is not, fix the shot/reference before writing longer prose.

For map clips, give exact date/region/status, approved map anchor, fixed coastline/border/route geometry, limited animation, label inventory and camera move. For allowed visible text, quote exactly the matching `plan/text-events.json` string in Spanish, preserve accents/case/punctuation, state when it appears and holds, forbid other text, and flag it for frame-level review. Do not make a text exception implicit or use ordinary subtitles in H3. Every prompt must contain **exactly once**: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.` Request only isolated short natural SFX with silence between cues; if an effect risks becoming tonal music, request silence.

Compare each finished prompt with its assigned actual reference, narration window, source claims and previous/next state. Reject ungrounded geography, changed identities, premature consequences, contradicting shot counts or impossible staging. Pure prompt validation passes before job JSON. More words are not a substitute for reference coverage or a final-setting pilot.
