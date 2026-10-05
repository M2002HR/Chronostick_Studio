# Supplied Spanish voice — intake review

User supplied `historia_07.mp4` and explicitly asked to extract/store its voice
for final assembly. Archived source: `source/voice-export-es-r001.mp4`.
Assembly candidate: `narration-es-r001.wav`; native AAC copy: `narration-es-r001.m4a`.

The WAV preserves decoded PCM samples, 24 kHz, mono and the complete 800,768
samples (33.365333 s). Archive bytes, WAV decoded samples and AAC packet data
were independently compared to the supplied export and match. No gain, silence
trim, resampling or time stretch was applied. Extraction provenance and technical
QC are recorded beside these files. The MP3 in `../timestamps/ajil/` is only an
STT derivative; it is not the assembly narration.

## Actual Ajil transcription

Groq Whisper large-v3-turbo through Ajil returned 76 words and six segments.
Its text matches the clean 80-word script apart from number formatting:
`mil seiscientos cinco` → `1605`, `treinta y seis` → `36`. These are equivalent
number forms, not evidence of missing spoken content. Names and the final
`Suscríbete.` are present. No direction tag appears in the recognized text;
this is STT evidence, not a complete perceptual listening verdict.

Raw provider word coverage is 0.18–33.28 s; segment CTA span is approximately
32.40–32.94 s. Provider word and segment endpoints differ. Three word overlaps
and one nonmonotonic start remain in the raw output. Do not split number tokens
into invented word times or silently correct boundaries. See the exact response,
word CSV, segment JSON and validation in `../timestamps/ajil/`.

## Open decisions

The full voice is 3.365333 seconds longer than the 30-second working target.
The recognized closing content extends past 30 seconds, so the difference is
not simply trailing silence. Preserve this candidate for the requested final
assembly; an eventual accepted duration/voice revision requires an explicit
decision and its own timing. Do not cut off the payoff or CTA to fit the target.

Perceptual delivery, pronunciation, tag execution and absence of background
music have not been independently heard/accepted in this intake. No accepted
voice or final timing map is fabricated. Source speech and technical checks
are available for that review; scenario/storyboard approval remains separate.
