# Export to PNG / SVG

Export a generated diagram to `.svg` and/or `.png` when the user requests it, including `/diagram-design:export-diagram <html-file>`. Write requested formats next to the source using its basename, or to the user’s explicit output path. Keep the source HTML unchanged.

## Scope

Export the diagram’s `<svg>` element. A request for the header, cards, or whole page uses a page screenshot or print workflow. For a gallery or multiple candidate diagrams, establish which figure the user means before exporting.

Preserve the diagram’s complete meaning, typography, and accessibility. Export the complete static frame unless the user requests a named step; follow [animation.md](animation.md) for motion state.

## SVG

Produce valid standalone SVG from the selected figure, using an available DOM/XML tool:

- Preserve the `viewBox`, SVG namespace, required styles and definitions, `role="img"`, and `aria-labelledby` references to the original prefixed `<title>` and `<desc>` IDs. Keep `<title>` first.
- Carry the source typography into the SVG; escape XML characters correctly, including ampersands in font URLs. Merge needed font/style definitions with existing ones.
- Include the complete semantic diagram while omitting HTML controls and scripts.
- Verify that the saved file parses as XML and renders as intended.

Remote fonts may be substituted by offline viewers or importers that cannot load them. Explain that portability limit when applicable; PNG preserves the captured typography.

## PNG

Use an available browser capture capability to render the original HTML and capture only the selected SVG’s bounding box, with a transparent background.

1. Load the source at the intended export layout. For motion, use the static override and confirm `data-frame="static"` before capture.
2. Wait for fonts to load and verify the expected faces are actually rendered. Resolve font failures before claiming faithful export.
3. Measure the SVG’s rendered bounds and capture its complete frame at the chosen scale.
4. Inspect the saved image for clipping, missing labels, font substitution, and motion remnants. Verify its actual pixel dimensions against the requested dimensions.

Choose among installed browser tools; Python Playwright is one option. When capture capability is unavailable, report the missing capability and the applicable setup instructions. A help command or package import alone does not establish capture readiness.

## Sizing the export

The `viewBox` sets the diagram’s coordinate system; PNG dimensions depend on the **rendered SVG bounds × capture scale**. Responsive page CSS may make those bounds differ from the `viewBox`. Use [output-spec.md](output-spec.md) for the layout preset and measure the export layout before choosing scale.

Default to scale 2; scale 1 suits compact assets and scale 3 suits print. For an exact target, divide its width by the measured SVG width and verify that the height yields the same scale. Fractional scales are valid: a rendered 960px-wide figure at scale 1.25 produces 1200px.

Keep scale between 1 and 4. If the target needs a scale outside that range or a different aspect ratio, use a matching layout preset before export. Preserve the complete frame and safe margins rather than cropping or padding to force a fit. Any source-layout revision is separate from this export operation.

## Completion

Deliver the requested files with their paths, actual dimensions for PNG, and any font-portability limitation for SVG. The files open correctly, show the selected complete frame, retain SVG accessibility, and leave the source unchanged. If the source lacks an SVG or `viewBox`, report that prerequisite instead of guessing a frame.
