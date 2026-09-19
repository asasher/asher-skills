---
name: motion-graphics
description: Create educational motion graphics from an idea, script, or narration. Build explanatory animated scenes with persistent objects, timed transformations, and editable sources for standalone clips or video assembly.
metadata:
  optional: [diagram-design, writing-for-humans]
---

# Motion graphics

Make the viewer understand a change. Begin with the concept and what the viewer should be able to explain afterward. Read the project's `DESIGN.md` and use its visual choices.

## Plan the explanation

Resolve canvas, duration or narration cues, output frame rate, and any reserved regions such as captions or platform controls. If these are supplied, treat them as layout inputs. When graphics share the frame with footage, compose inside the assigned graphic panel and preserve the project’s camera/graphic arrangement. A concept-only request can start with a scene plan; a request for a clip ends with a rendered clip.

Write a short sequence of beats: establish the objects, show the relationship or transformation, expose its consequence, and hold the result. Use this when it fits the idea rather than imposing four beats on every scene. Keep object identity and spatial continuity across changes. Animate the operation itself instead of replacing it with a sequence of unrelated labels.

Record each scene's narration cue, duration, persistent objects, change, and final state. Align to actual narration when supplied. Leave enough time to read the result; animation tempo follows meaning rather than a fixed beat interval.

## Choose a renderer

Read [rendering](references/rendering.md) for implementation and export. Use Manim for geometry, equations, algorithms, and continuous transformations. Use HTML/SVG with a deterministic timeline for diagrams, UI, text, and screen explanations. An installed project renderer can replace either when it preserves editable sources and precise timing.

For applicable diagram semantics and static assets, use `diagram-design` with the project's visual system. Its static-first and interactive-page defaults do not define the video timeline. If unavailable, build simple SVG geometry directly and keep the requested design. Rendered video controls belong to the review page, not the frames.

## Build and inspect

Use typography, grouping, and contrast before decoration. Keep critical objects and their full motion paths inside the supplied usable regions and clear of caption lanes. Reflow the scene for portrait; do not center-crop a finished landscape diagram. Choose one focal event at a time unless simultaneous change is the lesson.

Render a low-cost preview first. Inspect initial, intermediate, and final states at delivery size, then play the sequence with its narration. Static frames cannot establish pacing. Look for jumpy object identity, unreadable labels, path collisions, unintentional blanks, and a final state that disappears before it is understood.

Deliver editable scene sources, required assets/fonts, reproducible render command and renderer versions, scene cue timing, and rendered clips with exact dimensions, frame rate, and duration. Include alpha only when the chosen codec supports it; otherwise supply the intended background or a separate mask. State any playback or narration checks that remain unverified. Use `writing-for-humans` when available for the handoff.
