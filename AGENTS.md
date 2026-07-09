# asher-skills

Skills Asher made or likes, kept in one repo so they can be installed elsewhere with
`npx skills add <repo-url> --skill <name>`.

## Layout

- `skills/<name>/` — one skill per directory: `SKILL.md` (entry point), `README.md`, and optionally
  `reference/`, `templates/`, `scripts/`, `agents/`, `evals/`.
- `docs/patterns/` — reusable skill-building patterns (evals, state, harness compat).
  **Read it before designing infrastructure for a new or reworked skill** — most of what a collaborative
  skill needs already exists as a documented, copyable pattern.
- `<skill>-workspace/` dirs at the root — working state from actually using the skills; not part of any
  install.

## Conventions

- **Skills are self-contained at the file level.** A skill's files live in its own directory — it never
  imports another skill's files or a shared library. Installing one skill copies one directory.
- **Skills compose by name, not by file.** A skill may lean on a sibling skill by referring to it in plain
  language ("present it via the `review-loop` skill") — a runtime pointer resolved by the installed skill
  set, not a file dependency. Every skill declares its **dependency surface** as three kinds of pointer:
  *bundled references* (its own contract, shipped in-directory), *project playbooks* (repo-specific
  instructions installed under `docs/agents/`), and *sibling skills* (other skills invoked by name).
- **Copy a pattern; extract a primitive.** A small, local technique is reused by copying its canonical
  files from `docs/patterns/` and noting the source in the copy's header (`docs/patterns/README.md`). A
  capability that several skills genuinely share — the review surface, model staffing — is instead
  extracted into its own skill and referenced by name, never forked into every caller.
- **Composers declare and degrade.** A skill that references siblings names them in its `SKILL.md`; the
  `setup-asher-skills` installer guarantees a project has the siblings a skill needs. Absent a sibling, a
  skill states the requirement rather than failing silently.
- Scripts are stdlib-only Python 3.
- Skills that must present well in Codex ship `agents/openai.yaml` (`docs/patterns/codex-compat.md`).
- New or reworked skills get a pre-deployment eval before first real use (`docs/patterns/probe-evals.md`).
