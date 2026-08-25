# Embedded output

Use embedded mode when a diagram belongs inside a larger self-contained HTML artifact.

Return one HTML fragment containing the scoped style and figure. Do not add `<!DOCTYPE>`, `<html>`, `<head>`, or `<body>` elements. Do not create a second published artifact unless the user asks for one.

## Fragment contract

The fragment contains, in this order:

1. One scoped `<style data-diagram-design="<slug>">` block.
2. One `<figure class="diagram-design" data-diagram="<slug>">`.
3. An optional visible `<figcaption>` when the surrounding prose does not already introduce the figure.
4. One inline `<svg>` that follows the accessible SVG contract in `SKILL.md`.

Scope every selector beneath `[data-diagram="<slug>"]`. Define visual tokens as custom properties on that figure. Do not style global elements such as `body`, `h1`, `svg`, or `*`. The containing artifact owns page layout, headings, and font loading.

Prefix every SVG ID with the diagram slug, including markers, masks, clips, filters, gradients, patterns, title, and description. Update every `url(#...)`, `href`, and `aria-labelledby` reference to use the prefixed ID. Two figures must be safe to place in the same document.

Make the SVG responsive with `width: 100%`, `height: auto`, and its intrinsic `viewBox`. Keep the selected size preset as the `viewBox`; embedded mode does not shrink the type ramp.

Keep the fragment self-contained. Use no external images, stylesheets, or fonts. Use the containing artifact's declared fonts with safe system fallbacks. Keep static output script-free. If the user asks for motion, use the canonical controller and scope its root to this figure.

Run `python3 scripts/self_check.py <fragment-file>` on a temporary file containing the fragment. Then run the same check on the completed containing artifact. Embedded output is complete only when both checks pass and the containing artifact renders the figure without horizontal clipping at its intended width.
