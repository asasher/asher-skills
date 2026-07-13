---
name: review-opportunities
description: Audit the commercial Opportunity portfolio and return a read-only action report.
disable-model-invocation: true
metadata:
  invocation: user
  execution: thread
  requires: [manage-opportunities]
  optional: []
---

# Review Opportunities

Run an explicit, report-only portfolio audit. Read Opportunity shape and lifecycle through the required
`manage-opportunities` sibling, then apply [review contract](reference/review-contract.md). Do not create,
edit, move, close, promote, or repair any record, task, map, or file during this run.

## Commands

- **review** (default) - audit all Opportunity notes.
- **review `<name>`** - audit one Opportunity while retaining portfolio link/map checks.

Return findings ordered by severity, then a compact portfolio table and explicit `not checked` items. Each
finding names the Opportunity, evidence location, failed rule, and proposed owner/action. Missing commercial
data remains missing; never fabricate a value, probability, contact, date, reason, or gate artifact.

Completion criterion: every selected Opportunity has a result for every review category, all claims cite a
workspace record or path check, and the workspace is byte-for-byte unchanged.

## Dependency surface

- **Bundled reference:** report categories, severity, and output contract.
- **Project playbook:** `docs/agents/opportunities.md` through `manage-opportunities` for map/stale bindings.
- **Sibling skills:** required `manage-opportunities`, invoked by name for Opportunity schema and validation.
