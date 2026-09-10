# Capture

Captures the loose items a conversation has surfaced (bugs reported in passing, enhancement ideas, follow-ups) as minimal work-typed GitHub issues, each carrying its chat context but no readiness label. It is capture, not decomposition: several unrelated undecided things into the intake queue. One decided thing into ordered parts is the `to-slices` sibling.

## When to use

- **Mid-interview or mid-shaping**: the user names bugs and ideas that are not this thread's subject; sweep them into issues instead of losing them with the chat.
- **Mid-build**: work surfaces adjacent items or gaps in an approved spec parent's direction; `capture <parent>` attaches those gaps as sub-issues that block the spec parent.
- **After user testing**: group distinct findings in a named milestone, with shared session context in its description.
- **Any conversation that accumulated work nobody wrote down.** `backlog capture` is the same move from the dispatcher.

Not for splitting a spec (`to-slices`), not for routing or readiness (grooming), not for writing a direction (`to-spec`).

## Shape

Sweep, confirm, publish, readback. One compact list (title, work-type, context note), and nothing publishes before the user approves. A requested batch uses a milestone. With an approved spec parent argument, each captured gap is attached as its sub-issue and blocker. [Milestone grouping](../backlog/reference/milestones.md) covers inheritance, conflicting assignments, and migration from organizational parents.

## Provenance

Formerly `to-backlog`. No external sources.
