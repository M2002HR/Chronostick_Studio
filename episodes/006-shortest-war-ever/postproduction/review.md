# Local narration and active-word caption review

Distribution: `final/episode-006-shortest-war-ever-es-1920x1080-r008.mp4`

Status: technical validation and sampled subtitle review passed; user playback/release approval pending.

## User specification

Latest instruction: Arial Bold 64px, single line only, unchanged 80% safe width and slightly higher placement. Bottom inset is 88px, 20px above the first 68px trial. Every non-active word stays white; only the current word is yellow. Native video audio is completely excluded. Only the supplied root voice is present; music, ambience and SFX await actual assets.

## Evidence

- Fixed 1920×1080, 24fps, 655.000-second timeline and all 15720 frames retained; one stereo 48kHz AAC Spanish audio stream. Full decode passed without errors.
- Encoded output: -16.03 LUFS, -1.50 dBTP, 3.60 LU loudness range. Source voice is normalized in a separate lossless stem, never trimmed or stretched.
- All 1772 words present in 295 single-line cues. Maximum measured line width 1532.969px within 1536px. Every word has a highlight visible on the actual 24fps grid; no cumulative highlighting or second lines.
- Exact Arial Bold was installed locally from the original Core Fonts package, loaded by libass and bound by hash.
- Source voice/timing originals remain intact. Root export differs from the prior voice by a measured 1600/44100-second seam drift from paragraph 16. Three near-duplicate starts use explicit preceding supplied-word ends only in the display map. Unquantized and frame-quantized display boundaries remain separate. These are disclosed display derivatives, not newly measured speech timestamps.
- Actual final frames reviewed at 0.5, 1.1, 4.2, 37.5, 64.8, 244.65, 296.46, 300.5, 515.125, 542.458333, 548.1, 620.0, 650.8 and 653.0 seconds: active-word transitions, repaired starts, a 40ms word, clock inserts, light/dark backgrounds, unchanged single-line width, last word and subtitle-free tail. A 480×270 phone preview was inspected.
- Actual output contact sheet: `postproduction/exports/r008/subtitle-review-contact-sheet.jpg`; phone preview: `postproduction/exports/r008/subtitle-phone-actual.jpg`. Source/ASS previews are clearly named separately.

## Scope and remaining work

This review checks the requested finishing layer and technical export. It does not newly approve the underlying latest-revision generated picture, verify historical claims or claim full human audio/video playback. Earlier picture approval remains pending under the documented user-authorized assembly policy. User viewing and later supplied music/background/SFX mix remain next actions.

Earlier typography trials were superseded; interrupted renders were never released. r007 was interrupted before release and r008 completed detached with the same final edit. Original picture, accepted voice/timing and prior completed distributions are preserved.

Reviewed: 2026-10-05T16:25:34.756557+03:30
