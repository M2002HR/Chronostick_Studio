# Episode 002 r003 targeted review

## Clip 04 — diagnosis only

Status: rejected candidate; no rerender requested or submitted.

Observed result: the curtain appears first, then an uncontrolled bald human figure forms at the curtain edge before the video opens into a wider street scene.

Likely cause: the prompt asked for an anonymous pair of sandal-clad legs under the curtain without supplying a controlled foreground-character reference. The model completed that partial human cue into a whole person. At the same time, the city reference contained tiny background residents and the later beat requested three residents plus a handcart, so the model had several competing human-composition cues. The curtain-to-street transition gave it room to morph those cues instead of preserving one clean reveal.

Recommended correction for a future retry: use a single-scene curtain/street anchor that already contains the exact intended feet and lower legs, describe the curtain as an occluder rather than a source from which a person emerges, keep the same camera and geometry across the reveal, and avoid introducing the later group until a hard cut. More sampling steps alone will not resolve this semantic/reference ambiguity.

## Clip 17 — r003 rejection and r004 correction

Clip 17 r003 was rejected because it began with imagery resembling an earlier transition state and created a bright new explosive event near the ending. The prompt included enough event-related semantics for the model to reconstruct a narrative transition instead of holding the already-completed aftermath.

The r004 prompt removes event vocabulary and defines the aftermath as an existing state before frame 1. It requires one locked-off, unbroken shot with constant geometry, exposure, skyline, and subdued illumination. Motion is limited to slow haze and a small foreground paper movement, followed by a resolved still hold.

Render job `dd6d58e4-5d11-4cf5-bee9-0f4a81178942` completed successfully. Review at four samples per second across the full 5.00 seconds confirmed the same post-event city view from start to finish, with no earlier intact state, flash, growing focal cloud, fireball, or new explosive event. Use `renders/editorial/clip-17-aftermath-r004.mp4` for final selection.
