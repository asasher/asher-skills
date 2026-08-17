# asher-skills

Skills Asher made or likes, kept in one repo so they can be installed elsewhere with `npx skills add github:asasher/asher-skills --skill <name>`.

## Layout

- `skills/<category>/<name>/` — one published skill per directory: `SKILL.md` (entry point), `README.md`, and optionally `reference/`, `templates/`, `scripts/`, `agents/`, `evals/`.
- `skills/in-progress/<name>/` — the holding category for skills under active development: mergeable to main and installable knowingly, but not yet graduated into a permanent category. A skill leaves in-progress when its field test passes; record the move in `skills/source-migration.json`.
- `CHANGELOG.md` — the reconcile ledger. Every merge that changes `skills/` appends an entry naming the skills it touched and the setups to re-run. Consumers (this repo included) reconcile from it — see § Agent skills.
- `docs/agents/` — this repo's own project playbooks, written by the installed skills' setups (`backlog setup` and its siblings) plus the repo-authored `probe-evals.md` (the eval discipline).
- `<skill>-workspace/` dirs at the root — the working space for developing a skill: eval and test runs, research, scratch artifacts produced while building it; not part of any install.
- `plans/`, `evidence/` — artifacts from running the loop on this repo (plan HTML, review evidence); working state, not part of any install. Evidence media (screenshots, video) is never committed — it uploads via the `to-web` skill and is referenced by URL.
- `artifact/*` branches — specs, prototypes, and research dossiers as HTML: version-controlled while useful, never merged to main, deleted when spent. Named `artifact/<ticket>-<slug>` (`artifact/<slug>` when ticketless). Every sweep skips them on purpose.
- `site/` — the repo's documentation app (eventually skills.ashanjum.com): a static, framework-free viewer that renders skill sources live with dependency edges parsed from frontmatter. Maintained per `site/MAINTENANCE.md`; `site/check.py` gates manifest drift. Not part of any install.
- `.agents/skills/` — primary mounts for skills installed _into_ this repo; `.claude/skills/` holds symlink alias mounts. See § Vocabulary.

## Vocabulary

This repo both authors skills and has skills installed into it, so the bare word "skill" is ambiguous. Use these terms precisely — say which one you mean, and know which one you are touching.

Where a skill lives — three distinct places, three terms:

- **Skill source** — `skills/<category>/<name>/`. The canonical skill this repo exists to publish. All authoring happens here; every install is derived from it.
- **Skill workspace** — `<name>-workspace/` at the root. The author-side working space for _working on_ a skill: running its evals and tests, research, drafts, and scratch artifacts from development. The skill's shipped files still live in the source — the workspace holds the work _around_ them, and is never part of any install.
- **Installed skill package** — the replaceable copy of a skill source that a harness loads, installed with `npx skills add`. It is a build product: never edit it in place — edit the skill source, merge, and reconcile from the changelog, or the edit is lost on the next refresh.
- **Primary installed skill mount** — the path `.agents/skills/<name>`, always a real copied directory.
- **Alias installed skill mount** — a harness path such as `.claude/skills/<name>`, a symlink to the primary. There are no per-provider variants: one source, one package, harness-specific guidance as context pointers inside the skill text.
- **Skill instance** — the consumer-owned project materialization created or maintained by running an installed package: an editable directory containing scaffold, configuration, state, and artifacts. It is project material, not a package mount or author-side skill workspace, and a package reinstall must preserve it.
- **Skill state** — the mutable data inside or associated with a skill instance: checkpoints, queues, decisions, and resume artifacts.

How skills and instructions relate:

- **Sibling skill** — another skill in this repo that a skill relies on by name (§ Conventions: compose-by-name), e.g. `implement` routes defects through the `diagnosing-bugs` sibling. A plain-language runtime pointer resolved by the installed skill set — never a file import.
- **Reference skill** — an all-reference sibling cited by name and never run as a workflow: `writing-for-humans` (the communication standard), `agent-ready-codebase` (the repo-readiness standard), `experience-first` (the shaping decision-ordering standard), `staffing` (the roster and resolution doctrine). Reference skills stay model-invoked with tight descriptions, or siblings cannot cite them.
- **External requirement** — a skill relied on whose canonical source lives outside this repo, declared in the consuming skill source's `metadata.external` and installed only after provenance review and explicit consent. Its consumer-owned record lives in `external-dependencies.lock.json`. The rule: an adapted lift becomes our skill with README credits; an unmodified lift stays an external, never vendored. `writing-for-agents` (mattpocock/skills) is the standing example.
- **Playbook** — a repo-tuned markdown file under `docs/agents/`, written by an installed skill's setup (e.g. `environment.md`, `platform.md`). Skills speak in role nouns; the playbook binds those roles to this repo's reality. Owned by the repo once written — setups reconcile them, never blindly overwrite.
- **Global agent instruction files** — retired on this machine (asher-skills#114); do not recreate `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md`. A machine truth belongs to the skill that owns it or to this repo's `environment.md`.
- **Project agent instruction files** — this repo's `AGENTS.md` (harness-neutral base; Claude Code never reads it natively, so `CLAUDE.md` inlines it via an `@AGENTS.md` import) and `CLAUDE.md` (that import plus Claude Code-specific additions and deltas).

## Staffing

Read `docs/agents/staffing.md` before model choice, delegation, or dispatch. It is the sole authority for this repo: the roster's judgment numbers (cost, intelligence, taste, effort), the pins, and the repo deltas. Resolution follows the `staffing` reference skill's doctrine — **bars, then cheapest**: state the intelligence and taste bars the task needs, remove every model below them, take the cheapest survivor; escalate without asking when cheaper output misses the bar. There is no machine overlay and no probe record: routes are tried at the point of use, and a failure warns and falls back to the next survivor. If the playbook is missing, run `staffing setup` (a template fill plus a repo-deltas interview).

## Context documents

Durable documents carrying this repo's domain and direction — read the one whose clause matches the work:

- `CONTEXT.md` — the domain glossary (skill kinds, layer law, shaping vocabulary); read before naming things or when a term of art is ambiguous. It is also the approved technical dictionary of the `writing-for-humans` standard.
- `docs/adr/` — architecture decision records, sequentially numbered; read before revisiting a settled structural decision, and write one when a hard-to-reverse call would otherwise look arbitrary later.

## Conventions

- **Skills are self-contained at the file level.** A skill's files live in its own directory — it never imports another skill's files or a shared library. Installing one skill copies one directory.
- **Skills compose by name, not by file.** A skill may lean on a sibling skill by referring to it in plain language ("dispatch it via the `to-subagent` skill") — a runtime pointer resolved by the installed skill set, not a file dependency. The dependency record has one machine-readable home — frontmatter `requires`/`optional` (plus `metadata.external`) — and each dependency's degradation is stated inline at its point of use. A closing "Dependency surface" section appears only where it indexes dependencies the body scatters across many sections or files; it never restates what the body already carries.
- **Composers declare and degrade.** A skill that references siblings names them in its `SKILL.md`; an install carries a skill's sibling closure. Absent a sibling, a skill states the requirement rather than failing silently.
- **Copy a technique; extract a primitive.** A small, local technique is reused by copying its canonical files and noting the source in the copy's header — improvements flow back deliberately. A capability several skills genuinely share is extracted into its own skill and referenced by name, never forked into every caller.
- **Credits live in the README.** Skill content never carries external attribution; each skill's `README.md` (plus `THIRD_PARTY_LICENSES.md` where the license requires it) is the single home for source credits.
- **User-facing text follows the `writing-for-humans` reference skill** — ASD-STE100 discipline, `CONTEXT.md` as the dictionary, no bare ticket/PR numbers.
- **Main carries only what must stay true.** Anything with a shelf life — specs, prototypes, dossiers, one-work verification scripts, evidence media — lives on `artifact/*` branches, in the tracker, or on the artifact store; never on main.
- **A merge that changes `skills/` writes its `CHANGELOG.md` entry** naming the changed skills and the setups to re-run — the build lands the delta, applied to this repo itself.
- **A work branch pushes early and often.** Commits on work, feature, and artifact branches reach the remote as they land — the remote is the backup. Pushing is not publication; the change request is. Holding work local until PR time is the failure this rule ends.
- Scripts are stdlib-only Python 3.
- **Prose is unwrapped.** Markdown paragraphs and bullets are single lines — no fill-column hard wrapping; let the editor soft-wrap. Enforced by Prettier (`.prettierrc`, exclusions in `.prettierignore`): `npx prettier@3.6.2 --check '**/*.md'` is the gate, `--write` the fix. Installed mounts and workspaces are excluded.
- Skills that must present well in Codex ship `agents/openai.yaml` (valid YAML naming the skill's interface, with `allow_implicit_invocation` set to match how the skill should trigger).
- New or reworked skills get a pre-deployment eval before first real use (`docs/agents/probe-evals.md`).

## Agent skills

These skills are installed for this project — self-hosted from this repo's categorized `skills/` sources. `writing-for-agents` is an external (mattpocock/skills), recorded in `external-dependencies.lock.json` and untouched by installs.

| Skill | What it does here | Scope |
| --- | --- | --- |
| backlog | Dispatcher: `groom` routes and merges tickets then fans shaping threads; `build` claims ready tickets and fans build threads, then exits; `status` is the pure query and teardown arm | project |
| shape | Settles one subject's decisions in an attended thread; exits with a spec on an artifact branch, blessed at a commit hash | project |
| build-change | Runs one unit of work — a ticket, or spec'd work without one — to a review-ready change request in one worktree; stages via synchronous `to-subagent` | project |
| adversarial-review | Converges a change request to LGTM via reviewer and fixer subagents | project |
| code-review | Two-axis diff review — Standards and Spec | project |
| implement | Routes one unit: defect → diagnosing-bugs, new behavior → tdd; lands the spec's context delta when its change makes the terms true | project |
| tdd | Red → green loop with pre-agreed seams and the anti-pattern list | project |
| diagnosing-bugs | Six-phase defect diagnosis behind a red-capable feedback loop | project |
| verify-your-work | Runs the spec-declared proof split: durable criteria get suite tests, throwaway checks run as scaffolding — findings, never fixes | project |
| prove-your-work | Evidence package on the change request; media via `to-web`, embedded by URL | project |
| merge-change | The human merge gate, per change: `delivered` on slice merges, the intent-tier conflict ladder, teardown of what it merges | project |
| to-spec | Writes the spec HTML to the artifact branch; the ticket gets a projection — summary, render URL, commit hash | project |
| to-slices | Presents a justified split and a landing shape (stacked default); publishes slices under the `spec` parent | project |
| to-backlog | Captures a conversation's loose items as work-typed, readiness-unlabeled tickets | project |
| interview | Frontier-round questioning: numbered, titled questions with recommended answers | project |
| domain-modeling | Terms and ADR drafts into the spec's context delta during shaping; direct writes only for what is already true | project |
| research | Primary-source dossier: every claim cited, an as-of boundary, the claim audit; HTML on an artifact branch | project |
| prototype | Throwaway artifact answering one design question — a self-contained HTML for logic, variants on one route for UI | project |
| worktree | Project-owned prepare, inspect, and remove mechanics for isolated working copies | project |
| to-thread | Spawns a named session in the outermost harness — detection first, five routes, liveness before success | project |
| to-subagent | Synchronous staffed dispatch: declaration first, deliverable validated before a success is accepted | project |
| watch-until | Watches a target until a condition holds, then relays | project |
| to-tailnet | Serves one HTML artifact over the tailnet — the deliberate don't-publish path | project |
| to-web | Uploads a file to the bound store and returns a durable hash-keyed URL — evidence's home, artifacts' preview deploy | project |
| writing-for-humans | Reference: the communication standard (ASD-STE100, CONTEXT.md dictionary, no bare numbers) | project |
| experience-first | Reference: the shaping decision-ordering standard — users → experience → system behavior → implementation, the seam, per-register blessing | project |
| agent-ready-codebase | Reference: the repo-readiness standard `backlog setup` certifies against | project |
| staffing | Reference: the roster and bars-then-cheapest resolution doctrine; playbook at `docs/agents/staffing.md` | project |
| handoff | Compacts the conversation into a handoff document | project |
| skill-loop | Iterates a skill through eval → revise cycles | project |
| retro | Tracked repo-level friction ledger; note as it happens, pass on request | project |
| writing-for-agents | Authoring guidance for documents agents consume (external: mattpocock/skills) | project |

**How they fit together:** `backlog` is a dispatcher with no supervision loop — the tracker is the ledger. `groom` routes captured tickets, merges small related ones into one shapeable subject (absorption; safe because slicing re-creates structure later), confirms a chat-readable plan, then fans attended shaping threads via `to-thread` at a width the user picks. Each thread runs `shape` on one subject — composing `interview` and `domain-modeling`, dispatching `research` and `prototype` via `to-subagent` — and exits when `to-spec` has written the spec to its artifact branch and the user has blessed a commit hash; nothing from shaping ever merges, and the spec carries the context delta and the test split for the build to land. `to-slices`, on the user's call, splits a blessed spec into slices under the `spec`-typed parent and picks a landing shape — stacked by default: a feature branch whose root commit is the context delta, slice PRs into it, the parent's own PR being the feature→main merge that closes all children. `backlog build` claims ready tickets (children all closed or `delivered`), posts the dispatch declaration as the claim comment — model, effort, harness, absolute deadline — fans one unattended `build-change` thread per ticket via `to-thread`, and exits; re-running it is idempotent. `build-change` runs implement → verify-your-work → change request → adversarial-review → prove-your-work in the ticket's one worktree, all stage dispatch synchronous. Outcomes land on the tracker; `backlog status` reads claims × worktrees × change requests × deadlines and derives finished, stalled, and abandoned — nothing is ever written as abandoned. `merge-change` remains the explicit human authorization gate. `agent-ready-codebase` defines what a repo must provide (the four-item checklist, use ≠ change); `backlog setup` certifies against it and writes the answers into `environment.md`; a repo that fails the gate does not dispatch builds.

**Source & updates:** install with the standard tool, then run the setups each installed skill declares:

```sh
npx skills add github:asasher/asher-skills --skill backlog build-change staffing …
```

**Reconcile:** after merges that touch `skills/`, read the `CHANGELOG.md` entries since your last reconcile; re-install the skills they name, remove mounts for skills dropped from your set, and re-run the setups the entries name. This repo reconciles its own mounts the same way. There is no first-party installer and no install-state file — the changelog is the record.
