# Skill-building patterns

Reusable patterns that recur across the skills in this repo. Read this directory **before designing
infrastructure for a new or reworked skill** — review loops, evals, state, harness compatibility. Most of
what a collaborative skill needs already exists; the failure mode these docs prevent is reinventing it.

Each pattern doc names a **canonical implementation** (a real file in a real skill) and tells you how to
adopt it. Two rules govern the directory:

- **Rule of three.** A pattern earns a doc here once it has appeared in at least two skills and a third is
  plausible. One-off cleverness stays in its skill.
- **Copy with provenance, never extract.** Skills install standalone (`npx skills add`), so they can never
  depend on a shared library in this repo. Adopt a pattern by copying the canonical files into the new
  skill and noting the source in the copied file's header comment (e.g. `Adapted from
  skills/backlog/scripts/review-server.py`). Improvements flow back to the canonical version deliberately,
  not automatically.

## Patterns

| Pattern | One line | Canonical |
|---|---|---|
| [review-surface.md](review-surface.md) | **Superseded** — extracted into the `review-loop` skill; compose it by name, don't copy scripts | `review-loop` skill (extracted primitive) |
| [probe-evals.md](probe-evals.md) | Situated dry-run probes against executor models before shipping a skill; scripted invariant dry-runs for tool mechanics | maquette / fair-deal |
| [multi-session-state.md](multi-session-state.md) | Resumable workspace state so a bare command picks up exactly where the last session left off | bayes / goodwork |
| [codex-compat.md](codex-compat.md) | Ship `agents/openai.yaml` so the skill presents correctly when installed into Codex | backlog |

When a new pattern crosses the rule-of-three threshold, add a doc with this structure: **Problem · When to
use · Canonical implementation · How to adopt · Gotchas · Instances.**
