# Asher Skills

Skills that I made or that I like. This is a single repo that I can use to install these skills in other places.

## Install

Installing is two jobs — mount the skills, then run each one's setup against the repo it landed in — so hand it to an agent. The main point of this repository is the software development lifecycle family; it installs together with its supporting skills, and this command mounts all of it:

```sh
npx skills add github:asasher/asher-skills --skill adversarial-review agent-ready-codebase backlog bare-minimum-design capture code-review deliver diagnosing-bugs diagram-design domain-modeling handoff implement interview merge principle-codebase-design principle-experience-first principle-type-system-discipline prototype prove-your-work research retro shape staffing tdd technical-writing to-branch to-slices to-spec to-subagent to-thread to-web typescript-best-practices unslop verify-your-work worktree writing-for-humans
```

The other categories — creative, thinking, personal — are the appendix: browse the catalog and install what you want by name.

The mount is the easy half; the setups need judgment, so hand the whole job to an agent. Paste this into whichever coding agent you use, in the repository you want the skills in:

```text
Install Asher's skills into this repository, and finish the job.

1. From the repository root, run the install command from
   https://github.com/asasher/asher-skills#install — it mounts the software
   development lifecycle family and its supporting skills. If I have named a
   different set, use mine instead, and ask me before running anything if you
   are unsure which skills I want. Each skill's SKILL.md names the sibling
   skills it composes with; when installing a subset, install those siblings
   too so the set is closed.
2. For each installed skill, read its SKILL.md. If it declares a setup, run that
   setup now: backlog's setup writes docs/agents/environment.md, certifies the
   repo against agent-ready-codebase, and creates the labels, so it goes first;
   retro's setup asks for consent. A setup writes and reconciles this
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

The setups are the half that needs judgment: they record how this repository runs, seeds, authenticates, and proves itself, and they sometimes have to ask. The platform itself is fixed: GitHub issues and PRs, git, an S3-compatible bucket.

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

Categories organize source browsing. Skill names, `--skill <name>`, sibling references, and installed directories remain flat and unchanged. Invocation and execution are independent axes. `user` means **explicit-only**: a human, orchestrator, or delegated prompt must name the skill. `model` also permits a working thread to discover the skill when needed. `reference` skills are model-invoked but never run as workflows — siblings cite them by name, and citing one does not make the citer a composite.

| Category | Skill | Invocation | Kind |
| --- | --- | --- | --- |
| system | `skill-loop` | user | orchestrator |
| system | `staffing` | model | reference |
| system | `to-subagent` | model | composite |
| system | `to-thread` | model | composite |
| creative | `bare-minimum-design` | model | reference |
| creative | `codex-imagegen` | model | primitive |
| creative | `diagram-design` | model | primitive |
| creative | `maquette` | model | primitive |
| creative | `shadixfy` | model | primitive |
| creative | `watch-video` | model | primitive |
| thinking | `bayes` | user | primitive |
| thinking | `constraints` | user | primitive |
| thinking | `dissolve` | user | orchestrator |
| software-development | `adversarial-review` | model | orchestrator |
| software-development | `agent-ready-codebase` | model | reference |
| software-development | `backlog` | user | orchestrator |
| software-development | `capture` | model | composite |
| software-development | `code-review` | model | composite |
| software-development | `deliver` | model | orchestrator |
| software-development | `diagnosing-bugs` | model | primitive |
| software-development | `domain-modeling` | model | primitive |
| software-development | `handoff` | user | primitive |
| software-development | `implement` | model | composite |
| software-development | `interview` | model | composite |
| software-development | `merge` | user | composite |
| software-development | `principle-codebase-design` | model | reference |
| software-development | `principle-experience-first` | model | reference |
| software-development | `principle-type-system-discipline` | model | reference |
| software-development | `prototype` | model | primitive |
| software-development | `prove-your-work` | model | composite |
| software-development | `research` | model | composite |
| software-development | `retro` | model | composite |
| software-development | `shape` | model | orchestrator |
| software-development | `tdd` | model | primitive |
| software-development | `technical-writing` | model | reference |
| software-development | `to-branch` | model | primitive |
| software-development | `to-slices` | user | primitive |
| software-development | `to-spec` | model | composite |
| software-development | `to-web` | model | primitive |
| software-development | `typescript-best-practices` | model | reference |
| software-development | `unslop` | model | reference |
| software-development | `verify-your-work` | model | primitive |
| software-development | `worktree` | model | primitive |
| software-development | `writing-for-humans` | model | reference |
| personal | `learn-anything` | user | primitive |
| personal | `relay` | model | primitive |
| personal | `to-tailnet` | user | primitive |
| in-progress | `goodwork` | model | primitive |

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

An external skill that an authored skill needs is a different thing — it ships from this repo: copied wholesale or rewritten as our own version, with credits in that skill's README. This pins the version we reviewed, not a copy that upstream controls. See `CONTEXT.md`.
