# Backlog

Groom the backlog with the human, then run each ready-for-agent issue through the issue loop to a reviewed PR. Subcommands also run standalone. Platform-bound, not platform-bound-to-GitHub: the tracker, review surface, version control, and harness are roles the skill reasons in, bound per repo by `backlog setup` — GitHub and a local on-disk tracker ship as defaults; anything else is derived at setup.

## File locations

- **Bundled reference** (`reference/`, `templates/`) ships with the skill; it is not looked for in the target repo. References hold only orchestration — targets, gates, staffing, handoffs.
- **Project playbook** (`docs/agents/*.md`) lives in the target repo and holds the working instructions for each step: the technique (shipped inlined, no external skills required) plus this codebase's conventions and platform bindings. Created by `backlog setup`; override a step by editing its playbook.

## Use

```bash
backlog setup                     # scaffold playbooks, bind the platforms, prep isolation (run once per repo)
backlog groom                     # triage the backlog with you; label what's ready-for-agent
backlog run                       # work every ready-for-agent, unblocked issue
backlog                           # groom, then offer to run the ready ones
backlog diagnose 42               # run a single subcommand standalone
backlog prototype "does optimistic locking fit this editor?"
backlog adversarial-review 88
```

`backlog setup` scaffolds the playbooks, binds the four platform ports (tracker, change review, version control, harness — recorded as verified commands in `docs/agents/platform.md`), provisions the tracker's role labels (`ready-for-agent`, `in-flight`, `ready-for-human`, work-types, exclusions), asks whether work runs in parallel or sequentially — scaffolding worktree isolation on approval when parallel — identifies the seed and check commands, confirms the agent has a way to drive, authenticate to, and capture evidence from the app (shell for a CLI, a driveable browser for web, an emulator for mobile, computer-use for desktop), optionally smoke-tests the whole contract, and offers to fold any existing house practice (debugging docs, testing guides, review checklists) into the scaffolded playbooks.

## Credits

The technique inlined in the shipped playbooks adapts Matt Pocock's [`diagnosing-bugs`, `tdd`, `code-review`, `prototype`, and `to-prd` skills](https://github.com/mattpocock/skills) (MIT) and the review bar of Cursor's [thermo-nuclear code-quality review](https://github.com/cursor/plugins).
