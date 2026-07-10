# Workbook lanes, component decomposition, and merge-back

Choose the lane before building. An import that renders is not proof that a full re-export is safe.

## 1. Capability preflight

For an existing workbook, inventory the raw package and the workbook model before importing. Record counts
and locations for:

- sheets, used ranges, formulas, defined names, tables, validation, and conditional formatting;
- charts, pivots, slicers, images, drawings, comments, hyperlinks, and hidden/grouped structure;
- VBA, external links, connections, Power Query/data model parts, signatures, and unknown extensions;
- formula errors, repair prompts, excessive used ranges, and calculation mode.

Classify every detected feature:

| Class | Meaning | Action |
|---|---|---|
| **Browser-safe** | Import, edit, and export are covered by a tested symmetric mapping | May enter lane 1 or 2 |
| **Declared** | Supported only through an explicit sidecar declaration, such as a chart or flattened pivot | Review declaration and fidelity tier |
| **Preserve-only** | The browser cannot reconstruct it, but a merge may leave it untouched | Original remains authoritative |
| **Excel-native** | The requested change requires Excel runtime or an unsafe structural mutation | Route the operation outside the browser |

Write the result into `SPEC.md`. Do not hide a long list behind “some features may be lost.” Name the feature,
location, lane, and consequence.

## 2. Lane decision

### Lane 1 — browser-native build

Use for greenfield workbooks or inputs whose entire required feature set is browser-safe/declared. The
snapshot and `objects.json` are authoritative. Compile a new `.xlsx`; never imply preservation of an
unrelated source package.

### Lane 2 — scoped browser + merge

Use when an existing workbook is authoritative and the requested edits can be isolated from preserve-only
features. Import a **working copy or selected components**, never overwrite the source. The browser produces a
reviewed changeset; a merge adapter applies it to another copy of the source.

### Lane 3 — Excel-native

Use when the edit touches VBA, external connections, unsupported native objects, signatures, calculation
behaviour, or a structure the available merge adapter cannot preserve. Work through file-native tooling or
Excel Computer Use. Browser artifacts may still specify or prototype the change.

## 3. Component decomposition

Write `COMPONENTS.md` before loading a complex model into Univer. A component is a coherent unit such as
Inputs, Revenue, Staffing, Cost, Summary, Reporting, or Integrations. It may own a whole sheet or bounded
ranges across sheets.

Each component contract states:

- owned sheets/ranges and cells users may edit;
- inputs, outputs, named ranges, and formulas it owns;
- upstream and downstream dependencies;
- read-only fixtures or interfaces used while isolated;
- browser lane and preserve-only neighbours;
- assertions: totals, balance checks, expected formula-error count, and reconciliations;
- merge operations allowed: values, formulas, styles, validation, names, rows/columns, or declared objects.

Prefer a focused workbench. Do not import 77 sheets merely because the source contains 77 sheets. If a
component needs a dependency, expose the narrow output range or named-range interface it consumes.

## 4. Review artifact

Render `SPEC.md`, `MODEL.md`, `LAYOUT.md`, and `COMPONENTS.md` to self-contained HTML with stable section ids.
Present through `review-loop`. The review must make these decisions visible:

- authoritative file and chosen lane;
- browser-safe, preserve-only, and Excel-native feature table;
- component map and dependency edges;
- exact scope of changes and out-of-scope objects;
- merge method, fallback, assertions, and final verification.

Approval binds the scope. Expanding a component boundary or changing lanes requires another review.

## 5. Changeset contract

For lane 2, record browser work as a machine-readable changeset rather than treating the snapshot as a
replacement workbook. A changeset should contain:

```jsonc
{
  "source": { "path": "model.xlsm", "sha256": "..." },
  "component": "Revenue",
  "operations": [
    { "op": "set_formula", "sheet": "Revenue", "cell": "D12", "value": "=B12*C12" },
    { "op": "set_style", "sheet": "Revenue", "range": "D12:D20", "style": "currency" }
  ],
  "assertions": [
    { "kind": "formula", "sheet": "Revenue", "cell": "D21", "equals": "=SUM(D12:D20)" }
  ],
  "preserve": ["vba", "externalLinks", "nativeCharts"]
}
```

Use stable sheet ids when the source exposes them; include names for review. Reject stale source hashes and
operations outside the approved component. Structural operations need explicit approval because inserting a
row can affect tables, shared formulas, drawings, print areas, and external references.

## 6. Merge-back rules

Merge into a new output file; never mutate the authoritative source in place.

1. Verify the source hash and capability inventory have not changed.
2. Validate every operation against the component contract and adapter capabilities.
3. Apply only declared operations. Preserve untouched package parts and relationships.
4. Refuse an operation when the adapter would force a lossy full-library re-save of preserve-only content.
5. Reopen the output, run component assertions, compare package inventories, and inspect in real Excel.

`openpyxl(keep_vba=True)` is not by itself a preservation guarantee: unsupported extensions may still be
dropped. Prefer a surgical OOXML patcher or Excel-native automation when the preservation inventory demands
it. Until such an adapter exists, stop at the changeset and hand off; do not label a full converter export as
a merge.

## 7. Report

Report three outcomes separately:

- **Browser result:** what rendered and passed component assertions.
- **Merge result:** what operations were applied and what original features were preserved.
- **Outside-lane work:** what still requires Excel or a human.

This separation is the product promise: useful browser work without pretending unsupported Excel features
disappeared safely.
