# Review Contract

Read the Opportunity contract and project `docs/agents/opportunities.md` through `manage-opportunities`. Take
a before-state of candidate files when practical so report-only behavior can be verified.

## Categories

For each selected Opportunity, report:

1. **Shape** - required identity fields, allowed stage, body sections, field types, and structural validator
   result.
2. **Next action** - active pursuits have exactly one unblocked designated task ID; it resolves once in that
   Opportunity backlog or its `TODO.md` heading; due/plan dates and blockers are visible.
3. **Freshness** - latest material event and next-action date compared with the project-bound stale threshold.
   If no threshold is bound, report freshness as not checked rather than inventing one.
4. **Stage evidence** - recorded evidence satisfies the current stage gate; file existence alone is not proof
   of sending, discussion, acceptance, or outcome.
5. **Commercial completeness** - unknown contacts, value, currency, recurring value, probability, assumptions,
   or close reason are flagged only where relevant. Missing values are never estimated.
6. **Paths and artifacts** - `workspacePath` resolves when present and important body links resolve. It is not
   interpreted as repository-triage authority.
7. **Terminal integrity** - closed-won has an outcome date and linked reciprocal Projects or an explicit
   no-delivery reason; closed-lost and dormant satisfy their required fields.
8. **Maps** - configured Company, Customer, People, and Project relationships are current and bidirectional.

## Severity

- **Critical** - false `closed-won`, broken promotion integrity, or task duplication that makes the active
  commitment ambiguous.
- **High** - active pursuit has no valid next action, stage gate lacks evidence, or required identity is absent.
- **Medium** - stale pursuit, broken path/link, missing relevant commercial data, or one-way map.
- **Low** - optional hygiene that does not obscure state or action.

## Output

Lead with findings grouped by severity. Then include one row per Opportunity: stage, owner, next-action ID,
freshness, gate status, and finding count. End with checks that could not run and why. Propose mutations as a
separate follow-up through `manage-opportunities`; never perform them inside review.

Completion criterion: all eight categories have evidence-backed status for every record and a post-run diff
confirms no workspace mutation.
