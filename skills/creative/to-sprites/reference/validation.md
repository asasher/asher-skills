# Validation

`--validate` turns extraction into a pass/fail command. It is structural QA for a flat-key sprite sheet, not
a visual taste check.

## Checks

- **Asset count** — with `--expect N`, the manifest must contain exactly `N` elements. Without `--expect`,
  extraction must produce at least one element.
- **Empty cells** — grid cells whose keyed alpha is fully transparent are reported and fail validation.
- **Alpha corners** — every exported asset's four corner pixels must have alpha `0`, proving the flat
  background was removed and trimming left transparent corners.
- **Key remnants** — opaque pixels whose RGB is still within the key tolerance are reported as likely leftover
  background.

Any failed check exits nonzero from the CLI and raises `ValidationError` from the importable API.

## Common Fixes

- Wrong count: check `--cols`, `--rows`, `--tile`, `--margin`, and `--spacing`; for packed sheets, switch to
  `--slice components`.
- Empty cells: regenerate with one isolated subject per grid cell, or lower the expected count if blanks are
  intentional and validation is not required.
- Alpha corners fail: use `--key auto` only when the border is entirely the key color; otherwise pass
  `--key #RRGGBB`.
- Key remnants: widen the ramp with a higher `--key-hi`, or regenerate on a key color that is not present in
  the subject.
