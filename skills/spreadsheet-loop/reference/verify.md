# Verify — is the .xlsx faithful?

Integration is only trustworthy if it is checked. Phase 6 confirms the browser result, exported/merged file,
and authoritative-file promise agree. Run the common layers, then the lane-specific checks.

## 1. Recompute formulas headlessly

Formulas carry a cached `v` in the snapshot, but a cached value can lie. Load the snapshot in Univer's
**Node core** (no browser) and recompute:

```js
import { createUniver, LocaleType } from '@univerjs/presets';
import { UniverSheetsNodeCorePreset } from '@univerjs/preset-sheets-node-core';
const { univerAPI } = createUniver({ locale: LocaleType.EN_US, presets: [UniverSheetsNodeCorePreset()] });
const fWorkbook = univerAPI.createWorkbook(snapshot);
const formula = univerAPI.getFormula();
formula.executeCalculation();
await formula.onCalculationResultApplied();
const recomputed = fWorkbook.save();
```

Compare each formula cell's recomputed value against the cached `v` in the snapshot. A mismatch means the
cached result was stale — refresh it before compiling. The verify harness ships in `templates/app/verify/`
(scaffolded into the project as `verify/`).

## 2. Read the .xlsx back and diff

Run `python3 verify/read-back-check.py dist/workbook.xlsx workbook.snapshot.json objects.json` — it opens the
compiled `.xlsx` with `openpyxl` and asserts the committed feature set survived: values and formulas present,
number formats intact, merges and freeze in place, named ranges defined, and **each declared chart and pivot
materialized** (declared objects resolve by stable `sheetId` first, then display name — the same order the
compile uses). This catches converter regressions directly. It also complements the converter's own
`converter/test.py` (the 53-check self-test on the shipped sample). Allow documented sizing rounding.

## 3. Drive a real spreadsheet app

The strongest check is opening the file in real Excel where Computer Use is available. Confirm it opens
without a repair prompt, inspect the changed component, and compare it with the browser screenshot. If only
LibreOffice headless is available, use it to convert or re-read the file and confirm it opens cleanly.

Use agent-browser/Chrome for the browser side and Computer Use for Excel; do not substitute one screenshot for
the other when claiming a merge preserved the authoritative file.

## 4. Lane-specific proof

- **Lane 1:** recompute, read back, compare declared objects, and visually compare browser ↔ Excel.
- **Lane 2:** also verify the source hash, changeset scope, component assertions, package-part inventory,
  preserve-only features, VBA/signature presence where applicable, external-link/chart/image counts, and no
  unapproved sheet/range changes. A structural OOXML diff is required for high-risk sources.
- **Lane 3:** verify the Excel-native operation and record which assertions were checked; do not claim browser
  round-trip fidelity.

## Reporting a gap

A fidelity gap is one of three things — say which:

- **A converter bug** — a mapping that should work but doesn't. Fix the mapper, add a case to its test, re-run.
- **An out-of-scope feature** — the workbook used something the fence excludes (a chart, a pivot, a
  colour-scale rule). This is expected: report it, and resolve per intake's options (drop, hand-finish in
  Excel, or extend the converter deliberately with a new test).
- **A merge/preservation bug** — a declared change escaped its component or an untouched source feature
  changed. Reject the output and return to the original source copy plus changeset.

Never report "looks fine" without having run at least layers 1 and 2. Faithful-by-construction is the design;
verification is how you prove the construction held.
