---
name: chronostick-youtube
description: Design and save a topic-specific, high-impact ChronoStick Shorts thumbnail prompt, optionally generate it only when explicitly requested, and prepare upload-ready YouTube metadata. Use at final delivery; do not generate, upload, or publish beyond the user's authorization.
---

# Chronostick Youtube

Use the approved distribution master when available; otherwise clearly label the package provisional. Verify current YouTube limits from official Help before final delivery because platform rules change.

## Thumbnail

Read `assets/branding/youtube-shorts/README.md` before thumbnail work.

### Prompt gate

1. Inspect the approved script, hook, payoff, final video when available, and episode-specific style/character/world references.
2. Develop three genuinely different concepts suited to this episode's subject, mood, emotional tension, and audience promise. Do not force a previous episode's layout, palette, font treatment, or composition.
3. Select the strongest truthful concept for mobile click-through. Never promise an event, person, scale, or reveal absent from the video.
4. Write the exact on-image headline, reference roles, full image-generation prompt, negative constraints, composition logic, and acceptance checklist.
5. Save that work first as the next immutable `delivery/youtube/thumbnail-prompt-rNNN.md`. Do not generate an image before this file exists.

Stop after the saved prompt unless the user explicitly asked to generate the thumbnail in the same request or gives a later generation instruction. A request to prepare metadata or a thumbnail prompt does not authorize image generation.

### Reference policy

- Approved episode references control ChronoStick world style, recurring identity, period details, vehicles, props, and locations.
- External thumbnails from other channels are inspiration only. Extract abstract lessons such as hierarchy, contrast, curiosity, or visual economy; never copy their characters, objects, wording, brand style, palette, layout, or font treatment.
- Do not pass external inspiration images to the image generator by default. Use them as generation inputs only when the user explicitly requests that role.
- Do not turn one successful ChronoStick thumbnail into a mandatory composition template. Reuse it only as a quality benchmark when relevant.

### Optional generation gate

When generation is explicitly authorized, use the saved prompt and approved episode references. If the prompt changes materially, save a new prompt revision before generation. Generate the complete 9:16 artwork—including its exact short headline—inside one image; do not add or repair text with a later overlay. Archive the generated source, a 2160×3840 delivery master, provenance, and an immutable review status. Reject misspelling, extra text, weak hierarchy, wrong identity, non-stick-world content, misleading imagery, or unsafe crops.

## Metadata

Create `delivery/youtube/metadata.json` and a readable Markdown copy containing:

- primary title plus two truthful alternatives; hard limit 100 characters
- unique description with the main topic in the first lines; hard limit 5,000 characters
- focused tags mainly for names, variants, and likely misspellings; YouTube says tags otherwise play a minimal discovery role
- 3–5 relevant hashtags, category, language, recording/location fields when applicable
- audience/made-for-kids and age-restriction fields as explicit operator decisions, never guesses
- related-video suggestion, credits/sources, filename, thumbnail path, distribution-master path, and upload checklist

Avoid keyword stuffing, fake urgency, unverified claims, graphic sensationalism, or metadata that promises footage not present.

## Closeout

Record prompt revision, generation authorization/status, final hashes/revisions when generated, external Google Vids finishing status, thumbnail review, metadata review, and publication status in the episode manifest. Preparation does not authorize image generation, upload, visibility changes, or publication.
