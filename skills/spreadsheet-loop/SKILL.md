---
name: spreadsheet-loop
description: Build complex Excel workbooks on a browser-native surface instead of in Excel, then compile to .xlsx as the last step. Excel is slow and opaque to iterate on; a web spreadsheet (Univer) plus HTML spec docs is fast for human and agent to collaborate on. The Univer snapshot is the single source of truth; a converter we own compiles it to .xlsx, preserving formulas, styles, merges, number formats, named ranges, data validation, and conditional formatting. Keeps the data model (semantics, named ranges, inputs vs computed) and the layout (visual language) as separate reasoning artifacts. Use to author a financial model, pricing sheet, budget, dashboard, or any non-trivial workbook; to bring an existing .xlsx onto a web surface and iterate; or to compile a web spreadsheet to Excel. Not for editing an existing Excel file in place, one-off data dumps, or CSV munging.
argument-hint: "[what workbook to build, or path to an existing .xlsx]"
user-invocable: true
---

# Spreadsheet Loop

Excel is a bad surface for an agent to work on — slow, laggy, stateful, hard to diff, hard to reason about.
The web is the opposite: a browser spreadsheet is fast, inspectable, and something a human and an agent can
edit **together**. So do the whole build on the web and treat Excel as a **compile target**, not a workshop.

The loop: author on a browser-native spreadsheet ([Univer](https://docs.univer.ai/guides/sheets)) alongside
HTML/markdown spec docs, iterate with the human until the workbook is right, then **compile to `.xlsx`** as
the final step. The `.xlsx` is a build output, the way a binary is — never the place you edit.

## The one idea that makes export faithful

**The source of truth is the Univer snapshot plus a small `objects.json`.** The browser renders them; Excel is
produced from them by a converter *we own* ([converter](reference/converter.md)). Views of one source can't
drift, so a faithful export falls out by construction — there is no second *authored* artifact to keep in sync.

Univer's own high-fidelity xlsx exchange is a commercial server feature; we do **not** depend on it. The
converter is Python built on **`openpyxl`** (MIT), license-free and watermark-free. It reliably round-trips the
cell **spine** — literal values, dates, formula text, number formats, merges, named ranges, sheet structure —
and materializes **native charts** and flattened **pivots** from declared objects.

> **Status: BETA (2026-07-10).** After a real-workbook hardening pass, the conformance harness
> (`verify/conformance.py`) reports **100% round-trip** of values, formulas, cached results, number formats,
> resolved styles (theme colours included), data validation, and conditional formatting on two real financial
> workbooks — a 77-sheet macro `.xlsm` also round-trips without crashing. **Still not "authoritative-file"
> trust:** comments/hyperlinks/images/sheet-visibility aren't modeled, colour tint is approximate, and results
> aren't yet verified by opening in Excel — so audit before distributing and keep the source. Full measured
> status + residual backlog in [converter](reference/converter.md).

**Closure is the invariant:** what the browser renders, what the exporter writes, and what the importer reads
must be the same set. Cell-level features round-trip symmetrically; charts and pivots hold closure by
discipline (declared, previewed, materialized — never free-drawn in the browser where they couldn't export).

## Two separated concepts — hold them apart on purpose

The human and agent reason about the workbook through two artifacts that must never be conflated
([model-vs-layout](reference/model-vs-layout.md)):

- **The model** (`MODEL.md`) — the data model: entities, inputs vs. computed cells, named ranges, the
  formula logic and the relationships between them, units, validation rules. What the workbook *means*.
- **The layout** (`LAYOUT.md`) — the visual language: sheet structure, sections, header treatment, number
  formats, colour and border conventions, the grid design. What the workbook *looks like*.

Both govern the snapshot; neither *is* the snapshot. Charts and pivots are **declared objects** — the model
decides a pivot's fields, the layout decides a chart's placement — recorded in `objects.json` and compiled
natively. Keeping model and layout apart is what lets a human and an agent iterate fast — you change the model
without re-deciding the look, and restyle the layout without touching the logic.

## Pipeline

Run the phases in order. Each phase names the reference to load when you enter it. Phases 1 and 2 end in
explicit human sign-off through the `review-loop` skill (see [sign-off](reference/sign-off.md)); do not build
past an unapproved gate — everything downstream is expensive to redo. Build-out is staffed through the
`staffing` skill.

### 1. Intake — load [intake](reference/intake.md)

A short interview, **one question at a time**: what workbook, for whom, greenfield or starting from an
existing `.xlsx`, the complexity, the numbers and formulas that matter, the look. Output: `SPEC.md`.
**Gate:** present `SPEC.md` for sign-off through `review-loop`; proceed only on an approving verdict.

### 2. Model & layout — load [model-vs-layout](reference/model-vs-layout.md)

Write `MODEL.md` and `LAYOUT.md` as two separate documents. This is where the data model (named ranges,
inputs, computed logic, relationships) and the visual language are decided, on paper, before a single cell
exists. **Gate:** present both for sign-off through `review-loop`; proceed only on approval. Paper is cheap
to change; a built workbook is not.

### 3. Scaffold — load [univer-surface](reference/univer-surface.md)

Stand up the browser surface: a local Vite + `@univerjs/presets` app that loads and persists
`workbook.snapshot.json`, plus the converter and the verify harness. If starting from an existing `.xlsx`,
run the import converter first to seed the snapshot ([converter](reference/converter.md)).

### 4. The loop — load [the-loop](reference/the-loop.md)

Serve the surface on the repo's presentation surface and iterate. The human edits cells directly and/or the
agent applies changes through the Facade API; either way the snapshot is the persisted state. Every
iteration is checked back against `MODEL.md` and `LAYOUT.md` — the docs and the snapshot move together.

### 5. Compile — load [converter](reference/converter.md)

Run `snapshot → .xlsx`. Preserves the committed feature set; the converter is the authority on what survives
and what does not.

### 6. Verify — load [verify](reference/verify.md)

Recompute formulas headlessly (Univer's Node core), open the produced `.xlsx`, and diff it against the
browser rendering. Where the machine allows, drive a real spreadsheet app to confirm it opens clean. A
fidelity gap is a converter bug or an out-of-scope feature used — name which.

## How it composes

- **`review-loop`** presents `SPEC.md`, `MODEL.md`, and `LAYOUT.md` for sign-off — rendered to review HTML,
  served with annotation chrome, gated on a batched verdict. The **live Univer surface** is not a review-loop
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
  [intake](reference/intake.md), [univer-surface](reference/univer-surface.md) (the scaffold recipe),
  [snapshot-model](reference/snapshot-model.md) (the `IWorkbookData` shape we rely on),
  [converter](reference/converter.md) (the `openpyxl` mapping, declared objects, and its fidelity table),
  [the-loop](reference/the-loop.md) (the edit protocol), [verify](reference/verify.md), and
  [sign-off](reference/sign-off.md). Plus runnable `templates/` (the tested converter, the Vite/Univer app,
  the verify harness, the `MODEL.md`/`LAYOUT.md` skeletons). They import no other skill's files.
- **Project playbook** — the repo-specific **surface config** under `docs/agents/` (the tailnet root, the
  publish/proxy commands) that `review-loop` and the live-surface serving read. Absent one, both degrade to
  a local open rather than improvising a tunnel.
- **Sibling skills** — **`review-loop`** (sign-off) and **`staffing`** (build routing), composed by name, no
  imports. `spreadsheet-loop` is a composer: these two are load-bearing dependencies.
