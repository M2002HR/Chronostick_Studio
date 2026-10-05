# Visual style rules

The permanent ChronoStick language is detailed cinematic stick-figure historical animation.

## Required visual identity

- round off-white heads
- tiny black eyes and minimal facial features
- simplified stick-figure anatomy
- thick, clean, dark outlines
- detailed and period-grounded clothing
- muted historical palette
- controlled soft shading
- readable silhouettes and cinematic composition in the named profile's aspect ratio

This visual language applies to every pixel of every shot, including empty landscapes, sky, sea, animals, hands, props, buildings, smoke, shadows, and tiny background figures. A stick person over a photographic background is a style failure. Keep the same dark drawn contours, simplified forms, and non-photographic shading in wide views and extreme inserts.

## Forbidden drift

Do not drift into photorealism, realistic human anatomy, glossy CGI mascots, anime, painterly or watercolor rendering, whiteboard doodles, or generic modern cartoon style.

Reject a generated clip if even a brief frame contains an unapproved photographic or mixed-style element. Fix an unsupported shot or its reference before relying on stronger negative prompt wording.

## Control hierarchy

1. The approved master style reference controls rendering language.
2. An approved character sheet controls that character's identity.
3. An approved world sheet controls architecture, materials, palette, and recurring props.
4. The episode shot plan controls scene-specific staging.

Character references are identity sources, not permission to copy their reference-sheet layout into a scene. Style Master has priority if a character sheet contains incidental rendering artifacts.

## Complexity fallback

Preserve, in order: character identity, costume, silhouette, main action, primary prop, environment, background extras. Reduce detail from the end of that list first.

The full locked definitions live under `docs/specs/`; approved visual files live under `assets/`.
