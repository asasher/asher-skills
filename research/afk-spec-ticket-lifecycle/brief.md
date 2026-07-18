# Brief: discovery-to-AFK lifecycle

## Question

How should this repository standardize the path from an idea or problem through user interview, optional
specification, ticket slicing, and AFK backlog execution—while reusing the useful mechanics of Matt Pocock's
`batch-grill-me`, correcting the unreliable spec/ticket handoffs, and making UX/UI practice a first-class part
of the lifecycle?

## Intended use

Inform the next refactors of the interview, `to-spec`, `to-tickets`, and `backlog` skill surfaces. This is a
design investigation, not an implementation plan and not approval to change those skills.

## Scope

- The current local `to-spec`, `to-tickets`, `backlog`, and `bare-minimum-ux` skill sources.
- Matt Pocock's current `batch-grill-me`, `grilling`, `to-spec`, and `to-tickets` sources.
- Primary requirements-elicitation research relevant to interview structure, prompts, follow-ups, prototypes,
  synthesis, and completion criteria.
- The current public Impeccable design workflow as a possible external design capability.

## Exclusions

- Choosing final skill names or directory layout.
- Writing an implementation plan or modifying tracker state.
- Treating one interview technique as universally best across every project and stakeholder population.
- Reproducing Impeccable's design rules inside this repository.

## Definitions

- **Strategic decision:** product, user, scope, UX, or cross-ticket judgment that requires explicit authority.
- **Tactical plan:** implementation choices an executor may make within an approved ticket's delegated authority.
- **Spec:** an optional durable artifact for decisions shared by multiple tickets or too substantial to live in
  one ticket.
- **Ticket:** the smallest independently executable and verifiable unit placed in the tracker.
- **Backlog:** the organizational queue and execution orchestrator; not the place where product intent is
  invented.
- **Execution-ready:** sufficient authority, context, acceptance, dependencies, and capability bindings exist
  for AFK execution without an expected human decision.

## As-of boundary

2026-07-18. Upstream GitHub sources were inspected at:

- `mattpocock/skills` commit `9603c1cc8118d08bc1b3bf34cf714f62178dea3b`
- `pbakaus/impeccable` commit `8967edc988ee146823bca3c51fcf51296e9dec18`

## Source map

This was a single-coordinator investigation with no parallel shards:

1. Compare local and upstream skill contracts.
2. Examine empirical and professional requirements-elicitation guidance.
3. Inspect Impeccable's design-context model and compare it with `bare-minimum-ux`.
4. Reconcile the findings into a lifecycle model and bounded recommendations.

## Sufficient answer

The answer is sufficient if it identifies the concern boundary, explains why `batch-grill-me` alone cannot
make specs or tickets reproducible, defines when a spec is optional, defines the admission contract for AFK
backlog execution, and shows where UX/UI knowledge enters and is verified.
