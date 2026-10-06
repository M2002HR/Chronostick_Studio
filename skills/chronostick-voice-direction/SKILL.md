---
name: chronostick-voice-direction
description: Prepare a paste-ready Google Vids narration copy using registered pace, emotion and style tags while preserving the clean spoken text. Use before Google Vids voice handoff for Shorts, long-form or localization; this does not generate or accept audio.
---

# ChronoStick Voice Direction

Read `docs/google-vids-voice-direction.md` for the user's observed account menu
and voice rules, then the episode's clean narration and performance target.
Prepare the tagged Google Vids copy immediately after every new or revised
clean narration, including a draft; do not defer it until storyboard review or
wait for another request. Deliver clean and tagged versions together. Use many
purposeful emotion/style tags by default for every new voice script, including
Shorts, long-form and localization, unless the user explicitly asks otherwise.
The registered menu is the vocabulary authority; do not invent tags or import
another provider's syntax. Whisper is forbidden by the user's explicit rule.

Keep clean narration authoritative. Create `script/voiceover-google-vids-<lang>.md`
with inline tags only, preserving spoken words, order and punctuation. Keep
headings, notes and review decisions in `script/voice-direction-notes.md`.
For long-form, split ordered `scene-NN.txt` paste inputs within the registered
character limit; their concatenation must reconstruct the tagged master.

For an energetic Short, use a rushed base and frequent purposeful emotion/style
turns by default: curiosity for the hook, determination for action, surprise
for reversals, enthusiasm for payoff. Direct important words within a sentence
where useful. Give names and numbers clear articulation and harm a serious tone.
Return to the fast base after a brief natural-paced consequence. Pauses should
serve the reveal; avoid delay from long pauses or unrequested vocal sounds.
Use fitting emotional cues in every sentence and at meaningful clause turns or
important words, rather than only at the opening. Keep this dense expressive
direction in all formats; adapt emotions and base pace to the content. Do not
pad with random emotions, long pauses or vocal sounds just to increase tag count.

New narration defaults to a tiny closing subscribe CTA from `chronostick-script`
(Spanish `Suscríbete.`). Choose its pace/emotion to fit the ending—brisk and
enthusiastic here, restrained after a solemn story. Preserve the brief spoken
wording; do not add a longer pitch. If it is missing, reconcile the clean script
first, then regenerate its tagged copy and hashes; never append it only to the
tagged version or silently change an already accepted voice.

Run `scripts/validate-google-vids-script.py` against the clean and tagged files;
archive the report and source/tagged hashes. It checks registered tags, forbidden
whisper, unchanged spoken text and scene limits/joins. It cannot certify a voice.
When Google Vids is selected, this is a required immediate post-script stage;
skip it only on an explicit user/provider choice. Use/skipped and
artifact paths belong in the manifest/state. An explicitly requested preparatory
copy can remain a draft before script approval; do not infer other creative
approvals from it.

Give the user the exact paste input. The user returns actual generated audio;
review delivery, intelligibility, pronunciation, words, duration and any audible
tags before accepting it. Then route the accepted voice to `chronostick-transcribe`
for real target-language timing. Changed words or tags require a new audition;
changed accepted audio invalidates downstream timing. External voice tags never
enter H3 prompts or allow generated music, speech, lip sync or on-screen text.
