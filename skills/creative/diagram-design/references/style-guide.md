# Style Guide

This file defines the diagram's semantic roles and their shipped values. Every type reference uses these role names instead of its own color or typography values.

The shipped skin is dark: true-black paper, near-white ink, a neutral gray scale, and one blue accent. Chrome is carried by hairline borders and type, not by fills or glow. It supplies the complete visual system when the project has no `DESIGN.md` and fills roles that a project visual system leaves unspecified. A light variant is defined alongside it for pages that cannot host a dark figure.

---

## Tokens

### Semantic roles

Every token is referred to by **semantic role**, not by its hex value. Type references (`type-*.md`) and SKILL.md say `accent`, not `#0070f3`.

| Role | Purpose | Dark (default) | Light |
| --- | --- | --- | --- |
| `paper` | Page background, default node fill | `#000000` | `#fafafa` |
| `paper-2` | Raised surface: container bg, card and backend-node fill | `#0a0a0a` | `#ffffff` |
| `ink` | Primary text, primary stroke | `#ededed` | `#171717` |
| `muted` | Secondary text, default arrow stroke | `#a1a1a1` | `#666666` |
| `soft` | Sublabels, boundary labels | `#878787` | `#7d7d7d` |
| `rule` | Hairline borders | `rgba(237,237,237,0.14)` | `rgba(23,23,23,0.08)` |
| `rule-solid` | Stronger borders, baselines | `#454545` | `#c9c9c9` |
| `accent` | Focal / 1–2 max per diagram | `#0070f3` | `#0070f3` |
| `accent-tint` | Fill for accent-bordered boxes | `rgba(0,112,243,0.14)` | `rgba(0,112,243,0.08)` |
| `link` | HTTP/API calls, external arrows | `#8ab4f8` | `#2e5aa8` |

> **Palette source:** a monochrome gray scale plus one blue. `ink`, `muted`, `soft`, and `rule-solid` are steps on the same neutral ramp; `rule` is ink at opacity; `accent` is the one saturated hue; `link` is the accent's hue at low saturation so HTTP arrows read as a family member of the accent without competing with the focal node. On black, `accent` measures 4.6:1 and `muted` 8.1:1; on light paper they measure 4.4:1 and 5.5:1.

> **Note:** The pre-baked example HTML files in `assets/` were built under an earlier light skin (`example-<type>.html`) and its dark twin (`example-<type>-dark.html`). Use them for layout and rhythm, not for color. New diagrams the skill produces use the tokens above.

### Inversion rule (dark → light)

Any `rgba(237,237,237, X)` in the default skin becomes `rgba(23,23,23, X)` in light. Same opacities, RGB flipped. Tints on black need more alpha than tints on white: where a table lists both columns, the dark column carries the higher alpha. The accent keeps one hex in both modes.

### Series palette (multi-series chart types only)

A small set of desaturated, editorial-tone colors for chart types that genuinely need to distinguish multiple overlapping entities (currently: **radar**). The "1-focal" rule still holds — `accent` is reserved for the focal series; the palette below covers the rest.

| Token      | Dark (default)         | Light     | Notes            |
| ---------- | ---------------------- | --------- | ---------------- |
| `series-1` | `#9caf8f` (sage)       | `#7c8f6f` | Non-focal series |
| `series-2` | `#82a0c0` (dusty-blue) | `#5e7a9b` | Non-focal series |
| `series-3` | `#d3ad7a` (mustard)    | `#b8915a` | Non-focal series |
| `series-4` | `#b88670` (rust-brown) | `#9c6b50` | Non-focal series |
| `series-5` | `#8d8298` (slate)      | `#6e6479` | Non-focal series |

Fills sit at `0.22` opacity on dark paper, `0.18` on light; strokes use the full color. **Don't backfill these tokens to non-chart types** — architecture, swimlane, etc. continue to use muted-ink variants. The series palette is opt-in for diagrams where overlapping shapes demand distinguishable color, not a license to add color elsewhere.

### Terminal skin (opt-in alternate)

A self-contained palette for the terminal-window primitive (see [primitive-terminal.md](primitive-terminal.md)) — a CLI-chrome register for dev-tool posts and technical social cards. It is a second, fixed skin selected per diagram.

| Token | Hex | Purpose |
| --- | --- | --- |
| `terminal-page` | `#0a0a0a` | Page background behind the window |
| `terminal-paper` | `#141414` | Window body, node fill |
| `terminal-bar` | `#1b1b1b` | Titlebar strip |
| `terminal-border` | `#2b2b2b` | Window border, hairlines |
| `terminal-ink` | `#f5f5f5` | Primary text, primary stroke |
| `terminal-muted` | `#9a9a9a` | Secondary text, sublabels, ring stroke |
| `terminal-soft` | `#5c5c5c` | Tertiary — inactive dots, spokes |
| `terminal-accent` | `#ff5a36` | The one accent — focal station, prompt sign, active dot |
| `terminal-accent-tint` | `rgba(255,90,54,0.12)` | Fill for accent-bordered boxes |

**1-accent rule still holds.** Everything that isn't `terminal-ink` or `terminal-muted`/`terminal-soft` should be `terminal-accent` — never introduce a second hue.

---

## Typography

| Role | Family | Size | Weight | Usage |
| --- | --- | --- | --- | --- |
| `title` | Instrument Serif | 1.75rem | 400 | Page H1 |
| `node-name` | Geist (sans) | 12px | 600 | Human-readable labels |
| `sublabel` | Geist Mono | 9px | 400 | Port, protocol, URL, field type |
| `eyebrow` | Geist Mono | 7–8px | 500, tracked 0.18em, uppercase | Type tags, axis labels |
| `arrow-label` | Geist Mono | 8px | 400, tracked 0.06em | Arrow annotations |
| `callout` | Instrument Serif _italic_ | 14px | 400 | Editorial asides only |

### Font stack

```html
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

**Load-bearing rule:** Mono is for _technical_ content (ports, commands, URLs, field types). Names go in Geist sans. Page title is Instrument Serif. Italic Instrument Serif is reserved for annotation callouts (see [primitive-annotation.md](primitive-annotation.md)). **Never JetBrains Mono** as a blanket "dev" font.

---

## Stroke, radius, spacing

| Token | Value | Use |
| --- | --- | --- |
| `stroke-thin` | `0.8` | Tag-box outlines, leaf nodes |
| `stroke-default` | `1` | Most strokes |
| `stroke-strong` | `1.2` | Emphasis strokes |
| `radius-sm` | `4` | Small tags |
| `radius-md` | `6` | Node boxes |
| `radius-lg` | `8` | Containers, rings |
| `grid` | `4` | Every coord, size, and gap is divisible by 4 (hard rule) |

---

## Node type → treatment

Semantic role combinations — reference these by name in type specs.

| Type              | Fill            | Stroke                       |
| ----------------- | --------------- | ---------------------------- |
| `focal` (1–2 max) | `accent-tint`   | `accent`                     |
| `backend`         | `paper-2`       | `ink`                        |
| `store`           | `ink @ 0.05`    | `muted`                      |
| `external`        | `ink @ 0.03`    | `ink @ 0.30`                 |
| `input`           | `muted @ 0.10`  | `soft`                       |
| `optional`        | `ink @ 0.02`    | `ink @ 0.20` dashed `4,3`    |
| `security`        | `accent @ 0.05` | `accent @ 0.50` dashed `4,4` |

---

## Constraints

- **Contrast**: `ink` must hit WCAG AA on `paper`. `muted` must hit AA on `paper` for 11px+ text.
- **One accent**: pick one color for `accent`. Two accents erases the focal signal.
- **No rainbow palette**: if your brand ships 8 colors, pick 3 (paper, ink, accent). The rest become `muted` variants.
- **Serif + sans + mono**: three families, not more. If brand typography is all sans, keep Instrument Serif for `title` and `callout` anyway — the contrast is load-bearing.
- **Paper is true black, and the lift is the border**: `paper-2` sits one step above `paper`, so a raised surface reads through its hairline `rule`, not through a fill contrast. No gradients, no glow, no shadow. In the light variant, paper is off-white and `paper-2` is white.
- **Dot pattern is optional, not default**: the 22×22 dot pattern is an opt-in "dotted paper" variant (good for long-form editorial hero diagrams). The default background is a clean `paper` fill, no pattern. When the pattern is enabled, it should sit at ~10% opacity of `ink` on `paper` — visible but quiet.
- **Container is clean by default**: the diagram sits directly on the page paper, no secondary container background or border. A framed variant (`paper-2` bg + `rule` border + 8px radius + padding) is available as an opt-in for card-heavy layouts, but don't reach for it by default — the extra chrome fights the figure.
