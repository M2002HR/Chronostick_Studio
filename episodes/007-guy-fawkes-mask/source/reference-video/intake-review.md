# Actual-reference intake review — 2026-10-05

User title: **Why does this Mask mean Boom boom?**
User URL: https://www.youtube.com/watch?v=JgBU_c7RVq0
The downloaded file is the inspected source; channel/creator metadata was not retrieved.

Original `reference-guy-fawkes-mask-r001.mp4` is byte-identical to the incoming
download: SHA-256 `ef2ca0ebcf74f750607b302ec60c105b58dfb5d60c069e8987622f8ac291b289`,
3,037,997 bytes. Container 71.70322 s; portrait 360×640, 30 fps; AAC audio.
The original root filename is retained in `manifest.json`. The relocation did
not transcode or crop it.

## Extraction and actual inspection

Ajil returned English speech using Groq Whisper large-v3-turbo in extraction
r003. Derived revision r004 preserves those response bytes and the same MP3
derivative exactly, with **no additional STT request**. It contains 204 timed
words and 15 segments; first word 0.10 s, last word end 71.62 s. Reconstructed
word tokens agree with provider transcript text. This is source timing only.

The provider has ten overlapping-word rows and four nonmonotonic starts.
See `transcription/reference-validation-r004.json`; no original timestamps were
rewritten to conceal them. They are usable for approximate source analysis,
not an approved frame-accurate alignment. r001/r002 timed-out requests and the
r003 parser failure remain archived with their raw responses/provenance.

Actual video inspection covers 144 sampled frames at 2 fps across the complete
timeline, viewed in all nine `inspection-r001/contact-NN.jpg` boards alongside
the transcript. `sampling.json` records extraction. Observations and uncertainty
are in `../../plan/reference-video-analysis.md`. Frame sampling supports framing,
subjects and broad visual sequence; it does not prove every cut or continuous
motion between samples.

A supplementary native-video/audio review was attempted through Ajil/Gemini.
All three machine-review attempts failed or returned a local fallback; none is
accepted as actual video analysis. r001's initial success flag was corrected to
rejected. Native-video review and perceptual audio review remain unavailable.
Do not claim the source's music, sound design, delivery or exact STT pronunciation
was heard and checked. The new script is a review draft, not accepted voice.

## Initial direction

Preserve the recognizable mask question, short historical chain, powder threat,
arrest reversal and image/idea payoff. Adapt the long religious exposition,
gang roll-call and platform-game barrel sequence into a short, legible causal
chain that H3 can generate. Keep period Fawkes separate from the modern mask.
Verify facts independently; this reference is creative input, not historical
authority. Neutral storyboard and scenario require the user's review before
production reference design.
