# Independent clean SFX

Use this module when an actual render's sound violates the episode contract or
when separately selected physical effects are requested. It preserves the
approved picture. The reference-first route allows only short dry physical
cues, with silence between events and no background music. Narration remains
the unchanged accepted user voice.

Default priority is the actual reviewed native engine SFX, generated with
strong silence/no-music locks. Independent replacement is a fallback for
soundtracks that actually fail review. Episode007's latest user direction
accepts the shown three-cue replacement as a fallback and explicitly prefers
the engine's more naturally synchronized SFX where it produces clean audio;
see `plan/native-sfx-priority-r001.json`. This supersedes the earlier blanket
native-exclusion proposal for future takes.

## Source and timing evidence

Inspect actual output frames before selecting effects. Record material, contact
or motion time and narrative purpose; the intended prompt alone is insufficient.
If the engine omits a latch release or other action, omit that cue too. Use
sparse effects at actual actions instead of a sound on every cut.

Prefer an independently recorded source with a verified reusable license.
Store its creator, page URL, exact license, downloaded bytes/hash and quality.
An HQ MP3 preview is not the original PCM file. Derive a short one-shot from a
real transient, record source in-point/gain/fades, and inspect/listen to the
result. Source titles and license labels do not certify absence of music.
Keep source approval separate from a particular placement or final mix review.

## Native soundtrack exclusion

Repeated music after stronger generation locks is a demonstrated engine issue.
Do not call another prompt iteration a guarantee. Record the episode's choice
to exclude native sound completely and preserve immutable original takes.
Use an independent clean stem; never lower a contaminated soundtrack under
voice or crop supposedly clean events from it.

`scripts/clean-short-sfx.py EPISODE --plan PLAN --preview` creates an unapproved
listening candidate. The JSON plan binds `source`, `source_sha256`, unused
`output`/`stem` paths, `native_audio: exclude_completely` and sorted `cues`.
Each recorded cue binds `asset_path`, `asset_sha256`, `review_evidence`,
`review_status`, `start_seconds`, `gain_db` and `observed_action`. This module
currently accepts mono 48 kHz PCM16 one-shots of at most 150 ms; longer effects
need an explicitly reviewed contract extension. No effects are looped.

Without `--preview`, source sounds must have an actual review decision. Preview
paths cannot enter final-selected. The script maps source video only and the
new stem's audio, stream-copies the picture, compares every decoded frame and
records exact-zero PCM intervals. Audio encoding can spread a transient by a
few samples; technical zero in the source stem is separate from final listening.
The sidecar explicitly records zero native samples contributing to the mix.

## Episode 007 evidence

Both native 16-step clip-04 pilots contained user-reported music despite prompt
and JSON locks. The user accepted the second animation. Its independent sound
preview keeps all 110 picture frames unchanged, excludes the whole native
track, and places three separately recorded short cues at real handoff,
lantern-handle and sleeve-grip events. The absent independent latch action gets
no cue. Source pages, licensed previews, excerpts, plans and hashes are under
`episodes/007-guy-fawkes-mask/audio/sfx/` and `plan/`.

The real source candidates are paper by BenjaminNelan (Freesound 353125), cloth
by zazz.sound.design (435296), and a small metal contact by scaevola (333260).
Each actual source page records CC0. Preserve this provenance and the user's
actual sound decision; no preview is an accepted final mix by default.


## Dynamic-clip audio assembly

After selection, preserve the approved per-clip native/fallback choices. Decode
selected audio to a common48kHz stereo stem, reset each clip origin, and silence-
pad/trim decoder or mux tails to its exact editorial frame count before audio
concatenation. At24fps, each frame is2000 samples. Archive inputs, sample counts,
hashes and FFmpeg command. This gives one continuous SFX timeline without time
stretch or any new music/ambience. Mix it once beside the unchanged narration;
exclude the old concatenated soundtrack to avoid doubling sound. A framewise
picture export resets the same ordered decoded pictures to the declared fps.
Episode007 records801 frames /1602000 stereo samples /33.375 seconds in
`audio/sfx/selected-full-stem-r001.json`.
