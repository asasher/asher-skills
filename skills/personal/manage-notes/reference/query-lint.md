# Query and Lint

## Query

1. Search `Notes/`, `Projects/`, `Opportunities/`, `Companies/`, `Customers/`, and `People/` as relevant before
   answering.
2. Cite each workspace-derived claim with a `[[wikilink]]`. Label inference and say when the workspace cannot
   answer.
3. Treat Opportunity commercial fields and stage as recorded facts only. Invoke `manage-opportunities` for a
   mutation; Query itself is read-only.
4. Offer to ingest a non-trivial durable answer only when filing it would add knowledge rather than duplicate
   an existing note.

## Lint

Report findings first; fix only what the user confirms. Check:

- contradictions and claims no longer supported by their source;
- stale dated material;
- orphan notes, body-linkless notes, and notes unreachable from a hub within two hops;
- working documents misfiled in `Notes/`;
- broken wikilinks and one-way entity relationships;
- duplicate notes covering one idea;
- Note Shape failures.

Include `Opportunities/` in link, reachability, stale-reference, and relationship checks. Opportunity schema,
stage gates, next actions, and promotion integrity belong to `manage-opportunities`: invoke that sibling by name
for those checks. If it is unavailable, report Opportunity shape as `not checked (manage-opportunities absent)`;
do not restate or approximate its schema.

Completion criterion: every category has a pass/finding/not-checked result and the run made no unconfirmed edit.
