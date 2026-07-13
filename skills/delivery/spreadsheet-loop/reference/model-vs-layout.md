# Model vs. layout — the separation doctrine

The whole reason this skill is faster than editing Excel is that it lets a human and an agent reason about a
workbook through **two artifacts that are deliberately kept apart**. Conflating them is the failure mode that
makes spreadsheets unmaintainable — a formula change tangled up with a formatting change, a data model you
can only infer by clicking through cells.

- **`MODEL.md` — what the workbook *means*.** The data model, in prose plus a small machine-readable block.
- **`LAYOUT.md` — what the workbook *looks like*.** The visual language.
- **`COMPONENTS.md` — how the workbook is divided.** Ownership, dependencies, lane, assertions, and merge
  boundaries for each coherent part of the model.

Both **govern** the snapshot; neither *is* the snapshot. The snapshot is the compiled concretion of the two.
You should be able to change the model without re-deciding the look, and restyle the layout without touching
a formula.

## `MODEL.md` — the data model

Write it so a reader understands the workbook's logic without opening a single cell. Sections:

- **Entities & grain.** What each sheet represents and at what grain (one row per product? per month? per
  scenario?).
- **Inputs vs. computed.** The bright line. Inputs are the cells a human types; computed cells are formulas
  derived from inputs. Every cell is one or the other — say which, and never let a computed cell be silently
  overtyped.
- **Named ranges.** The workbook's vocabulary. Give the human-meaningful cells names (`TotalRevenue`,
  `TaxRate`) rather than referring to `D5`. Named ranges are the relationships that must survive to Excel —
  the converter maps them to real Excel defined names.
- **Formula logic.** The derivations, in words and as the canonical formula. `Revenue = Units × UnitPrice`;
  `Total = SUM(per-product revenue)`. Describe the *relationship*, so the formula can be regenerated if the
  layout moves.
- **Units & validation.** Currencies, percentages, allowed value sets (which become data-validation
  dropdowns), sanity bounds.

End `MODEL.md` with a **named-range registry** — a small fenced block the converter and the loop can read as
the source of truth for the workbook's vocabulary:

```yaml
# named ranges: name -> meaning (cell ref is assigned during layout, not here)
inputs:
  TaxRate:       "sales tax applied to line totals"
  WidgetUnits:   "units of Widget sold this quarter"
computed:
  TotalRevenue:  "SUM of per-product revenue"
```

The registry names *what exists and whether it's an input*; the **cell address** for each name is a layout
decision, assigned in `LAYOUT.md` and realized in the snapshot. That is the seam between the two documents.

## `LAYOUT.md` — the visual language

Write it so a reader can picture the workbook. Sections:

- **Sheet structure.** The sheets, their order, and what occupies each region (title band, input block,
  calculation area, output/summary).
- **Placement.** Where each named range from the model lands (`TaxRate` → `Assumptions!B2`). This is where the
  model's vocabulary gets addresses.
- **Header & section treatment.** Title rows, header rows, merges, freeze panes.
- **Number formats.** Currency, percent, thousands, dates — per column or per named range.
- **Colour & border conventions.** The *system*, not one-off styling: e.g. inputs on a green fill, computed
  cells plain, totals bold on a highlight fill, section headers on the brand blue. A convention a reader can
  restate is worth more than a screenshot.
- **Conditional emphasis.** Where highlight-cell rules draw the eye (a total over threshold turns green).

## `COMPONENTS.md` — the construction map

Define coherent components before implementation. For each, record owned sheets/ranges, input/output named
ranges, dependencies, editable cells, assertions, chosen lane, preserve-only neighbours, and permitted merge
operations. A component may be smaller than a sheet or span several sheets. The purpose is bounded reasoning:
load and review the part being changed, not the entire workbook by default. Use the shipped template and
[lanes-and-merge](lanes-and-merge.md).

## Charts & pivots are declared objects — split across both documents

A chart and a pivot are the two objects that live outside the cell grid, in `objects.json`
([snapshot-model](snapshot-model.md)). They still obey the separation — each is split across the two documents
along the same meaning/appearance line:

- **A pivot is mostly a model decision.** *What* it summarizes — its source range, the row/column fields, the
  aggregated value — is data-model logic, so it's specified in `MODEL.md`. Only its placement (which sheet,
  which anchor) is layout.
- **A chart is mostly a layout decision.** *What* it plots is just a reference to model data (a range); its
  type, title, and placement are visual language, so it's specified in `LAYOUT.md`.

Record each in the relevant document in prose, and keep the machine-readable declaration in `objects.json`.
The browser shows a **preview** of the declaration and the converter materializes it — so a declared object is
never something the browser can show but the export can't write. Note the one honest caveat in `LAYOUT.md` if
it applies: a default pivot compiles to a faithful *static* table, not a draggable Excel pivot (interactivity
is the LibreOffice tier — see [converter](converter.md)).

## The rule

- A change that alters **meaning** (a new input, a changed derivation, a new named range, a pivot's fields) is
  a `MODEL.md` change first, then the snapshot / `objects.json`.
- A change that alters **appearance** (a colour, a format, a merge, placement, a chart's type) is a
  `LAYOUT.md` change first, then the snapshot / `objects.json`.
- If a proposed change needs edits to *both* documents, that is a signal to slow down and confirm with the
  human — it usually means a genuine redesign, not a tweak.
- If a change crosses a component or merge boundary, update `COMPONENTS.md` and re-run the review gate before
  editing.

Keeping the two apart is not bureaucracy; it is what makes the loop fast and the export trustworthy.
