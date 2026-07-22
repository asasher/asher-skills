# Asher Skills

Skills that I made or that I like. This is a single repo that I can use to install these skills in other places.

## Install

Install globally:

```bash
npx skills add <repo-url> --skill <skill-name> -g
```

Install in the current project:

```bash
npx skills add <repo-url> --skill <skill-name> -y
```

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
| delivery | `spreadsheet-loop` | user | orchestrator |
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
| personal | `goodwork` | model | thread |
| personal | `learn-anything` | user | thread |
| personal | `manage-notes` | model | thread |
| personal | `manage-opportunities` | model | thread |
| personal | `manage-tasks` | model | thread |
| personal | `projects-triage` | user | orchestrator |
| personal | `relay` | model | thread |
| personal | `review-opportunities` | user | thread |
| personal | `teamdrive` | user | thread |
| personal | `until-zero` | model | thread |

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
