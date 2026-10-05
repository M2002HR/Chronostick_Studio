# 007-guy-fawkes-mask — Why does this Mask mean Boom boom?

Reference-first Spanish Short using the complete supplied narration.
The original 30-second target has an episode-only voice-led exception:
33.365333 seconds of untouched voice, covered by 801 picture frames at 24 fps
(33.375 seconds). The default for future Shorts remains 20–30 seconds.
Profile `h3-short-dynamic-16step-20-30s`: six 4–7-second editorial clips,
16 steps, no music, isolated diegetic SFX and separate narration.

## Source, scenario and storyboard

- Original download: `source/reference-video/reference-guy-fawkes-mask-r001.mp4`;
  original bytes and source-title provenance preserved.
- Actual Ajil source transcription: 204 words, 15 segments; successful raw r003
  and independently derived r004 retained. Source overlaps are documented.
- [Timecoded reference analysis](plan/reference-video-analysis.md) follows
  actual source frames across the complete timeline beside the transcript.
  [Historical corrections](source/research/claims.md) distinguish source art
  from evidence. Supplementary source machine-video/audio reviews failed.
- [Original Spanish narration](script/narration-es.md), scenario and three
  neutral rough r002 storyboard pages were accepted through contextual user
  continuation; [decision evidence](plan/review-decisions.json) binds exact
  artifacts. Their text/art has not been replaced by the final timing plan.
- [Google Vids paste copy](script/voiceover-google-vids-es.md) includes 30
  registered pace/emotion tags, unchanged spoken wording and `Suscríbete.`.

## Accepted voice and timing

[Full assembly WAV](audio/narration-es-r001.wav), mono 24 kHz PCM24, retains
all 800768 original decoded samples. Original export and native AAC are
archived separately. [Actual Ajil voice timing](timestamps/ajil/voice-transcript-r001.md)
contains 76 provider words and six segments; numerical aggregates `1605` and
`36` correspond to the 80-word clean script without invented constituent times.
[Voice/runtime decision](plan/voice-acceptance-r001.json) records the user's
contextual continuation of the complete-voice proposal; no assistant personal
listening is claimed. Three provider overlaps are retained byte-for-byte in
[source CSV](timestamps/word-timestamps-source.csv) and separately normalized
for production, with the exact adjustments in [timing map](timestamps/timing-map.json).
No speed change, sentence removal or speech truncation is used.

## Reviewed production plan

[Gallery](plan/references/gallery-fa.md): 23 independent stick-world images,
six identities and seventeen scene/prop anchors, reviewed at full and phone size.
[Reference assignment review](plan/references/reference-review-r004.json)
binds their current six-clip allocation to unchanged selected image hashes.
Rejected alternatives remain archived. No reference sheets enter H3.

[Final shot plan](plan/shot-plan.md) contains 46 planned shots across six
variable clips. [Storyboard reconciliation](plan/storyboard/timing-reconciliation.json)
accounts for all 36 accepted panels and explains retiming/crop splits.
[State ledger](plan/story-state-ledger.json) protects identities and event order;
object-only powder returns do not depict Fawkes alive after the consequence.
[Actual directing review](plan/timed-direction-review-r003.json) binds all inputs.

| Clip | Timeline | Editorial frames | Engine raw frames | Shots |
| --- | --- | --- | --- | --- |
| 01 — mask to London | 0–5.500 s | 132 | 141 | 8 |
| 02 — conspiracy | 5.500–11.458 s | 143 | 158 | 8 |
| 03 — powder watch | 11.458–15.667 s | 101 | 124 | 6 |
| 04 — letter/search/arrest | 15.667–20.250 s | 110 | 124 | 7 |
| 05 — consequence/mask | 20.250–26.500 s | 150 | 158 | 9 |
| 06 — symbol/payoff/CTA | 26.500–33.375 s | 165 | 175 | 8 |

The plan requires actions to resolve at the editorial endpoint, with an extra
raw hold trimmed without time stretch. Actual raw-tail review is mandatory:
some first takes put a required final shot inside that tail and need repair.

## Current execution

Six pure [video prompts](prompts/) and deterministic [jobs](automation/jobs/)
are reviewed and packaged. [Native live preflight](automation/preflight.json)
passed all six jobs without warnings, checking actual resolver frame counts,
16 steps, ordered anchors, unchanged input hashes and one exact music policy
in the resolved generator text. All 30 related tests, repository validation
and skill validation passed. The failed CLI-option attempts are preserved
in `automation/live-validation-r001` and `r002`; successful evidence is `r003`.

The initial native clip-04 pilot r001 completed with the correct 110 editorial
frames, but was rejected for missing intended cut coverage, ambiguous sleeve
ownership, and the user's actual report of background music. All original
media and the full input package remain archived. [Actual review](renders/review-r001.json)
and [audio-policy reaffirmation](plan/audio-policy-reaffirmation-r001.json)
record these findings. The supplementary machine review repeated intended cut
times incorrectly; its limitations are explicit and do not override actual frames.

All six pure prompts now open and close with a strict silent-default audio lock:
absolutely no music, only tiny dry physical SFX with silence between events.
The exact required policy remains once per resolved prompt. A new dedicated
S26 grip image controls the blue lead sleeve/Fawkes brown sleeve distinction.
Two close coverage pairs are consolidated into seven deliberate clip-04 shots,
keeping all nine panels and event order; total directing coverage is 46 shots.

The revised r002 clip-04 pilot retained 110 frames. The user accepted its
animation but again reported music. Its observed cut variant is recorded in
[actual-picture review](plan/storyboard/actual-clip04-variant-r001.json), rather
than claiming all seven planned cuts occurred. The user heard the exact
three-cue recorded-foley preview and accepted it **as fallback**, explicitly
preferring clean engine-native SFX wherever the engine produces them. This
[latest sound decision](plan/native-sfx-priority-r001.json) supersedes the
blanket native-exclusion proposal. Clip04's selected derivative contains the
same 110 decoded picture frames and zero original soundtrack contribution.

The remaining five r002 jobs completed successfully in batch
`7e5896e6-a7dd-4a5a-9ee3-ed20de64fd3e`. [Actual timing audit](renders/timing-audit-r002.json)
checks executed JSON/graphs, all frame PTS, counts and trims: editorial lengths
5.500000, 5.958333, 4.208333, 4.583333, 6.250000 and 6.875000 seconds total
801 frames / **33.375 seconds**. MP4 endpoint rounding is separately reported.
This technical pass does not approve internal cut timing or sound.

[Actual cut audit](renders/cut-timing-audit-r001.json) found essential missing
coverage in the first clip02/03 takes. Their r003 replacements restore the
Parliament plan and watchful Fawkes; their usable observed variants are recorded
rather than claiming all intended cuts. The user actually heard and confirmed
native SFX for clip02 r003, clip03 r003 and clip05 r002. Those exact native
files are selected without sound replacement.

Clip06 r003 fixes the incorrect post-execution return of Fawkes using the
reviewed empty-barrel anchor. Its minor cosmetic mask blink is accepted under
[the user's usable-quality policy](plan/usable-quality-policy-r001.json).
The already-running r004 completed, but introduced burning powder barrels;
[comparison](renders/clip-06-picture-review-r002.json) retains the coherent
r003 picture and stops cosmetic retries. The user reported music in r003,
so its entire native soundtrack is excluded and one previously accepted dry
cloth cue accompanies the actual holding-hand adjustment.

[Six selected clips](renders/selection-manifest.json) preserve native engine
SFX in02/03/05 and use recorded fallback only in01/04/06. Every fallback keeps
the decoded picture frames identical, with zero native-audio contribution.
[Current-take timing audit](renders/timing-audit-r003.json) passes all six
executed jobs and their exact editorial lengths:801 frames /33.375 seconds.
[Execution state](automation/runtime/execution-state.json) archives actual
terminal generation statuses. Assembly/upscale/voice-caption export are the
completed stage; complete-master human playback remains separate from clip review.

## Current distribution master

[Distribution r003](final/mascara-guy-fawkes-complot-1605-es-007-r003.mp4)
is technically validated:1080×1920,24fps,801frames,33.375seconds.
The [export manifest](postproduction/exports/r003/manifest.json) records the
unchanged accepted voice, clean selected SFX and full decode pass. Assembly,
framewise upscale and precise audio alignment are complete; no further clip
generation is queued.

Following the user's screenshot, Shorts captions use licensed Montserrat
Bold104px, short single-line phrases, white text/current-word yellow and a
300px bottom inset. This is a visual approximation of an unknown screenshot
font; landscape Arial typography remains separate. [Actual caption review](postproduction/review-r003.json)
and [portrait preview](postproduction/review-evidence-r003/portrait-caption-r003.png)
document rendered samples. Previous distribution revisions remain archived.
The user accepted the caption style and continued to delivery after this
handoff. [Scoped acceptance](postproduction/user-acceptance-r001.json) records
that decision without inferring a complete audio audition.

[YouTube package](delivery/youtube/metadata.md) is ready and bound to r003.
Primary title:`¿De dónde salió esta máscara?` (29characters).
[Generated thumbnail](delivery/youtube/thumbnail-episode-007-r003.png)
is2160×3840; [actual image QC](delivery/youtube/thumbnail-review-r003.json)
passes identity, text, mobile readability and the upper crop. Earlier sources
are preserved; lettering was generated inside the artwork with the built-in
image tool. Artwork has assistant QC, not fabricated user approval.
[Complete upload package](delivery/release/episode-007-es-release-r001.zip)
contains the video, thumbnail, captions and copy-ready title/description/tags.
Uploading and publishing have not been performed.

## Reusable commands

`build-short-timing.py` derives slots from accepted real voice timestamps;
`validate-short-plan.py` checks frames, words, panels, references and cue bounds;
`build-short-prompts.py` renders explicit reviewed creative decisions;
`build-short-jobs.py` packages immutable jobs;
`preflight-short-batch.py` archives live checks without generation;
`prepare-short-review.py` extracts actual frames/audio without approving them;
`audit-short-render-timing.py` checks executed request/graph and every frame PTS;
`clean-short-sfx.py` preserves picture while replacing an actually failed native soundtrack.
Use `python3 scripts/validate-reference-first.py episodes/007-guy-fawkes-mask`
and the repository/skill validators before handoff.
