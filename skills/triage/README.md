# Triage

Routes open GitHub issues through a per-issue development loop — classify, then run the matching branch (diagnose / plan → implement / refactor), verify, open a PR, and drive an adversarial review until LGTM. One installable skill with a single command surface; each subcommand also runs standalone.

## File locations

- **Bundled reference** (`reference/`, `templates/`) ships with the skill; it is not looked for in the target repo.
- **Project playbook** (`docs/agents/*.md`) lives in the target repo and holds how this codebase does each step. Created by `triage setup`.

## Use

```bash
triage setup                      # scaffold docs/agents/ playbooks (run once per repo)
triage                            # triage all unlabeled open issues
triage diagnose 42                # run a single subcommand standalone
triage adversarial-review 88
```

`triage setup` also offers to install the external skills the playbooks can defer to (e.g. Matt Pocock's `diagnosing-bugs`, `tdd`).
