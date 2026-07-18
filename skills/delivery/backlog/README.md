# Backlog

Groom the backlog with the human, then run each ready-for-agent issue through the build loop to a reviewed PR. Subcommands also run standalone. Platform-bound, not platform-bound-to-GitHub: the tracker, review surface, version control, and harness are roles the skill reasons in, bound per repo by `backlog setup` — GitHub and a local on-disk tracker ship as defaults; anything else is derived at setup.

## File locations

- **Bundled reference** (`reference/`, `templates/`) ships with the skill; `templates/` is shared `common/` plus per-domain packs, with `software/` the shipped default. It is not looked for in the target repo. References hold only orchestration — targets, gates, handoffs — resolving staffing, review, planning, and prototyping against sibling skills by name.
- **Sibling skills** — `backlog` composes `diagnosing-bugs` (bug method), `research` (primary-source investigation), `staffing` (roster/roles/fallback), `review-loop` (presentation + interactive review), and `prototype` (throwaway design questions) **by plain name**; setup ensures their required closure.
- **Project playbook** (`docs/agents/*.md`) lives in the target repo and holds this codebase's conventions and platform bindings. Backlog-owned techniques are shipped inline; sibling-owned techniques are reconciled by that sibling's setup. Override a step by editing its playbook.

## Use

```bash
backlog setup                     # scaffold playbooks, bind the platforms, prep isolation (run once per repo)
backlog groom                     # triage the backlog with you; label what's ready-for-agent
backlog run                       # work every ready-for-agent, unblocked issue
backlog                           # groom, then offer to run the ready ones
backlog diagnose 42               # run a single subcommand standalone
backlog prototype "does optimistic locking fit this editor?"   # delegates to the prototype sibling skill
backlog research "what does the upstream protocol guarantee?"  # delegates to the research sibling skill
backlog adversarial-review 88
```

`backlog setup` scaffolds the playbooks, binds the four platform ports (tracker, change review, version control, harness — recorded as verified commands in `docs/agents/platform.md`), provisions the tracker's role labels (`ready-for-agent`, `in-flight`, `ready-for-human`, work-types, exclusions), asks whether work runs in parallel or sequentially — scaffolding worktree isolation on approval when parallel — identifies the seed and check commands, confirms the agent has a way to drive, authenticate to, and capture evidence from the app (shell for a CLI, a driveable browser for web, an emulator for mobile, computer-use for desktop only behind its recorded-use-case + explicit-approval gate), optionally smoke-tests the whole contract, and offers to fold any existing house practice (debugging docs, testing guides, review checklists) into the scaffolded playbooks.

## Credits

- **Relationship:** adapted and internally decomposed.
- **Sources:** Matt Pocock's MIT-licensed [`tdd`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/tdd/SKILL.md) and [`code-review`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/code-review/SKILL.md); Cursor's MIT-licensed [`thermo-nuclear-code-quality-review`](https://github.com/cursor/plugins/blob/a29f5a8ca161b1de4ffc5484454958bebc04eaa5/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md).
- **Borrowed:** the red/green implementation discipline and adversarial quality-review shape.
- **Local changes:** made the lifecycle tracker/platform-neutral, added durable dispatch/verify/evidence gates,
  and moved bug diagnosis to the separately credited `diagnosing-bugs` skill.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
