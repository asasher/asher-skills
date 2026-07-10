#!/usr/bin/env node
// recompute.mjs — verify layer 1: load the snapshot headlessly (Univer Node core, no browser),
// recompute all formulas, and report any cell whose cached `v` disagrees with the fresh result.
// A stale cache is a silent lie in the .xlsx — catch it before compiling.
// Usage: node verify/recompute.mjs <workbook.snapshot.json>
import { readFile } from 'node:fs/promises';
import { createUniver, LocaleType } from '@univerjs/presets';
import { UniverSheetsNodeCorePreset } from '@univerjs/preset-sheets-node-core';

const [, , snapshotPath] = process.argv;
if (!snapshotPath) { console.error('usage: recompute.mjs <snapshot.json>'); process.exit(2); }
const snapshot = JSON.parse(await readFile(snapshotPath, 'utf8'));

const { univerAPI } = createUniver({
  locale: LocaleType.EN_US,
  presets: [UniverSheetsNodeCorePreset()],
});
const fWorkbook = univerAPI.createWorkbook(snapshot);

const formula = univerAPI.getFormula();
formula.executeCalculation();
await formula.onCalculationResultApplied();
const recomputed = fWorkbook.save();

const stale = [];
const order = snapshot.sheetOrder || Object.keys(snapshot.sheets || {});
for (const sheetId of order) {
  const before = snapshot.sheets[sheetId]?.cellData || {};
  const after = recomputed.sheets[sheetId]?.cellData || {};
  for (const [r, row] of Object.entries(before)) {
    for (const [c, cell] of Object.entries(row)) {
      if (!cell?.f) continue;
      const fresh = after[r]?.[c]?.v;
      if (cell.v !== undefined && String(cell.v) !== String(fresh)) {
        stale.push(`${sheetId} r${r}c${c}: cached ${cell.v} -> recomputed ${fresh}  (${cell.f})`);
      }
    }
  }
}

if (stale.length) {
  console.error(`STALE — ${stale.length} formula cell(s) have an out-of-date cached value:`);
  for (const s of stale) console.error('  - ' + s);
  console.error('\nRe-save the snapshot from the browser (or persist `recomputed`) before compiling.');
  process.exit(1);
}
console.log('OK — all cached formula values match a fresh headless recompute');
