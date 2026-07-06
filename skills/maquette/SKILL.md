---
name: maquette
description: Build a sellable, high-fidelity, browser-only prototype of a greenfield product — every user journey clickable, realistic mock data, simulated network feel, a live MCP demo surface, and a handoff contract a full-stack agent can implement from. Use when the user wants a demo-quality prototype to pitch/sell a product idea, a clickable greenfield app prototype, or a pre-implementation product mockup. Not for MVPs, real backends, or changes to existing products.
argument-hint: "[product idea or brief]"
user-invocable: true
---

# Maquette

A maquette is the architect's scale model: built entirely to sell the building before it exists, precise
enough that engineering can start from it. That is the deliverable — **not an MVP**. No real auth, no
database, no external services. A Next.js app that runs locally (and deploys statically) and is
indistinguishable from a finished product for the length of a sales meeting.

One build produces three artifacts wearing one trench coat:

1. **A sales asset** — the demo that closes the deal.
2. **A product spec** — journeys, screens, and states, defined by existing rather than by documents.
3. **An implementation contract** — the typed mock data is the future schema; the mock API layer is the
   future backend contract; `HANDOFF.md` makes the full-stack build mechanical.

Every decision below serves all three at once. When two goals conflict, the demo wins — but record the debt
in the handoff notes instead of silently dropping the other two.

## Non-negotiables

- **The seam.** Every screen talks to `lib/api/*.ts` — async functions with simulated latency over one
  client-side store seeded from typed fixtures. Components never import fixture data directly. Real
  implementation later = replace `lib/api/` and keep the types. See [architecture](references/architecture.md).
- **No dead clicks.** Every rendered control either works or does not exist. A button that does nothing is
  worse than no button.
- **Session-coherent state.** Create a record on one screen and it appears everywhere it should — counts,
  lists, feeds, detail pages. This is the line between a clickable Figma and a maquette.
- **Data realism is the #1 fidelity lever.** Domain-correct names, believable volumes and distributions,
  cross-referenced entities, dates relative to now. See [mock data](references/mock-data.md). "John Doe,
  $100.00, March 2025" kills a demo faster than any missing feature.
- **Every faked behavior carries a greppable `@mock` marker** with a one-line note on what the real
  implementation needs. The handoff doc is generated from these.
- **Demo-first prioritization.** The intake identifies the beats that close the deal; those get the fidelity
  budget. Everything else can be shallower — but still clickable.

## Pipeline

Run the phases in order. Each phase names the reference to load — load it when you enter the phase, not
before. Phases 1 and 3 end in explicit user sign-off gates; do not build past an unapproved gate, because
everything downstream is expensive to redo.

### 1. Intake interview — load [intake](references/intake.md)

A back-and-forth interview, **one question at a time**, until you and the user reach shared understanding:
what is being built, for whom, the deal context, the journeys, the look and feel, reference products, brand
guidelines, the agent (MCP) surface, and the research mandate. The intake does the heavy lifting for the
whole pipeline. Output: `BRIEF.md`, read back to the user. **Gate: user approves the brief.**

### 2. Research (per the mandate from intake)

Only as deep as the intake agreed. Typical briefs: how practitioners in this domain actually run the
business process today, competitor teardowns (screens, terminology, pricing pages), the vocabulary and data
fields users expect to see. Use whatever parallel research capability the environment provides; verify
load-bearing claims from a second source. Fold findings back into `BRIEF.md` as amendments — flag anything
that contradicts what the user said in intake rather than silently overriding.

### 3. Journey and screen design — load [ux-rules](references/ux-rules.md)

From the brief, produce `JOURNEYS.md`:

- Personas and the demo's "current user".
- User journeys ranked by demo criticality; the scope fence (what is explicitly out).
- **Agent journeys** — what a coding agent connected over MCP should be able to do; the planned tool surface.
- Screen inventory: for each screen, its journeys, states (populated / loading / empty / error where
  deliberate), and the planning checklist from ux-rules (visual hierarchy, explicitness spectrum,
  progressive disclosure, action/consequence co-location).
- The demo beats: the 3-or-so scripted moments that close the deal, and which screens carry them.

**Gate: user approves `JOURNEYS.md`.** A journey map is cheap to change; built screens are not.

### 4. Data design — load [mock-data](references/mock-data.md)

Write `lib/schema.ts` (the domain types — this is the future database schema) and the seeded fixture
generators. Get volumes, distributions, edge cases, and cross-references right here; realism is engineered,
not sprinkled.

### 5. Build — load [architecture](references/architecture.md), [design-language](references/design-language.md), [web-quality](references/web-quality.md)

Scaffold per the architecture recipe, then build screens in journey order (demo-critical first). Design
language: the client's brand tokens if intake produced them, otherwise stock shadcn/ui — never invent a
third option. When the screens work, do a dedicated **details pass** with [feel](references/feel.md):
motion, typography, depth, perceived latency. Fidelity is an explicit pass, not an ambient hope.

### 6. Demo hardening — load [demo](references/demo.md)

Demo script, persona switcher, hidden demo panel, reset-to-pristine, scripted live moments (including the
MCP agent moment), the offline/projector checklist, and the **dead-click sweep** — walk every route and
control; any dead end fails the phase.

### 7. Handoff — load [handoff](references/handoff.md)

Generate `HANDOFF.md` from the schema, the api seam, the `@mock` inventory, and the MCP tool surface. It
must be self-contained: a full-stack agent with no access to this conversation should be able to implement
the real product from the repo + that one file.

## Operating rules

- The user's product copy rules apply to everything rendered: never leak build guidance, internal names, or
  acceptance criteria into user-facing copy ([ux-rules](references/ux-rules.md)).
- Small scope is fine. A maquette can be four screens. Depth of believability beats breadth of surface.
- If the user arrives mid-pipeline (has a brief, has journeys), enter at the matching phase — but confirm
  the earlier gates' outputs exist and are approved before building.
- Keep `BRIEF.md`, `JOURNEYS.md`, and `HANDOFF.md` in the repo root of the prototype. They are deliverables,
  not scratch.
