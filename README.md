# Asher Skills

Skills that I made or that I like. This is a single repo that I can use to install these skills in other places.

## Install

Installing is two jobs — mount the skills, then run each one's setup against the repo it landed in — so hand it to an agent. Paste this into whichever coding agent you use, in the repository you want the skills in:

```text
Install Asher's skills into this repository, and finish the job.

1. From the repository root, run:
       npx github:asasher/asher-skills install --skill backlog build staffing
   That list is a default — if I have named a different set, use mine, and ask me
   before running anything if you are unsure which skills I want. If this repository
   already has an `.agents/asher-skills/install.json`, it already has skills from
   here: run the same command with no `--skill` at all instead, which refreshes
   exactly the set that file records. Whenever you do name a set, name the whole set
   I want, including what is already there — `--skill` replaces the recorded set and
   removes the skills left out of it, so adding one is naming all of them. If there is
   a `skills-lock.json` naming skills from here and no `install.json`, ask me which
   set to record before running anything.
2. The install prints a JSON report. Read its `setup_report`: `setup_order` names the
   installed skills that declare a setup, already in the order to run them, and the
   summary on stderr says the same thing.
3. Run those setups yourself, one at a time, in that order. For each, read the skill
   as installed — its `SKILL.md`, plus whatever that points you to — and follow the
   setup it describes. A skill compiled per harness is mounted once per harness and
   the copies differ, so read the one belonging to the harness you are running in.
   A setup writes and reconciles this repository's playbooks, the files under
   `docs/agents/` that the skills read at runtime, so work from what this repository
   actually does, edit an existing playbook rather than replacing it, and ask me when
   a setup needs a decision I have not given you.
4. Review the whole diff before you commit it: the skill mounts, the install state in
   `.agents/asher-skills/install.json`, and every playbook a setup touched. A playbook
   naming a command, branch, or tool this repository does not use is a defect to fix,
   not a detail to wave through.
5. Commit, with a message naming the skills you installed and the setups you ran.
   Leave the installed skill directories alone otherwise — they are build products, and
   the next install rewrites them.
```

The setups are the half that needs judgment: they bind role nouns like _tracker_, _change request_, and _base branch_ to what this particular repository uses, and they sometimes have to ask. The installer names them and invokes nothing, so something with judgment has to close that gap — hence the prompt.

### Driving the installer yourself

The installer runs straight from GitHub; nothing is published to npm.

```bash
npx github:asasher/asher-skills install --skill backlog build staffing   # first install: name the set
npx github:asasher/asher-skills install                                  # refresh the recorded set
npx github:asasher/asher-skills check                                    # diff mounts against source
```

Run it from the target repo. `install` mounts each skill at `.agents/skills/<name>` with a `.claude/skills/<name>` alias, pulls in any required siblings, compiles per-provider trees for skills declaring `metadata.variants` (today: `staffing`), and removes anything dropped from an explicit `--skill` set. A bare `install` refreshes exactly what is already recorded, so it never silently widens a curated selection.

An install ends with a `setup_report` in its JSON output, summarized on stderr: which installed skills' sources changed since the recorded revision — plus any mounted here for the first time — and, as `setup_order`, the changed skills that declare a setup, in the order the catalog resolves them. Running those setups is an agent's job — the installer names them and invokes nothing. Its `basis` field says how the set was arrived at: a real comparison needs git history in the source tree, so an install from the `npx`-packed package — which ships no `.git` — reports every installed skill as changed rather than guessing at nothing-to-do. Installing from a checkout with uncommitted work is comparable: the sources carrying it are recorded, and count as changed on the next install too, since reverting that work changes their mounts as much as making it did.

State lives in `.agents/asher-skills/install.json` — the set, each skill's source path, provider variants, the source revision, and which sources were uncommitted against it. No integrity hashes: `check` diffs each mount against the source it was built from and names the files that drifted, exiting 1 if any did. It is a dev-time command — skills are dev-time tooling and do not belong in a project's CI.

From a checkout, the same thing without npx:

```bash
python3 tools/install.py install --into <repo> --skill <names...>
python3 tools/install.py check --into <repo>
```

> **Not `npx skills add`.** That CLI cannot install these correctly: it ignores `metadata.variants` (so `staffing` lands as uncompiled source with no roster), skips directories named `build`, and never removes a skill dropped from the set — see [#103](https://github.com/asasher/asher-skills/issues/103). It stays fine for skills from repos it does understand — several under [Skills I Like](#skills-i-like) install that way. This installer touches only its own rows in `skills-lock.json` and otherwise leaves that file alone.

Categories organize source browsing and the interactive installer. Skill names, `--skill <name>`, sibling references, and installed directories remain flat and unchanged. Invocation and execution are independent axes. `user` means **explicit-only**: a human, orchestrator, or delegated prompt must name the skill. `model` also permits a working thread to discover the skill when needed. `orchestrator` execution owns delegation boundaries; `thread` execution runs within its caller. Thus an orchestrator may explicitly dispatch any installed skill, including one marked `user`.

## Authored skills

| Category | Skill | Invocation | Execution |
|---|---|---|---|
| system | `skill-loop` | user | orchestrator |
| system | `staffing` | model | thread |
| creative | `bare-minimum-ux` | model | thread |
| creative | `codex-imagegen` | model | thread |
| creative | `maquette` | model | thread |
| creative | `shadixfy` | model | thread |
| creative | `watch-video` | model | thread |
| thinking | `bayes` | user | thread |
| thinking | `constraints` | user | thread |
| thinking | `dissolve` | user | orchestrator |
| software-development | `adversarial-review` | model | orchestrator |
| software-development | `backlog` | user | orchestrator |
| software-development | `build` | model | orchestrator |
| software-development | `code-review` | model | orchestrator |
| software-development | `diagnosing-bugs` | model | thread |
| software-development | `domain-modeling` | model | orchestrator |
| software-development | `handoff` | user | thread |
| software-development | `implement` | model | thread |
| software-development | `interview` | model | orchestrator |
| software-development | `merge-changes` | model | orchestrator |
| software-development | `prototype` | model | orchestrator |
| software-development | `prove-your-work` | model | thread |
| software-development | `research` | model | orchestrator |
| software-development | `serve-via-tailnet` | user | orchestrator |
| software-development | `shape` | model | orchestrator |
| software-development | `tdd` | model | thread |
| software-development | `to-backlog` | model | thread |
| software-development | `to-slices` | model | thread |
| software-development | `to-spec` | model | thread |
| software-development | `to-subagent` | model | orchestrator |
| software-development | `to-thread` | model | orchestrator |
| software-development | `verify-your-work` | model | thread |
| software-development | `watch-until` | model | orchestrator |
| software-development | `worktree` | model | thread |
| personal | `capture-to-inbox` | model | thread |
| personal | `learn-anything` | user | thread |
| personal | `manage-notes` | model | thread |
| personal | `manage-opportunities` | model | thread |
| personal | `manage-tasks` | model | thread |
| personal | `relay` | model | thread |
| personal | `review-opportunities` | user | thread |
| in-progress | `goodwork` | model | thread |
| in-progress | `retro` | model | thread |

The install/setup graph is compiled on demand from each skill's frontmatter (`python3 tools/catalog.py compile`).

## Skills I Like

Other people's skills I install alongside these. They come from their own repos, on their own terms — follow each project's own install instructions rather than any recorded here, which only go stale.

| Skill(s) | Source |
| --- | --- |
| `impeccable` | [impeccable](https://www.npmjs.com/package/impeccable) — vendor CLI, `npx impeccable install` |
| `uncodixfy` | [cyxzdev/Uncodixfy](https://github.com/cyxzdev/Uncodixfy) |
| `agent-browser` | [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) |
| `agentmail`, `portless` | [agentmail-to/agentmail-skills](https://github.com/agentmail-to/agentmail-skills) |
| `greploop` | [greptileai/skills](https://github.com/greptileai/skills) |
| `tdd`, `caveman`, `diagnose`, `grill-me`, `improve-codebase-architecture`, `prototype`, `zoom-out`, `teach` | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `use-railway` | [railwayapp/railway-skills](https://github.com/railwayapp/railway-skills) |
| `vercel-cli` | [vercel/vercel](https://github.com/vercel/vercel) |
| convex skills | [get-convex/agent-skills](https://github.com/get-convex/agent-skills) |
| `btca-local` | [davis7dotsh/better-context](https://github.com/davis7dotsh/better-context) |
| `liteparse` | [run-llama/llamaparse-agent-skills](https://github.com/run-llama/llamaparse-agent-skills) |

An external skill that an authored skill actually depends on is a different thing — it is declared in that skill's `metadata.external`, installed only after provenance review and explicit consent, and recorded in `external-dependencies.lock.json`. See `AGENTS.md` § Vocabulary.
