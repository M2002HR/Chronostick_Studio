# Final-setting pilot review — 12 steps, 2026-10-02

> Historical experiment report. The deterministic 45-slot graphics proposal below was subsequently superseded by `graphics-method-decision.md`; it is not the current production route. The newer integrated r003 pilot completed, but resume inspection found visual failures. See `resume-audit.md` and `resume-audit.json` for current evidence and reopened gates. The earlier log's `renders/graphics/` directory is absent at the resume audit; no recovery or approval is inferred.

All pilots used the actual installed MiniMax H3 reference-to-video service at 1024×576, 16:9, 24 fps, five seconds, 12 steps, `res_multistep`, `beta`, Lightning off and SFX-only audio. Each completed with a 120-frame five-second editorial MP4 and an AAC stream. Technical success did not imply creative acceptance.

| Pilot | Job ID | Visual result | Decision |
| --- | --- | --- | --- |
| Clock 075 r001 | `777960a0-3b24-4cf7-b3f2-783ef844c7b7` | `08:59` stayed readable, but H3 invented a detailed harbour/ship background outside both flat reference cards. | Reject for approved clock language. |
| Clock 075 r002 | `0f85c386-2859-4325-a6c9-f42d9150892c` | A stricter clock-only prompt produced a nearly black realistic corridor and tiny card, disregarding the supplied flat clock artwork. | Reject. |
| Character 100 r001 | `80ccc760-8c30-4304-b2cc-daf611de1206` | Khalid approached the same consulate guard and stopped at the gate; identity, figure count, warm illustrated Stone Town style and resolved final frame were preserved in sampled frames at 0.0–4.95s. | Pass as a representative 12-step **scene** capability probe; this does not approve future scene outputs automatically. |
| Map 064 r002 | `009c432e-2d25-4824-8090-d1aa27948fa0` | H3 changed the tactical map by adding many unplanned people, a new ship/flag and invented readable labels. | Reject for accurate maps. |

The map pilot's first submission failed before generation because a derived 64-bit seed exceeded SQLite's signed integer range. `scripts/build-longform-jobs.py` now masks derived seeds to 63 bits, the validator rejects unsafe seeds, and all 131 prepared job JSON seeds were corrected before batch submission. This was a real service-preflight gap, not a rendered clip failure.

Production decision: H3 will render the 86 illustrated historical scene clips at the requested 12 steps. The 45 exact clock/map clips are made from the reviewed original ChronoStick graphics with a deterministic frame renderer (`scripts/render-longform-graphics.py`) at 1024×576, 24 fps, 120 frames, five seconds and silent AAC. This keeps the same geography, exact writing and ship/icon counts in every frame. It is an explicit episode-specific substitution following failed final-setting pilots; those clips have no diffusion sampling-step value and are not described as 12-step H3 output. The accepted Spanish voice remains separate. All 131 timeline slots retain their five-second timing, and the graphic clips have been created and sampled at the exact event onsets.
