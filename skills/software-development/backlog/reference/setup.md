# Setup — project playbooks

Install or reconcile the project playbooks from `templates/` — the shared `common/` baselines plus a per-domain pack, `software/` being the shipped default:

- `docs/agents/platform.md` — platform bindings, with each verb verified live.
- `docs/agents/backlog-policy.md` — label roles, dependency edges, the readiness decision.
- `docs/agents/environment.md` — run/seed/check.
- `docs/agents/codebase.md` — how the code is written and checked: seeded from the repo's own docs, accreting what sessions learn.
- `docs/agents/evidence.md` — the evidence bar.
- `docs/agents/change-description.md` — the change-request body outline.

Reconcile with what exists — a repo-owned playbook is edited, never blindly overwritten.

Verify the label roles exist in the tracker; create missing ones with the user's consent.
