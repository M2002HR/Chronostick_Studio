# Localizing an approved ChronoStick picture master

## Purpose and boundary

Localization turns one approved ChronoStick picture/SFX master into a separate
language release without rerunning image or video generation. It is a
post-assembly branch, not a revision of the source episode. Each branch lives
at:

```text
episodes/<id>/localizations/<bcp47-language>/
```

Use the language tag from BCP-47 in lowercase: `fa`, `es-mx`, `pt-br`. Never
replace the source-language voice or master. A language branch may change only
its narration, captions, language metadata, mix, and distribution master.

The essential idea is **semantic cue synchronization**, not word-for-word
synchronization. A Persian phrase does not need to begin when the equivalent
Spanish word began. It must land while the same visual idea is on screen: a
name when the character is revealed, a count while its visual counter is shown,
an action as it occurs, and the CTA while its closing image is held.

## Preconditions

- An approved immutable picture/SFX master exists. It is the fixed duration and
  visual-timeline authority.
- The source script, its actual timing map, and the shot plan are available.
  If the original voice is unavailable, this is still sufficient for a manual
  target-language branch because the picture/SFX master is the authority.
- The master contains no source narration, or a separate approved picture/SFX
  master or SFX stem exists. Never cover an embedded Spanish voice with Persian.
- The target-language translation has been fact-checked and editorially
  adapted. It is not a literal translation quota.

Episode 001 currently has only a mixed external video and no archived source
voice/timestamps, so it needs an SFX-only master (or a fresh approved SFX mix)
before a clean Persian replacement track can be made. Episodes 002 and 003
already have picture/SFX masters, but their Spanish narration files remain
external; that does not block manual Persian localization.

## Required branch artifacts

Start from
[`templates/localization-manifest-template.json`](templates/localization-manifest-template.json).
The manifest records paths, provider provenance, and review state; it is not a
generator prompt. Use this structure:

```text
localizations/fa/
  localization-manifest.json
  script/narration-fa.md                 # canonical words actually spoken
  timing/visual-timing-map.json          # fixed visual cues and tolerances
  timing/segments.json                   # adapted Persian text per cue window
  synthesis/                              # provider inputs and attempt records
  audio/narration-fa-rNNN.wav             # immutable accepted/rejected takes
  timestamps/word-timestamps-source.json  # raw provider/STT result, unchanged
  timestamps/word-timestamps.csv          # reviewed canonical word timing
  timestamps/timing-map.json              # timing derivation and validation
  captions/captions-fa.srt
  final/<episode>-fa-rNNN.mp4
  review-rNNN.md
```

Do not put internal decisions in a generation prompt. `narration-fa.md` is the
canonical spoken text, while a provider control input such as an Eleven v3
file containing `[pause]` may live under `synthesis/` and must identify the
script revision it realizes.

## 1. Lock the visual timing authority

Hash the selected picture/SFX master and record its actual duration in
`localization-manifest.json`. Copy the source timing map's semantic beats and
the shot plan's visual reveals into `timing/visual-timing-map.json`. Do not copy
the source words as target timestamps.

Use a cue for each point where wording visibly matters. A cue has a fixed
start/end window, a concise visual intent, an allowed tolerance, and a target
language text unit. Prefer 5–20 second complete thoughts. Split only at a
natural breath/pause; do not force every five-second render slot to be a voice
chunk.

The default review tolerances are:

| Check | Default |
| --- | ---: |
| important visual cue onset | ±0.25 s |
| ordinary beat boundary | ±0.50 s |
| narration end versus picture end | 0.12 s or an explicitly planned silent hold |

These are review thresholds, not a license to warp a voice. An action with a
single obvious visual moment may require a tighter documented tolerance.

## 2. Adapt the script to time budgets

Write natural target-language narration from the source meaning and visual cue
map. Persian usually needs different word order and phrase length than Spanish;
make the Persian concise or explanatory where the picture allows it. Preserve
historical qualifications and do not add claims merely to fill time.

For every cue window, record `localized_text`, target start/end, and intent in
`timing/segments.json`. Review the script aloud before synthesis. If a unit is
too long, shorten or restructure the Persian text first; if it is too short,
add a meaningful clarification or allow a natural visual hold. Do not use a
literal translation, a stretched waveform, or a changed video as the primary
timing control.

## 3. Choose the synthesis route

### Preferred when ElevenLabs Enterprise is available: Dubbing v2 with supplied segments

ElevenLabs Dubbing supports Persian (`fa`) and is designed to preserve delivery
timing. Its enterprise "bring your own transcript/translations" workflow takes
segments with explicit `start_s`, `end_s`, source text, and supplied target
translation. Use the approved source-language narrated master as source media,
or the source voice plus approved SFX background where available. Create
segments from the visual cue map, not automatically detected arbitrary cuts.

The service renders each Persian translation into its segment span. Keep every
segment 0.1–25 seconds, use natural pauses between segments, and keep the
spoken length comparable to its window. Store the provider project/language
IDs and the downloaded lossless output in the manifest. Transcript and
translation editing/regeneration through the Dubbing v2 API are documented as
Enterprise-only; do not build production around that control on a self-serve
plan.

### Recommended self-serve ElevenLabs route: Eleven v3 + measured iteration

Eleven v3 supports Persian, but its numeric speed setting is unavailable.
Generate a clean lossless narration take from the time-adapted Persian script.
Punctuation, line breaks, and carefully tested `[pause]` controls can create
planned breathing room, but are creative directions rather than timing
guarantees. Preserve every candidate as `narration-fa-rNNN` and record its
script revision, voice, model, control input, measured duration, and rejection
reason in `synthesis/attempts.json`.

Use this correction order for an out-of-window take:

1. rewrite only the affected Persian cue unit;
2. regenerate that natural thought with the same voice/model;
3. adjust a documented pause or delivery direction;
4. accept natural silence where the visual is already holding;
5. only use a provider-supported local rate control after an audible review.

Never globally time-stretch the accepted narration or the video merely to
force an exact endpoint. A new audio take is a new immutable revision.

### Useful fallback for strict cue instrumentation

Google Cloud Gemini-TTS lists Persian (Iran) as `fa-IR` in Preview and exposes
speaking-rate control. Its SSML `<mark>` timepoints can be placed at semantic
cue boundaries. It is a valid controlled alternative if its Persian voice
passes your editorial listening test. It remains a provider evaluation, not a
silent substitute for the selected ElevenLabs voice.

## 4. Derive actual Persian timings

The target voice is the only authority for its word timings. Preserve the raw
provider/STT response unchanged as
`timestamps/word-timestamps-source.json`, record its SHA-256, and derive the
reviewed CSV separately. Do not estimate timing from text length and do not
translate the Spanish CSV.

ElevenLabs Forced Alignment is not the Persian route: its published supported
language list does not include Persian. Use ElevenLabs Scribe v2 instead for a
first word-timestamp pass; Scribe v2 supports Persian and returns word-level
timestamps. Supply key terms for historical names when available, compare the
result against `narration-fa.md`, then correct only canonical transcript labels
or word boundaries that an editor has audibly verified, with a review note. The
raw response remains untouched.

Create `timestamps/timing-map.json` with narration start/end, words overlapping
each visual cue, cue deviations, silence/holds, source hashes, and the result
of text-coverage validation. The timing stage is approved only after the
accepted Persian audio—not a draft or a provider preview—matches the canonical
script and lands within the declared visual-cue tolerances.

## 5. Captions, mix, and review

Generate Persian captions from the approved Persian timing CSV. Render a real
RTL test: verify glyph joining, right alignment, punctuation direction,
line-break order, Latin names/numbers, and safe-area placement on a phone. Do
not infer caption timing from Spanish captions.

Mix the target narration with the allowed natural SFX from the approved master.
Remove or mute no narration by guesswork: source-language speech audible under
the Persian voice is a failure. Keep the no-background-music policy unchanged.
Export a new immutable language master and review at normal speed for factual
meaning, cue sync, pronunciation, captions, source-language leakage, SFX,
loudness, audio clipping, duration, and vertical geometry.

## Provider evidence checked on 2026-09-28

- [ElevenLabs Dubbing](https://elevenlabs.io/docs/overview/capabilities/dubbing)
  supports Persian `fa`, preserves timing/background audio, and distinguishes
  automatic Dubbing v2 from editable Dubbing Studio/Enterprise capabilities.
- [Bring your own transcript](https://elevenlabs.io/docs/eleven-api/guides/how-to/dubbing/bring-your-own-transcript)
  documents explicit 0.1–25 second segments and explains that their timing
  controls the dubbed performance.
- [Eleven v3 language support](https://elevenlabs.io/docs/help-center/other/what-languages-do-you-support)
  includes Persian, while [Eleven v3 speed guidance](https://elevenlabs.io/docs/eleven-creative/playground/text-to-speech)
  states that numeric speed is unavailable on v3.
- [Scribe v2](https://elevenlabs.io/docs/overview/capabilities/speech-to-text/)
  supports Persian and provides word-level timestamps; [Forced Alignment](https://elevenlabs.io/docs/overview/capabilities/forced-alignment)
  publishes a smaller language list that excludes Persian.
- [Google Gemini-TTS](https://docs.cloud.google.com/text-to-speech/docs/gemini-tts)
  lists `fa-IR` as Preview; [its SSML API](https://docs.cloud.google.com/text-to-speech/docs/ssml)
  documents semantic `<mark>` timepoints and rate controls.

Provider features and commercial access can change. Recheck these sources
before a new production integration.
