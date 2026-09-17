---
colors:
  primary: "#171717"
  surface: "#FAFAFA"
  text: "#171717"
typography:
  family: "Arial, Helvetica, sans-serif"
  scale: [12, 14, 16, 20, 24, 32, 48, 64]
spacing:
  scale: [4, 8, 12, 16, 24, 32, 48, 64]
radii:
  scale: [0, 4, 8]
---

## Overview

Video design system, revision 3. On September 18, 2026, Asher accepted light/dark monochrome without the blue accent. Use either mode consistently within an edit. Typography and motion details can continue to evolve through examples. This file is the visual reference for the video work, not a global redesign of this authoring repo.

## Visual Theme & Atmosphere

Monochrome editorial graphics: clear labels, open space, thin borders, and one focal element per beat. Use the diagram-design skill's neutral palette and semantic roles. Default to monochrome light for the reference page; choose light or dark for a video's graphic scenes and retain that choice across the edit.

## Colors

| Diagram role | Light | Dark | Use |
| --- | --- | --- | --- |
| paper | `#FAFAFA` | `#0A0A0A` | Graphic canvas. |
| paper-2 | `#FFFFFF` | `#1A1A1A` | Quiet secondary surface. |
| ink | `#171717` | `#EDEDED` | Primary labels and selected-element outlines. |
| muted | `#666666` | `#A1A1A1` | Secondary labels and connectors. |
| soft | `#666666` | `#A1A1A1` | Small labels use the readable secondary value. |
| rule | `#D4D4D4` | `#333333` | Decorative dividers. |
| rule-solid | `#737373` | `#878787` | Boundaries that carry meaning. |
| accent | `#171717` | `#EDEDED` | Default monochrome focus. |
| accent-tint | `#E8E8E8` | `#262626` | Subtle focal fill. |
| link | `#171717` | `#EDEDED` | Underlined links; distinguish external connectors with labels. |
| on-accent | `#FAFAFA` | `#171717` | Text on an inverted focal node. |

Inversion is the strongest emphasis: ink fill with on-accent text. Limit it to one focal node per scene. Use thicker outlines, labels, and spatial grouping for other distinctions. Meaning never depends on hue alone.

Use the monochrome role values above. The blue comparison in the historical HTML was rejected; blue, green, and teal are outside the accepted palette.

## Typography

Use Arial/Helvetica for diagrams, captions, and body text; SFMono-Regular/Consolas/monospace for timestamps and technical metadata. The HTML reference uses Georgia for its editorial page heading. Video titles remain sans-serif so the specimen does not silently introduce the diagram skill's default serif titles into every shot.

At a 1080-pixel-wide video output, start with 64 px titles, 44 px node names, 32 px secondary labels, and 48 px captions. Use regular body weight and 600–700 weight for hierarchy. Reflow or split a scene before shrinking labels. The web reference uses the smaller frontmatter scale; its diagrams scale proportionally with their viewBox.

## Layout

Landscape: 1920 × 1080, 64 px outer margin, screen or graphic dominant, camera beside it or in an inset. Portrait: 1080 × 1920, 56 px horizontal margin, camera and graphic stacked. Reserve caption and platform-overlay areas per delivery format; verify the actual destination layout rather than treating one safe-area measurement as universal.

Keep a graph's entities recognizable between shots. Prefer three to five visible concepts per beat. A dense landscape scene becomes several portrait beats. Captured screens and camera footage retain their source colours; monochrome applies to authored graphic elements.

## Elevation & Depth

Use surface tone, outline weight, and containment. Keep surfaces flat, without shadows, gradients, glow, or decorative textures.

## Shapes

Use 8 px radii for containers and 4 px for nodes at the reference diagram scale. Use circles only for entities whose meaning calls for them. Use 1–2 px boundaries and 3 px focal strokes in a 600-pixel-wide reference; scale proportionally in the render.

## Components

- Entity: name plus an optional short explanation. Focal entities invert fill or gain a stronger outline.
- Group: named boundary containing only its members. A Harness contains the Model and its tool interface.
- Relationship: labeled, orthogonal connector when containment or adjacency cannot carry the meaning.
- Captions: short phrases in the primary sans family. Use a contrasting plate over variable footage; preserve words from the actual speech.
- Motion: reveal entities, establish the group or connection, then hold the complete result. Start with 480 ms transitions and 900 ms between beats. Align actual scene cues to speech; these timing values are specimen defaults.

The reference uses diagram-design's canonical controls and complete static fallback. Rendered video uses the same visual rules on the edit timeline; browser controls are not part of the export.

## Do's and Don'ts

- Use whitespace and type hierarchy before adding decoration.
- Keep primary and secondary text contrast at least 4.5:1 against its actual surface.
- Keep camera, diagram, and caption regions readable at normal playback size.
- Preserve a complete, understandable static diagram and a stable final animation frame.
- Avoid continuous background motion, abrupt theme switching, and colour-only distinctions.

## Agent Prompt Guide

Read this file before creating a video specimen. Apply its explicit roles through diagram-design's project-design mapping. The historical HTML records the alternatives that were reviewed. Light and dark monochrome are accepted; its blue toggle is not part of the chosen system. Keep one mode stable within a sequence.
