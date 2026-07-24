# Playbook: Change Description

> Project playbook for this repo. The `build` skill's create-PR step reads this file for the body structure; the orchestration constraints (ready-for-review not draft, base branch, the deferred evidence capture) live in that skill, and where the PR physically lives — GitHub, a committed review file, elsewhere — in `platform.md` § Change review. Tailor the outline to this team's conventions.

## Body outline

The body is the index for this change's evidence. In order:

- The close linkage per `platform.md` (GitHub: `Closes #<issue-number>`; local: name the issue whose `state` flip rides this branch) and the work-type.
- **Summary** — what changed and why, in the issue's terms, including any scope discovery that shaped the change (e.g. "the backend already supported this end to end, so this is frontend-only").
- **Changes** — the significant files/modules with the design reasoning a reviewer needs (why a save lands on this action, why a component was extracted), not a raw file list.
- **Plan** (enhancements) — SHA-pinned link to the committed plan, noting where it was approved.
- **Checks run** — each command and its result (`codebase.md` § Checks: the probe eval, `py_compile`, driven scripts).
- **CI status** — this repo has no CI, so state that plainly: readiness is the green probe eval + review `LGTM`, not a status check. On a repo with CI, this line names the gate and whether it is green.
- **Verification** — what stack the criteria were exercised against and the per-criterion outcome, including the verify step's recorded caveats: any criterion verified through a workaround names the gap and the substitute observation, framed as environment gaps vs product issues. Disclosed limitations, never silent claims.
- **Evidence** — normally a placeholder: "Captured after review converges." Filled by the evidence step per `evidence.md`. For `research`, use **Research dossier** instead: link the canonical dossier, state its as-of boundary and claim-audit result, and do not promise a duplicate evidence package.

## This repo

- Title convention, required sections beyond the outline, or an existing PR template to honor: no PR template — use the outline. Title: imperative, sentence-case (matching the commit style in `codebase.md` § Conventions). Include a `Closes #<n>` line so the issue closes on merge (`platform.md` § Tracker). Under Claude Code, the PR body ends with the harness's own `🤖 Generated with [Claude Code](https://claude.com/claude-code)` line.
