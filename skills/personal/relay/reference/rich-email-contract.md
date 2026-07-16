# Rendering contract

The portable default is a compact, unbranded React Email template derived from the proven project-section
layout: short summary, restrained dividers, small status/visibility labels, and title/detail items. It ships
authored light and dark palettes and renders HTML and plain text from the same schema-version-2 bag.

Setup copies the version-pinned renderer into the consumer instance only when missing and validates Node 20+
and npm 10+ before declaring the instance ready. The approval manifest records the local template identity,
version, and file hashes. The consumer owns brand name, mark, accent, typography, footer, wording, and
extensions; setup preserves edits and emits upgrade candidates instead of overwriting.

Run `npm run render -- --bag <bag.json> --out <run-dir>`. A successful render creates:

- `rendered-email.html` — delivery HTML with declared light/dark color-scheme support;
- `rendered-email.txt` — semantically equivalent plain text;
- `rendered-email-light.html` and `rendered-email-dark.html` — authored forced-theme previews.

Keep structure table-safe and readable without images, custom fonts, classes, or client dark-mode behavior.
The default contains no Dunn Harland name, asset, path, or studio-specific copy. The configurable provenance
footer is visible and included in both HTML and text.

Rendering is complete only when all four files exist, HTML/text carry the same headings and item content, both
forced previews are readable, and the run manifest records the selected local renderer/template identity.
