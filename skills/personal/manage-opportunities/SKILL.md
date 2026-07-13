---
name: manage-opportunities
description: Track commercial opportunities in a workspace. Use when a lead or pursuit is created or queried, receives a material interaction or deliverable, changes stage or designated follow-up, is won, lost, or dormant, creates a delivery Project, or when another skill needs the Opportunity Note Shape.
metadata:
  invocation: model
  execution: thread
  requires: [manage-tasks]
  optional: []
  setup: reference/setup.md
---

# Manage Opportunities

Own the Opportunity Note Shape and every material Opportunity mutation. Load [Opportunity contract](reference/opportunity-contract.md)
for schema and stage gates, then the reference for the selected command. `manage-tasks` remains authoritative
for task vocabulary, movement, and Project Note Shape.

## Commands

| Command | Result | Reference |
|---|---|---|
| `create` / `intake` | Create one evidence-backed pursuit | [lifecycle](reference/lifecycle.md) |
| `log event` | Append a material interaction, deliverable, or outcome | [lifecycle](reference/lifecycle.md) |
| `change stage` | Apply one evidence gate and stage transition | [lifecycle](reference/lifecycle.md) |
| `next action` | Designate exactly one task ID | [lifecycle](reference/lifecycle.md) |
| `close` | Close lost or dormant, or record a no-delivery win | [lifecycle](reference/lifecycle.md) |
| `promote` | Create and validate delivery Project links before winning | [promotion](reference/promotion.md) |
| `query` | Answer from Opportunity records without mutation | [query](reference/query.md) |
| `setup` | Create or reconcile workspace bindings | [setup](reference/setup.md) |

Infer the command from an unambiguous request; otherwise ask which material mutation is intended. Never infer
stage movement from artifact existence alone, and never invent missing value, probability, dates, contacts,
or evidence.

## Invariants

- An Opportunity remains the commercial history after a win; delivery lives in linked Projects.
- `nextAction` is one task ID whose task exists exactly once in the Opportunity backlog or active `TODO.md`.
- `workspacePath` may point to pursuit artifacts. It is never repository-triage authority; only a Project
  `localPath` is.
- Company, Customer, Opportunity, and Project maps are explicit and bidirectional.
- For a delivery win, `stage: closed-won` is the final write after Project creation, reciprocal links, path
  ownership, task movement, and validation all succeed.

Run `python3 scripts/validate_opportunities.py <workspace-root-or-Opportunities-dir>` after structural
mutations. A validator failure leaves the operation incomplete and must not be hidden by a stage update.

## Dependency surface

- **Bundled references:** schema, lifecycle, promotion, query, and setup contracts; stdlib validator.
- **Project playbook:** optional `docs/agents/opportunities.md`, created or reconciled by setup, binds workspace
  paths, maps, and local policy.
- **Sibling skills:** required `manage-tasks`, invoked by name for task movement and Project Note Shape.
