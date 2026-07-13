# Task Contract

## Identity and origin

Every durable task carries one stable `🆔 <id>`. Generate a compact unique ID programmatically when a task
first needs to move, block another task, or become an Opportunity's `nextAction`; never change it during a
move.

Its **origin** is exactly one known-home note:

- `Projects/<Name>.md` for delivery or project administration;
- `Opportunities/<Name>.md` for commercial pursuit work.

In `TODO.md`, put the task under an origin heading whose text is the note name or wikilink. That heading is
the routing key used by Stop Work. If the heading is ambiguous or its note is missing, stop and resolve the
origin before moving the task.

## Locations

A task exists in exactly one of these locations:

- `TODO.md` under its origin heading while active today;
- its origin's `## Backlog` while inactive;
- its origin's `## Done` after completion or cancellation.

Move the complete markdown line instead of copying it. Before and after a move, search the three location
classes for its ID. The precondition is one occurrence; the postcondition is one occurrence at the destination.
If zero or multiple occurrences exist, repair or report the ambiguity before continuing.

An Opportunity `nextAction` is a frontmatter reference to the task ID, not another copy of the task text.
Moving that task between its Opportunity backlog and `TODO.md` does not change `nextAction`.

## Statuses

- `[ ]` open, not started
- `[/]` in progress
- `[>]` deferred from today; valid only in `TODO.md`
- `[<]` scheduled on a calendar; counts as done for the day
- `[!]` blocked or waiting
- `[x]` done
- `[-]` cancelled

## Inline metadata

- `🆔 4ATLh` - stable task ID
- `⛔ 4ATLh` - blocking task ID; repeat for multiple blockers
- `🛫 2026-06-16` - start date for in-progress work
- `✅ 2026-06-22` - completion date
- `❌ 2026-06-22` - cancellation date
- `📅 2026-06-12` - due date
- `⏳ 2026-06-10` - planned date
- `🔁 every Monday` - recurrence
- `[🔗](url)` - calendar event on a scheduled task
- `#email`, `#deep-work` - context tags

A task is blocked until every referenced blocker is done. An unresolved blocker ID remains blocked and is
reported. Convert a nested implicit dependency into IDs on both task lines.

## TODO shape

```markdown
## 2026-07-13

### [[CBH - Quotient]]

- [/] Send revised proposal 🆔 p4nQ2 🛫 2026-07-13

### [[Metis]]

- [ ] Review feature requests 🆔 m8K2c
```

Remove empty headings. Keep calendar groupings only when they contain scheduled work.
