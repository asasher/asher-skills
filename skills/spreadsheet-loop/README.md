# Spreadsheet Loop

Build complex Excel workbooks **on a browser-native surface instead of in Excel**, then compile to `.xlsx` as
the last step. Excel is slow, laggy, and opaque for an agent to iterate on; a web spreadsheet
([Univer](https://docs.univer.ai/guides/sheets)) plus HTML/markdown spec docs is fast for a human and an agent
to collaborate on. Excel is the compile target, not the workshop.

## When to use

- **Authoring a non-trivial workbook** — a financial model, pricing sheet, budget, dashboard, or tracker,
  where the formulas and layout matter and you'd otherwise be clicking around Excel.
- **Bringing an existing `.xlsx` onto a web surface** to iterate on it fast, then recompile.
- **Not for** editing an existing Excel file in place, one-off data dumps, or CSV munging.

## The idea

- **The source of truth is the Univer snapshot + a small `objects.json`.** The browser renders them; Excel is
  produced from them by a converter *we own*. Views of one source can't drift — a faithful export falls out by
  construction.
- **We don't depend on Univer's commercial exchange.** A Python/`openpyxl` converter gives license-free,
  watermark-free export for a broad feature set: values, formulas, styles, merges, number formats, freeze,
  named ranges, all validation and conditional-formatting types, images, and **native charts**. **Pivot
  tables** — which no open-source library creates live — are *declared objects*, flattened to a faithful
  computed table by default and upgradeable to a real interactive pivot via a LibreOffice pass. The only
  honest gap is pivot interactivity in the file, named at intake.
- **Closure is the invariant:** browser-renders ⟺ exporter-writes ⟺ importer-reads is the same set. Import
  even *detects and reports* charts/pivots it can't reconstruct, rather than silently dropping them.
- **Model and layout are held apart.** `MODEL.md` (data model: inputs vs. computed, named ranges, formula
  logic) and `LAYOUT.md` (visual language) are separate reasoning artifacts. That separation is what makes the
  loop fast.

## Shape

A gated pipeline: **intake → SPEC** (sign-off) · **model & layout** (sign-off) · **scaffold** the Vite/Univer
app · **the loop** (edit the snapshot together on the live surface) · **compile** to `.xlsx` · **verify**
(headless recompute + read-back diff + real-app open). Sign-off on the paper artifacts runs through the
`review-loop` skill; build-out is staffed through the `staffing` skill. The live spreadsheet surface is driven
directly, not gated.

## Layout

`SKILL.md` is the pipeline, how it composes review-loop + staffing, and the dependency surface.
`reference/` holds the contract: `model-vs-layout.md` (the separation doctrine), `intake.md`,
`univer-surface.md` (scaffold recipe), `snapshot-model.md` (the `IWorkbookData` shape + `objects.json`),
`converter.md` (the `openpyxl` mapping, declared objects + fidelity table), `the-loop.md` (edit protocol),
`verify.md`, and `sign-off.md`.
`templates/app/` is the complete, self-contained project (the **tested** converter, the Vite/Univer app with
snapshot persistence, and the verify harness); `templates/MODEL.md` and `templates/LAYOUT.md` are the doc
skeletons. `agents/openai.yaml` is the Codex manifest. `evals/` is the pre-deployment probe eval.

Self-contained at the file level; composes by name. **Sibling dependencies: `review-loop` + `staffing` —
`spreadsheet-loop` is a composer, not a root primitive** (it depends on those two by name and imports none of
their files).

## Install

`npx skills add <repo-url> --skill spreadsheet-loop`, then hand it a workbook to build (or the path to an
existing `.xlsx`). The scaffolded project is polyglot: Node (`npm install` → Univer presets + Vite) for the
browser surface, and Python (`pip install -r requirements.txt` → openpyxl) for the converter.
Presenting an artifact for sign-off and serving the live surface use the repo's presentation surface config
(`docs/agents/environment.md`); absent it, both degrade to a local open. Sign-off needs the `review-loop`
skill installed; staffing the build needs the `staffing` skill installed.
