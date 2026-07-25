# Asher Skills

Skills that I made or that I like. This is a single repo that I can use to install these skills in other places.

## Install

These skills install through this repo's own installer, run straight from GitHub — nothing is published
to npm:

```bash
npx github:asasher/asher-skills install --skill backlog build staffing   # first install: name the set
npx github:asasher/asher-skills install                                  # refresh the recorded set
npx github:asasher/asher-skills check                                    # diff mounts against source
```

Run it from the target repo. `install` mounts each skill at `.agents/skills/<name>` with a
`.claude/skills/<name>` alias, pulls in any required siblings, compiles per-provider trees for skills
declaring `metadata.variants` (today: `staffing`), and removes anything dropped from an explicit
`--skill` set. A bare `install` refreshes exactly what is already recorded, so it never silently widens a
curated selection.

State lives in `.agents/asher-skills/install.json` — the set, each skill's source path, provider variants,
and the source revision. No integrity hashes: `check` diffs each mount against the source it was built
from and names the files that drifted, exiting 1 if any did. It is a dev-time command — skills are
dev-time tooling and do not belong in a project's CI.

From a checkout, the same thing without npx:

```bash
python3 tools/install.py install --into <repo> --skill <names...>
python3 tools/install.py check --into <repo>
```

> **Not `npx skills add`.** That CLI cannot install these correctly: it ignores `metadata.variants` (so
> `staffing` lands as uncompiled source with no roster), skips directories named `build`, and never
> removes a skill dropped from the set — see
> [#103](https://github.com/asasher/asher-skills/issues/103). It remains the right tool for the
> third-party skills listed further down, which come from repos it does understand; this installer
> touches only its own rows in `skills-lock.json` and otherwise leaves that file alone.

Categories organize source browsing and the interactive installer. Skill names, `--skill <name>`, sibling
references, and installed directories remain flat and unchanged. Invocation and execution are independent axes. `user` means
**explicit-only**: a human, orchestrator, or delegated prompt must name the skill. `model` also permits a
working thread to discover the skill when needed. `orchestrator` execution owns delegation boundaries;
`thread` execution runs within its caller. Thus an orchestrator may explicitly dispatch any installed skill,
including one marked `user`.

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
| software-development | `merge-changes` | user | orchestrator |
| software-development | `prototype` | model | orchestrator |
| software-development | `prove-your-work` | model | thread |
| software-development | `research` | model | orchestrator |
| software-development | `serve-via-tailnet` | model | orchestrator |
| software-development | `shape` | model | orchestrator |
| software-development | `tdd` | model | thread |
| software-development | `to-spec` | model | thread |
| software-development | `to-subagent` | model | orchestrator |
| software-development | `to-thread` | model | orchestrator |
| software-development | `to-tickets` | model | thread |
| software-development | `verify-your-work` | model | thread |
| software-development | `watch-until` | model | orchestrator |
| personal | `capture-to-inbox` | model | thread |
| personal | `control-plane` | user | orchestrator |
| personal | `eloquent` | model | thread |
| personal | `fair-deal` | user | orchestrator |
| personal | `learn-anything` | user | thread |
| personal | `manage-notes` | model | thread |
| personal | `manage-opportunities` | model | thread |
| personal | `manage-tasks` | model | thread |
| personal | `projects-triage` | user | orchestrator |
| personal | `relay` | model | thread |
| personal | `review-opportunities` | user | thread |
| personal | `teamdrive` | user | thread |
| personal | `until-zero` | model | thread |
| in-progress | `goodwork` | model | thread |

The install/setup graph is compiled on demand from each skill's frontmatter
(`python3 tools/catalog.py compile`).

## Skills I Like

### Project
```bash
## Almost always
npx impeccable skills install
npx skills add cyxzdev/Uncodixfy
npx skills add https://github.com/vercel-labs/agent-browser --skill agent-browser
npx skills add https://github.com/agentmail-to/agentmail-skills --skill agentmail portless
npx skills add https://github.com/greptileai/skills --skill greploop
npx skills@latest add mattpocock/skills --skill tdd

## Depending on the deployment setup
npx skills add https://github.com/railwayapp/railway-skills --skill use-railway
npx skills add https://github.com/vercel/vercel --skill vercel-cli
npx skills add https://github.com/get-convex/agent-skills
```

### Global

```bash
npx skills add cyxzdev/Uncodixfy -g
npx skills add https://github.com/vercel-labs/agent-browser --skill agent-browser portless -g
npx skills add https://github.com/agentmail-to/agentmail-skills --skill agentmail -g
npx skills@latest add mattpocock/skills --skill caveman diagnose grill-me improve-codebase-architecture prototype zoom-out teach -g
npx skills add https://github.com/greptileai/skills --skill greploop -g
npx skills add https://github.com/railwayapp/railway-skills --skill use-railway -g
npx skills add https://github.com/vercel/vercel --skill vercel-cli -g
npx skills add https://github.com/davis7dotsh/better-context --skill btca-local -g
npx skills add run-llama/llamaparse-agent-skills --skill liteparse -g
```
