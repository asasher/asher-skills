# Triage

Groom the GitHub backlog with the human, then run each ready-for-agent issue through the issue loop to a reviewed PR. Subcommands also run standalone.

## File locations

- **Bundled reference** (`reference/`, `templates/`) ships with the skill; it is not looked for in the target repo. References hold only orchestration — targets, gates, staffing, handoffs.
- **Project playbook** (`docs/agents/*.md`) lives in the target repo and holds the working instructions for each step: the technique (shipped inlined, no external skills required) plus this codebase's conventions. Created by `triage setup`; override a step by editing its playbook.

## Use

```bash
triage setup                      # scaffold playbooks, provision labels, prep isolation (run once per repo)
triage groom                      # triage the backlog with you; label what's ready-for-agent
triage run                        # work every ready-for-agent, unblocked issue
triage                            # groom, then offer to run the ready ones
triage diagnose 42                # run a single subcommand standalone
triage prototype "does optimistic locking fit this editor?"
triage adversarial-review 88
```

`triage setup` scaffolds the playbooks, provisions the GitHub role labels (`ready-for-agent`, `ready-for-human`, work-types, exclusions), asks whether work runs in parallel or sequentially — scaffolding worktree isolation on approval when parallel — identifies the seed and check commands, confirms the agent has a way to drive, authenticate to, and capture evidence from the app (shell for a CLI, a driveable browser for web, an emulator for mobile, computer-use for desktop), optionally smoke-tests the whole contract, and offers to fold any existing house practice (debugging docs, testing guides, review checklists) into the scaffolded playbooks.

## Credits

The technique inlined in the shipped playbooks adapts Matt Pocock's [`diagnosing-bugs`, `tdd`, `code-review`, `prototype`, and `to-prd` skills](https://github.com/mattpocock/skills) (MIT) and the review bar of Cursor's [thermo-nuclear code-quality review](https://github.com/cursor/plugins).
