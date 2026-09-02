# To-Slices

Splits a decided direction into ready tracer-bullet GitHub issues with blocking edges, only on the user's explicit call. Its primary input is a spec'd issue (the spec read from the `artifact/<issue>` branch at the blessed hash); it also accepts a spec document, a plan document, or the raw current conversation. It drafts vertical slices and presents the split as a justified recommendation the user edits, then, on approval, publishes the issues in dependency order, blockers first. A split parent becomes the `spec` issue over its slices: each slice a sub-issue and a blocker, so the parent unblocks when the last child closes.

## When to use

- **At the close of shaping**: `shape` runs it inline when the approved spec recommends a split and the user says yes.
- **From a plan or a live conversation**: when no spec was written, split a plan or the current conversation the same way.

Not for writing the direction itself; that is `to-spec`. Not for loose capture; that is `capture`.

## Layout

`SKILL.md` is the command surface and points into `reference/`: `slicing.md` (the split method) and `template-guide.md` (the issue contract and the split draft).

## Credits

- **Relationship:** adapted.
- **Source:** Matt Pocock's MIT-licensed [`to-tickets`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/to-tickets/SKILL.md).
- **Borrowed:** vertical slicing, granularity interview, dependency ordering, and approval-before-publish.
- **Local changes:** GitHub-native issues, sub-issues, and blocking edges; the wide-refactor lane; the justified-recommendation posture; the stacked landing on the spec branch; `spec` parentage over slices; the rename to `to-slices`.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
