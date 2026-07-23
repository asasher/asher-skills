# Site diagram stack — research findings

Four parallel research passes (2026-07-19) into how to implement the site's two required primitives:
a **swim-lane flowchart** (lanes × phases, BPMN-pool style) and a **grouped graph layout**, while
preserving the two things that already work — obstacle-aware edge routing and the hover
neighborhood-dim interaction. Constraints: static framework-free site, no build step, vendorable
single-file libraries, permissive licenses, deterministic output, pan/zoom + click + rich HTML labels.

## The central architectural finding

For a diagram where every node's lane **and** phase are fixed by data, the literature and every
serious product converge on **grid placement + a real orthogonal edge router**, not a general layout
engine:

- The canonical BPMN auto-layout paper (Kitzmann et al. 2009, IEEE CEC) is explicitly grid-based:
  place in a 2D grid, route edges Manhattan-style. <https://etc.leif.me/papers/Kitzmann2009a.pdf>
- bpmn.io's own `bpmn-auto-layout` (MIT, v1.3.0 2026-03) works the same way — and still refuses to
  lay out pools/lanes. <https://github.com/bpmn-io/bpmn-auto-layout>
- draw.io/mxGraph ships a purpose-built `mxSwimlaneLayout` that takes the ordered lane list as
  *input* — a special case, not a general engine coerced into lanes.
- The ELK team, asked for years to "route edges without moving my fixed nodes," integrated the
  **libavoid** router rather than bend ELK Layered: "existing layout algorithms such as ELK Layered
  cannot easily do this." <https://eclipse.dev/elk/blog/posts/2022/22-11-17-libavoid.html>
- Every general engine has a years-old open swimlane issue: D2 discussion #236 (2022–), Graphviz
  #2016, elkjs #92/#245 (maintainer: "neither see anyone from the core team to work on this topic").

Conclusion: the hand-rolled constrained grid was the architecturally respected approach. What failed
was hand-drawing the *edges* and *lane labels* too. The fix is a real router and lane headers that
are part of the lane shape, not floating labels.

## Candidate-by-candidate summary

### ELK / elkjs (EPL-2.0 OR GPL-3.0; 1.6 MB, ~457 KB gz; v0.12.0 2026-07-17, active)
- Empirically verified (Node): deterministic; returns real orthogonal edge routes
  (`sections` with bendPoints) and *placed* edge-label coordinates; `elk.json.edgeCoords: ROOT`
  flattens nested coordinate systems.
- **cytoscape-elk is a dead end** — source-verified: it applies node positions only and discards
  ELK's routes (Cytoscape always draws its own edges); pins elkjs 0.9; minimal maintenance.
- No native swimlanes; best verified recipe (partitions as phases + `semiInteractive` crossing
  minimization + lane-indexed pseudo-positions + `separateConnectedComponents: false`) still needs
  per-lane y band-snapping that invalidates routed verticals.
- No routing-only mode in the browser (the libavoid integration is a JVM-side external process).
- Strong for auto-layout of a *dependency* graph via custom SVG rendering (mermaid's ELK renderer
  is the precedent — with heavy defensive post-processing of routes). License is weak-copyleft,
  outside a strict permissive list.

### AntV X6 (MIT; single 583 KB UMD `dist/x6.min.js`, global `X6`; v3.1.7 2026-03-18)
- 3.x merged all former plugin subpackages into core — one vendorable file (panning, mousewheel
  zoom, selection, export all included).
- **Best free obstacle-avoiding orthogonal router in the field**: `manhattan` with
  `excludeShapes/excludeNodes/step/padding/fallbackRouter` — strictly stronger than Cytoscape taxi
  (which avoids nothing).
- Vanilla HTML nodes (`Shape.HTML.register`), events + `model.getNeighbors` make hover-dim a
  ~30-line hand-built layer. Parent/child embedding for lanes/groups.
- No lane primitive and no built-in auto-layout: lanes are a custom rect node whose *markup contains
  the header* (which fixes label placement structurally); placement is our grid math (endorsed by
  the central finding). Cadence slowed in 2026 (no release since March; last push June).

### LogicFlow (Apache-2.0; core+extension+CSS multi-file UMD; core 2.2.4 / ext 2.3.0, 2026-07-06, very active)
- **Only true maintained BPMN Pool/Lane primitive on the market** (`PoolElements`, ~4.5 months old);
  built-in `Highlight` plugin is a verbatim implementation of the loved hover-dim (`neighbour`/`path`
  modes); `@logicflow/layout` is uniquely lane-aware (Dagre+ELK, 1.6 MB).
- **Fatal for us: routing.** Core polyline A* avoids only the source/target nodes — edges cross
  unrelated nodes. That regresses the one thing already working.
- Script-tag path second-class (generic UMD globals `Core`/`Extension`, ergonomics unverified);
  open perf issue #2396 (full re-render on zoom).

### AntV G6 v5 (MIT; single 1.38 MB UMD; v5.1.1 2026-05-08)
- ~90% out-of-the-box for a grouped *network* graph: combos, `hover-activate` with `inactiveState`
  (the hover-dim as config), built-in antv-dagre, HTML nodes. No swimlane story at all; router less
  battle-tested than X6's. Wrong tool for the flowchart primitive; would only make sense in a
  two-library split with LogicFlow.

### maxGraph (Apache-2.0; v0.24.0 2026-07-08, pre-1.0)
- The draw.io lineage successor; kept `SwimlaneLayout`/`SwimlaneModel`/`SwimlaneManager` and
  hierarchical layout. **No browser build** — "direct usage in a web page is not supported"; needs
  a one-time offline bundling step to vendor; swimlane-layout port quality unverified; API churn risk.

### JointJS core (MPL-2.0; UMD on CDN; v4.3.0)
- Best-documented free `manhattan` obstacle-avoiding router; dagre-based layout package (MIT);
  foreignObject HTML labels. But pools/swimlanes and the pan/zoom PaperScroller are **JointJS+
  commercial**; free/paid boundary historically migrates toward paid. You'd hand-build the exact
  parts that failed before.

### bpmn-js — MIT-style **plus mandatory visible watermark**; no lane-aware auto-layout. Rejected.
### GoJS — commercial ($3,995/dev). Rejected.
### Mermaid v11 — subgraphs ≠ lanes×phases; cross-lane edges break subgraph direction; 2.75 MB IIFE; hover = fragile SVG surgery. Rejected for these primitives.
### D2.js — no swimlanes (open since 2022); grid cells have no path-finding; best layout (TALA) is proprietary/watermarked; MPL + multi-MB WASM + worker files. Rejected.
### Graphviz-WASM — clusters fine, swimlanes famously painful (invisible-node grid recipes); `splines=ortho` officially incompatible with dot edge labels. Rejected for the flowchart.
### React Flow / xyflow — no vanilla path as of 2026-07 (React/Svelte only, build required). Rejected.
### Drawflow / Rete.js / react-diagrams — stale, framework-bound, or no auto-layout. Rejected.

## Standalone orthogonal edge routers (for the grid + router architecture)

1. **libavoid-js** — WASM port of Adaptagrams libavoid; production-grade nudging/separation; the
   ELK team's own choice. **LGPL-2.1**, beta (0.5.0-beta.5, 2026-02), single maintainer, ~0.8 MB.
   `elkjs-libavoid` (MIT wrapper) accepts ELK-JSON with fixed positions.
2. **Pure-JS A*/Dijkstra grid router** — the jose-mdz OrthogonalConnector pattern (~300 lines) or
   X6/JointJS's built-in manhattan. Adequate at docs-site scale; lacks libavoid's parallel-edge
   nudging (approximate with per-edge offsets).

## Decision frame

| Option | Swimlane | Grouped graph | Routing | Hover-dim | License | Vendoring |
|---|---|---|---|---|---|---|
| X6, one engine | hand lanes w/ header-in-markup + our grid | embedding + our grid (dagre optional) | best-in-field manhattan | ~30 lines on events | MIT | 1 file, 583 KB |
| elkjs + custom SVG | partition recipe + band-snap (fights engine) | excellent auto-layout | real routes (while ELK owns positions) | trivial in own SVG | EPL flag | 1 file, 1.6 MB + renderer we own |
| LogicFlow (+G6 split) | true primitive, 90% OOTB | G6 combos 90% OOTB | **weak (crosses nodes)** | built-in | Apache/MIT | multi-file, ~2.4 MB total |
| Grid + libavoid + own SVG | our grid + real router | our grid + real router | production-grade | trivial | LGPL flag | wasm + wrapper, beta |
