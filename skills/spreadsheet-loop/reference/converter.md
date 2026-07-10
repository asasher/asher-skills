# The converter — snapshot (+ objects) ↔ .xlsx

The converter is the **compile step** and the authority on what survives the trip to Excel. It lives in the
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

## Two source files

The source of truth is two files, because a couple of objects live outside Univer's native model:

- **`workbook.snapshot.json`** — Univer-native: cells, formulas, styles, merges, sizing, freeze, named
  ranges, list validation, conditional formatting. Edited live in the browser; autosaved by the app.
- **`objects.json`** — **declared objects**: charts and pivots (things Univer OSS can't natively hold or
  export). Authored by the agent from the model/layout decisions, previewed in the browser, never touched by
  Univer's save. See [model-vs-layout](model-vs-layout.md) and [the-loop](the-loop.md) for the discipline
  that keeps this symmetric.

## Status: BETA — hardened against real workbooks, with named residual gaps

> **Measured 2026-07-10 against real financial workbooks** (`Revenue.xlsx`, `PS v0.8.xlsx`, a 77-sheet `.xlsm`),
> before → after a hardening pass. On the two Revenue/PS workbooks the conformance harness
> (`verify/conformance.py`) now reports **100% preservation of values, formula text, cached results, number
> formats, resolved styles, merges, named ranges, data validation, and conditional formatting** — up from
> ~16% and total DV/CF loss. The 77-sheet macro `.xlsm` imports and re-exports without crashing (charts/macros
> detected, not reconstructed — by design). **This is good, but not "authoritative-file" trust:** verify
> against real Excel before distributing, and see the residual gaps below.
>
> A **LibreOffice render diff** (2026-07-10) confirmed page-1 of `Revenue.xlsx` round-trips as a visual match
> (after fixing a font-fallback and a literal-`=` defect it caught). Residual gaps (still open): colour tint is
> a linear approximation (not pixel-verified against Excel); macros/charts in an imported file are
> detected-and-reported, not reconstructed; page-break position stays render-sensitive near thresholds; and
> the visual pass used a headless render, not interactive Excel. Backlog #8 tracks these.

## Feature set & measured real-workbook status

`snapshot (+ objects) → .xlsx`. Self-test 32/32 on the sample; the "measured" column is the conformance
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
| Comments, hyperlinks, images, sheet visibility, grouped column spans | — | — | ❌ not modeled (backlog #9) |

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
numbers. Either way the browser preview and the export agree on the values.

## Import — and fail-safe detection of what it can't recover

`xlsx-to-snapshot.py` recovers literal values, dates, formula text, styles (RGB colours only), merges, sizing,
freeze, named ranges (workbook scope only), and conditional formatting (`colorScale` / `cellIs`). A raw-package
**preflight** runs *first* and reports charts, pivots, macros, images, and external links it cannot
reconstruct — writing them into `objects.json` and to stderr **before** any crash-prone work, so detection is
fail-safe. Writes are atomic (temp + rename), so a mid-import failure can't leave a truncated, plausible file.

Known import gaps (see backlog): **data validation is not read at all** (export-only today), CF differential
fonts and thresholds are dropped, theme/indexed colours collapse, and cached formula results, comments,
hyperlinks, sheet visibility, and images are not modeled.

## Closure — the invariant, and where it currently leaks

The *goal* is browser-renders ⟺ exporter-writes ⟺ importer-reads = the **same set**. The cell spine holds.
But the 2026-07-10 review showed the invariant is **not yet enforced in code**, and leaks in real ways:
- **Detection ≠ closure.** The import "note" is advisory — `compile` ignores it and will happily emit a
  chart-free `.xlsx`. There is no gate that blocks compile on unresolved gaps.
- **No schema for `objects.json`**; unknown chart types silently become bar charts; objects reference sheets
  by *mutable name*, so a browser rename staleness the sidecar.
- **Interactivity gap**: a Tier-A pivot is a static table, not a draggable pivot.

Most of these are now closed (a JSON schema + validator + compile gate exist, and the browser registers the
DV/CF presets and renders real chart/pivot previews). What remains is stable-ID references (objects still key
on mutable sheet names) and the structure items in #9.

## Hardening backlog (from the 2026-07-10 gpt-5.6 review + real-workbook round-trip)

1. **Type-safety + atomicity** — ✅ done: dates/times/array-formulas serialize; `default=str` net; atomic writes; fail-safe preflight incl. macros.
2. **Theme/indexed colour model** — ✅ done (`xlsx_theme.py`): theme+indexed colours resolve to RGB with tint; explicit black kept. Fonts/fills 16%→100% on Revenue. Tint = linear approx (not pixel-verified).
3. **Cached formula values** — ✅ done: import loads `data_only=True`; export injects `<v>` post-save. Cached-lost → 0.
4. **Data-validation import parity** — ✅ done: import emits the DV resource; inline lists quoted, range/named refs passed through; all DV types.
5. **Conditional-formatting fidelity** — ✅ done: CFVO types/values, priority, `stopIfTrue`, differential fonts preserved both ways.
6. **Charts/pivots/names** — ✅ done: cross-sheet chart refs resolve to their own sheet; pivots do rows×cols with sum/count/avg/min/max and reuse an existing sheet; defined-name scope preserved.
7. **Closure enforcement** — ✅ mostly: `objects.schema.json` + stdlib `validate_objects.py` + compile gate (fails on invalid declared objects, warns on unresolved import gaps) + manifest hashes. **Open:** stable sheet-ID references instead of mutable names.
8. **Real round-trip conformance suite** — ✅ mostly: `verify/conformance.py` gates on real workbooks (cells + structure); a **LibreOffice render diff** (PDF→PNG) was run as a visual ground-truth pass and caught two defects the openpyxl read-back can't see, now fixed: (a) font name/size were dropped for "default" Calibri/11, so exported cells had no explicit font and rendered **serif** in LibreOffice — now always emitted; (b) a literal string starting with `=` was misclassified as a formula — now keyed on `cell.data_type` with a `t:"s"` literal marker. **Open:** Univer-Facade-generated fixtures; computer-use visual check (LibreOffice computer-use was unavailable in the headless Codex run — the render-diff fallback was used).
9. **Worksheet structure** — ✅ done: sheet visibility, grouped column spans + exact widths, exact row heights, comments, hyperlinks, and images now round-trip; the conformance structural line measures them. (Residual: page-break position is still LibreOffice-render-sensitive near thresholds.)
10. **Operational** — ✅ done: `dist/` creation, one-arg `npm run import`, atomic `/save` + `/save-objects` + `response.ok`, pinned deps.

## Running it

```bash
npm run compile         # snapshot-to-xlsx.py … objects.json  (compile gate validates objects.json first)
npm run import -- x.xlsx # xlsx-to-snapshot.py — captures caches, DV, CF; reports charts/pivots/macros it can't rebuild
npm run verify          # read-back-check.py: diff dist/workbook.xlsx against snapshot + objects
npm run test:converter  # the converter self-test on the shipped sample (32 checks)
# closure gate on its own:
python3 converter/validate_objects.py objects.json workbook.snapshot.json
# measured round-trip fidelity against real workbooks (the gate for any converter change):
python3 verify/conformance.py --converter converter --min 0.9 path/to/*.xlsx
```

Extending a feature = extend the mapper *and* add a case to `converter/test.py`, **and confirm
`verify/conformance.py` doesn't regress on real workbooks**, before shipping. The measured table above must
always describe the code, not an aspiration. Never hand-edit the `.xlsx`: the snapshot + objects are the
source of truth and the next compile overwrites it.
