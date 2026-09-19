# Rendering motion scenes

Choose the lightest renderer that expresses the required transformation. Preserve the project's working stack where it already works. Record exact renderer versions, fonts, asset paths, canvas, fps, and frame count with the scene. Keep output times distinct from narration source times.

## HTML/SVG

Use SVG for crisp diagrams and text. A JS timeline such as GSAP can manage coordinated transformations; use a project-installed, pinned version. Hyperframes is another possible wrapper when the project already has it. Neither is required for a scene that can compute state directly from time.

Make the scene seekable: expose `window.renderFrame(seconds)` which sets **all** visible state for that time. Reset state deterministically on every call; seeking backward must work. Await fonts and image decoding before the first capture. Avoid relying on wall-clock animations, timers, user clicks, or network completion during capture.

The supplied `scripts/render-html.mjs` captures a local HTML scene with that API into a silent H.264 clip. Install Playwright in the project with bun and provide its browser installation (or set `CHROME_PATH` to a compatible Chrome executable). The script resolves Playwright from the working project, not from another skill's package.

```text
node /path/to/this-skill/scripts/render-html.mjs scene.html clip.mp4 WIDTH HEIGHT FPS SECONDS
```

The helper captures ceil(SECONDS × FPS) frames at times n/FPS. Put the settled final state before the last frame, or add a hold. It captures the exact viewport and checks document overflow. Make the scene canvas fill that viewport; omit editorial wrappers and browser controls. The helper supports opaque scenes; alpha delivery needs another codec/pipeline.

## Manim

Use a project-local Python environment. Pin the Manim version and inspect its current CLI before running. Select scene dimensions and frame rate explicitly; install LaTeX only when the scene needs TeX typesetting. Use project fonts and colours rather than renderer defaults.

Keep related objects persistent through transformations, use explicit narration cue durations, and render each required clip with predictable start/end states. Save the scene class, inputs, and render command. A geometry animation should preserve the mathematical claim throughout the transformation, not merely resemble the endpoints.

## Assembly contract

Supply a manifest listing each clip's filename, dimensions, fps, duration/frame count, background or alpha mode, and narration/output cue. Keep clip-local time starting at zero. Inspect a full decode and actual rendered frames, including the final hold. Play with narration when available; record unverified pacing rather than inferring it from screenshots.
