# Reference-first Shorts workflow

This is the new-video default when the user supplies a downloaded reference.
It implements the 2026-10-05 user direction: Spanish, a chosen 20–30-second
target, rapid purposeful cuts, 4–7-second editorial clips and 16 H3 steps.
Existing episodes retain their approved profiles. The original text-first
route remains in `workflow.md`; long-form retains its own format contract.

## Stage order

1. Create the episode with `scripts/new-short-episode.py`, preserve original
   video bytes and provenance, probe its streams, and record a working output
   target. Input duration is not the output target.
2. Use `chronostick-transcribe` and `scripts/ajil-transcribe.py` for the original
   speech with word and segment timing. Preserve the raw response, traceable
   audio derivative and failed revisions. Review text against the actual input.
3. Use `chronostick-reference-video` to inspect actual footage alongside its
   transcript. Record timecoded story/editing observations, source claims,
   character roles, generation feasibility and retained/adapted/dropped ideas.
   Preserve supplied claims, numbers, dates, causal links and payoff. Independently
   verify only on the user's explicit request; otherwise record
   `fact_check_requested: false` and source provenance without claiming verification.
4. Use `chronostick-script` to draft the compressed scenario and original spoken
   Spanish. Preserve the useful source story and directing mechanisms closely
   while maintaining ChronoStick identity/style authority and factual meaning.
   Immediately after writing or revising narration, run
   `chronostick-voice-direction`: deliver the clean script plus its Google Vids
   paste copy with many fitting emotion/style cues, notes and text validation.
   Do this for drafts before storyboard review and without a separate request.
   Record preparation in the `voice` substage; actual audio acceptance stays
   a later gate. Every revision regenerates its tagged copy. Only an explicit
   user/provider override skips this preparation.
5. Use `chronostick-storyboard` to draw a complete neutral monochrome rough
   storyboard. It is deliberately outside the stick-world production style.
   User review of scenario and storyboard gates production reference generation.

6. After that review, references and voice can progress independently:
   - `chronostick-references`: pure prompts first, then reviewed single-person
     stick identities and enough full-frame single-scene anchors to support
     every planned shot. No production sheets, grids or multi-pose images.
     Inspect the actual approved storyboard pages while planning and reviewing
     anchors. Map every reference to `storyboard_panel_ids` and source-analysis
     IDs; preserve composition, roles, action and prop state while translating
     neutral sketches into the approved production style.
     Freeze each image request with `scripts/reference-artifacts.py freeze`,
     verify its exact prompt/input hashes before the built-in image call, then
     `ingest` the returned PNG unchanged. Candidates become selected only after
     actual full-frame/phone-size storyboard comparison; keep rejected revisions.
     The style board controls rendering, never the new scene's architecture or
     era. Check tiny prop drawings for anachronisms as well as the main scene.
   - Finalize the exact Spanish script. Before Google Vids handoff, use
     `chronostick-voice-direction` to prepare the separately tagged paste input
     from the registered menu: fast expressive Short delivery, frequent useful
     emotions and no whisper. Validate unchanged spoken text; record the voice
     direction substage, paths and hashes. Ingest the user's generated voice
     with `scripts/ingest-narration.py`: archive source bytes and save a full
     native-rate/channel PCM WAV for assembly, plus a native AAC stream copy
     when applicable. Record the assembly voice path separately from compressed
     STT derivatives. Review pronunciation, words, delivery and actual duration.
7. Use `chronostick-transcribe` in voice mode with `--language es` and
   `--expected-script`. Preserve this response separately from source timing;
   resolve mismatches before the accepted-voice timing map.
8. Reconcile scenario/sketch/reference coverage with actual voice timing using
   `chronostick-timestamps` and `chronostick-shot-plan`. Choose variable 4–7-
   second editorial slots and frame-aligned local cut times. Reopen affected
   creative decisions when voice timing requires material revisions.
   Inspect the actual sketch pages and map each final shot to its panel IDs.
   Record combined, omitted or retimed panels and reasons separately in
   `plan/storyboard/timing-reconciliation.json`; never silently replace the
   storyboard with an unrelated shot plan or use sketches as H3 references.
9. Write detailed pure video prompts, deterministic jobs and complete preflight.
   Each prompt states its actual durations, reference roles, inventory,
   identity/state, rapid local shots, camera/light, isolated SFX and resolved
   end. Generation defaults to 16 steps, Lightning off. Use the exact sentence
   `NO BACKGROUND MUSIC. Natural diegetic sound effects only.` once in each file.
   `scripts/build-short-prompts.py` renders the already reviewed directing
   decisions into pure files; `scripts/build-short-jobs.py` packages the fixed
   seeds and native request durations. Run `scripts/preflight-short-batch.py`
   against the actual local service to archive resolver responses and the full
   CLI dry-run in `automation/preflight.json`. These commands do not queue work.
10. Generate the authorized batch, review actual clips and sound, replace only
    failures, then select, concatenate, upscale, mix the accepted voice and QC
    the full distribution master. Close with thumbnail/metadata/provenance.
    Local voice/caption/sound finishing follows `docs/postproduction.md`, with
    an explicit native-audio choice and immutable distribution revision.

## Timing and engine contract

Speed comes from purposeful cuts and contrast with moderate motion: one primary
action and at most one simple camera move per shot. Shot density follows the
chosen duration, word timing, legibility and references; the older exactly-
eight-shots-per-five-seconds rule is not inherited as a fixed quota. Plan a
strong immediate hook, escalation, payoff and useful replay return. Add the
default tiny spoken subscribe CTA after the payoff (`Suscríbete.` in Spanish),
with delivery matching the scene, within the chosen total runtime. An explicit
user override can omit it; it does not require a generated button/text scene. Do not
compress by dropping qualifications, truncating speech or making it unintelligible.

The new profile is `h3-short-dynamic-16step-20-30s`. Raw H3 output uses the
service's frame grid; each slot separately records editorial duration and
generation request duration. A 4-second editorial slot may use a supported
5-second request with action resolved by 4 seconds and a terminal hold, followed
by automatic trimming without time stretch. Pilot this strategy before relying
on quality. No creative manual-editing pass is assumed: engine-generated shots
must supply the planned cuts, scenes and effects.

Use `scripts/build-short-timing.py` to preserve provider bytes and derive the
reviewed integer-frame slots, then `scripts/validate-short-plan.py` for actual
cut/reference/panel coverage. Word-overlap normalization stays a separate
derived estimate; number phrases keep their aggregate provider intervals.
An accepted full voice outside the original target requires a scoped
`episode.json.duration_override` with user evidence and the accepted voice hash.
The picture ends on the first frame covering the complete voice; future targets
stay 20–30 seconds. Episode 007's recorded continuation uses 33.375 seconds,
six dynamic slots, and no narration trim or time stretch.

## State and review

The new route uses `pipeline-state.json` schema version `2.0` with semantic
stage IDs and `workflow: reference-first-v1`. `validated` means a technical
check; `needs_review` means a reviewable artifact exists; `approved` requires
actual recorded reviewer/decision evidence. Source extraction never approves
scenario, storyboard, production references or accepted narration.

Changing source analysis affects selected scenario/sketch ideas; changing the
script or accepted voice invalidates its timing and affected direction/prompts/
jobs. Changing a reference invalidates affected mappings/jobs and requires a
new render revision. Replacing one selected take invalidates downstream masters,
not unrelated accepted clips. Keep independent reference and voice branches
explicit, and preserve all media under immutable `-rNNN` revisions.

`scripts/validate-reference-first.py` checks this route. The general repository
validator dispatches by episode format; legacy profiles and checks remain.
Validate scripts/skills, references, missing artifacts and `git diff --check`
at each handoff. Additional duration/job/selection contracts must be exercised
against the real example when those stages are reached; pre-voice plans remain
provisional.

The extraction and joint video/transcript analysis modules can also serve
long-form. Audio larger than the transcription helper's 24 MiB limit needs
offset-preserving chunking before that path is usable. Shared module reuse
does not change long-form's landscape format, target duration or named profile.


## Actual render timing gate

Use `scripts/audit-short-render-timing.py EPISODE --revision rNNN` after outputs
appear and again when all clips are ready. Keep each audit immutable. The job
request, compiled H3 raw grid, raw media, editorial frame count and every PTS
must agree with the approved timing map. Missing takes remain pending.

Internal cut timing is a separate actual-frame review. Record the observed cut
frames and beat mapping, not only the intended prompt timings. Inspect every
raw-tail frame: a required late shot in that tail makes automatic trimming
creative loss, even when the editorial length is exact. Repair only affected
takes or record a scoped actual-picture acceptance; never silently call that
late story action a resolved hold. Accepted voice is never stretched to cover
container rounding or a failed picture take.
