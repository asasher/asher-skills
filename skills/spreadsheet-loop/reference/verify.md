# Verify — is the .xlsx faithful?

The compile is only trustworthy if it's checked. Phase 6 confirms the produced `.xlsx` matches the browser
truth. Three layers, cheapest first; run as many as the machine allows.

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
cached result was stale — refresh it before compiling. The verify harness ships in `templates/verify/`.

## 2. Read the .xlsx back and diff

Run `python3 verify/read-back-check.py dist/workbook.xlsx workbook.snapshot.json objects.json` — it opens the
compiled `.xlsx` with `openpyxl` and asserts the committed feature set survived: values and formulas present,
number formats intact, merges and freeze in place, named ranges defined, and **each declared chart and pivot
materialized**. This catches converter regressions directly. It also complements the converter's own
`converter/test.py` (the 19-check self-test on the shipped sample). Allow the documented ±1px sizing rounding.

## 3. Drive a real spreadsheet app (where possible)

The strongest check is opening the file in a real client. If the environment has LibreOffice headless, use it
to convert or re-read the file (`libreoffice --headless --convert-to ...`) and confirm it opens without
repair prompts and formulas evaluate. If computer-use / a screenshot surface is available, open the `.xlsx`
and visually diff against the browser rendering.

> Note: on this machine, headless-Chrome screenshotting has been unreliable (SIGKILL). Prefer a
> LibreOffice re-read or a DOM/value transcript over a browser screenshot for visual evidence, unless the
> environment has changed.

## Reporting a gap

A fidelity gap is one of two things — say which:

- **A converter bug** — a mapping that should work but doesn't. Fix the mapper, add a case to its test, re-run.
- **An out-of-scope feature** — the workbook used something the fence excludes (a chart, a pivot, a
  colour-scale rule). This is expected: report it, and resolve per intake's options (drop, hand-finish in
  Excel, or extend the converter deliberately with a new test).

Never report "looks fine" without having run at least layers 1 and 2. Faithful-by-construction is the design;
verification is how you prove the construction held.
