# Triage

Groom the GitHub backlog with the human, then run each ready-for-agent issue through the issue loop to a reviewed PR. Subcommands also run standalone.

## File locations

- **Bundled reference** (`reference/`, `templates/`) ships with the skill; it is not looked for in the target repo.
- **Project playbook** (`docs/agents/*.md`) lives in the target repo and holds how this codebase does each step. Created by `triage setup`.

## Use

```bash
triage setup                      # scaffold playbooks, provision labels, prep isolation (run once per repo)
triage groom                      # triage the backlog with you; label what's ready-for-agent
triage run                        # work every ready-for-agent, unblocked issue
triage                            # groom, then offer to run the ready ones
triage diagnose 42                # run a single subcommand standalone
triage adversarial-review 88
```

`triage setup` scaffolds the playbooks, provisions the GitHub role labels (`ready-for-agent`, `ready-for-human`, work-types, exclusions), asks whether work runs in parallel or sequentially — scaffolding worktree isolation on approval when parallel — identifies the seed and check commands, optionally smoke-tests them, and offers to install the external skills the playbooks defer to (e.g. Matt Pocock's `diagnosing-bugs`, `tdd`).
