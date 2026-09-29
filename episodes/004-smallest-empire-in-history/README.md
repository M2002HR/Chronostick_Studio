# Episode 004 — The Smallest Empire in History

## Current state

- Spanish script and supplied word timestamps are accepted. The word timing ends at 62.120 seconds; the user approved a 65.000-second picture timeline of 13 five-second clips.
- The three-seed r003/r004/r005 queue finished successfully: 39 jobs, 14 sampling steps each. Earlier r001/r002 attempts and their reviews remain archived.
- The user selected one editorial render per slot. The exact mixed-revision selection and source hashes are in `renders/selection-manifest-r001.json`; no substitution was made.
- The selected clips were concatenated to `final/episode-004-smallest-empire-in-history-concat-r001.mp4` and upscaled frame by frame to `final/episode-004-smallest-empire-in-history-picture-master-1080x1920-r001.mp4`. Technical review is in `final/picture-master-review-r001.md`: 1080×1920, 24 fps, 1,560 frames, 65.000 seconds of picture with original SFX. Background upscale succeeded and ComfyUI was restored.
- The Spanish narration candidate `audio/narration-es-candidate-r001.m4a` was extracted from `/home/mhr/Downloads/historia_04.mp4`. It lasts 62.322 seconds and is **not yet confirmed** as the approved voice. The picture/SFX master must not be labeled as the narrated release.
- A provisional narrated review copy is ready at `final/episode-004-smallest-empire-in-history-narrated-preview-r001.mp4`. It keeps the picture bitstream unchanged and mixes the candidate voice over quieter native SFX; provenance and loudness checks are in `final/narrated-preview-review-r001.md`.
- A complete thumbnail was generated at `delivery/youtube/thumbnail-episode-004-r001.png`. Its prompt, provenance and assistant visual review are in `delivery/youtube/`. Spanish upload metadata is drafted in `metadata.json` and `metadata.md`. Channel review and operator upload decisions remain pending. No upload or publication occurred.

## Next release step

Confirm whether the extracted narration is the final approved Spanish take. Then mix it against the immutable picture/SFX master, review the complete narrated playback and CTA timing, and save a separate distribution-master revision. Review the thumbnail and upload decisions before publication.
