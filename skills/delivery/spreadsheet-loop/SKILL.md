---
name: spreadsheet-loop
description: Plan, build, test, and safely modify complex Excel workbooks through a browser-native Univer workbench. Use for financial models, pricing sheets, budgets, dashboards, and other non-trivial workbooks; for decomposing a large workbook into reviewable components; for importing a supported workbook into a browser lane; or for merging scoped browser-authored changes back into an authoritative Excel file while preserving unsupported features. Chooses among a browser-native build lane, a scoped browser-plus-merge lane, and an Excel-native lane after capability preflight. Not for one-off data dumps or CSV munging.
disable-model-invocation: true
metadata:
  invocation: user
  execution: orchestrator
  requires: [serve-via-tailnet, staffing]
  optional: []
---

# Spreadsheet Loop

Excel is often a poor construction surface for an agent: it is stateful, hard to diff, and expensive to
inspect repeatedly. A browser spreadsheet is fast, inspectable, and testable. But an existing `.xlsx` or
`.xlsm` may contain VBA, external links, native charts, images, pivots, or OOXML extensions that a browser
model cannot safely reconstruct. **Choose the authority and lane before editing.**

The common loop is still powerful: author a scoped model on a browser-native spreadsheet
([Univer](https://docs.univer.ai/guides/sheets)) alongside markdown specs rendered to HTML for review,
iterate with the human, run machine checks, then compile or merge. The difference is that Excel is a compile
target **only when the workbook is greenfield or fully supported**. Otherwise the original Excel package
remains authoritative and the browser produces a reviewed, bounded changeset.

## Three lanes — decide explicitly

Run capability preflight and choose one lane ([lanes-and-merge](reference/lanes-and-merge.md)):

1. **Browser-native build.** Greenfield or fully supported workbook. The Univer snapshot plus
   `objects.json` is authoritative; `.xlsx` is compiled output.
2. **Scoped browser + merge.** Existing authoritative workbook with preserve-only features. Import only the
   approved components, produce a machine-readable changeset, and apply it to a **copy of the original**.
   Untouched VBA, charts, links, images, pivots, and OOXML parts remain byte-preserved where possible.
3. **Excel-native.** The requested change depends on Excel runtime behaviour or unsupported structures.
   Work outside the browser lane with file-native tooling and/or Excel Computer Use; use the browser only for
   specs, isolated prototypes, or checks that do not pretend to round-trip the authoritative file.

Never silently demote a workbook from lane 2 to a full re-export. If no preservation-safe merge adapter is
available for the requested operation, stop at a reviewed changeset and hand the change to Excel.

## Decompose before constructing

Treat a complex workbook as components with contracts, not as one enormous grid. Write `COMPONENTS.md` with
each component's owned sheets/ranges, inputs, outputs, dependencies, editable cells, assertions, lane, and
merge boundary. Prefer focused browser workspaces over loading all 77 sheets when the task concerns one
pricing block. Cross-component references become explicit interfaces or read-only fixtures.

Univer's own high-fidelity xlsx exchange is a commercial server feature; we do **not** depend on it. The
converter is Python built on **`openpyxl`** (MIT), license-free and watermark-free. It reliably round-trips the
cell **spine** — literal values, dates, formula text, number formats, merges, named ranges, sheet structure —
and materializes **native charts** and flattened **pivots** from declared objects.

> **Status: BETA (2026-07-10).** After a real-workbook hardening pass, the conformance harness
> (`verify/conformance.py`) reports **100% round-trip** of values, formulas, cached results, number formats,
> resolved styles (theme colours included), data validation, and conditional formatting on two real financial
> workbooks. Browser smoke tests also cover live rendering, declared objects, autosave, and reload-on-agent
> edits; Revenue and PS exports open in real Excel. A 77-sheet macro `.xlsm` imports and renders, but its VBA,
> native charts, external links, and some images prove why lane 2/3 exists. Full measured status + residual
> backlog in [converter](reference/converter.md).

**Closure is lane-relative:** in lane 1, browser-renders ⟺ exporter-writes ⟺ importer-reads. In lane 2, the
invariant is narrower: every browser-authored change is declared, reviewed, merged, and verified, while every
out-of-lane feature in the original is preserved or explicitly handed off. “The file opened” is not proof.

## Three separated concepts — hold them apart on purpose

The human and agent reason about the workbook through three artifacts that must never be conflated
([model-vs-layout](reference/model-vs-layout.md)):

- **The model** (`MODEL.md`) — the data model: entities, inputs vs. computed cells, named ranges, the
  formula logic and the relationships between them, units, validation rules. What the workbook *means*.
- **The layout** (`LAYOUT.md`) — the visual language: sheet structure, sections, header treatment, number
  formats, colour and border conventions, the grid design. What the workbook *looks like*.
- **The component map** (`COMPONENTS.md`) — ownership and boundaries: which sheets/ranges belong together,
  what they consume and emit, which lane they use, and how they are validated and merged.

All three govern the workbench; none *is* the authoritative file in lane 2. Charts and pivots are **declared objects** — the model
decides a pivot's fields, the layout decides a chart's placement — recorded in `objects.json` and compiled
natively. Keeping model and layout apart is what lets a human and an agent iterate fast — you change the model
without re-deciding the look, and restyle the layout without touching the logic.

## Pipeline

Run the phases in order. Each phase names the reference to load when you enter it. Phases 1 and 2 end in
explicit human sign-off through the `serve-via-tailnet` skill (see [sign-off](reference/sign-off.md)); do not build
past an unapproved gate — everything downstream is expensive to redo. Build-out is staffed through the
`staffing` skill.

### 1. Intake & capability preflight — load [intake](reference/intake.md) and [lanes-and-merge](reference/lanes-and-merge.md)

A short interview, **one question at a time**: what workbook, for whom, greenfield or existing, the numbers
and formulas that matter, the look, and the authoritative-file constraints. For an existing workbook, scan
features before promising a round trip. Output: `SPEC.md` with a capability table and proposed lane.
**Gate:** present `SPEC.md` for sign-off through `serve-via-tailnet`; proceed only on an approving verdict.

### 2. Model, layout & components — load [model-vs-layout](reference/model-vs-layout.md)

Write `MODEL.md`, `LAYOUT.md`, and `COMPONENTS.md`. For lane 2, include the merge boundary and preserve-only
features. **Gate:** render the documents as a self-contained HTML review artifact and present them through
`serve-via-tailnet`; proceed only on approval. Paper is cheap to change; a built workbook is not.

### 3. Scaffold — load [univer-surface](reference/univer-surface.md)

Stand up the browser surface for the approved components: a local Vite + `@univerjs/presets` app that loads
and persists `workbook.snapshot.json`, plus the converter and verify harness. In lane 2, import into an
isolated workbench; never replace the authoritative source.

### 4. The loop — load [the-loop](reference/the-loop.md)

Serve the surface and iterate **in turns** — one party holds the pen at a time. On a human turn they edit in
the browser (autosaved to disk); on an agent turn the agent edits the files (directly or via a headless
Facade script) and the browser reloads to the new state. A version-guarded save + reload-on-agent-edit keep
turns safe inside the workbench. Every turn is checked back against `MODEL.md`, `LAYOUT.md`, and
`COMPONENTS.md` — the docs, snapshot, and lane boundary move together.

### 5. Integrate — load [converter](reference/converter.md) and [lanes-and-merge](reference/lanes-and-merge.md)

- **Lane 1:** compile `snapshot + objects → .xlsx`.
- **Lane 2:** emit a changeset, merge it into a copy of the original through a preservation-safe adapter, and
  refuse unsafe structural operations.
- **Lane 3:** execute or hand off in Excel; keep the reviewed component contract and assertions.

### 6. Verify — load [verify](reference/verify.md)

Recompute formulas headlessly, read the produced file back, verify component assertions, and check the merge
preserved all out-of-lane features. Where the machine allows, drive real Excel to confirm the result opens
without repair prompts. A fidelity gap is a converter bug, a merge bug, or an out-of-scope operation — name
which.

## How it composes

- **`serve-via-tailnet`** presents `SPEC.md`, `MODEL.md`, `LAYOUT.md`, and `COMPONENTS.md` for sign-off — rendered to review HTML,
  served with annotation chrome, gated on a batched verdict. The **live Univer surface** is not a serve-via-tailnet
  artifact; it is a live interactive surface, served on the presentation surface and driven directly (the
  same distinction the `prototype` skill draws between a rendered artifact and a live prototype). Invoked by
  name; this skill never forks a review UI.
- **`staffing`** staffs the build. Framing, model/layout decisions, and reading the result stay with the
  invoking thread; mechanical build-out (scaffold, converter wiring, bulk cell population) routes to the
  pinned mechanical model, and taste-weighted work (the layout's visual language) to a taste-ranked model.
  This skill asks staffing; it does not hardcode the roster.

## Dependency surface

- **Bundled references** — this skill's own contract, shipped in-directory:
  [model-vs-layout](reference/model-vs-layout.md) (the separation doctrine),
  [intake](reference/intake.md), [lanes-and-merge](reference/lanes-and-merge.md) (capability, decomposition,
  changesets, preservation), [univer-surface](reference/univer-surface.md) (the scaffold recipe),
  [snapshot-model](reference/snapshot-model.md) (the `IWorkbookData` shape we rely on),
  [converter](reference/converter.md) (the `openpyxl` mapping, declared objects, and its fidelity table),
  [the-loop](reference/the-loop.md) (the edit protocol), [verify](reference/verify.md), and
  [sign-off](reference/sign-off.md). Plus runnable `templates/` (the tested converter, the Vite/Univer app,
  the verify harness, and `SPEC.md`/`MODEL.md`/`LAYOUT.md`/`COMPONENTS.md` skeletons). They import no other
  skill's files.
- **Project playbook** — the repo-specific **surface config** under `docs/agents/` (the tailnet root, the
  publish/proxy commands) that `serve-via-tailnet` and the live-surface serving read. Absent one, both degrade to
  a local open rather than improvising a tunnel.
- **Sibling skills** — **`serve-via-tailnet`** (sign-off) and **`staffing`** (build routing), composed by name, no
  imports. `spreadsheet-loop` is a composer: these two are load-bearing dependencies.
