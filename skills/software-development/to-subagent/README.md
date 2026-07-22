# To Subagent

Dispatch adapter for non-interactive work: staffs the subagent from the roster (degrading to the parent's
model when no roster is installed), requires a self-contained prompt whose final message is the
deliverable, isolates file-editing work in a worktree (created in one step, never by switching the
primary checkout), and wires a wake path so the dispatcher learns of
completion without polling. One call
dispatches one subagent; how many a piece of work needs is the caller's decision.

## When to use

- Any skill or session needs work done outside its own context — a lookup, a probe, a verification pass,
  an implementation — without the user attending it.
- It is the single sanctioned route to `staffing`: other skills dispatch "via `to-subagent`" instead of
  reading the roster themselves.

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Siblings (optional, by name):** `staffing` — roster and wake-path ladder; absent it, the subagent
  runs on the dispatching session's model and effort.

## Provenance

No external sources.
