# Merge

`merge review` reads all open PRs and suggests a merge order. Only the human's named selections authorize merging. Current verification, evidence, independent review, and required CI gate each merge. Confirm the merge and ticket closure before removing disposable worktrees and finished branches; retain active, dependent, or unmerged work. Published HTML and evidence remain available.

## Provenance

Formerly `merge-change`; the check-watching cadence rule was folded in from the retired `watch-until` skill.

Conflict-resolution guidance is informed by Matt Pocock's [resolving-merge-conflicts](https://github.com/mattpocock/skills/blob/3cca18b368ae95cdbdebbff572ccafa662551015/skills/engineering/resolving-merge-conflicts/SKILL.md), reviewed at commit `3cca18b368ae95cdbdebbff572ccafa662551015`. Rewritten here to use approved tickets and specs, check behavioral interactions even when Git merges cleanly, and stop for a ruling when approved requirements cannot settle the resolution.
