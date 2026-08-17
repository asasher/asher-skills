---
name: experience-first
description: The decision-ordering standard for shaping — users, then experience, then system behavior, then implementation. Use when building a shaping decision tree, structuring a spec, or routing a partially shaped ticket to its next shaper.
user-invocable: true
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Experience-first

The order shaping decisions are settled in: what the system looks like from outside before how it is built inside. This is a reference skill: it defines the standard; sibling skills cite it by name and apply it in place.

## The two registers

- **Experience register** — everything observable from outside the system: who the users are, what each affected user sees, touches, and does, and the system's behavior that no single user owns (background jobs, retention, side effects). Settled by product judgment; prototyped heavily.
- **Implementation register** — how it is achieved: schema, module architecture, interface design. Settled by technical judgment, and often derivable: once behavior is settled there is frequently one good design.

An operator, an admin, an API consumer, the support person reading logs — each is a user type, not a special case.

## The gradient

Work the registers as a gradient, from the outside in:

1. **Users** — select the affected user types from the project's user-type roster (a repo context-file fact, maintained like any glossary term; a change that invents a new type extends the roster through the context delta). The roster makes selection a checklist where recall would forget someone.
2. **Experience** — per affected type: what changes in what they see, touch, and do.
3. **System behavior** — observable behavior no single type owns.
4. **Implementation** — schema, modules, interfaces.

## The tree law

The experience register sits entirely above the implementation register in the decision tree: an implementation question enters the frontier only when the behavior that governs it is settled. Implementation questions asked beside open behavior questions are the failure this standard exists to end — a table column debated before anyone has said what the user does.

Answers may arrive out of register — a product answer that names a widget is a constraint to record, not a violation. Questions are what the ordering governs.

## The seam

When the experience register's frontier empties, say so: "Experience is settled — implementation is next. This is a handoff point." The user continues in the same sitting, or blesses the experience register and parks the subject for another shaper. One thread, one skill, a named pause — never a separate stage.

## Recommend, don't ask

In the implementation register, state the recommended design in the spec and surface only genuine forks — two defensible designs with real trade-offs — as questions. A design with one good answer is a spec statement the technical reviewer can veto, not a question that costs a round.

## Skipping and blessing

- A register whose frontier is empty is skipped, never ceremonially visited. A copy change has no implementation questions; a pure refactor has no experience questions; a settled ticket has neither.
- Blessing is per register, recorded against the spec's commit hash. A subject stays in shaping until every register it actually needs is blessed; which registers it needs is the routing judgment of whoever grooms it. A later commit reopens a register's blessing only when it **changes that register's text** — compare the register's sections at the blessed hash and at the head; unchanged text keeps its blessing, so implementation commits stack on top of a blessed experience without disturbing it.
- Implementation discoveries can invalidate blessed experience — infeasibility forces an edit to approved experience text, and that edit reopens the experience blessing by the same rule. No separate mechanism exists.
