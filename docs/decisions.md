# Decision record

This file records durable production decisions and the evidence behind them. Active rules derived from these decisions live in the focused documents under `docs/`.

## 2026-09-30 — Default picture-master enhancement

### Decision

ChronoStick picture/SFX masters use the local frame-preserving Spandrel workflow with `RealESRGAN_x4plus_anime_6B.pth`, processed one frame at a time in FP16 and fitted with `cover` to an exact 1080×1920 vertical output. Preserve the original audio stream, retain the immutable upscale provenance report, and require picture-master QC before approval.

Do not adopt SoL-Refiner as the production default. It may be reconsidered only after an isolated, reviewed pilot on supported high-memory hardware.

### Reason

The existing model is compatible with the local single-GPU production stack and preserves the detailed cinematic stick-figure visual language without a generative video-refinement pass. The available SoL-Refiner H3 release requires a separate, substantially higher-memory runtime and would need a separate temporal, identity, audio-remux, and portrait-format validation before it could safely replace the established finishing step.

## 2026-09-27 — Sub-second final-frame extension

### Decision

When approved narration ends no more than 1.000 second after the last complete five-second H3 slot, a future episode may omit the otherwise-empty extra generation and extend the concatenated picture by cloning the final frame for the exact overhang. The last generated clip must intentionally reach a resolved, freeze-safe state before its boundary. Native generated audio is padded with silence while separately recorded narration continues.

The timing map records the normal ceiling count, the reduced generated count, and the exact extension. `scripts/extend-last-frame.sh` performs the immutable post-concat, pre-upscale operation and writes provenance. Longer overhangs or any overhang containing a new visual event still require another generated clip.

### Reason

Episode 003 narration ends at 45.640 seconds. Generating a tenth five-second clip solely for the last 0.640 seconds would add cost and a visually unnecessary scene. A controlled freeze preserves the complete narration, keeps the resolved ending stable, and avoids time stretching or silent truncation.

## 2026-09-22 — Omni prompt complexity and pacing

### Decision

Generator-facing Omni prompts must remain operational and visually specific, but should avoid unnecessary historical-person naming, identity discussion, metadata-like language, or other information that the video generator does not need in order to render the scene.

Internal ChronoStick files may retain full historical names, research context, and production mapping.

Generator-facing prompts should primarily describe:

- reference usage
- visible character design
- environment
- shot timing
- camera
- action
- cuts
- motion
- ending frame
- visual prohibitions

### Confirmed Test

Episode 001 Clip 02 initially failed before generation when using the longer identity-heavy prompt.

A simplified generator-facing prompt using the same visual character reference successfully generated the intended video.

Therefore, future generator-facing prompts should prefer direct visual instructions over unnecessary identity exposition.

### Pacing Rule

Controlled motion must NOT result in slow videos.

ChronoStick pacing target:

- Hook clips: 6–8 visual beats per 10 seconds
- Standard body clips: 4–6 visual beats per 10 seconds
- Final clips: 4–5 beats, slowing only near the final resolved frame

Typical shot duration:

- Hook: approximately 0.6–1.8 seconds
- Body: approximately 1.0–2.5 seconds
- Ending hold: approximately 0.5–1.5 seconds

Fast pacing should come primarily from:

- hard cuts
- framing changes
- reaction shots
- inserts
- close-ups

Individual shots should still use moderate, controlled motion.

Permanent principle:

FAST EDITING + MODERATE MOTION.

Never interpret motion control as static or slow storytelling.

## 2026-09-22 — Separate internal specifications from generator prompts

### Decision

Files in prompt directories contain only paste-ready generator input. Metadata, design rationale, checklists, approvals, and generation logs live elsewhere.

### Reason

Long internal specifications are valuable to collaborators but add irrelevant identity and process language when sent directly to a generator. Separation keeps both layers precise.

## 2026-09-22 — Style and identity authority

### Decision

The approved master style reference controls rendering. Character sheets control identity only. World sheets control recurring environments and prop language. If complexity must be reduced, simplify backgrounds before characters.

### Reason

This prevents character-reference artifacts from overriding the studio style and prevents recurring people from being redesigned between shots.

## 2026-09-22 — Complete ten-second generations

### Decision

Every AI video generation is exactly 10 seconds, finishes its action, settles camera motion, and reaches a readable ending without depending on the next generated clip.

### Reason

Cross-generation motion and match-frame dependencies are unreliable. Editorial continuity comes from narration, story logic, and hard cuts.

### Historical scope

This remains the Episode 001 Omni contract. It is not a global duration rule for engines introduced later.

## 2026-09-25 — H3 short-clip production profile

### Decision

The `h3-short-5s` profile uses 17 independent 5.00-second editorial slots at 480×864, 24 fps, 12 steps, `res_multistep`, `beta`, Lightning disabled, and two to four ordered references per clip. MiniMax H3 emits 124 frames for the request, so the immutable raw result is retained and an exact 5.000-second editorial copy is created without time stretching.

All jobs are schema-, path-, collision-, reference-mapping-, and capability-validated before any batch child is queued. The batch is sequential on a single GPU, preserves seeds on retry, continues after non-transient clip failures when configured, and never overwrites a revision.

### Reason

Engine constraints and editorial timing are different contracts. Keeping them in a named profile preserves Episode 001 history while allowing repeatable H3 production without misleading global rules.

## 2026-09-26 — Episode 002 r003 continuity references

### Decision

Episode 002 r003 uses the `h3-short-5s-16step-continuity` profile. It increases sampling from 12 to 16 steps and replaces the multi-panel style, world, character, and vehicle inputs at generation time with nine episode-scoped single-scene anchors. Most clips use one anchor; Clip 12 uses two because it must show both the recurring couple and the separate airborne object.

Each five-second prompt uses three to four precisely timed beats and declares a resolved end state. Recurring-character prompts inherit the prior character state explicitly, particularly across Clips 12–15. Pre-event aircraft and falling-object prompts state only the current physical state and unchanged intact environment; later consequence concepts are omitted from those prompts.

### Reason

The r002 results showed three coupled failure modes: contact-sheet imagery copied into video frames, duplicate recurring characters from multi-pose identity sheets, and narrative completion occurring earlier than the narration. Single-scene anchors reduce compositional ambiguity, while fewer timed actions and explicit start/end states improve identity tracking and narrative order. More sampling steps may improve refinement but are not treated as the mechanism that fixes continuity.

## 2026-09-26 — Selected-clip master assembly

### Decision

Each episode keeps a `renders/final-selected/` staging directory containing exactly one human-approved video for every numbered clip. Filenames retain both the two-digit clip number and immutable render revision. Final assembly validates a complete, duplicate-free number sequence, sorts naturally by filename, concatenates through the automation service, waits for a terminal result, and writes the next unused master revision under the episode's `final/` directory.

Captions, narration mix, and background audio are not implicit parts of concatenation. If those stages are approved later, they must be explicit and independently reviewable post-production stages.

### Reason

The best take can differ per clip across render revisions. A dedicated selection layer makes that choice visible, prevents accidental ordering or omission, preserves provenance in filenames, and keeps future finishing work separate from lossless assembly.

## 2026-09-22 — No background music

### Decision

ChronoStick uses no background music at generation or assembly time. Natural diegetic effects and separately recorded narration are allowed. Every video prompt includes the exact sentence: `NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

### Supersedes

Earlier Episode 001 working notes that mentioned a continuous music track.

## 2026-09-22 — Git and media revision strategy

### Decision

Git history versions text. Generated media uses immutable `-rNNN` revisions. Media is never overwritten, and filename suffixes such as `final2` are forbidden.

## 2026-09-22 — Missing Episode 001 prompts remain missing

### Decision

The owner confirmed that the final video was completed but the final prompts from Clip 03 onward were not saved. Clip 03–06 prompt files remain intentionally empty. They must not be reconstructed and represented as the original successful prompts.

### Reason

An explicit gap is more trustworthy than a plausible fabrication. Future prompts may be newly authored from the shot plan, but must be labeled as new drafts.

## 2026-09-28 — Episode 003 rapid-cut profile and symbolic presidential identities

### Decision

Episode 003 uses `h3-short-5s-16step-rapid-cut`: nine five-second H3 clips at 16 steps, each directed as eight short hard-cut shots. The user explicitly selected 16 steps as an episode override of the 14-step future default. Cut frequency, inserts, framing changes, and silhouette contrast create speed; the one-action/one-camera-move motion budget remains unchanged. Clip 09 locks its final memorial frame at local 4.20 seconds so the approved 0.640-second external tail freeze contains no new visual event.

The four assassinated presidents each receive a reusable, full-frame, single-person ChronoStick identity anchor. Their distinguishing cues are Lincoln's extreme height, stovepipe hat, and chin beard without mustache; Garfield's broader silhouette and full beard with mustache; McKinley's clean-shaven receding hair and scarlet lapel carnation; and Kennedy's youthful swept hair and modern navy suit. Six episode-scoped single-scene anchors combine those identities with the required historical worlds. H3 receives no more than two scene anchors per clip and does not receive the identity anchors directly under normal operation.

### Reason

The user explicitly prioritized a pace faster than prior episodes while requiring all four figures to remain recognizable in the symbolic stick-figure language. A named profile prevents this episode-specific density from silently changing global H3 behavior. Separating four identity authorities from six generation-safe scene anchors keeps the four people distinct without exposing H3 to multi-pose sheets, repeated identities, or unnecessary references.

## 2026-10-01 — Separate long-form production route

### Decision

Long historical videos use a separate `docs/longform/` workflow and `chronostick-longform-*` skills while retaining shared style, identity, audio and versioning rules. The first long-form profile targets Spanish narration lasting 10–15 minutes, a 16:9 picture, independent five-second H3 clips at 1024×576/24 fps/14 steps with Lightning disabled, and a reviewed 1920×1080 final master. The installed service's `youtube_shorts_hq` API profile is used with explicit landscape overrides; that API name does not define the project format. The settings are a production contract pending a representative actual render and capability review, not a claim of proven long-form quality.

The pipeline gates source verification, faithful Spanish script, accepted voice and word timing, episode-wide visual direction, timed shot/state plans, sourced historical maps and identities, reviewed full-frame references, a full animatic and pilot, pure video prompts, deterministic JSON/preflight, clip-by-clip QC, selection, finishing and YouTube packaging. Full-episode planning precedes chapter-wise generation. Exact generated dates, numbers and short terms are allowed only as per-clip approved exceptions with render review; ordinary captions remain a finishing layer. No background music is allowed. Four-step `draft` output may filter concepts but cannot certify a 14-step output because the service changes model settings as well as steps.

### Reason

At ten minutes, roughly 120 independent clips make omissions, continuity drift and unreviewed bulk rendering expensive. Stage ledgers and validators expose missing evidence, reference coverage, job mapping and selected-media gaps before these compound. The source example's maps, market scenes, diagrams and time cards inspire an original ChronoStick visual grammar; the other video's transcript and screenshots are neither historical proof nor assets to reproduce.

## 2026-10-01 — Google Vids voice tags follow the observed account menu

### Decision

For Google Vids voice-direction drafts, use the Pace, Pauses, Emotion, Style and Sounds options observed in the user's account and cataloged in `docs/google-vids-voice-direction.md`. The user confirmed that selecting Rushed pace inserts `[rushed pace]`; the other observed labels are written in the same lowercase bracket form. Previous Gemini API and older Vids tag examples are not the production vocabulary for this route. Keep tagged voice text separate from the clean narration and accept timing only after listening to generated audio.

The user subsequently prohibited `[whisper]` for all future voice scripts. It stays in the catalog as an observed menu item, but is not part of the usable ChronoStick tag set.

### Reason

The user's current menu supplies a concrete tag inventory for their voice workflow. It also provides a moderate pace option after the first scene trial felt too fast.

## 2026-10-03 — Short titles and conversational YouTube delivery

The user requested roughly 30-character, few-word hook titles for Shorts from Episode 003 onward, with no tags or hashtags in titles. Delivery now includes three pinned-comment candidates and 3–5 casual viewer-comment examples for both Shorts and long-form; grouped topic, history/animation, and format/discovery hashtags; a smaller matching description subset; naturally integrated search terms; and a proposed final upload filename. Current trend status requires evidence. The present retrofit is limited to Episode 003.

## 2026-10-05 — Reference-first Short workflow

Current user direction makes downloaded video the new Short intake: actual Ajil
word/segment extraction, joint video/transcript direction, original Spanish
scenario and neutral rough storyboard. The user reviews scenario and storyboard
before single-image stick-world identities/scene references. Reference and voice
branches can then proceed independently. The user supplies voice; Ajil extracts
its real timing. New named profile `h3-short-dynamic-16step-20-30s` targets a chosen
20–30 seconds with dynamic 4–7-second editorial slots, 16 steps, rapid purposeful
hard cuts, moderate motion, no music and isolated small diegetic SFX. Raw engine
request duration/frame grid is recorded separately and needs a real pilot.
Semantic state v2 preserves review gates; technical validation is not approval.
Existing episode profiles and long-form numerical contracts remain unchanged.
Episode 007 exercises intake through reviewable scenario/storyboard; later
stages continue after actual approval and accepted voice.

## 2026-10-05 — Required Google Vids tagged narration handoff

The user explicitly added registered-tag voice direction to the production
workflow: deliver a paste-ready tagged copy of the final clean narration for
Google Vids, with frequent emotions and relatively fast exciting performance.
Use `chronostick-voice-direction`; provider selection remains explicit, and
tagging is required when Google Vids is selected. Spoken words/punctuation stay
identical. Preserve the existing no-whisper rule; keep harm serious. Semantic
Short state v2 records direction as a `voice` substage without migrating its
15-stage order; long-form retains `02a`. Episode 007 exercises the handoff with
28 registered tags. Accepted voice and real Ajil timing remain later inputs.

## 2026-10-05 — Tiny subscribe CTA by default

The user requested a small closing call to action that says only subscribe.
Future clean narrations append Spanish `Suscríbete.` (or the equally brief
target-language equivalent) after the payoff by default, with delivery matching
the scene and counted in the runtime. Explicit user overrides take priority.
Update the clean authority before its Google Vids copy and timing; narration
CTA does not authorize an in-engine button/text shot or alter approved masters.
Episode 007's clean/translated/tagged copies and scenario record this change.
## 2026-10-05 — Storyboard remains an active directing input

The user explicitly required the reference/shot-plan skills to attend to the
storyboard during use. Both skills now require inspecting the actual selected
sketch pages and panel records while designing and reviewing production art or
directing timed shots. Reference entries and final shots retain
`storyboard_panel_ids`; retiming, merging and omissions have separate reasons.
Neutral sketches control composition and action, while the locked stick-world
style and researched identities control production appearance. Material changes
require renewed creative review. The reference-first validator checks panel
mapping/coverage and detects changes to artifact bytes bound to a recorded
creative acceptance. Existing profiles without this storyboard route remain
unchanged.

## 2026-10-05 — Local voice, active-word captions and separate sound layers

The user requested local finishing here for Episode 006 and repeatable future
episodes: accepted voice, Arial Bold subtitles with only the spoken word
highlighted and all other words white, then supplied music/background/SFX.
This supersedes the old ban on external finishing music; generated clips and
all video prompts retain their exact no-music policy. The local edit records
explicit tracks and native-audio mute/preserve. Episode 006 explicitly excludes
all native sound and has no music/ambience/SFX supplied yet.

`scripts/postproduce-episode.py` binds source hashes, actual timing and font,
preserves the fixed picture frames, writes ASS/SRT/VTT and separate stems,
normalizes loudness in two passes and verifies the encoded immutable export.
The newer root voice has a measured 1600/44100-second export drift from
paragraph16; evidence and derived caption adjustments remain separate from
the original accepted timing CSV. Technical QC and sampled visual review do
not claim full human playback or approval of the earlier generated picture.

## 2026-10-05 — Storyboard-led single-image reference coverage

Episode 007 exercised the reference-first design branch with 21 selected
single images: six identities and fifteen scene/prop views for 36 approved rough
panels. Closed/open doors, folded/read letters, off-face/worn masks and an actual
over-shoulder plan need distinct start-state or viewpoint coverage. Preserve the
selected sketch bytes and record these asset allocations separately; do not
replace a panel merely because another image is available.

`scripts/reference-artifacts.py` freezes exact pure prompts, ordered input roles
and hashes before the built-in image call, verifies them, then archives returned
PNG bytes without approving them. It rejects more than five image-tool inputs;
that cap is separate from H3's validated per-job reference allowance. Await every
parallel result, including failures, to preserve provenance. Actual full-frame
and phone-size review selects an immutable revision. Check drawings inside props
for anachronisms and keep master-style background content out of new-era scenes.
The episode's 33.365333-second supplied voice remains intact while its duration
choice is pending; static reference approval does not settle final timing.

## 2026-10-05 — Real voice-led dynamic timing and native preflight

Episode 007 continues with the supplied complete 33.365333-second voice after
contextual user continuation of the explicit full-voice proposal. The exact
quote, acceptance scope and immutable voice/provider hashes are recorded in
`plan/voice-acceptance-r001.json`; this is not an invented numeric user quote
or assistant personal listening. Its picture covers 801 frames / 33.375 seconds.
The global 20–30-second default remains unchanged. Three provider overlaps
remain in the original CSV and have separately documented derived start clamps;
aggregate numerical tokens are not expanded into invented measured timings.

Six variable editorial clips contain 48 reviewed cuts, all mapped to the 36
unchanged rough storyboard panels and 21 selected single-image references.
Reusable timing/plan/prompt/job/preflight helpers implement the explicit
contracts. H3 raw frames are 141, 158, 124, 124, 158 and 175; exact editorial
frames are 132, 143, 101, 110, 150 and 165. Raw terminal holds are dropped
without speed changes. Custom SFX suffix prevents the service default from
repeating the mandatory music policy in the final engine text.

The six-job live preflight passed without warnings at native 16 steps, with
input and service-source hashes archived. A one-job native clip-04 pilot is
submitted first under the user's existing complete-production instruction;
its actual motion/audio/duration review gates the remaining five jobs. Its
submission record is execution evidence, not creative approval.

## 2026-10-05 — Native pilot rejects music and unexecuted cuts

Episode 007 clip04 r001 produced the correct110 editorial frames at16 steps,
but direct all-frame inspection found seven actual compositions rather than
the planned nine and an ambiguous clothing-owner crop. The user separately
reported background music and explicitly restated zero music in every clip,
with only short SFX. This candidate is rejected; its media and original full
input package remain archived. No other clip was launched from that package.

All six pure prompts now begin with the exact audio policy and emphasize a
completely silent default at opening/ending and between dry isolated cues.
The deterministic job helper adds the corresponding strict suffix. A dedicated
single-frame S26 gripreference shows the blue lead-guard sleeve grabbing
Fawkes's brown upper sleeve. Clip04 consolidates two coverage pairs into seven
deliberate shots, preserving all nine neutral panels and actual voice slots.
Revised full preflight passed; a native 16-step r002 pilot precedes further launch.

Supplementary Gemini review repeated exact intended cut times despite missing
cuts in the actual frames. Its visualclaims are not accepted. Future generated
media audits omit the intended generation prompt with `--media-only`; user
listening and direct frame evidence retain priority. Prompt/JSON locks alone
never certify absence of music.

## 2026-10-05 — Prefer engine SFX; independent sound is a reviewed fallback

After the second user-reported music failure, episode 007 clip 04 received a
preview with the entire native soundtrack excluded and three independently
recorded CC0 paper, cloth and metal transients. The decoded 110 picture frames
are identical. The user found the result acceptable **as a fallback** and
explicitly preferred the engine's better synchronized SFX whenever it produces
clean audio. This supersedes the earlier blanket native-exclusion proposal.

The workflow therefore keeps strong silence/no-music locks on every generated
prompt/job, reviews actual sound per take, and preserves clean native SFX.
`chronostick-sfx` handles only demonstrated sound failures or an explicit
separate-effects request. It derives placements from real actions, archives
licenses/source quality/hashes, preserves picture frames, and separates an
unapproved listening preview from final selection. User approval of the shown
three cues does not approve the full downloaded recordings or future mixes.
Recorded physical effects are preferred to the explicitly labeled procedural
test alternative. No melody, sound bed or continuous ambience is introduced.


## 2026-10-05 — Actual duration and actual cuts are separate gates

Episode007's six r002 takes match executed job request durations, compiled raw
frame grids, 24fps presentation timestamps and editorial counts (801frames /
33.375seconds total). That success did not establish shot compliance. Actual
frame review found required shots late in raw tails and missing cut coverage.
Use the reusable render-timing audit for technical checks and separately record
actual cut starts, visible beats, drift and all raw-tail frames. Preserve the
accepted complete narration; perform only targeted immutable replacements.


## 2026-10-05 — Usable clip quality, no perfection loop

The user accepts approximately95% practical quality. This is an editorial
judgment, not a calculated score. Preserve understandable story beats, period
chronology, identity/style, real voice sync, exact editorial duration and the
no-music rule. Accept recorded minor cut drift, consolidated nonessential
inserts or a brief non-disruptive cosmetic detail. Do not regenerate usable
clips to perfect every prompt instruction. A repair already running may finish;
select the stronger usable take and stop cosmetic refinement.


## 2026-10-05 — Separate Shorts caption typography

The user supplied a Short screenshot and requested distinct font/size from
long-form. New portrait finishing starts with licensed Montserrat Bold104px
at1080×1920, short single-line phrases (maximum4 words/1.8seconds),300px
bottom inset and current-word yellow over white text. The source screenshot
font is unknown; this is a visual approximation reviewed on actual output.
Landscape retains Arial Bold64px/88px inset and existing grouping. Saved
configurations and accepted exports do not migrate silently. Episode007
uses immutable r002 and r003 caption-only distribution revisions; actual
r002 output review led to the current104px r003 size, with unchanged
picture, accepted voice timing and selected native/fallback SFX.

The user subsequently accepted this style («خوبه» and «از این به بعد ...
دقیقا همینجوری زیر نویس») and asked for thumbnail/delivery completion.
Use this style prospectively for new Shorts finishing configurations; the
bound decision is Episode007's `postproduction/user-acceptance-r001.json`.
