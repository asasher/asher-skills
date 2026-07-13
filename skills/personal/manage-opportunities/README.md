# Manage Opportunities

Owns commercial Opportunity records from intake through event logging, stage changes, next-action designation,
closure, and promotion into delivery Projects. Opportunities retain commercial history; Projects own delivery
and repository triage.

The compact command surface is in `SKILL.md`. `reference/opportunity-contract.md` owns schema and gates,
`reference/lifecycle.md` owns routine mutations, and `reference/promotion.md` owns the closed-won transaction.
`scripts/validate_opportunities.py` provides stdlib structural checks and accepts either a workspace root or
its `Opportunities/` directory.

## Source

Derived from the Opportunity Control Plane handoff in `asher-workspace` and integrated with the installed
`manage-tasks` contract. This is an original portable rewrite.
