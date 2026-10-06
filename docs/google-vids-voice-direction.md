# Google Vids voice-direction stage

When Google Vids is the selected voice provider, prepare this required workflow handoff immediately after script creation/revision, for Shorts, long-form and localization. Route through `chronostick-voice-direction`. Keep clean narration as the spoken-text authority. Save a separately tagged, paste-ready copy under `script/voiceover-google-vids-<lang>.md`; place direction notes and review decisions outside that file. For long narration, split the tagged copy into ordered scene files. Prepare drafts before script approval; final voice generation uses the reviewed wording and updated tagged copy. Preparation does not imply script, storyboard or voice acceptance.

The user's 2026-10-05 instruction makes preparation immediate: every new or
revised script is delivered with its Google Vids tagged copy, notes and text
validation, including drafts. Do not wait for storyboard review or a separate
formatting request. Use many fitting emotional/style cues throughout by default
in all formats, unless the user explicitly requests another approach/provider.
Preparation does not approve the narration or accept generated audio.

## Current Google Vids menu observed in the user's account

On 2026-10-01, the user supplied screenshots of the **Pace** and **Pauses** menus and HTML from the **Emotion**, **Style** and **Sounds** menus. The labels below are transcribed from those materials, preserving the menu wording and grouping. This account's menu is the tag vocabulary for ChronoStick Google Vids voice scripts. Do not substitute tags recalled from a Gemini API guide or an older Vids example.

The user also copied the exact text inserted after choosing **Rushed pace**: `[rushed pace]`. The paste-ready notation below applies that observed lowercase, square-bracket form to the other menu labels. If a later menu selection inserts a different spelling, update the catalog and affected script from the inserted text.

| Pace (screenshot) | Pauses (screenshot) |
| --- | --- |
| `[slow pace]` | `[short pause]` |
| `[natural pace]` | `[medium pause]` |
| `[rushed pace]` | `[long pause]` |

| Emotion (HTML menu) | Emotion (HTML menu) | Emotion (HTML menu) | Emotion (HTML menu) |
| --- | --- | --- | --- |
| `[admiration]` | `[adoration]` | `[amused]` | `[awe]` |
| `[confusion]` | `[curiosity]` | `[determination]` | `[enthusiasm]` |
| `[excited]` | `[frustration]` | `[happy]` | `[hope]` |
| `[interest]` | `[positive]` | `[surprised]` | `[thoughtful]` |

| Style (HTML menu) | Sounds (HTML menu) |
| --- | --- |
| `[whisper]` | `[swallow]` |
| `[authoritative]` | `[inhale]` |
| `[bold]` | `[clear throat]` |
| `[cautious]` | `[gasp]` |
| `[natural]` | `[shush]` |
| `[robotic]` | `[ugh]` |
| `[sarcasm]` | `[snorts]` |
| `[serious]` | `[giggles]` |
| `[shouting]` |  |

The observed inventory has **3 pace, 3 pause, 16 emotion, 9 style and 8 sound options**. A menu option's presence does not mean every episode should use it. Select tags to support the meaning of each line. For historical narration, comic tags belong on jokes, suspense tags on genuine turns, and a grounded tone belongs on harm or loss.

**ChronoStick rule:** The user has explicitly ruled out `[whisper]` for all future voice scripts. It remains listed above only to keep the observed menu inventory accurate. Do not insert it into any Short, long-form episode or localization; use another fitting emotion/style cue or ordinary punctuation for suspense.

## Placement and pacing

1. Copy the reviewed narration exactly. Add only inline tags from the observed menu inventory; do not change spoken words, order, names, numbers, qualifications or punctuation in the tagged copy. Keep paste-ready files free of headings, commentary, emoji and production instructions.
2. Give each scene a deliberate starting pace. For a fast Short, `[rushed pace]` can establish the brisk opening, with `[natural pace]` at dense facts or the ending. For long-form, start with `[natural pace]`, reserve `[rushed pace]` for short action bursts, and explicitly return to `[natural pace]`. Use `[slow pace]` only when a slower delivery serves a specific beat.
3. Use many emotion/style cues in every sentence, at story turns and meaningful clauses or important words. This expressive default applies to Shorts, long-form and localization; adapt base pace and emotions to the story. For energetic Shorts use frequent within-sentence changes. Vary curiosity, determination, surprise and enthusiasm where appropriate; use `[thoughtful]` or `[serious]` for human consequences. Avoid random cues or added vocal sounds simply to inflate the count. Keep pauses short unless a reveal earns a longer hold.
4. Use the same voice across scene files. The [Google Vids help page](https://support.google.com/docs/answer/15070345?hl=en) documents the `[` menu and a **2,500-character maximum per script**. Split longer narration into ordered scene files below that limit. Their concatenation must reproduce the tagged master apart from scene-boundary whitespace.
5. Generate and listen to the actual audio. Confirm intelligibility, tag behavior, emotional fit, scene joins and measured duration. Record the accepted voice/audio and derive word timestamps only from that audio. A text draft or menu observation alone does not approve a voice.

This stage controls the external narration track. It does not authorize dialogue, music or readable text in generated H3 video clips.

## Validation and handoff record

Run `scripts/validate-google-vids-script.py --clean CLEAN.md --tagged TAGGED.md`
with `--scenes-dir` when split inputs exist and `--report` pointing at an unused
validation revision. The validator reads the registered table above, rejects
unknown/malformed tags and whisper, compares every spoken word and punctuation,
and checks input length and scene reconstruction. Passing is a text check only.

Record provider, `used`/`skipped` selection, tagged/notes/report paths, hashes
and review status under the episode manifest's `voice_direction`. In semantic
Short state v2 it is a substage of `voice`, so the existing 15-stage order remains
compatible; accepted voice is still missing while only tagged text exists.
Long-form retains its explicit `02a` stage. A changed tagged script needs a new
audition; timing is always extracted from actual accepted audio, never tag count
or a reading-speed estimate.
