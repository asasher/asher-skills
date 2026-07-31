# asher-skills

Skills Asher made or likes, kept in one repo so they can be installed elsewhere with
`npx github:asasher/asher-skills install --skill <name>`.

## Layout

- `skills/<category>/<name>/` — one published skill per directory: `SKILL.md` (entry point), `README.md`, and optionally
  `reference/`, `templates/`, `scripts/`, `agents/`, `evals/`.
- `skills/in-progress/<name>/` — the holding category for skills under active development: mergeable to
  main and installable knowingly, but not yet graduated into a permanent category. A skill leaves
  in-progress when its field test passes; record the move in `skills/source-migration.json`.
- `docs/agents/` — this repo's own project playbooks, written by the installed skills' setups
  (`backlog setup` and its siblings) plus the repo-authored `probe-evals.md` (the eval discipline).
- `<skill>-workspace/` dirs at the root — the working space for developing a skill: eval and test runs,
  research, scratch artifacts produced while building it; not part of any install.
- `plans/`, `evidence/` — artifacts from running the loop on this repo (plan HTML, review evidence);
  working state, not part of any install.
- `site/` — the repo's documentation app (eventually skills.ashanjum.com): a static, framework-free viewer
  that renders skill sources live with dependency edges parsed from frontmatter. Maintained per
  `site/MAINTENANCE.md`; `site/check.py` gates manifest drift. Not part of any install.
- `tools/` — repo plumbing: the skill-catalog compiler (`catalog.py` + its tests); not part of any
  install.
- `.agents/skills/` — primary mounts for skills installed *into* this repo; `.claude/skills/` may hold alias
  mounts. Install provenance is tracked in `.agents/asher-skills/install.json`. See § Vocabulary.

## Vocabulary

This repo both authors skills and has skills installed into it, so the bare word "skill" is ambiguous.
Use these terms precisely — say which one you mean, and know which one you are touching.

Where a skill lives — three distinct places, three terms:

- **Skill source** — `skills/<category>/<name>/`. The canonical skill this repo exists to publish. All
  authoring happens here; every Asher-authored install is derived from it.
- **Skill workspace** — `<name>-workspace/` at the root. The author-side working space for *working on* a skill:
  running its evals and tests, research, drafts, and scratch artifacts from development. The skill's
  shipped files still live in the source — the workspace holds the work *around* them, and is never part
  of any install.
- **Installed skill package** — the replaceable copy of a skill source that a harness loads. It is a build
  product: never edit it in place — edit the catalog-resolved skill source and reinstall, or the edit is lost
  on refresh. Install provenance is tracked in `.agents/asher-skills/install.json`.
- **Primary installed skill mount** — the Codex path `.agents/skills/<name>`, always a real copied directory.
  For a declared provider variant it is the compiled Codex tree; otherwise it is the shared package.
- **Alias/provider installed skill mount** — a harness path such as `.claude/skills/<name>`. Unvaried skills
  use a symlink to the primary. A declared provider variant uses a separately compiled real directory plus
  `.agents/asher-skills/install.json`; an undeclared independent copy is invalid.
- **Skill instance** — the consumer-owned project materialization created or maintained by running an
  installed package: an editable directory such as `relay/` containing scaffold, configuration,
  state, and artifacts. It is project material, not a package mount or author-side skill workspace, and a
  package reinstall must preserve it.
- **Skill state** — the mutable data inside or associated with a skill instance: checkpoints, queues,
  decisions, and resume artifacts. State is part of the consumer's ongoing work, while the instance is the
  broader materialization that may also contain editable configuration, scaffold, and durable artifacts.

How skills and instructions relate:

- **Sibling skill** — another skill in this repo that a skill relies on by name (§ Conventions:
  compose-by-name), e.g. `implement` routes defects through the `diagnosing-bugs` sibling. A plain-language runtime
  pointer resolved by the installed skill set — never a file import.
- **External requirement** — a skill or Codex plugin relied on by a selected skill whose canonical source
  lives outside this repo and is declared in that skill source's `metadata.external`. It is not a sibling and
  is installed only after provenance review and explicit consent. Its consumer-owned record lives in
  `external-dependencies.lock.json`, separate from Asher-authored skill provenance.
- **Playbook** — a repo-tuned markdown file under `docs/agents/`, written by an installed skill's setup
  (e.g. `environment.md`, `platform.md`). Skills speak in role nouns; the playbook binds those roles to
  this repo's reality. Owned by the repo once written — setups reconcile them, never blindly overwrite.
- **Global agent instruction files** — the machine-level files a harness loads from the home directory when
  they exist: `~/.claude/CLAUDE.md` (Claude Code) and `~/.codex/AGENTS.md` (Codex). **Retired on this
  machine** (asher-skills#114) — staffing, their last content, moved into each repo's own playbook and the
  files were removed (backups: `evidence/114-global-staffing-retirement/`). Being unversioned and
  unreviewable, they were never a home for durable knowledge: a fact only they carry is invisible to a fresh
  clone, a cloud runner, and every diff. A machine truth belongs to the skill that owns it, or to this repo's
  `environment.md`; nothing goes here — do not recreate these files.
- **Project agent instruction files** — this repo's `AGENTS.md` (harness-neutral base; Claude Code never
  reads it natively, so `CLAUDE.md` inlines it via an `@AGENTS.md` import) and `CLAUDE.md` (that import
  plus Claude Code-specific additions and deltas). They extend and override the global files for work in
  this repo.

Kinds of skill: defined in `CONTEXT.md` (the two axes — primitive/composite/orchestrator and
pure/effectful/stateful — the layer law, and the agent-decision/shipped-script split).

## Staffing

Read `docs/agents/staffing.md` fully before model choice, delegation, child/worktree creation,
capability-provider work, watcher assignment, or route-loss fallback. It is the sole authority for this repo:
the complete roster and this repo's deltas, with per-harness eligibility, capability bindings, and
reachability in the machine-local overlay it declares (`docs/agents/local/staffing.md`). Claude Code and
Codex sessions read the same files.

Do not resolve from a home-directory roster or from the `staffing` skill's bundled seed. If a machine-level
staffing instruction is loaded ahead of this one, it is superseded — the repo's playbook wins.

If the playbook is missing, or its overlay is missing or stamped with a machine other than this one, say so
and run `staffing setup` rather than dispatching on rows nobody verified here.

## Context documents

Durable documents carrying this repo's domain and direction — read the one whose clause matches the work:

- `CONTEXT.md` — the domain glossary (skill kinds, layer law, shaping vocabulary); read before naming
  things or when a term of art is ambiguous.
- `docs/adr/` — architecture decision records, sequentially numbered; read before revisiting a settled
  structural decision, and write one when a hard-to-reverse call would otherwise look arbitrary later.

## Conventions

- **Skills are self-contained at the file level.** A skill's files live in its own directory — it never
  imports another skill's files or a shared library. Installing one skill copies one directory.
- **Skills compose by name, not by file.** A skill may lean on a sibling skill by referring to it in plain
  language ("dispatch it via the `to-subagent` skill") — a runtime pointer resolved by the installed skill
  set, not a file dependency. Every skill declares its **dependency surface** as three kinds of pointer:
  *bundled references* (its own contract, shipped in-directory), *project playbooks* (repo-specific
  instructions installed under `docs/agents/`), *sibling skills* (other Asher-authored skills invoked by
  name), and declared *external requirements* (provenance-checked skills or Codex plugins installed by their
  provider after consent).
- **Copy a technique; extract a primitive.** A small, local technique is reused by copying its canonical
  files from the skill that has them and noting the source in the copy's header (e.g. `Adapted from
  skills/software-development/serve-via-tailnet/scripts/review-server.py`) — improvements flow back to the canonical version
  deliberately, not automatically. A capability that several skills genuinely share — the review surface,
  model staffing — is instead extracted into its own skill and referenced by name, never forked into every
  caller.
- **Credits live in the README.** Skill content — `SKILL.md`, `reference/`, `templates/`, shipped playbook
  text — never carries external attribution; each skill's `README.md` (plus `THIRD_PARTY_LICENSES.md` where
  the license requires it) is the single home for source credits. Internal `Adapted from skills/...` pointers
  in copied script headers (previous bullet) are provenance plumbing, not credits, and stay.
- **Composers declare and degrade.** A skill that references siblings names them in its `SKILL.md`; an
  install carries a skill's sibling closure. Absent a sibling, a skill states the requirement rather than
  failing silently.
- Scripts are stdlib-only Python 3.
- Skills that must present well in Codex ship `agents/openai.yaml` (valid YAML naming the skill's
  interface, with `allow_implicit_invocation` set to match how the skill should trigger).
- New or reworked skills get a pre-deployment eval before first real use (`docs/agents/probe-evals.md`).

## Agent skills

These skills are installed for this project — self-hosted from this repo's categorized `skills/` sources,
so `install.json` records a local source. The mounts carry the v2 family. **This repo's mounts are real
copies, decoupled from the sources** (asher-skills#118) — exactly what a consumer repo gets, `staffing`
compiled per provider as everywhere. Editing a source changes nothing a running session reads: changes
land on a branch, merge when working, and reach the mounts only through the **reconcile step** — running
the refresh command below in the main checkout after a merge that touches `skills/`. Until then
`tools/install.py check` reporting drift against merged sources is the expected signal, not a fault.
`writing-great-skills` is an external (mattpocock/skills), recorded in
`external-dependencies.lock.json` and untouched by installs.

| Skill | What it does here | Scope |
|-------|-------------------|-------|
| backlog | Dispatcher: fans needs-shaping tickets into shaping threads, ready tickets into supervised build subagents | project |
| shape | Settles one subject's strategic decisions in an interactive thread | project |
| build | Runs one ticket to a review-ready change request | project |
| adversarial-review | Converges a change request to LGTM via reviewer and fixer subagents | project |
| code-review | Two-axis diff review — Standards (smell baseline) and Spec | project |
| implement | Routes one ticket: defect → diagnosing-bugs, new behavior → tdd | project |
| tdd | Red → green loop with pre-agreed seams and the anti-pattern list | project |
| diagnosing-bugs | Six-phase defect diagnosis behind a red-capable feedback loop | project |
| verify-your-work | Fresh-eyes verification of built changes — findings, never fixes | project |
| prove-your-work | Evidence package posted on the change request | project |
| merge-changes | Merges explicitly authorized changes; closes tickets, cleans worktrees and stacks | project |
| to-spec | Synthesizes the conversation into a spec deliverable | project |
| to-slices | Splits a direction into tracer-bullet tickets with blocking edges; a split parent becomes the capstone over its slices | project |
| to-backlog | Captures a conversation's loose items as work-typed, readiness-unlabeled tickets for groom's intake | project |
| interview | Frontier-round interview until shared understanding | project |
| domain-modeling | CONTEXT.md glossary and ADRs, written as decisions land | project |
| research | Primary-source dossiers with traceable claims | project |
| prototype | Throwaway artifact answering one design question | project |
| worktree | Project-owned prepare, inspect, and remove mechanics for isolated working copies | project |
| to-thread | Spawns named, attachable sessions through the outermost harness | project |
| to-subagent | Staffed non-interactive dispatch with a wake path | project |
| watch-until | Watches a target until a condition holds, then relays | project |
| serve-via-tailnet | Serves HTML artifacts on the tailnet, optionally annotated with verdicts — only on the user's explicit invocation, never as a default presentation path | project |
| handoff | Compacts the conversation into a handoff document | project |
| staffing | Owns the model roster; both harnesses resolve it from `docs/agents/staffing.md` (§ Staffing) | project |
| skill-loop | Iterates a skill through eval → revise cycles | project |
| writing-great-skills | Authoring guidance for writing skills (external: mattpocock/skills, see `external-dependencies.lock.json`) | project |

**How they fit together:** `backlog` is a dispatcher. `to-backlog` is its intake feeder: any
conversation's loose items — bugs, ideas, follow-ups — land as work-typed tickets with no readiness
role. `backlog groom` sweeps tickets carrying no readiness role and
`needs-shaping` tickets into user-confirmed batches, then prepares one project-owned worktree and fans
one interactive shaping thread per batch via `to-thread`, including the single-batch case; each runs
`shape` — one engine per
subject, composing `interview` and `domain-modeling`, dispatching `research` and `prototype` through
`to-subagent` — and a settled subject crystallises automatically via `to-spec` (the spec on its ticket,
diagram first), the thread watching the spec'd tickets for AFK comments until the user blesses
readiness. A changed shaping branch merges and cleans up before the batch advances atomically.
`to-slices` splits a spec'd ticket into born-shaped child slices only on the user's
approval, the parent staying alive as the `capstone` over them — undispatchable while any child is
open, closing with a coverage check once they're done. `backlog build` fans ready, unblocked tickets with no open children into
worktree-isolated subagents it babysits — building is autonomous, so outcomes flow back; each runs
`build`: `implement` (defect → `diagnosing-bugs`, new behavior
→ `tdd`) → `verify-your-work` (the thread fixes) → change request → `adversarial-review` (driver-run
`code-review` passes to convergence) → `prove-your-work`, all in the issue's one project-owned
worktree. `merge-changes` remains the explicit human
authorization gate after a review-ready change request. `to-subagent` is the single staffing-aware
dispatch route; both dispatch adapters consume prepared directories and never add harness-native
isolation.

**Source & updates:** installed from this repo itself, via this repo's own installer — **not
`npx skills add`**, which cannot install these skills correctly (it ignores `metadata.variants`, so
`staffing` lands as uncompiled source with no roster; it skips directories named `build`; and it never
removes a skill dropped from the set — asher-skills#103).

```sh
python3 tools/install.py install --self --into .            # refresh the recorded set — also the post-merge reconcile
python3 tools/install.py install --self --into . --skill …  # change the set
```

**Reconcile:** after a merge to main that touches `skills/`, run the refresh in the main checkout so the
mounts catch up to the merged sources. Nothing updates implicitly; sessions pick the change up at their
next start. The refresh prints a `setup_report` (below) naming which of the freshly copied skills need
their setup re-run — copying a source forward does not re-run the setup that source's playbooks came from.

A bare `install` refreshes exactly the set `.agents/asher-skills/install.json` already records, so it can
never silently widen a curated selection; naming `--skill` sets the selection, and anything dropped from it
is removed in the same pass. Only skills that file records are ever pruned — third-party and external
mounts are untouchable.

Every install ends with a `setup_report` in its JSON output, summarized on stderr for whoever is reading
the terminal: `changed` — the installed skills whose source moved since the recorded revision, plus any
newly mounted here, whose setup has never run against this repo — and `setup_order` — the subset of those
declaring a setup, in the catalog's resolution order. Setups are agent-run: they bring repo-owned playbooks
into line and sometimes ask the user, so the installer names them and invokes nothing.

`basis` says how much to trust the set. `revision-diff` is a real comparison; `first-install` and
`unknown-revision` both report **every** installed skill as changed, because an unanswerable comparison
must not read as nothing-to-do. `unknown-revision` covers four cases: a revision the source clone lacks,
a recorded revision that is not an object name at all, a source tree carrying no git history — which
is what the installer runs from under `npx`, since the published package ships no `.git` — and state
that cannot say which sources were uncommitted at the last install. Discrimination
is a property of installing from a checkout; from `npx`, expect the whole set every time.

Mounts are built from the working tree while the recorded revision is HEAD, so an install that followed
uncommitted work carries content no revision describes. The state file records which sources those were,
and the next install counts them as changed — reverting that work changes their mounts just as making it
did, and only the record makes that visible once the tree is clean again.

State is one first-party file. It records the set, each skill's source path, provider variants, the
source revision, and which sources were uncommitted against it — **no integrity hashes**. Drift is
answered on demand instead:

```sh
python3 tools/install.py check --into <repo>   # exit 1 and names the drifted files
```

That diffs each mount against the source it was built from, so it reports *which file* changed rather than
"hash mismatch", and there is no stored quantity to keep in sync. `skills-lock.json` belongs to a different
installer (`npx skills`); we read it once to migrate, strip our entries, and never write it again. Skills
are dev-time tooling — nothing here belongs in a project's CI.

Consumers install the same way without a checkout, since `npx` runs a public GitHub repo directly and
this package is never published:

```sh
npx github:asasher/asher-skills install --skill backlog build staffing …
```
