# asher-skills

Skills Asher made or likes, kept in one repo so they can be installed elsewhere with
`npx skills add <repo-url> --skill <name>`.

## Layout

- `skills/<category>/<name>/` — one published skill per directory: `SKILL.md` (entry point), `README.md`, and optionally
  `reference/`, `templates/`, `scripts/`, `agents/`, `evals/`.
- `docs/agents/` — this repo's own project playbooks, written by the installed skills' setups
  (`backlog setup` and its siblings) plus the repo-authored `probe-evals.md` (the eval discipline).
- `<skill>-workspace/` dirs at the root — the working space for developing a skill: eval and test runs,
  research, scratch artifacts produced while building it; not part of any install.
- `research/` — durable general research dossiers; local-skill authoring research instead follows
  `<skill>-workspace/research/`. The `research` skill and `docs/agents/researching.md` own the boundary.
- `plans/`, `evidence/` — approved plan HTML and criterion-linked review proof respectively; neither is a
  catch-all for research or other human-reviewed artifacts. Working state, not part of any install.
- `.agents/skills/` — primary mounts for skills installed *into* this repo; `.claude/skills/` may hold alias
  mounts. Install provenance is tracked in `skills-lock.json`. See § Vocabulary.

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
  on refresh. Install provenance is tracked in `skills-lock.json`.
- **Primary installed skill mount** — the path `.agents/skills/<name>`, which must be a real copied directory
  exposing one installed skill package. It is never a symlink and never the consumer's skill instance.
- **Alias installed skill mount** — an optional harness path such as `.claude/skills/<name>`, which must be a
  symlink to the primary installed skill mount. There may be zero or more aliases; each exposes the same
  installed package and is not an independent copy.
- **Skill instance** — the consumer-owned project materialization created or maintained by running an
  installed package: an editable directory such as `control-plane/` containing scaffold, configuration,
  state, and artifacts. It is project material, not a package mount or author-side skill workspace, and a
  package reinstall must preserve it.
- **Skill state** — the mutable data inside or associated with a skill instance: checkpoints, queues,
  decisions, and resume artifacts. State is part of the consumer's ongoing work, while the instance is the
  broader materialization that may also contain editable configuration, scaffold, and durable artifacts.

How skills and instructions relate:

- **Sibling skill** — another skill in this repo that a skill relies on by name (§ Conventions:
  compose-by-name), e.g. `plan` presents through the `review-loop` sibling. A plain-language runtime
  pointer resolved by the installed skill set — never a file import.
- **External requirement** — a skill or Codex plugin relied on by a selected skill whose canonical source
  lives outside this repo and is declared in that skill source's `metadata.external`. It is not a sibling and
  is installed only after provenance review and explicit consent. Its consumer-owned record lives in
  `external-dependencies.lock.json`, separate from Asher-authored skill provenance.
- **Playbook** — a repo-tuned markdown file under `docs/agents/`, written by an installed skill's setup
  (e.g. `environment.md`, `platform.md`). Skills speak in role nouns; the playbook binds those roles to
  this repo's reality. Owned by the repo once written — setups reconcile them, never blindly overwrite.
- **Global agent instruction files** — the machine-level memory files every session on this machine
  loads: `~/.claude/CLAUDE.md` (Claude Code) and `~/.codex/AGENTS.md` (Codex). Carry machine truths —
  presentation conventions, the staffing base — never project specifics.
- **Project agent instruction files** — this repo's `AGENTS.md` (harness-neutral base; Claude Code never
  reads it natively, so `CLAUDE.md` inlines it via an `@AGENTS.md` import) and `CLAUDE.md` (that import
  plus Claude Code-specific additions and deltas). They extend and override the global files for work in
  this repo.

Kinds of skill:

- **Stateless skill** — each invocation is self-contained; nothing carries over between sessions.
- **Stateful skill** — maintains skill state in the consumer's working directory (for example `bayes`,
  `goodwork`, `backlog`), so a bare invocation reads it and resumes exactly where
  the last session left off — no human recap. State lives with the work, never in chat context or memory
  files; a session's last act is updating it. Stateful skills get extra probe-eval attention on the
  resume-after-a-gap path, since their mistakes compound across sessions.

## Conventions

- **Skills are self-contained at the file level.** A skill's files live in its own directory — it never
  imports another skill's files or a shared library. Installing one skill copies one directory.
- **Skills compose by name, not by file.** A skill may lean on a sibling skill by referring to it in plain
  language ("present it via the `review-loop` skill") — a runtime pointer resolved by the installed skill
  set, not a file dependency. Every skill declares its **dependency surface** as three kinds of pointer:
  *bundled references* (its own contract, shipped in-directory), *project playbooks* (repo-specific
  instructions installed under `docs/agents/`), *sibling skills* (other Asher-authored skills invoked by
  name), and declared *external requirements* (provenance-checked skills or Codex plugins installed by their
  provider after consent).
- **Copy a technique; extract a primitive.** A small, local technique is reused by copying its canonical
  files from the skill that has them and noting the source in the copy's header (e.g. `Adapted from
  skills/system/review-loop/scripts/review-server.py`) — improvements flow back to the canonical version
  deliberately, not automatically. A capability that several skills genuinely share — the review surface,
  model staffing — is instead extracted into its own skill and referenced by name, never forked into every
  caller.
- **Composers declare and degrade.** A skill that references siblings names them in its `SKILL.md`; the
  `setup-asher-skills` installer guarantees a project has the siblings a skill needs. Absent a sibling, a
  skill states the requirement rather than failing silently.
- Scripts are stdlib-only Python 3.
- Skills that must present well in Codex ship `agents/openai.yaml` (valid YAML naming the skill's
  interface, with `allow_implicit_invocation` set to match how the skill should trigger).
- New or reworked skills get a pre-deployment eval before first real use (`docs/agents/probe-evals.md`).

## Agent skills

These skills are installed for this project — self-hosted from this repo's categorized `skills/` sources,
so `skills-lock.json` records a local source. Re-run `setup-asher-skills` (audit mode)
to reconcile them against the repo.

| Skill | What it does here | Scope |
|-------|-------------------|-------|
| backlog | Runs issues through groom → plan → build → review to a merged PR | project |
| diagnosing-bugs | Runs the reusable six-phase defect diagnosis discipline | project |
| plan | Turns an intent into a reviewed plan held at an approval gate | project |
| prototype | Answers one design question with a throwaway artifact — keep the answer, delete the artifact | project |
| research | Establishes primary-source facts and observations, then separates supported inferences and unknowns | project |
| review-loop | Serves a rendered artifact for human sign-off and blocks until the verdict | project |
| staffing | Owns the model roster — who staffs which task (global base in `~/.claude/CLAUDE.md` § Staffing; this repo's deltas in `CLAUDE.md` § Staffing) | project |
| setup-asher-skills | The installer/auditor for this skill set — sets a project up, adds skills with their sibling closure, audits for drift | project |
| skill-loop | Iterates a skill through eval → revise cycles | project |
| writing-great-skills | Authoring guidance for writing skills (from mattpocock/skills) | project |

**How they fit together:** composers pull their siblings — `plan` and `prototype` use `review-loop`
(to sign off) and `staffing` (to pick the model); `research` uses `staffing` for bounded fan-out; `plan`
may consume research findings; `backlog` also uses `diagnosing-bugs` and `research` as work-type branches.
`staffing` and `review-loop` depend on nothing.

**Source & updates:** installed from this repo itself. To add a skill, change scope, or check for drift,
re-invoke `setup-asher-skills`; to refresh sources, install the complete desired local set in one atomic
`npx skills add <path-to-this-repo> --skill <names...> -y` command—sequential single-skill adds can replace
earlier selections. **Never `npx skills remove` here:** with the
lockfile's local source path it deletes the skill *source* under `skills/`, not just the installed copy —
uninstall by hand instead (remove the `.agents/skills/<name>` dir, the `.claude/skills/<name>` symlink,
and the lockfile entry).
