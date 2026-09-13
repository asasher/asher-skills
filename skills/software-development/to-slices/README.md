# To-Slices

Splits one ticket's approved spec into ready tracer-bullet GitHub issues with native blocking edges. Read the source at its approved hash, draft vertical slices, and obtain approval of the concrete split. Prior approval counts when it covers that exact revision and plan. Changed direction needs a revised approved spec.

Create or reconcile unreleased issues in dependency order, wire and read back the complete graph, then release the held tickets. The parent retains the approved draft and issue mapping for recovery. Each child is a sub-issue and blocker of the `spec` parent, whose work branch is their integration base.

## When to use

At the close of shaping, or on an existing ticket with an approved published spec. Documents, plans, and conversations first need that ticket and approval. Use `to-spec` to write direction and `capture` to establish a ticket.

## Layout

`SKILL.md` is the command surface and points into `reference/`: `slicing.md` (the split method) and `template-guide.md` (the issue contract and the split draft).

## Credits

- **Relationship:** adapted.
- **Source:** Matt Pocock's MIT-licensed [`to-tickets`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/to-tickets/SKILL.md).
- **Borrowed:** vertical slicing, granularity interview, dependency ordering, and approval-before-publish.
- **Local changes:** GitHub-native issues, sub-issues, and blocking edges; the wide-refactor lane; the justified-recommendation posture; the stacked landing on the spec branch; `spec` parentage over slices; the rename to `to-slices`.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
