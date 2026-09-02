# Merge

The human authorization gate. Every build ends at a review-ready PR; nothing merges until the user asks, and invoking this skill is that ask. Merges in dependency order, re-checks CI on the head immediately before each merge, closes a child issue when its PR lands on the spec branch, resolves conflicts by documented intent, and tears down the working copy, the work branch, and the closed issue's artifact branch.

## Provenance

Formerly `merge-change`; the check-watching cadence rule was folded in from the retired `watch-until` skill. No external sources.
