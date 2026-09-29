# Picture/SFX master r001 — technical review

**Decision:** technical assembly and upscale passed; full narrated distribution master is pending confirmation of the Spanish voice source.

## Inputs and provenance

- User-selected set: `renders/selection-manifest-r001.json`, exactly one 5.000-second editorial clip for each slot 01–13. Source revisions remain immutable.
- Concat: `episode-004-smallest-empire-in-history-concat-r001.mp4`, SHA-256 `04825f89da024da052db03e5964195b83fe1a9b8c99959a6688fefb9911ae077`. Service job `4fe057a5-0f16-4a8c-a68c-7729f6736087` succeeded; adjacent `.run.json` records the sorted input order.
- Upscale: `episode-004-smallest-empire-in-history-picture-master-1080x1920-r001.mp4`, SHA-256 `2da32e451abcb3b17b0c7591165d4dad303f68914b64a68644caa36949095550`. Framewise RealESRGAN_x4plus_anime_6B, `fit=cover`; adjacent `.framewise-upscale.json` records model hash, settings, resources and completion. Background service succeeded and ComfyUI was restored.

## Checks

- Every selected input was probed before concat: 480×864, 24 fps, 120 frames, 5.000 seconds, with video and audio streams. The 13 selected hashes match their editorial sources.
- Concat and upscaled picture each have 1,560 video frames at 24 fps: exactly 65.000 seconds of picture. The AAC tail makes the MP4 container 65.021333 seconds; it does not add picture frames.
- Upscale output probes as 1080×1920 H.264 with AAC stereo. It retains the full selected sequence and SFX stream.
- A contact sheet of the 13 upscaled midpoint frames was visually inspected for shot order, crop, composition and gross style/identity changes. The final CTA frame was inspected separately; the selected red button reads white `SUBSCRIBE` and remains inside the safe frame.
- Audio stream exists throughout. Measured decoded SFX mean is approximately −24.1 dBFS; sample peak reaches 0.0 dBFS. No loudness processing or narration mix has been applied. This measurement does not establish whether individual generated effects contain music or clipping.

## Remaining release check

The user-selected clips are honored as supplied, including Clip 13 r001. A frame sampling review does not replace a complete frame-by-frame and listening review. Confirm the final Spanish narration source, mix it with the picture/SFX master, then review voice timing, CTA timing, SFX balance, seams and full playback before approving a narrated distribution master. The thumbnail has separate assistant visual QC and awaits channel approval.
