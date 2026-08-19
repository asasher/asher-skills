---
name: experience-first
description: Use when shaping, designing or implementing any change to the system, product decision, ux or feature-scope trade-off. Chose user delight over implementation convenience.
---

# Experience-first

The product is the experience. Every technical decision either helps or hurts it. When implementation convenience conflicts with user delight, choose delight.

- Say no to 1,000 things (every feature, control, and option must earn its place)
- Ship less, ship better (polished experience with three features beats rough one with ten)
- Prototype before committing (design decisions are cheaper in throwaway HTML than production code)
- Sweat the details (transitions, alignment, spacing, feedback, error states)
- Tighten the core loop (every feature should serve the central workflow or get out of the way)

The user is whoever consumes the work. For a UI that is the end user. For a library or an internal API it is the colleague who imports it. The engineer who maintains the code next is a user too. Weigh their experience the same way, and explain impact from their seat.

Foundations should serve the experience, not the other way around. Foundational thinking governs the sequence of work; this principle governs the target.

Design from outside-in, starting from the users' experience first.

## The two registers

- **Experience register** — what users are there, how do they currently experience and interact with the product and how will their observable experience be different after this change. This also applies to system behaviors that users don't directly interact with but experience the effects of (background jobs, retention, side effects etc).
- **Implementation register** — how it is achieved: seams, schema, module architecture, interface design. Settled by technical judgment, and often derivable: once behavior is settled there is frequently one good design.

## The gradient

Work the registers as a gradient, from the outside in:

1. **Users** — select the affected user types from the roster in the project's `PRODUCT.md`, if we need a new type of user record it there as well. If no `PRODUCT.md` exists create it lazily using [PRODUCT-FORMAT](./PRODUCT-FORMAT.md).
2. **Experience** — per affected type: what changes in what they see, touch, and do and experience.
3. **System behavior** — observable behavior that is shared across users or is only experienced indirectly.
4. **Implementation** — seams, schema, modules, interfaces etc

## The tree law

The experience register sits entirely above the implementation register in the decision tree: an implementation question enters the frontier only when the behavior that governs it is settled. Implementation questions asked beside open behavior questions are the failure this standard exists to end — a table column debated before anyone has said what the user does.

Answers may arrive out of register — a product answer that names a widget is a constraint to record, not a violation. Questions are what the ordering governs.

## The seam

When the experience register's frontier empties, say so: "Experience is settled — implementation is next. This is a handoff point." The user continues in the same sitting, or blesses the experience register and parks the subject for another shaper.

## Recommend, don't ask

In the implementation register, state the recommended design in the spec and surface only genuine forks — two defensible designs with real trade-offs — as questions. A design with one good answer is a spec statement the technical reviewer can veto, not a question that costs a round.

## Skipping and blessing

- A register whose frontier is empty is skipped, never ceremonially visited. A copy change has no implementation questions; a pure refactor has no experience questions; a settled ticket has neither.
- Blessing is per register, recorded against the spec's commit hash. A subject stays in shaping until every register it actually needs is blessed; which registers it needs is the routing judgment of whoever grooms it. A later commit reopens a register's blessing only when it **changes that register's text** — compare the register's sections at the blessed hash and at the head; unchanged text keeps its blessing, so implementation commits stack on top of a blessed experience without disturbing it.
- Implementation discoveries can invalidate blessed experience — infeasibility forces an edit to approved experience text, and that edit reopens the experience blessing by the same rule. No separate mechanism exists.
