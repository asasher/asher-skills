# Manage Tasks

Owns workspace task identity, statuses, dependencies, exactly-one-location movement, Start Work / Stop Work,
and the Project Note Shape. Project and Opportunity tasks share the same movement contract while their note
schemas remain separately owned.

`SKILL.md` is the command surface. `reference/task-contract.md` owns task semantics and
`reference/project-note-shape.md` owns Project structure. Opportunity lifecycle work composes with the optional
`manage-opportunities` sibling by name.

## Source

Adapted from the installed `manage-tasks` workspace skill and the Opportunity Control Plane handoff in
`asher-workspace`; rewritten as a portable skill source with no workspace-specific commit policy.
