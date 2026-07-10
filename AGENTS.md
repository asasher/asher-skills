# asher-skills

Skills Asher made or likes, kept in one repo so they can be installed elsewhere with
`npx skills add <repo-url> --skill <name>`.

## Layout

- `skills/<name>/` — one skill per directory: `SKILL.md` (entry point), `README.md`, and optionally
  `reference/`, `templates/`, `scripts/`, `agents/`, `evals/`.
- `docs/agents/` — this repo's own project playbooks, written by the installed skills' setups
  (`backlog setup` and its siblings) plus the repo-authored `probe-evals.md` (the eval discipline).
- `<skill>-workspace/` dirs at the root — the working space for developing a skill: eval and test runs,
  research, scratch artifacts produced while building it; not part of any install.
- `plans/`, `evidence/` — artifacts from running the loop on this repo (plan HTML, review evidence);
  working state, not part of any install.
- `.agents/skills/` (+ `.claude/skills/` symlinks) — the skills installed *into* this repo, tracked in
  `skills-lock.json`. See § Vocabulary.

## Vocabulary

This repo both authors skills and has skills installed into it, so the bare word "skill" is ambiguous.
Use these terms precisely — say which one you mean, and know which one you are touching.

Where a skill lives — three distinct places, three terms:

- **Skill source** — `skills/<name>/`. The canonical skill this repo exists to publish. All authoring
  happens here; every install anywhere is a copy of it.
- **Skill workspace** — `<name>-workspace/` at the root. The working space for *working on* a skill:
  running its evals and tests, research, drafts, and scratch artifacts from development. The skill's
  shipped files still live in the source — the workspace holds the work *around* them, and is never part
  of any install.
- **Installed skill** — `.agents/skills/<name>`, the canonical installed copy, with a per-harness symlink
  at `.claude/skills/<name>`; tracked in `skills-lock.json`. This is what the harness loads when a skill
  runs *in this repo*. It is a build product of the source: never edit it in place — edit
  `skills/<name>/` and reinstall (`npx skills add <path-to-this-repo> --skill <name>`), or the edit is
  silently lost on the next reinstall.

How skills and instructions relate:

- **Sibling skill** — another skill in this repo that a skill relies on by name (§ Conventions:
  compose-by-name), e.g. `plan` presents through the `review-loop` sibling. A plain-language runtime
  pointer resolved by the installed skill set — never a file import.
- **External skill** — a skill relied on by name whose source lives *outside* this repo. **Reserved — we
  have none today**; if a skill ever actually depends on one, call it this so the out-of-repo provenance
  is explicit. (`writing-great-skills` is externally *sourced* from mattpocock/skills, but nothing relies
  on it, so it is just an installed skill.)
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
- **Stateful skill** — maintains its state in the working directory (a state artifact in the skill's
  workspace, e.g. `bayes`, `goodwork`, `backlog`), so a bare invocation reads it and resumes exactly where
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
  instructions installed under `docs/agents/`), and *sibling skills* (other skills invoked by name).
- **Copy a technique; extract a primitive.** A small, local technique is reused by copying its canonical
  files from the skill that has them and noting the source in the copy's header (e.g. `Adapted from
  skills/review-loop/scripts/review-server.py`) — improvements flow back to the canonical version
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

These skills are installed for this project — self-hosted from this repo's own `skills/` (the skill
sources above), so `skills-lock.json` records a local source. Re-run `setup-asher-skills` (audit mode)
to reconcile them against the repo.

| Skill | What it does here | Scope |
|-------|-------------------|-------|
| backlog | Runs issues through groom → plan → build → review to a merged PR | project |
| plan | Turns an intent into a reviewed plan held at an approval gate | project |
| prototype | Answers one design question with a throwaway artifact — keep the answer, delete the artifact | project |
| review-loop | Serves a rendered artifact for human sign-off and blocks until the verdict | project |
| staffing | Owns the model roster — who staffs which task (global base in `~/.claude/CLAUDE.md` § Staffing; this repo's deltas in `CLAUDE.md` § Staffing) | project |
| setup-asher-skills | The installer/auditor for this skill set — sets a project up, adds skills with their sibling closure, audits for drift | project |
| skill-loop | Iterates a skill through eval → revise cycles | project |
| writing-great-skills | Authoring guidance for writing skills (from mattpocock/skills) | project |

**How they fit together:** composers pull their siblings — `plan` and `prototype` use `review-loop`
(to sign off) and `staffing` (to pick the model); `backlog` uses all four. `staffing` and `review-loop`
depend on nothing.

**Source & updates:** installed from this repo itself. To add a skill, change scope, or check for drift,
re-invoke `setup-asher-skills`; to refresh an installed skill after editing its source, re-run
`npx skills add <path-to-this-repo> --skill <name>`. **Never `npx skills remove` here:** with the
lockfile's local source path it deletes the skill *source* under `skills/`, not just the installed copy —
uninstall by hand instead (remove the `.agents/skills/<name>` dir, the `.claude/skills/<name>` symlink,
and the lockfile entry).
