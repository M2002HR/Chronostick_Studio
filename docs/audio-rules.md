# Audio rules

## Permanent policy

Generated images/video clips remain free of background music. Since the user's
2026-10-05 instruction, supplied music, ambience and SFX may be separate local
finishing tracks under [`postproduction.md`](postproduction.md). No track is
added implicitly; the edit records assets, gains, placement and mix review.

Forbidden in generated clips: soundtrack, score, melody, beat, orchestral music,
musical ambience, trailer risers, and generated cinematic music.

Allowed: separately recorded narration, footsteps, cloth, paper, wood, object handling, room tone, wind, restrained crowd ambience, and other natural diegetic sound effects.

Every video prompt must contain exactly:

`NO BACKGROUND MUSIC. Natural diegetic sound effects only.`

Generated clips must not contain dialogue, narration, vocal reactions, or lip-sync audio. The approved Spanish narration is a separate continuous track added during assembly. Generated ambience remains secondary and may be replaced or muted in editing.

For local finishing, choose `native_audio.mode` explicitly: `mute` excludes the
original audio completely, while `preserve` retains it as a configurable stem.
Keep the source picture/SFX master immutable. Episode 006 is narration-only
with native audio muted; music/background/SFX layers await actual supplied files.
Ordinary captions use the format-specific font in `docs/postproduction.md`
(Montserrat Bold for new Shorts; Arial Bold for long-form), white text and a yellow highlight on
only the currently spoken word, using actual accepted voice timings.

When Google Vids supplies the external voice, the optional voice-direction stage and tag evidence are in [`google-vids-voice-direction.md`](google-vids-voice-direction.md). Keep the clean narration separate from the tagged Vids input. Approve pace and duration by listening to the generated voice; derive timestamps only from that accepted audio.

## Localized narration

A translated narration is a separate program track, never a modification of a
generation prompt or visual render. It must be mixed only against the approved
picture/SFX master (or an approved SFX stem). If a supplied master has the
Spanish narration baked into the only available audio stream, do not attempt to
mask it with the new language; obtain the picture/SFX master or rebuild the
permitted natural effects first.

The target-language voice and captions have their own actual timestamps. A
spoken-language change invalidates only that localization's audio, timing,
caption, mix, and distribution master; it does not invalidate approved visual
assets or H3 renders.

## Reference-first Short sound contract

For `h3-short-dynamic-16step-20-30s`, use only brief isolated non-tonal diegetic cues with silence between them. No continuous ambience, room tone, rhythmic repetition, drone, musicalized sound bed or background music. Generated speech and lip sync remain forbidden; the accepted Spanish user voice is added as a separate track. Review actual audio, not just prompt wording.

Put this silent-default contract at the opening and ending of every generated
clip prompt, with the exact mandatory policy sentence once. Explicitly forbid
music on transitions and the final hold; each physical SFX ends immediately.
A user report of music rejects the take even when its prompt and JSON prohibit
music. Retain that evidence and review the replacement's actual sound. Do not
mix a contaminated native stem under narration or call stronger wording proof
of silence. Machine sound analysis is supplementary and must not be reported
as personal listening.

For independently sourced clean effects and full native-sound replacement,
follow [`clean-sfx-workflow.md`](clean-sfx-workflow.md) and `chronostick-sfx`.
