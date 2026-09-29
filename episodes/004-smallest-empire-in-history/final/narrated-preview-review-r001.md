# Spanish narrated preview r001

**Status:** provisional review copy. The source take has not been confirmed by the user as final; this is not the approved distribution master.

- Voice candidate: `audio/narration-es-candidate-r001.m4a`, extracted from `/home/mhr/Downloads/historia_04.mp4`; SHA-256 `1bc0776eddc746edeccdcb5336d1aa8f34b8e7a8e7268abe4b7bc2768130fd81`; 62.322358 seconds. The source basename matches the supplied `historia_04` word-timestamp CSV, whose last spoken word ends at 62.120 seconds. This is strong provenance evidence, not a final take approval.
- Input picture/SFX master: `final/episode-004-smallest-empire-in-history-picture-master-1080x1920-r001.mp4`.
- Preview: `final/episode-004-smallest-empire-in-history-narrated-preview-r001.mp4`; SHA-256 `5f046c6ba2e38a0d2ef3a1f60ef7b8e553186fcc6667f45368cf12093757298b`.
- Reproduction: `automation/mix-narration-candidate-r001.sh`. Voice starts at timeline zero and is raised 1.5 dB; native SFX are reduced 10 dB. Audio is resampled to 48 kHz, summed without automatic gain normalization, peak-limited to 0.95 linear, and encoded as 256 kb/s AAC. No music is added. The video bitstream is stream-copied unchanged.
- Probe: 1080×1920, 24 fps, 1,560 frames, 65.000 seconds. Encoded video elementary-stream SHA-256 matches the picture/SFX master exactly: `12d31ed93370295e6a339afff8f048dee3bb048e7cf351224671185445cba49e`.
- Measured preview audio: −15.6 LUFS integrated, 4.1 LU loudness range, −3.0 dBFS true peak.

**To release:** confirm this is the final Spanish narration, listen through the full preview for voice alignment, music leakage or clipping in selected SFX, CTA timing and end hold, then approve an immutable distribution master. The technical measures above do not replace listening QC.
