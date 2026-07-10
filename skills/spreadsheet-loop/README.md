# Spreadsheet Loop

Build and test complex workbook components on a browser-native surface, then either compile a new `.xlsx`,
merge a reviewed changeset into an authoritative Excel copy, or route the operation to Excel when the browser
cannot preserve it. The browser is an agent workbench; it is not automatically the authority.

## When to use

- **Authoring a non-trivial workbook** — a financial model, pricing sheet, budget, dashboard, or tracker,
  where the formulas and layout matter and you'd otherwise be clicking around Excel.
- **Bringing a supported component of an existing `.xlsx`/`.xlsm` onto a web surface**, then merging scoped
  changes back without replacing preserve-only features.
- **Decomposing a large workbook** into explicit inputs, calculations, outputs, reporting, and integration
  components with contracts and assertions.
- **Not for** silently re-exporting an authoritative macro/connection-heavy workbook, one-off data dumps, or
  CSV munging.

## The idea

- **Three explicit lanes.** Browser-native build for greenfield/supported work; scoped browser + merge when an
  existing Excel file remains authoritative; Excel-native when the requested change depends on unsupported
  objects or runtime behaviour.
- **Capability preflight and component contracts.** The user sees what is browser-safe, preserve-only, or
  Excel-native before approving the work.
- **We don't depend on Univer's commercial exchange.** A Python/`openpyxl` converter gives license-free,
  watermark-free export for a broad feature set: values, formulas, styles, merges, number formats, freeze,
  named ranges, all validation and conditional-formatting types, images, and **native charts**. **Pivot
  tables** — which no open-source library creates live — are *declared objects*, flattened to a faithful
  computed table by default and upgradeable to a real interactive pivot via a LibreOffice pass. VBA,
  external links/connections, imported native charts, signatures, and unknown OOXML extensions remain
  preserve-only or Excel-native and are named by preflight.
- **Closure is lane-relative:** lane 1 proves browser ↔ export parity; lane 2 proves changeset scope plus
  preservation of everything outside it.
- **Model, layout, and component boundaries are held apart.** `MODEL.md`, `LAYOUT.md`, and `COMPONENTS.md`
  make meaning, visual language, ownership, dependencies, assertions, and merge scope independently reviewable.

## Shape

A gated pipeline: **intake + capability preflight → SPEC** (HTML sign-off) · **model + layout + components**
(HTML sign-off) · **scaffold** the focused Vite/Univer workbench · **the loop** · **compile / merge / Excel
handoff** · **verify**
(headless recompute + read-back diff + real-app open). Sign-off on the paper artifacts runs through the
`review-loop` skill; build-out is staffed through the `staffing` skill. The live spreadsheet surface is driven
directly, not gated.

## Layout

`SKILL.md` is the pipeline, how it composes review-loop + staffing, and the dependency surface.
`reference/` holds the contract: `model-vs-layout.md` (the separation doctrine), `lanes-and-merge.md`, `intake.md`,
`univer-surface.md` (scaffold recipe), `snapshot-model.md` (the `IWorkbookData` shape + `objects.json`),
`converter.md` (the `openpyxl` mapping, declared objects + fidelity table), `the-loop.md` (edit protocol),
`verify.md`, and `sign-off.md`.
`templates/app/` is the complete, self-contained project (the **tested** converter, the Vite/Univer app with
snapshot persistence, and the verify harness); `templates/SPEC.md`, `templates/MODEL.md`,
`templates/LAYOUT.md`, and `templates/COMPONENTS.md` are the doc skeletons. `agents/openai.yaml` is the Codex
manifest. `evals/` is the pre-deployment probe eval.

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
