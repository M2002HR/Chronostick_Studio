# Banner source r002 review

Decision: **rejected for mobile-safe lockup positioning**. Retained as the
input for the single upward reposition in `banner-prompt-r004.md`.

- Source 1672×941 is essentially 16:9; final-resolution conversion can correct
  the subpixel rounding difference without a meaningful proportion change.
- Full-frame visual direction, five master-style characters, mascot identity,
  exact title and complete slogan: visually passed.
- Actual centered review crop after scaling to 2560×1440:
  `banner-mobile-review-r002.png`.
- Crop failed: slogan is below the safe band and mascot bust is cut at the
  bottom. Never deliver this revision as a safe upload banner.
- Required correction: move only the entire mascot/title/slogan lockup up
  approximately 100 source pixels and integrate the background. Keep the rest
  of the composition intact.

Review crop was made with FFmpeg for inspection only. No delivery master,
typography overlay, user approval, upload or publication was created.
