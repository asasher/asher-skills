<!-- MODEL.md skeleton — the DATA MODEL: what the workbook means. See reference/model-vs-layout.md.
     Keep this apart from LAYOUT.md. This governs the snapshot; it is not the snapshot. -->

# <Workbook name> — Model

## Entities & grain
<!-- What each sheet represents and at what grain (one row per product / month / scenario). -->

## Inputs vs. computed
<!-- The bright line. List the input cells a human types, and the computed cells derived from them.
     Every cell is one or the other. Never let a computed cell be silently overtyped. -->

- **Inputs:**
- **Computed:**

## Formula logic
<!-- Each derivation as a relationship AND its canonical formula, so it survives a layout move.
     e.g. Revenue = Units × UnitPrice ; Total = SUM(per-product revenue) -->

## Units & validation
<!-- Currencies, percentages, allowed value sets (become data-validation dropdowns), sanity bounds. -->

## Named-range registry
<!-- The workbook's vocabulary. Names + meaning; cell addresses are assigned in LAYOUT.md, not here.
     The converter maps these to real Excel defined names. -->

```yaml
inputs:
  # Name: "meaning"
computed:
  # Name: "meaning"
```
