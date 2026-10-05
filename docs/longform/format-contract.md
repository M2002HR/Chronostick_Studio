# Long-form format contract

## Story and picture

- Target 10:00–15:00 for the first format; the first release should reach at least 10:00 by actual accepted narration and useful content, not padding. If source material cannot support this, report the gap.
- Landscape 16:9, final 1920×1080, 24 fps. The project profile is `h3-long-5s-14step-16x9`; it uses independent 5.000-second H3 editorial slots. The service currently exposes `youtube_shorts_hq` and `draft` as request-profile names, so a job uses `youtube_shorts_hq` with all long-form generation dimensions/settings explicitly overridden. A service profile name is not the episode's production profile.
- H3 request: `1024×576` (exact 16:9, 0.6 MP), 24 fps, 5 seconds, 14 steps, `res_multistep`, `beta`, Lightning off, `ref_image_size: match`; keep the 124-frame raw output and exact 120-frame editorial copy. The local hardware and actual quality at these settings still require a representative probe before a full batch. No production render is implied by this contract.
- A user may explicitly choose a different step count for a named episode. Record the override in its `episode.json` under a matching production profile and validate the actual request against that value. Episode 006 uses 12 steps by explicit user direction; the default above remains 14 for future episodes.
- Use one generation-safe full-frame 16:9 scene anchor normally and two only when a documented handoff or separate identity/object truly requires it. The service maximum is nine, but that is not the creative target. Make as many *distinct approved anchors across the episode* as coverage requires. Never pass multi-panel identity or world sheets directly to H3.
- Episode006 has a user-authorized scoped exception for exactly slots014/118 after actual map failures: see [episode-006-map-exception.md](episode-006-map-exception.md). Those two inserts use reviewed controlled geographic motion with zero people. All other slots, including clocks, retain H3.
- All five-second picture slots, including maps, charts, clocks, displayed dates/numbers/short text and character-on-map movement, are generated as continuous H3 video. An image reference may be made with image generation or accurate geographic source geometry, but it is a still input, never substitute final moving footage. Do not replace an H3 map/text failure with deterministic graphic video or an editorial overlay. Keep all visual elements in the same stick world and solve failures with a better full-frame scene anchor, prompt and immutable H3 rerender.
- One primary action, at most one simple camera move, and no more than two subtle secondary motions per shot. Cut density follows comprehension and chapter rhythm; no inherited eight-shots-per-clip minimum. Every generated slot ends resolved, with story-state continuity across hard cuts.
- The visual master remains the detailed cinematic ChronoStick stick world in every pixel, including people, animals, maps, lettering surfaces, vehicles, sky, sea, and small inserts. Portrait research supplies recognizable cues; approved stick identity anchors control actual rendering.

## Audio and visible writing

Local post-picture voice, ordinary active-word captions and supplied external
sound tracks follow [`../postproduction.md`](../postproduction.md). This does
not relax any generated-clip restriction below. Original native audio is
explicitly muted or preserved only in the new distribution edit.

- Generated video has isolated short natural SFX only, with silence between cues. It has no music, tonal bed, generated speech, dialogue, narration, lip sync, or vocal reactions. The accepted Spanish voice is a separate continuous track. Every video prompt contains exactly `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`
- Dates, times, numbers, names, and short terms may be created **inside H3** only when listed as a specific exception in `plan/text-events.json`. Each exception has an exact Spanish string, historical source, relevant clip, entrance/hold/exit and frame-level review. All unlisted generated writing remains forbidden; captions and ordinary subtitles are separate finishing assets.
- A text-bearing single-scene anchor can supply exact orthography. H3 must preserve it; neither the anchor nor the prompt proves it succeeded. If spelling or stability fails, reject the render and correct the specific clip through H3. The picture pipeline does not use an editorial overlay as a substitute for requested in-engine writing.
- Historical maps require a dated map brief and source ledger: extent, political status, border/coastline authority, routes, symbols, exact labels, and scale changes. Do not equate a protectorate, colony, territory, and trade route. An H3 map clip must be reviewed for geographic deformation and label mutation across all frames.

## Preview and batch economy

- Build a full animatic from accepted voice, reference stills, provisional timing, and map/text cards before mass generation. This tests the ten-minute story without spending on every H3 slot.
- The local `draft` request profile changes steps, resolution, **and** Lightning LoRA. A four-step output, even with the same seed, does not predict the precise 14-step result. Use it to reject obvious concept or reference failures. Compare a small stratified sample of paired draft/final jobs before deciding where draft previews are useful. Critical text, maps, identity, physics, and SFX require final-setting acceptance.
- Stage generation by reviewed chapter after full-episode planning and complete job preflight. Preserve seeds, prompt/reference hashes, and revisioned outputs. A defective clip is replaced immutably; do not restart accepted chapters. Generated media is never overwritten.
- One uninterrupted five-second-generation timeline for ten minutes requires 120 slots; fifteen minutes requires 180. Plan capacity and cost before submission. Do not generate a complete batch merely because JSON validates. The user controls expensive launch.
