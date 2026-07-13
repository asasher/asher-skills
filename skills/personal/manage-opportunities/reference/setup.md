# Setup - Opportunity workspace bindings

Reconcile `docs/agents/opportunities.md`; the project owns it after creation.

## First setup

1. Inspect the workspace structure and entity maps. Confirm or create `Opportunities/` only with the user's
   requested workspace change.
2. Create `docs/agents/opportunities.md` from `templates/opportunities.md`, replacing placeholders only with
   verified workspace-relative paths, map notes, stale policy, and local promotion constraints.
3. Do not migrate Projects or create Opportunity records during setup. Report those as separate intake work.

## Reconcile

1. Read the existing playbook and current workspace.
2. Preserve project-owned policy and deliberate substitutions. Correct only stale factual bindings and add
   missing required roles; never overwrite the file wholesale.
3. Re-run setup mentally against the result; unchanged facts must produce no diff.

Do not write root instructions, another skill's playbook, or hard-coded machine policy into the bundled skill.

Completion criterion: one idempotent project playbook binds Opportunity root, entity maps, and local review
policy using verified paths; no records were silently migrated.
