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
2. Develop three genuinely different concepts suited to this episode's subject, mood, emotional tension, and audience promise. Do not force a previous episode's layout, palette, or composition.
3. Select the strongest truthful concept for mobile click-through. The complete thumbnail hook must communicate, within roughly one second at phone size, the subject or stakes plus a clear unanswered question, contradiction, countdown, consequence, or emotional tension. Reject generic labels that only name the topic. Never promise an event, person, scale, or reveal absent from the video, and never claim that click-through is guaranteed.
4. Write the exact on-image headline, reference roles, full image-generation prompt, negative constraints, composition logic, and acceptance checklist.
5. Save that work first as the next immutable `delivery/youtube/thumbnail-prompt-rNNN.md`. Do not generate an image before this file exists.

Stop after the saved prompt unless the user explicitly asked to generate the thumbnail in the same request or gives a later generation instruction. A request to prepare metadata or a thumbnail prompt does not authorize image generation.

### Channel typography lock

All ChronoStick thumbnails use one consistent generated display-lettering system derived from the accepted Episode 002 thumbnail:

- uppercase, very heavy rounded display letters with broad counters and compact spacing
- thick near-black outline, shallow dimensional extrusion or bevel, and a soft drop shadow
- warm white for the setup line and signal yellow-to-gold for the key word or payoff line when two levels of emphasis are useful
- large, uncluttered, mobile-readable letterforms with safe margins

Treat this as a visual font specification, not a separately installed typeface or post-production text layer. Generate the exact headline inside the complete artwork in the same image-generation pass. The Episode 002 thumbnail may be supplied only as a typography benchmark; do not copy its composition, subjects, palette distribution, or wording into another episode.

Keep the type system consistent while adapting line breaks, scale, placement, and emphasis color to the episode. Reject thin, condensed, serif, handwritten, distressed, horror, ornamental, or mismatched lettering, even when the words are spelled correctly.

### Upper-headline safe inset

When the selected design places headline text at the top, leave at least **12% of the full image height** between the top edge and the topmost visible headline pixel; aim for about 13% to leave review tolerance. Measure the complete text block, including accents, punctuation, stroke/outline, bevel/extrusion and shadow, not just the font baseline or main letter body. At 2160×3840 the minimum is 461 px; at 1080×1920 it is 231 px. This is a ChronoStick layout rule, not a claim about fixed YouTube UI overlays.

Record `headline_position` and the requested top-inset ratio/pixel target in the saved prompt before generation. After generation, inspect the actual lettering bounds and record the observed top coordinate, image height and inset ratio in the review/provenance. Check full resolution, a phone-size preview and a preview with the upper 12% hidden; the complete headline must remain visible and must not collide with the character, face or story-critical props. A prompt instruction alone is not a passed crop check. If the margin fails, make a focused image edit and save a new immutable revision; do not repair with a later text overlay.

For a headline intentionally placed in the middle, keep that approved placement and its normal legibility/object-separation checks. Do not move middle-position text or impose a new upper blank band on that composition.

### Reference policy

- Approved episode references control ChronoStick world style, recurring identity, period details, vehicles, props, and locations.
- External thumbnails from other channels are inspiration only. Extract abstract lessons such as hierarchy, contrast, curiosity, or visual economy; never copy their characters, objects, wording, brand style, palette, layout, or font treatment.
- Do not pass external inspiration images to the image generator by default. Use them as generation inputs only when the user explicitly requests that role.
- Do not turn one successful ChronoStick thumbnail into a mandatory composition template. Reuse it only as a quality benchmark when relevant.

### Optional generation gate

When generation is explicitly authorized, use the saved prompt and approved episode references. If the prompt changes materially, save a new prompt revision before generation. Generate the complete 9:16 artwork—including its exact short headline—inside one image; do not add or repair text with a later overlay. Archive the generated source, a 2160×3840 delivery master, provenance, and an immutable review status. Reject misspelling, extra text, weak hierarchy, wrong identity, non-stick-world content, misleading imagery, or unsafe crops.

Review the hook separately from rendering quality. A polished image still fails if the headline and visual do not create an immediate truthful reason to click. Record the hook mechanism and why the image leaves a specific question unresolved. Treat CTR as an empirical publishing metric, not something the prompt can guarantee.

## Metadata

Create `delivery/youtube/metadata.json` and a readable Markdown copy containing:

- primary title plus two truthful alternatives: for Shorts from Episode 003 onward, aim for about 30 characters (normally 25–35, including spaces and punctuation), a few words, and an immediate truthful hook; report each character count; platform hard limit 100 characters; no hashtags, appended tags, or keyword lists in any title
- unique description with the main topic in the first lines; hard limit 5,000 characters
- about 15 relevant Studio tags; follow the tag selection guidance below
- a focused main hashtag pool grouped as episode topic, history/animation niche, and broad format/discovery; use relevant broad terms such as `#Shorts`, `#YouTubeShorts`, and `#ViralShorts` for Shorts without promising virality; put a smaller exact subset of that pool at the end of the description (usually 3–5), covering all three groups
- category, language, recording/location fields when applicable
- exactly three pinned-comment candidates and 3–5 suggested viewer-comment examples (default five), in the release language: short, casual, conversational, varied, and tied to actual episode beats; label viewer comments as examples, never as existing audience reactions; preparation does not authorize posting
- a proposed final upload filename in `media.expected_upload_filename` and in the Markdown handoff: lowercase ASCII, hyphens, clear topic keywords, language/episode identity, immutable `-rNNN`, and the real container extension; keep the existing media untouched and do not imply filename keywords guarantee search ranking
- audience/made-for-kids and age-restriction fields as explicit operator decisions, never guesses
- related-video suggestion, credits/sources, filename, thumbnail path, distribution-master path, and upload checklist

Write the public description and comments in natural, informal release-language speech. Put the topic and hook in the first lines and weave relevant search phrases into real sentences, rather than a keyword list. Use current trend terms only when they fit the video; verify any claim that a term is currently trending with dated, locale-specific evidence and record the source. If that evidence is unavailable, label terms internally as relevant SEO candidates, not verified trends. Preserve citations and factual qualifications.

Store `hashtag_groups`, `description_hashtags`, `comments.pinned_candidates`, and `comments.viewer_examples` in JSON and mirror them in Markdown; keep the existing flat `hashtags` pool for compatibility. Titles contain no hashtags; Studio tags remain in their separate field.

Apply these defaults prospectively from Episode 003; update older or already prepared packages only when requested. Avoid keyword stuffing, fake urgency, unverified claims, graphic sensationalism, or metadata that promises footage not present.

## Studio tags

Prepare about 15 useful, unique YouTube Studio tags per episode (default 15; normally 12–18). Prioritize the main topic, people/place names, useful spelling or accent variants, closely related search phrases, history/animation niche and channel identity. Do not add unrelated or generic filler just to reach the count. Keep Studio tag lists separate from hashtags; do not append those lists to titles or the public description. Relevant keyword phrases may appear naturally in the title and description. Store the array as `tags` in metadata JSON and provide one comma-separated paste-ready line in Markdown; record the count and check the current Studio field character limit before upload. This is a channel packaging preference, not a guarantee of discovery; YouTube says tags otherwise play a minimal role.

## Title and opening-description review

Review the primary title and both alternatives against all three criteria: the video subject is explicit without thumbnail context; the wording creates emotion or curiosity through real stakes, surprise, or consequence; and the release-language phrasing is immediately easy to understand. Prefer concrete subjects and events to vague phrases such as “a fatal ending.” Do not meet the short-title target by removing the context needed to identify the topic. Keep hooks truthful and avoid unsupported rankings or sensational claims.

Choose and record one explicit `seo_target_keyword`. Use the user's tool-selected target when supplied; otherwise choose a truthful phrase from the hook title and record it as an editorial choice. Checking only loosely related topic words is insufficient. Keep the exact primary phrase in the title, one of the Studio tags (preferably first), and a natural sentence within the first 200 characters of the actual description. Add a few relevant supporting tag phrases/names within that opening where they fit naturally. Do not insert unrelated keywords or weaken the hook to satisfy an extension score.

Verify the complete primary phrase in all three fields, including its end position before character 201 in `description[:200]`. Count spaces, punctuation and newlines. Normalize Unicode to NFC and casefold for local comparisons; do not silently substitute plurals, synonyms, or accent spellings. Record the excerpt, phrase, start/end positions, title/tag matches and supporting matches in `description_opening_check`. Keep a separate `external_tool_status`: passing local checks does not prove the user's vidIQ upload-form check passed. [vidIQ's official scorecard guidance](https://support.vidiq.com/en/articles/9696241-the-vidiq-scorecard) discusses keywords across title, tags and description; it does not establish the exact implementation of every first-200-character warning.

Save the exact public description alone in `delivery/youtube/description.txt`, alongside identical JSON and Markdown copies. Do not put headings, status notes, character counts, SEO analysis or checklists before the description in that copyable file. Hashtags at the bottom do not satisfy the opening-keyword requirement. When vidIQ still reports missing keywords, compare the actual pasted title, Tags field and first 200 description characters with the saved package and any tool-selected target. Report the external check as pending until observed; do not claim the warning cleared or promise a score from local text checks alone. This is a channel delivery requirement, not a guaranteed YouTube ranking benefit.

## Closeout

Record prompt revision, generation authorization/status, final hashes/revisions when generated, external Google Vids finishing status, thumbnail review, metadata review, and publication status in the episode manifest. Preparation does not authorize image generation, upload, visibility changes, or publication.
