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
  installed package: an editable directory such as `control-plane/` containing scaffold, configuration,
  state, and artifacts. It is project material, not a package mount or author-side skill workspace, and a
  package reinstall must preserve it.
- **Skill state** — the mutable data inside or associated with a skill instance: checkpoints, queues,
  decisions, and resume artifacts. State is part of the consumer's ongoing work, while the instance is the
  broader materialization that may also contain editable configuration, scaffold, and durable artifacts.

How skills and instructions relate:

- **Sibling skill** — another skill in this repo that a skill relies on by name (§ Conventions:
  compose-by-name), e.g. `to-spec` presents through the `serve-via-tailnet` sibling. A plain-language runtime
  pointer resolved by the installed skill set — never a file import.
- **External requirement** — a skill or Codex plugin relied on by a selected skill whose canonical source
  lives outside this repo and is declared in that skill source's `metadata.external`. It is not a sibling and
  is installed only after provenance review and explicit consent. Its consumer-owned record lives in
  `external-dependencies.lock.json`, separate from Asher-authored skill provenance.
- **Playbook** — a repo-tuned markdown file under `docs/agents/`, written by an installed skill's setup
  (e.g. `environment.md`, `platform.md`). Skills speak in role nouns; the playbook binds those roles to
  this repo's reality. Owned by the repo once written — setups reconcile them, never blindly overwrite.
- **Global agent instruction files** — the machine-level files every session on this machine loads:
  `~/.claude/CLAUDE.md` (Claude Code) and `~/.codex/AGENTS.md` (Codex). Being unversioned and unreviewable,
  they are **not** a home for durable knowledge: a fact only they carry is invisible to a fresh clone, a
  cloud runner, and every diff. Staffing moved out of them for exactly that reason. A machine truth belongs
  to the skill that owns it, or to this repo's `environment.md`; nothing new goes here.
- **Project agent instruction files** — this repo's `AGENTS.md` (harness-neutral base; Claude Code never
  reads it natively, so `CLAUDE.md` inlines it via an `@AGENTS.md` import) and `CLAUDE.md` (that import
  plus Claude Code-specific additions and deltas). They extend and override the global files for work in
  this repo.

Kinds of skill: defined in `CONTEXT.md` (the two axes — primitive/composite/orchestrator and
pure/effectful/stateful — the layer law, and the agent-decision/shipped-script split).

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
  language ("present it via the `serve-via-tailnet` skill") — a runtime pointer resolved by the installed skill
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
so `install.json` records a local source. The mounts carry the v2 family. **This repo's mounts are
live symlinks** into `skills/<category>/<name>`, so editing a source *is* editing the mount and they can
never go stale; `staffing` is the one exception, compiled per provider because a compiled tree has no
on-disk source to point at. `writing-great-skills` is an external (mattpocock/skills), recorded in
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
| to-tickets | Splits a direction into tracer-bullet tickets with blocking edges | project |
| interview | Frontier-round interview until shared understanding | project |
| domain-modeling | CONTEXT.md glossary and ADRs, written as decisions land | project |
| research | Primary-source dossiers with traceable claims | project |
| prototype | Throwaway artifact answering one design question | project |
| to-thread | Spawns named, attachable, harness-native background sessions | project |
| to-subagent | Staffed non-interactive dispatch with a wake path | project |
| watch-until | Watches a target until a condition holds, then relays | project |
| serve-via-tailnet | Serves HTML artifacts on the tailnet, optionally annotated with verdicts | project |
| handoff | Compacts the conversation into a handoff document | project |
| staffing | Owns the model roster; each harness loads its global module plus this repo's deltas | project |
| skill-loop | Iterates a skill through eval → revise cycles | project |
| writing-great-skills | Authoring guidance for writing skills (external: mattpocock/skills, see `external-dependencies.lock.json`) | project |

**How they fit together:** `backlog` is a dispatcher. `backlog groom` sweeps unlabeled and
`needs-shaping` tickets into user-confirmed batches, then fans one interactive shaping thread per batch
via `to-thread` (a single batch runs in the groom session itself); each runs `shape` — one engine per
subject, composing `interview` and `domain-modeling`, dispatching `research` and `prototype` through
`to-subagent` — and a settled subject crystallises automatically via `to-spec` (the spec on its ticket,
diagram first), the thread watching the spec'd tickets for AFK comments until the user blesses
readiness; `to-tickets` supersedes a spec'd ticket with born-shaped children only on the user's
approval. `backlog build` fans ready tickets into
worktree-isolated subagents it babysits — building is autonomous, so outcomes flow back; each runs
`build`: `implement` (defect → `diagnosing-bugs`, new behavior
→ `tdd`) → `verify-your-work` (the thread fixes) → change request → `adversarial-review` (`code-review`
plus `watch-until` convergence) → `prove-your-work`. `merge-changes` remains the explicit human
authorization gate after a review-ready change request. `to-subagent` is the single staffing-aware
dispatch route.

**Source & updates:** installed from this repo itself, via this repo's own installer — **not
`npx skills add`**, which cannot install these skills correctly (it ignores `metadata.variants`, so
`staffing` lands as uncompiled source with no roster; it skips directories named `build`; and it never
removes a skill dropped from the set — asher-skills#103).

```sh
python3 tools/install.py install --self --into .            # refresh the recorded set
python3 tools/install.py install --self --into . --skill …  # change the set
```

A bare `install` refreshes exactly the set `.agents/asher-skills/install.json` already records, so it can
never silently widen a curated selection; naming `--skill` sets the selection, and anything dropped from it
is removed in the same pass. Only skills that file records are ever pruned — third-party and external
mounts are untouchable.

State is one first-party file. It records the set, each skill's source path, provider variants, and the
source revision — **no integrity hashes**. Drift is answered on demand instead:

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
