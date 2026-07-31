# Setup — project playbooks

Install or reconcile the project playbooks from `templates/` — the shared `common/` baselines plus a per-domain pack, `software/` being the shipped default:

- `docs/agents/platform.md` — platform bindings, with each verb verified live.
- `docs/agents/backlog-policy.md` — label roles, dependency edges, the readiness decision.
- `docs/agents/environment.md` — run/seed/check.
- `docs/agents/codebase.md` — how the code is written and checked: seeded from the repo's own docs, accreting what sessions learn.
- `docs/agents/evidence.md` — the evidence bar.
- `docs/agents/change-description.md` — the change-request body outline.

Reconcile with what exists — a repo-owned playbook is edited, never blindly overwritten.

Classify every machine fact per [machine facts](machine-facts.md): verify-at-use facts get their probe command, not their result; every recorded machine fact goes to the gitignored `docs/agents/local/` overlays — one per tracked playbook, regenerated here, opening with its machine-record stamp, with the `.gitignore` entry ensured and each overlay declared in its tracked playbook by the machine-local pointer marker. A tracked file never records a machine fact.

Verify the label roles exist in the tracker; create missing ones with the user's consent.

Finish by running `scripts/check-machine-facts.py` against the repo and resolving what it names.
