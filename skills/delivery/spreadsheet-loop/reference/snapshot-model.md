# The snapshot model — `IWorkbookData` (+ `objects.json`)

In lane 1 the source of truth is two files: the **Univer snapshot** (`workbook.snapshot.json`, the
`IWorkbookData` below) for everything Univer renders natively, and **`objects.json`** for declared charts and
pivots. The [converter](converter.md) compiles both to `.xlsx`. In lane 2 these files are an isolated
workbench; the authoritative Excel source and reviewed changeset govern the final merge. This reference
documents the subset the skill relies on — enough to read a snapshot, hand-edit one,
or reason about what the converter maps. The authority for anything beyond this is Univer's own docs
(`docs.univer.ai`) and `reference.univer.ai`.

The snapshot is persisted as `workbook.snapshot.json` and produced by the Facade API's `fWorkbook.save()`
(preferred over the deprecated `getSnapshot()`), which also folds in plugin resources (conditional
formatting, data validation, defined names).

## Top-level shape

```jsonc
{
  "id": "book-…",
  "name": "Q3 Model",
  "appVersion": "0.10.2",
  "locale": "enUS",
  "sheetOrder": ["sheet-rev"],          // render/tab order, by sheet id
  "styles": { "currency": { /* IStyleData */ } },  // workbook style table; cells reference by id
  "sheets": { "sheet-rev": { /* IWorksheetData */ } },
  "resources": [ { "name": "…_PLUGIN", "data": "<json string>" } ]  // plugin state (see below)
}
```

## `IWorksheetData`

```jsonc
{
  "id": "sheet-rev",
  "name": "Revenue",                    // becomes the Excel tab name
  "rowCount": 50, "columnCount": 8,
  "freeze": { "xSplit": 0, "ySplit": 2, "startRow": 2, "startColumn": 0 },
  "columnData": { "0": { "w": 180 }, "1": { "w": 110, "hd": 1 } },  // w = px, hd = hidden
  "rowData":    { "0": { "h": 28 } },                                // h = px
  "mergeData":  [ { "startRow": 0, "endRow": 0, "startColumn": 0, "endColumn": 3 } ],
  "cellData":   { "0": { "0": { /* ICellData */ } } }               // sparse: cellData[row][col]
}
```

`cellData` is a **sparse row→col→cell matrix**, 0-indexed. Absent rows/cols are empty.

## `ICellData`

```jsonc
{
  "v": 1198.8,          // origin value (string | number | boolean)
  "f": "=B3*C3",        // raw formula string, leading '='; when present, v holds the cached result
  "s": "currency",      // style: an id into workbook.styles, OR an inline IStyleData object
  "t": 2                // optional CellValueType (number/string/bool); usually inferable from v
}
```

A cell is a formula cell iff `f` is set. Keep `v` in sync as the cached result so tools that don't recompute
still show a value; the [verify](verify.md) step recomputes headlessly to confirm.

## `IStyleData` — the fields the converter maps

```jsonc
{
  "bl": 1, "it": 1, "ul": { "s": 1 }, "st": { "s": 1 },  // bold, italic, underline, strike
  "fs": 14, "ff": "Arial",                                 // font size, family
  "cl": { "rgb": "#FFFFFF" },                              // font colour
  "bg": { "rgb": "rgb(31,78,121)" },                       // fill (solid background)
  "bd": { "b": { "s": 1, "cl": { "rgb": "#000000" } } },   // borders per edge t/b/l/r; s = BorderStyleType
  "ht": 2, "vt": 2, "tb": 3,                                // h-align 1/2/3=L/C/R, v-align 1/2/3=T/M/B, tb 3=wrap
  "n": { "pattern": "$#,##0.00" }                          // number format (Excel pattern syntax)
}
```

Border style ids (`s`) follow Univer's `BorderStyleTypes`: `1` thin, `2` hair, `3` dotted, `4` dashed,
`7` double, `8` medium, `13` thick (full map in the converter). Colours may be `#RRGGBB` or `rgb(r,g,b)`.

## Plugin resources

Conditional formatting, data validation, and named ranges are **not** inline on cells — they live in the
top-level `resources` array, each a `{ name, data }` pair whose `data` is a JSON string keyed by sheet id (or,
for defined names, by definition id). The converter reads these by name:

- `SHEET_DEFINED_NAME_PLUGIN` — `{ "<id>": { "name": "TotalRevenue", "formulaOrRefString": "Revenue!$D$5" } }`
- `SHEET_DATA_VALIDATION_PLUGIN` — `{ "<sheetId>": [ { "type": "list", "formula1": "A,B,C", "ranges": [IRange] } ] }`
- `SHEET_CONDITIONAL_FORMATTING_PLUGIN` — `{ "<sheetId>": [ { "ranges": [IRange], "rule": { "type": "highlightCell", "operator": "greaterThan", "value": 1500, "style": { "bg": {…}, "cl": {…} } } } ] }`

An `IRange` is `{ startRow, endRow, startColumn, endColumn }`, all 0-indexed inclusive — the same shape as
`mergeData` entries.

When editing through the browser, you never hand-write these; the Facade builders produce them and
`save()` serializes them. Hand-edit the snapshot only for small surgical changes, and prefer round-tripping
through the running app for anything touching plugin resources.

## `objects.json` — declared charts & pivots

Charts and pivots don't live in the Univer snapshot (Univer OSS can't natively hold or export them). They are
**declared** in a sibling `objects.json`, authored by the agent from the model/layout decisions, previewed in
the browser, and materialized natively on compile. Univer's `save()` never touches this file, so a browser
edit can't wipe a declared object.

```jsonc
{
  "charts": [
    { "id": "chart-rev", "sheet": "Sales", "type": "bar",        // bar | line | pie
      "sheetId": "sheet-sales",                                    // optional stable id — survives renames
      "title": "Revenue by row",
      "categories": "Sales!B3:B6",                                 // A1 range for category labels
      "values": ["Sales!D3:D6"], "seriesTitles": ["Revenue"],
      "anchor": "F3" }                                             // top-left cell of the chart
  ],
  "pivots": [
    { "id": "pivot-region", "sheet": "Pivot by Region",           // sheet the pivot is written to
      "sheetId": "sheet-pivot",                                    // optional stable id — survives renames
      "source": "Sales!A2:D6",                                     // A1 range incl. header row
      "rows": ["Region"], "cols": [],                              // field names from the header row
      "values": [{ "field": "Revenue", "agg": "sum" }],           // agg: sum | count | avg | min | max
      "anchor": "A1" }
  ]
}
```

`sheetId` is the snapshot's stable sheet id; when present, the compile, validator, verify read-back, and
browser preview all resolve it before the display name, so a browser sheet rename cannot strand the
declaration. Declare it whenever the human can rename sheets.

A pivot's `source`, `rows`, and `values` are a **model** decision (what it summarizes); a chart's `type` and
`anchor` are a **layout** decision (how it looks) — see [model-vs-layout](model-vs-layout.md). The converter
reads this file alongside the snapshot; the [converter](converter.md) reference is the authority on how each
field maps and what fidelity tier a pivot gets.
