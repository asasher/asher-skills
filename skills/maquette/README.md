# Maquette

Build a sellable, high-fidelity, browser-only prototype of a greenfield product — the concept car, not the
MVP. One build yields three artifacts: the demo that closes the deal, the product spec (defined by
existing), and the implementation contract a full-stack agent can build the real product from.

## Shape

- **Intake interview first** — one question at a time until shared understanding; `BRIEF.md` sign-off gates
  everything, presented through the `review-loop` skill.
- **One architectural seam** — typed schema + seeded fixtures + a mock `lib/api/` layer with simulated
  latency over a localStorage-persisted client store. No dead clicks, session-coherent state, `@mock`
  markers everywhere reality is faked.
- **A real mini MCP server** bridges local coding agents into the mock store for a live "agent drives the
  product" demo beat.
- **Demo hardening** — script, persona switcher, hidden demo panel, offline-safe, dead-click sweep as the
  gate.
- **`HANDOFF.md`** — generated from the schema, api seam, and `@mock` inventory.

## Layout

`SKILL.md` is the pipeline spine; each phase loads one reference from `references/` (intake, mock-data,
architecture, design-language, feel, ux-rules, web-quality, demo, handoff). Self-contained by design: the
design/feel/quality references are distillations (shadixfy@a58e37d, bare-minimum-ux, Emil Kowalski's
design-eng skill, Jakub Krehel's interface-details essay, vercel-labs agent-skills) — sync deliberately,
not automatically.

## Evals

`evals/probes.md` — situated dry-run probes with an answer key (cheap pre-deployment comprehension check).
`evals/build-eval.md` — one full build against a sample brief, graded on dead clicks, data realism,
`@mock` coverage, and deliverable completeness.
