# The converter — snapshot (+ objects) ↔ .xlsx

The converter is the **lane-1 compile step** and the authority on what survives a full snapshot-to-Excel
trip. It is useful for producing a lane-2 workbench, but a full converter save is **not** a
preservation-safe merge for an authoritative workbook with preserve-only features. It lives in the
scaffolded project as Python scripts under `converter/`, built on
[`openpyxl`](https://openpyxl.readthedocs.io) — a permissively licensed (MIT) library, no server, no
watermark. The tested reference implementations ship in this skill's `templates/app/converter/`.

- `snapshot-to-xlsx.py <snapshot.json> <out.xlsx> [objects.json]` — the compile (phase 5).
- `xlsx-to-snapshot.py <in.xlsx> <out.snapshot.json> [out.objects.json]` — the import (phase 3).
- `converter/test.py` + `verify/read-back-check.py` — the converter's own test and a general diff.

## Why openpyxl (not a JS xlsx library, not Univer's paid exchange)

Univer's high-fidelity xlsx exchange is a commercial server feature; we don't depend on it. Among
open-source writers, **`openpyxl` is the most capable** — crucially, it creates **native Excel charts**, all
**conditional-formatting** types (colour scale, data bar, icon set, cell-is), all **data-validation** types,
**images**, and named ranges. (Node's `exceljs`, the obvious alternative, cannot author charts at all — that
was the deciding factor.) The one thing no open-source library creates is a **live pivot table**; that is
handled specially below.

## Lane-1 source files

In lane 1 the source of truth is two files, because a couple of objects live outside Univer's native model:

- **`workbook.snapshot.json`** — Univer-native: cells, formulas, styles, merges, sizing, freeze, named
  ranges, list validation, conditional formatting. Edited live in the browser; autosaved by the app.
- **`objects.json`** — **declared objects**: charts and pivots (things Univer OSS can't natively hold or
  export). Authored by the agent from the model/layout decisions, previewed in the browser, never touched by
  Univer's save. See [model-vs-layout](model-vs-layout.md) and [the-loop](the-loop.md) for the discipline
  that keeps this symmetric.

In lane 2 these files are an isolated workbench. The deliverable is a reviewed changeset applied to a copy of
the original through a preservation-safe adapter; see [lanes-and-merge](lanes-and-merge.md).

## Status: BETA — hardened against real workbooks, with named residual gaps

> **Measured 2026-07-10 against real financial workbooks** (`Revenue.xlsx`, `PS v0.8.xlsx`, a 77-sheet `.xlsm`),
> before → after a hardening pass. On the two Revenue/PS workbooks the conformance harness
> (`verify/conformance.py`) now reports **100% preservation of values, formula text, cached results, number
> formats, resolved styles, merges, named ranges, data validation, and conditional formatting** — up from
> ~16% and total DV/CF loss. The 77-sheet macro `.xlsm` imports, renders in Univer, and exports without
> crashing. Its VBA, native charts, external links, and some images are preserve-only and therefore require
> lane 2/3. Revenue and PS exports were also opened in real Excel. **This is not authoritative-file trust:**
> use preflight and the lane decision before distributing.
>
> A **LibreOffice render diff** (2026-07-10) confirmed page-1 of `Revenue.xlsx` round-trips as a visual match
> (after fixing a font-fallback and a literal-`=` defect it caught). Residual gaps (still open): colour tint is
> a linear approximation (not pixel-verified against Excel); macros/charts in an imported file are
> detected-and-reported, not reconstructed; page-break position stays render-sensitive near thresholds; and
> the visual pass used a headless render, not interactive Excel. Backlog #8 tracks these.

## Feature set & measured real-workbook status

`snapshot (+ objects) → .xlsx`. Self-test 53/53 on the sample; the "measured" column is the conformance
harness on the Revenue/PS real workbooks:

| Feature | Source | openpyxl target | Measured |
|---|---|---|---|
| Literal values / formula text | `cell.v` / `cell.f` | `cell.value` | ✅ 100% |
| Dates/times | `cell.v`+`t:"d"` | `datetime` | ✅ |
| Cached formula results | `cell.v` on formula | post-save `<v>` injection | ✅ (backlog #3 done) |
| Number formats | `style.n.pattern` | `cell.number_format` | ✅ 100% |
| Merges, freeze, named ranges (incl. scope) | resources | worksheet / `defined_names` | ✅ |
| Font/fill/border/align — theme+indexed resolved | `cell.s` | `Font`/`PatternFill`/`Border`/`Alignment` | ✅ (tint = approx) |
| Data validation (import **and** export) | `SHEET_DATA_VALIDATION_PLUGIN` | `DataValidation` (all types) | ✅ (backlog #4 done) |
| Conditional formatting (CFVO/priority/font) | `SHEET_CONDITIONAL_FORMATTING_PLUGIN` | `cellIs`/`colorScale`/`dataBar`/`iconSet` | ✅ (backlog #5 done) |
| **Charts** (bar/line/pie, cross-sheet) | `objects.charts[]` | **native** `openpyxl.chart` | ✅ (backlog #6 done) |
| **Pivots** (rows×cols, sum/count/avg/min/max) | `objects.pivots[]` | flattened table (Tier A) / LibreOffice (Tier B) | ⚠️ static (interactive = Tier B) |
| Comments, hyperlinks, images, sheet visibility, grouped column spans | snapshot/import | native worksheet/package parts | ✅ committed subset; preflight unknown extensions |

## Charts — native, free

A chart is declared in `objects.json` (`type`, `title`, `categories`, `values`, `anchor`) and materialized as
a real Excel chart via `openpyxl.chart`. What you declare is what compiles; the browser shows a preview of the
same declaration, so there's no "browser shows a chart we can't export."

## Pivots — the one hard object, handled in tiers

No open-source library *creates* a live pivot table. A declared pivot (`source`, `rows`, `cols`, `values`) is
handled at the best tier available:

- **Tier A — flattened (default, proven, always available).** The converter groups the source range and
  writes a static computed table (group rows + grand total) with pure stdlib. Values are 100% faithful; it
  just isn't an interactive Excel pivot. This is what ships and what the browser previews.
- **Tier B — live pivot via LibreOffice (scaffolded upgrade).** When `soffice` is available, a post-pass can
  drive LibreOffice headless (UNO DataPilot) to add a real, interactive pivot from the same declaration and
  re-save the `.xlsx`. Higher fidelity; **smoke-test pending** — treat as opt-in until verified on the target
  machine.
- **Tier C — template injection (documented).** Keep an `.xlsx` template holding a pre-built pivot over a
  named source range; `openpyxl` updates the source data and sets refresh-on-load. Real live pivot, but the
  template must be authored once in Excel/LibreOffice.

Pick the tier at intake based on whether the deliverable needs an *interactive* pivot or just the summary
numbers. Either way the browser preview and the export agree on the values: the five aggregations
(`sum`/`count`/`avg`/`min`/`max`) are implemented with one semantic in both — `count` counts **non-empty**
source values (Excel's pivot Count), the other four operate on numeric values only.

## Import — capability evidence, not permission to replace the source

`xlsx-to-snapshot.py` recovers literal values, dates, formula text, styles (RGB colours only), merges, sizing,
freeze, named ranges (workbook scope only), and conditional formatting (`colorScale` / `cellIs`). A raw-package
**preflight** runs *first* and reports charts, pivots, macros, images, and external links it cannot
reconstruct — writing them into `objects.json` and to stderr **before** any crash-prone work, so detection is
fail-safe. Writes are atomic (temp + rename), so a mid-import failure can't leave a truncated, plausible file.
Feed the report into the lane decision. Preserve-only findings make the snapshot a workbench unless the user
explicitly approves dropping them. A re-import over an existing `objects.json` **preserves** its declared
charts/pivots and refreshes only `_import_note`; discarding them requires the explicit `--reset-objects` flag.

Hard boundaries include VBA execution/preservation guarantees, external connections/links, signatures,
native imported chart reconstruction, unsupported image formats, interactive pivots without the selected
materialization tier, and unknown OOXML extensions. The preflight report is the authority for a given file.

## Closure — lane-relative

In lane 1 the goal is browser-renders ⟺ exporter-writes ⟺ importer-reads. In lane 2 closure is a declared,
verified changeset plus preservation of everything outside its scope. Detection is evidence, not closure: an
import note can warn about native charts or VBA while a full compile still emits a chart-free/macro-free
`.xlsx`. That output is a prototype, not a merge.

What enforces lane-1 closure today:

- **`objects.schema.json` + the stdlib validator run as a compile gate** — invalid declared objects refuse
  to compile; an unknown chart type or aggregation is rejected, never silently coerced. The browser preview
  accepts exactly the schema's enums, so it cannot render a declaration the compile would refuse.
- **One aggregation semantic** — pivot `sum`/`count`/`avg`/`min`/`max` are implemented identically in the
  preview and the converter (`count` = non-empty, Excel's pivot Count); the numbers the human approves in
  the browser are the numbers the `.xlsx` carries.
- **Stable `sheetId` references** — a declared object may carry the snapshot's sheet id alongside the
  display name, and the compile, the validator, the verify read-back, and the browser preview all resolve
  sheetId-first, so a browser sheet rename cannot strand the sidecar.
- **Re-import preserves declarations** — `xlsx-to-snapshot.py` carries existing `objects.json` charts/pivots
  through a refresh-from-source (`--reset-objects` is the explicit way to start over).

Genuinely open gaps:

- **Interactivity**: a Tier-A pivot is a static computed table, not a draggable pivot (Tiers B/C exist for
  that; see above).
- **`sheetId` is optional**: a declaration that omits it still keys on the mutable sheet name — declare
  `sheetId` whenever the human can rename sheets in the browser.
- The #8 residuals (tint approximation, render-sensitive page breaks) bound any visual-fidelity claim.

## Hardening backlog (from the 2026-07-10 gpt-5.6 review + real-workbook round-trip)

1. **Type-safety + atomicity** — ✅ done: dates/times/array-formulas serialize; `default=str` net; atomic writes; fail-safe preflight incl. macros.
2. **Theme/indexed colour model** — ✅ done (`xlsx_theme.py`): theme+indexed colours resolve to RGB with tint; explicit black kept. Fonts/fills 16%→100% on Revenue. Tint = linear approx (not pixel-verified).
3. **Cached formula values** — ✅ done: import loads `data_only=True`; export injects `<v>` post-save. Cached-lost → 0.
4. **Data-validation import parity** — ✅ done: import emits the DV resource; inline lists quoted, range/named refs passed through; all DV types.
5. **Conditional-formatting fidelity** — ✅ done: CFVO types/values, priority, `stopIfTrue`, differential fonts preserved both ways.
6. **Charts/pivots/names** — ✅ done: cross-sheet chart refs resolve to their own sheet; pivots do rows×cols with sum/count/avg/min/max and reuse an existing sheet; defined-name scope preserved.
7. **Closure enforcement** — ✅ done: `objects.schema.json` + stdlib `validate_objects.py` + compile gate (fails on invalid declared objects, warns on unresolved import gaps) + manifest hashes; stable `sheetId` references resolve end-to-end (compile, validator, verify read-back, browser preview). Residual: `sheetId` is optional — see Closure.
8. **Real round-trip conformance suite** — ✅ mostly: `verify/conformance.py` gates on real workbooks (cells + structure); a **LibreOffice render diff** (PDF→PNG) was run as a visual ground-truth pass and caught two defects the openpyxl read-back can't see, now fixed: (a) font name/size were dropped for "default" Calibri/11, so exported cells had no explicit font and rendered **serif** in LibreOffice — now always emitted; (b) a literal string starting with `=` was misclassified as a formula — now keyed on `cell.data_type` with a `t:"s"` literal marker. **Open:** Univer-Facade-generated fixtures; computer-use visual check (LibreOffice computer-use was unavailable in the headless Codex run — the render-diff fallback was used).
9. **Worksheet structure** — ✅ done: sheet visibility, grouped column spans + exact widths, exact row heights, comments, hyperlinks, and images now round-trip; the conformance structural line measures them. (Residual: page-break position is still LibreOffice-render-sensitive near thresholds.)
10. **Operational** — ✅ done: `dist/` creation, one-arg `npm run import`, atomic `/save` + `/save-objects` + `response.ok`, pinned deps.

## Running it

```bash
npm run compile         # snapshot-to-xlsx.py … objects.json  (compile gate validates objects.json first)
npm run import -- x.xlsx # xlsx-to-snapshot.py — captures caches, DV, CF; reports charts/pivots/macros it can't rebuild
npm run verify          # read-back-check.py: diff dist/workbook.xlsx against snapshot + objects
npm run test:converter  # the converter self-test on the shipped sample (53 checks)
# closure gate on its own:
python3 converter/validate_objects.py objects.json workbook.snapshot.json
# measured round-trip fidelity against real workbooks (the gate for any converter change):
python3 verify/conformance.py --converter converter --min 0.9 path/to/*.xlsx
```

Extending a feature = extend the mapper *and* add a case to `converter/test.py`, **and confirm
`verify/conformance.py` doesn't regress on real workbooks**, before shipping. The measured table above must
always describe the code, not an aspiration. In lane 1, never hand-edit the compiled `.xlsx`; fix the
snapshot. In lane 2, never overwrite the authoritative file or call a lossy full converter save a merge.
