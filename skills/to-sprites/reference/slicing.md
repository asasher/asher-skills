# Slicing

`to-sprites` has two slicing modes. Both feed the same tail: keying, trimming, naming, export, manifest, and
validation.

## Grid

Use `--slice grid` for regular sheets: game tiles, icon grids, animation frames, or generated sheets whose
prompt specified a fixed row/column layout.

Provide either:

- `--cols N --rows N`, optionally with `--margin L,T` and `--spacing X,Y`; tile size is inferred from the
  sheet.
- `--tile WxH`, optionally with `--cols`/`--rows`; missing counts are inferred by fitting tiles from the
  margin with the given spacing.

Grid order is row-major. Empty fully transparent cells are skipped as assets and reported by `--validate`.
When names are supplied, the first name maps to row 0 col 0, the second to row 0 col 1, and so on.

## Components

Use `--slice components` for packed or gridless sheets where each sprite is an isolated opaque blob after
keying. The script keys the whole sheet, thresholds alpha, labels 4-connected regions with an in-house
two-pass union-find, boxes each region, and sorts boxes top-to-bottom then left-to-right into rows.

Components mode requires separation. Touching sprites merge into one component by design; if a sheet has a
regular layout, prefer grid mode.

## Trimming and Padding

Each element is trimmed to its alpha content. `--pad N` expands the exported frame inside the sheet bounds so
the asset keeps transparent breathing room. `trimmed_bounds` records the true content box; `sheet_rect` and
`frame` record the exported frame on the original sheet.
