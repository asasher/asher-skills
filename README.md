# Asher Skills

Skills that I made or that I like. This is a single repo that I can use to install these skills in other places.

## Install

Installing is two jobs — mount the skills, then run each one's setup against the repo it landed in — so hand it to an agent. Paste this into whichever coding agent you use, in the repository you want the skills in:

```text
Install Asher's skills into this repository, and finish the job.

1. From the repository root, run:
       npx skills add github:asasher/asher-skills --skill backlog build-change staffing
   That list is a default — if I have named a different set, use mine, and ask me
   before running anything if you are unsure which skills I want. Each skill's
   SKILL.md names the sibling skills it composes with; install those too so the
   set is closed.
2. For each installed skill, read its SKILL.md. If it declares a setup, run that
   setup now, in an order that respects who writes what (backlog's setup writes
   the shared playbooks, so it goes first). A setup writes and reconciles this
   repository's playbooks — the files under docs/agents/ the skills read at
   runtime — so work from what this repository actually does, edit an existing
   playbook rather than replacing it, and ask me when a setup needs a decision
   I have not given you.
3. Review the whole diff before you commit it: the skill mounts and every
   playbook a setup touched. A playbook naming a command, branch, or tool this
   repository does not use is a defect to fix, not a detail to wave through.
4. Commit, with a message naming the skills you installed and the setups you ran.
   Leave the installed skill directories alone otherwise — they are build
   products, and the next install rewrites them.
```

The setups are the half that needs judgment: they bind role nouns like _tracker_, _change request_, and _base branch_ to what this particular repository uses, and they sometimes have to ask.

## Reconcile

After this repo's `main` moves, bring an existing install up to date from the changelog. Paste this into your agent, in the repository that has the skills:

```text
Reconcile Asher's skills in this repository from the changelog.

1. Read https://raw.githubusercontent.com/asasher/asher-skills/main/CHANGELOG.md
   and find the entries newer than the last reconcile recorded in this repo's
   history (the last commit that mentions reconciling these skills; if none,
   treat every entry as new).
2. For each entry: re-run `npx skills add github:asasher/asher-skills --skill <names>`
   for the changed skills in my installed set, remove the mounts of any skill an
   entry says was dropped or renamed away, and re-run the setups the entry names —
   reconciling the playbooks, never blindly overwriting them.
3. Review the diff, then commit with a message naming the entries you reconciled.
```

There is no first-party installer and no install-state file — the changelog is the record, and `npx skills add` is the mount tool.

## Catalog

Categories organize source browsing. Skill names, `--skill <name>`, sibling references, and installed directories remain flat and unchanged. Invocation and execution are independent axes. `user` means **explicit-only**: a human, orchestrator, or delegated prompt must name the skill. `model` also permits a working thread to discover the skill when needed. `reference` skills are model-invoked but never run as workflows — siblings cite them by name.

| Category             | Skill                    | Invocation | Kind         |
| -------------------- | ------------------------ | ---------- | ------------ |
| system               | `skill-loop`             | user       | orchestrator |
| system               | `staffing`               | model      | reference    |
| creative             | `bare-minimum-design`    | model      | reference    |
| creative             | `codex-imagegen`         | model      | primitive    |
| creative             | `maquette`               | model      | primitive    |
| creative             | `shadixfy`               | model      | primitive    |
| creative             | `watch-video`            | model      | primitive    |
| thinking             | `bayes`                  | user       | primitive    |
| thinking             | `constraints`            | user       | primitive    |
| thinking             | `dissolve`               | user       | orchestrator |
| software-development | `adversarial-review`     | model      | orchestrator |
| software-development | `agent-ready-codebase`   | model      | reference    |
| software-development | `backlog`                | user       | orchestrator |
| software-development | `build-change`           | model      | orchestrator |
| software-development | `code-review`            | model      | primitive    |
| software-development | `diagnosing-bugs`        | model      | primitive    |
| software-development | `domain-modeling`        | model      | primitive    |
| software-development | `handoff`                | user       | primitive    |
| software-development | `implement`              | model      | composite    |
| software-development | `interview`              | model      | primitive    |
| software-development | `merge-change`           | user       | composite    |
| software-development | `experience-first`       | model      | reference    |
| software-development | `writing-for-humans`     | model      | reference    |
| software-development | `prototype`              | model      | composite    |
| software-development | `prove-your-work`        | model      | composite    |
| software-development | `research`               | model      | composite    |
| software-development | `shape`                  | model      | orchestrator |
| software-development | `tdd`                    | model      | primitive    |
| software-development | `to-backlog`             | model      | primitive    |
| software-development | `to-slices`              | user       | primitive    |
| software-development | `to-spec`                | model      | composite    |
| software-development | `to-subagent`            | model      | composite    |
| software-development | `to-tailnet`             | user       | primitive    |
| software-development | `to-thread`              | model      | primitive    |
| software-development | `to-web`                 | model      | primitive    |
| software-development | `verify-your-work`       | model      | primitive    |
| software-development | `watch-until`            | model      | primitive    |
| software-development | `worktree`               | model      | primitive    |
| personal             | `capture-to-inbox`       | model      | primitive    |
| personal             | `learn-anything`         | user       | primitive    |
| personal             | `manage-notes`           | model      | primitive    |
| personal             | `manage-opportunities`   | model      | primitive    |
| personal             | `manage-tasks`           | model      | primitive    |
| personal             | `relay`                  | model      | primitive    |
| personal             | `review-opportunities`   | user       | primitive    |
| in-progress          | `goodwork`               | model      | primitive    |
| in-progress          | `retro`                  | model      | composite    |
| in-progress          | `writing-technical-docs` | model      | primitive    |

## Skills I Like

Other people's skills I install alongside these. They come from their own repos, on their own terms — follow each project's own install instructions rather than any recorded here, which only go stale.

| Skill(s) | Source |
| --- | --- |
| `impeccable` | [impeccable](https://www.npmjs.com/package/impeccable) — vendor CLI, `npx impeccable install` |
| `uncodixfy` | [cyxzdev/Uncodixfy](https://github.com/cyxzdev/Uncodixfy) |
| `agent-browser` | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) |
| `agentmail`, `portless` | [agentmail-to/agentmail-skills](https://github.com/agentmail-to/agentmail-skills) |
| `greploop` | [greptileai/skills](https://github.com/greptileai/skills) |
| `tdd`, `caveman`, `diagnose`, `grill-me`, `improve-codebase-architecture`, `prototype`, `zoom-out`, `teach`, `writing-for-agents`, `resolving-merge-conflicts` | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `use-railway` | [railwayapp/railway-skills](https://github.com/railwayapp/railway-skills) |
| `vercel-cli` | [vercel/vercel](https://github.com/vercel/vercel) |
| convex skills | [get-convex/agent-skills](https://github.com/get-convex/agent-skills) |
| `btca-local` | [davis7dotsh/better-context](https://github.com/davis7dotsh/better-context) |
| `liteparse` | [run-llama/llamaparse-agent-skills](https://github.com/run-llama/llamaparse-agent-skills) |

An external skill that an authored skill actually depends on is a different thing — it is declared in that skill's `metadata.external`, installed only after provenance review and explicit consent, and recorded in `external-dependencies.lock.json`. See `CONTEXT.md`.
