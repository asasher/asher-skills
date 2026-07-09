# Install, scope decision, reconciliation, and harness mechanics

## Two-layer install

The roster installs in two layers so the audited machine-wide truth is written once and each project records
only what differs.

- **Global base** — harness-coupled, written once from the [machine audit](machine-audit.md). It holds the
  full roster: the **audited rankings table**, the **generic routing rules**, the **task-pins**, the
  **capability matrix**, and the **CLI/tools mechanics**. Location depends on the harness the audit detected:
  - **Claude Code** → `~/.claude/CLAUDE.md`.
  - **Codex** → the global AGENTS layer, e.g. `~/.codex/AGENTS.md`.
  - If both harness layers exist on the machine, write the base to each so every harness reads the same
    roster.
- **Project override** — lives in the project's `docs/agents/` (a staffing playbook). It carries **only
  deltas** from the base — for example a stricter floor, one extra pin, or a capability correction for this
  repo. **It never re-copies the base.** If a project override restates the whole table, that is a bug: strip
  it back to just what differs.

### The resolver

To answer a staffing question in a project: **read the global base, then apply the project deltas on top.**
The base is the default; each delta overrides exactly the field it names (a stricter floor replaces the base
floor; an extra pin adds to the base pin list). Anything the override does not mention is inherited unchanged
from the base. Because overrides are sparse, what a project changed is legible at a glance, and drift between
base and override is obvious.

### Worked example — a project whose only difference is a stricter floor

Install for a repo that is identical to the machine default except it forbids staffing below a higher floor.
The override file contains **just that one delta** — the raised floor — and nothing else. It does **not**
copy the rankings table, the pins, or the capability matrix; those all resolve from the base. A correct
override here is a few lines naming the new floor; a full table copy is the failure mode.

## Scope-decision flow (on setup/invoke)

Choose the scope from an **audit of what is already installed** (machine-audit step 4), then:

- **Global staffing rules already exist** → **show them** to the user and **offer to add a project override**
  (deltas for the current repo). Do not silently overwrite the existing global base; extend it or layer a
  project override.
- **No staffing rules exist yet** → **ask** the user which install shape they want: **global-with-overrides**
  (write the global base now, projects add deltas later) or **project-only** (write just a project playbook,
  no global write). Then proceed down the chosen branch.

**Global writes are gated on consent.** Writing the global base touches the user's home-directory memory
(`~/.claude/` or `~/.codex/`), so it happens only after the user chooses a global branch in this flow —
never automatically, never as a side effect of a routing question.

## Reconciliation is an LLM audit — no version stamps

Re-invoking the skill (`reconcile`) **audits the installed base + overrides against this skill's own
definition** (its references and the intended roster shape) and **reports drift or conflict in prose** — e.g.
"the installed base lists a model the current harness can no longer reach", "the project override re-copies
the base table instead of carrying deltas", or "an override pin conflicts with a base pin". Read both layers,
compare them to the contract, and describe what is out of line and what to do about it.

This is a **deliberate departure** from the template-stamp approach used elsewhere (backlog stamps installed
sections with `<!-- ...: vNN -->` markers and reconciles by comparing version numbers). **Staffing introduces
no such stamp or marker.** Do not add a `vNN` comment, a hash, or any version token as the reconciliation
mechanism — reconciliation is the model reading the installed text and judging it against the skill, not a
number comparison. If you find yourself wanting to stamp a version to detect drift, that is the wrong
mechanism for this skill.

## CLI and tools mechanics (generic, harness-specializable)

The base carries the mechanics for reaching models the harness can't call natively. Write only the blocks for
tools the audit found present. A project override may specialize these; keep the generic form here.

### Codex CLI (include only if the audit found Codex installed)

- Some models are reachable only through the Codex CLI (e.g. gpt-5.5). Delegate with a self-contained prompt:
  `codex exec -s read-only --skip-git-repo-check` for investigation and review; `-s workspace-write` when it
  must edit. Add `-c tools.web_search=true -o <outfile>` for research runs.
- Codex runs can outlive shell timeouts — pass an explicit timeout, or run in the background and poll the
  outfile.
- Codex bills to its own subscription, which is why research and bulk fan-outs route there rather than to
  in-harness subagent fleets.

### Harness-specific mechanics (a project or harness base specializes this)

The generic rule: **Claude-family models run via the harness's native model dispatch; a non-native model
(e.g. gpt-5.5) is reached through its CLI, wrapped so the harness can drive it.** The Claude Code
specialization, written into `~/.claude/CLAUDE.md` when that harness is detected:

- Claude models run via the Agent/Workflow `model` parameter.
- gpt-5.5 inside workflows/subagents needs a **wrapper**: the `model` parameter takes only Claude models, so
  spawn a thin wrapper agent (`model: 'sonnet', effort: 'low'`) whose prompt writes a self-contained codex
  prompt, runs `codex exec` via Bash, and returns the report (use a `schema` for structured output).
- **Label** these agents with a `gpt-5.5:` prefix (e.g. `{label: 'gpt-5.5:review-auth'}`) — the UI shows the
  wrapper's Claude model, so the label is the only signal the real worker is gpt-5.5.
- Parallel gpt-5.5 implementation agents use `isolation: 'worktree'` so codex edits don't collide.
- Token budgets count only Claude tokens; codex work is free and invisible to the budget.

A different harness writes its own equivalent into its own memory layer; the generic rule above is what a
project override or a new harness base specializes.
