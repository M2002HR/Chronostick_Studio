# Episode 002 Persian narration — technical review candidate

Status: **needs native listening review; not approved for publication**.

The final candidate is `audio/narration-fa-r002.wav`; the viewing copy is
`final/episode-002-fa-review-r003.mp4`. The picture stream hash of the viewing
copy matches the source picture stream. The WAV is 85.021333 seconds long and
the viewing copy is 85.000 seconds long (the fixed 24 fps picture has exactly
2040 frames). The viewing copy is 1080×1920, with integrated loudness near
-18.3 LUFS and true peak near -1.7 dBFS. Only the approved natural SFX and new
Persian narration are mixed; no music or source-language narration was added.
The earlier narration r001 and viewing copies r001/r002 are retained as
superseded test renders, not delivery choices: r001 had less precise cue pauses,
and the first viewing-copy limiter setting produced an unsafe near-0 dBFS
encoded true peak. The final viewing copy uses corrected limiting.

Seventeen Gemini 3.8 Flash TTS takes were placed by semantic picture cue. Four
phrases received colloquial text revisions and new immutable takes. Three
documented subsecond silences were inserted at quiet phrase boundaries; no
speech or video was globally time-stretched. The important count/scene anchors
and their provisional offsets are in `timing/alignment-r002.json`. The final
spoken word ends near 83.53 seconds, leaving an intentional 1.49-second quiet
hold over the resolved aftermath wide frame.

The raw local faster-whisper result was saved directly from the assembled WAV
as `timestamps/word-timestamps-source-final-r002.json`. It recovers the story's
sequence but misspells several colloquial Persian words; it is **not** an
approved transcript or canonical word-timing CSV. An additional blind Gemini
audio-review request failed twice with temporary HTTP 503 service-unavailable
responses, so there is no independent provider listening verdict. No API key
was written into project files. The additional Ajil `.env` keys were not used.

Before calling this narration approved, listen to the complete viewing copy at
normal speed for Iranian-Persian accent and natural storytelling, sentence
joins at 6.4/10.1/50.3/70.45 seconds, the colloquial readings of “پونزده”
and “هزار و نهصد و چهل و پنج”, and balance of SFX against voice. The fictional
couple and exact countdown are dramatic devices, not recorded identities or a
literal historical clock. If any line sounds artificial, revise only that cue
and render a new immutable take; do not cover the flaw with speed warping.
