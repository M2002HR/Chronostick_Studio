---
name: chronostick-longform-youtube
description: Prepare a historically accurate 16:9 thumbnail, Spanish metadata, chapters, captions and end-screen plan for a reviewed ChronoStick long-form distribution master. Use at delivery; uploading or publishing requires explicit authorization.
---

# ChronoStick long-form YouTube package

Read the final approved Spanish narration, claim citations, chapter timing and distribution-master review. The title and thumbnail must promise something the first section and final payoff genuinely deliver. Build an original landscape 16:9 thumbnail brief/prompt that preserves ChronoStick identities and historical meaning; do not stretch a Shorts 9:16 design. Generated thumbnail media receives `-rNNN` and visual/typography review before it can be selected.

Prepare `delivery/youtube/metadata.json` and a readable `.md`: title variants, concise accurate description, source links for important claims, spelling variants of names, chapters starting at 00:00 with meaningful labels, caption language, end-screen target and operator-only settings. Cross-check chapter markers against the actual distribution duration. Avoid unsupported certainty, sensational imagery that contradicts the film, and title/thumbnail bait the opening does not repay. Verify the final file truly includes accepted voice and captions before calling it upload-ready.

Check current YouTube platform requirements when the actual delivery happens. Record thumbnail path/hash/review, distribution master path/hash, metadata revision and pending operator decisions. Do not upload, change visibility, schedule, or publish without explicit user authorization.

## Upper-headline safe inset

When the selected design places headline text at the top, leave at least **12% of the full image height** between the top edge and the topmost visible headline pixel; aim for about 13% to leave review tolerance. Measure the complete text block, including accents, punctuation, stroke/outline, bevel/extrusion and shadow, not just the font baseline or main letter body. At 1920×1080 the minimum is 130 px; at 3840×2160 it is 260 px. This is a ChronoStick layout rule, not a claim about fixed YouTube UI overlays.

Record `headline_position` and the requested top-inset ratio/pixel target in the saved prompt before generation. After generation, inspect the actual lettering bounds and record the observed top coordinate, image height and inset ratio in the review/provenance. Check full resolution, a phone-size preview and a preview with the upper 12% hidden; the complete headline must remain visible and must not collide with the character, face or story-critical props. A prompt instruction alone is not a passed crop check. If the margin fails, make a focused image edit and save a new immutable revision; do not repair with a later text overlay.

For a headline intentionally placed in the middle, keep that approved placement and its normal legibility/object-separation checks. Do not move middle-position text or impose a new upper blank band on that composition.

## Delivery copy and comments

From Episode 003 onward, keep title variants free of hashtags, appended tags, and keyword lists. The roughly 30-character title target applies only to Shorts; long-form titles keep the length needed for a clear truthful hook. Do not retrofit existing episode packages unless requested.

Write descriptions and comments in natural, informal release-language speech. Weave relevant topic/search phrases into the opening sentences without keyword stuffing. Claim a term is currently trending only with dated, locale-specific evidence recorded in the package; otherwise mark it internally as an SEO candidate. Preserve source links and historical qualifications.

Provide a focused hashtag pool in three groups: episode topic, history/animation niche, and broad format/discovery appropriate to long-form. Do not label a landscape long video `#Shorts` or `#ViralShorts`. Put a smaller exact subset of the main pool at the end of the description, usually 3–5 covering all three groups. Save the flat `hashtags` pool, `hashtag_groups`, and `description_hashtags` in JSON and mirror them in Markdown.

Include exactly three pinned-comment candidates and 3–5 suggested viewer-comment examples (default five). Keep them short, casual, varied, and grounded in actual video beats. Store them as `comments.pinned_candidates` and `comments.viewer_examples`, mirror them in Markdown, and label viewer comments as examples rather than existing audience reactions. Preparing comments does not authorize posting them.

Include the proposed final upload filename in `media.expected_upload_filename` and the readable handoff. Use lowercase ASCII, hyphens, clear topic keywords, language/episode identity, immutable `-rNNN`, and the real container extension. Preserve existing media; filename keywords are an organizational choice, not a guaranteed ranking benefit.

## Studio tags

Prepare about 15 useful, unique YouTube Studio tags per episode (default 15; normally 12–18). Prioritize the main topic, people/place names, useful spelling or accent variants, closely related search phrases, history/animation niche and channel identity. Do not add unrelated or generic filler just to reach the count. Keep Studio tag lists separate from hashtags; do not append those lists to titles or the public description. Relevant keyword phrases may appear naturally in the title and description. Store the array as `tags` in metadata JSON and provide one comma-separated paste-ready line in Markdown; record the count and check the current Studio field character limit before upload. This is a channel packaging preference, not a guarantee of discovery; YouTube says tags otherwise play a minimal role.

## Title and opening-description review

Review the primary title and both alternatives against all three criteria: the video subject is explicit without thumbnail context; the wording creates emotion or curiosity through real stakes, surprise, or consequence; and the release-language phrasing is immediately easy to understand. Prefer concrete subjects and events to vague phrases such as “a fatal ending.” Do not meet the short-title target by removing the context needed to identify the topic. Keep hooks truthful and avoid unsupported rankings or sensational claims.

Choose and record one explicit `seo_target_keyword`. Use the user's tool-selected target when supplied; otherwise choose a truthful phrase from the hook title and record it as an editorial choice. Checking only loosely related topic words is insufficient. Keep the exact primary phrase in the title, one of the Studio tags (preferably first), and a natural sentence within the first 200 characters of the actual description. Add a few relevant supporting tag phrases/names within that opening where they fit naturally. Do not insert unrelated keywords or weaken the hook to satisfy an extension score.

Verify the complete primary phrase in all three fields, including its end position before character 201 in `description[:200]`. Count spaces, punctuation and newlines. Normalize Unicode to NFC and casefold for local comparisons; do not silently substitute plurals, synonyms, or accent spellings. Record the excerpt, phrase, start/end positions, title/tag matches and supporting matches in `description_opening_check`. Keep a separate `external_tool_status`: passing local checks does not prove the user's vidIQ upload-form check passed. [vidIQ's official scorecard guidance](https://support.vidiq.com/en/articles/9696241-the-vidiq-scorecard) discusses keywords across title, tags and description; it does not establish the exact implementation of every first-200-character warning.

Save the exact public description alone in `delivery/youtube/description.txt`, alongside identical JSON and Markdown copies. Do not put headings, status notes, character counts, SEO analysis or checklists before the description in that copyable file. Hashtags at the bottom do not satisfy the opening-keyword requirement. When vidIQ still reports missing keywords, compare the actual pasted title, Tags field and first 200 description characters with the saved package and any tool-selected target. Report the external check as pending until observed; do not claim the warning cleared or promise a score from local text checks alone. This is a channel delivery requirement, not a guaranteed YouTube ranking benefit.
