# Asher Skills

A collection of skills by Asher. Skills are organized into families with main focus being the software development lifecycle skills.

## Language

**Project**: The repo a skill is installed into and runs in — the bare word in skill prose, and the only project a sealed skill can name, since an install carries no authoring context. This repo is itself a project for the skills installed into it. _Avoid_: consumer project, host repo.

**Authoring repo**: This repository, where skill sources live and every install derives from. Its own docs say "this repo"; "authoring repo" is the name when the dual role needs distinguishing — authoring a skill vs running one. _Avoid_: this project, skills repo.

**Primitive skill**: The bottom of the composition axis, and **sealed**: it names no other skill and never addresses "the caller" — its text reads complete to an agent that knows nothing about what composed it. It reads what is handed to it plus the environment (repo playbooks are environment, project instruction files, not caller), and classifies what it cannot settle instead of naming who settles it. Example: `domain-modeling`. _Avoid_: a primitive that names a sibling, an upper layer, or "whoever composed this" — all three break the seal.

**Composite skill**: Composes named lower-layer skills by their name, declares them in its dependency surface, and degrades explicitly when one is absent. All composition knowledge lives here: the composite knows its parts' contracts, the parts know nothing back. Example: `shape` (composes `interview` and `domain-modeling`, dispatching `research` and `prototype` through `to-subagent`). Even a thin edge makes a composite: `interview` names only `to-subagent` for fact lookups, and that one edge moves it off the primitive rung.

**Orchestrator skill**: Runs a loop over many units of work, owning dispatch and lifecycle state. A **dispatcher** is the thin case: it fans units out and exits — outcomes land on the tracker (the run ledger), and a later `status` read derives liveness instead of a supervising session holding it. Human-in-the-loop work goes to threads the user attends (`to-thread` — no result flows back); autonomous work goes to threads too, unattended, each unit's stages running as blocking `to-subagent` calls inside its thread. Examples: `backlog groom` (a `shape` thread per subject), `backlog build` (a `build-change` thread per ready ticket — the dispatch declaration posted as the claim, then exit).

**Dispatch adapter**: A thin composite owning _how_ work is dispatched, not what the work is: `to-thread` spawns named, interactive sessions the user attends through the outermost dispatching harness; `to-subagent` issues blocking calls to non-interactive subagents that return the result, deliverable validated before acceptance. Both consume an exact supplied directory without adding harness-native isolation. On direct invocation, an explicit isolation request composes the `worktree` primitive before dispatch; workflow-owned isolation arrives already prepared. `to-subagent` may additionally compose `staffing` for model and effort resolution. Every other skill reaches subagent dispatch solely by saying "via `to-subagent`".

**Stateful skill**: The top of the persistence axis — pure (writes nothing durable, e.g. `interview`) → effectful (durable artifacts, no resume state, e.g. `to-slices`) → stateful: its durable artifacts double as resume state, so a bare invocation reads them and continues exactly where the last session stopped — no human recap. State lives with the work, never in chat context or memory files; a session's last act is updating it. Examples: `backlog`, `shape`. Stateful skills get extra probe-eval attention on the resume-after-a-gap path, since mistakes compound across sessions.

**Repo context files**: The repo-owned strategic context a shaping session reads at intake, three files with three owners: `CONTEXT.md` (the domain glossary — `domain-modeling`), `PRODUCT.md` (strategy and the user-type roster — `experience-first`), `DESIGN.md` (the visual system — `bare-minimum-design`). Each is one line in the project instruction file's `## Context documents` index; creation and skeleton mechanics live with the owner skill. They carry domain and direction; playbooks under `docs/agents/` carry operational bindings — a shaping decision consults the former, a build step the latter.

**Skill source**: `skills/<category>/<name>/` — the canonical skill this repo exists to publish. All authoring happens here; every install derives from it.

**Skill workspace**: `<name>-workspace/` at the repo root — the author-side space for the work _around_ a skill: evals, research, drafts, scratch artifacts. The shipped files live in the source; the workspace is never part of an install.

**Installed skill package**: The replaceable copy of a skill source a harness loads, installed with `npx skills add` — mounted at `.agents/skills/<name>` (always a real copied directory), with harness paths such as `.claude/skills/<name>` symlinked to it; no per-provider variants. A build product: an edit made in place is lost on the next refresh — the change belongs in the skill source, merged and reconciled from the changelog.

**Skill instance**: The project-owned materialization an installed package creates or maintains — an editable directory of scaffold, configuration, and artifacts, including the skill's mutable data: checkpoints, queues, decisions, resume artifacts. Project material, not a mount or a workspace; a package reinstall preserves it.

**Sibling skill**: Another skill in this repo relied on by name — a plain-language runtime pointer resolved by the installed skill set, never a file import. Example: `implement` routes defects through the `diagnosing-bugs` sibling.

**Reference skill**: An all-reference sibling cited by name and never run as a workflow: `writing-for-humans` (communication), `agent-ready-codebase` (repo readiness), `experience-first` (shaping decision order), `staffing` (roster and resolution). A reference skill stays model-invoked with a tight description, or siblings cannot cite it.

**External skill**: A relied-on skill whose canonical source lives outside this repo — declared in the consuming skill's `metadata.external`, installed only after provenance review and explicit consent, recorded in `external-dependencies.lock.json`. An adapted lift becomes our skill with README credits; an unmodified lift stays an external, never vendored. Standing example: `writing-for-agents` (mattpocock/skills). _Avoid_: external requirement.

**Playbook**: A repo-tuned markdown file under `docs/agents/`, written by an installed skill's setup (e.g. `environment.md`, `platform.md`). Skills speak in role nouns; the playbook binds those roles to this repo. Repo-owned once written — setups reconcile it, never overwrite it.

**Project agent instruction files**: The instruction files a project's harnesses read: `AGENTS.md` (the harness-neutral base) and `CLAUDE.md` (an `@AGENTS.md` import plus Claude Code deltas — Claude Code never reads `AGENTS.md` on its own). Skill prose says "the project instruction file" for whichever file the running harness reads.

**Global agent instruction files**: Machine-level instruction files such as `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` — retired on this machine (asher-skills#114); do not recreate them. A machine truth belongs to the skill that owns it or to `docs/agents/environment.md`.
