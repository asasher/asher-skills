# Discovery-to-AFK lifecycle: findings

## Concise answer

The emerging direction is sound, but the lifecycle should not be encoded as a mandatory linear chain. It
should be a **progressive decision pipeline**:

`idea/problem → elicitation → durable decision record → optional spec → tickets → readiness admission → AFK backlog execution`

The spec is optional; the durable decision record is not. A small, settled change can become one ticket
directly. A direction spanning several tickets, containing shared product/UX decisions, or requiring coordinated
slicing earns a spec. The backlog is the organizational and execution unit. It should accept only work whose
strategic decisions are settled or explicitly delegated, while retaining freedom to make tactical implementation
choices.

Matt Pocock's `batch-grill-me` is a useful **round-based frontier scheduler for questions**, but it has no
coverage model, decision ledger, ambiguity audit, artifact playback, or execution-readiness test. Those missing
contracts—not a lack of persistence—explain why a long grill can still produce weak specs and tickets. The local
`to-spec` and `to-tickets` currently preserve the same gap: synthesis records unresolved questions without
blocking readiness, and ticket review confirms only granularity and dependency edges.

UX/UI should be a cross-cutting capability lane, not a final polish step. `bare-minimum-ux` is a valuable personal
policy overlay, while Impeccable supplies a broader design-context and critique system. UI work should bind both
where available: interview and shaping capture user tasks and design context; specs and tickets inherit it;
implementation loads the capability; verification checks states, responsiveness, accessibility, and visual fit.

## Facts and direct observations

### Local skill contracts

**O1 — `to-spec` assumes alignment already happened.** The local skill explicitly defines itself as pure
synthesis and sends unresolved matters to Notes instead of asking the user. It describes the spec as coarser than
a per-ticket plan. [Local `to-spec` lines 16–26 and 57–68](../../skills/delivery/to-spec/SKILL.md).

**O2 — `to-tickets` validates a narrow subset of readiness.** Its human quiz asks about ticket granularity and
blocking edges, after which it publishes; it leaves `ready-for-agent` to backlog grooming by default. It does not
state a check for inherited strategic decisions, UX states, acceptance completeness, authority, or unresolved
spec notes. [Local `to-tickets` lines 16–28 and 42–63](../../skills/delivery/to-tickets/SKILL.md).

**O3 — backlog's readiness gate is metadata-oriented.** Grooming clarifies ambiguous requirements, but its
explicit completion contract for `ready-for-agent` requires work type, surface, coordination class, and reason.
It does not require a linked approved decision artifact or prove that strategic decisions are closed.
[Local `groom` lines 17–34](../../skills/delivery/backlog/reference/groom.md).

**O4 — backlog currently crosses back into strategic planning.** The enhancement route invokes `plan`, may use a
prototype for design questions, and stops at a human approval gate before implementation. That is incompatible
with a normal AFK execution promise. [Local issue loop lines 26–34](../../skills/delivery/backlog/reference/issue-loop.md).

**O5 — the personal UX baseline is narrow and disconnected.** `bare-minimum-ux` currently contains five
non-negotiable rules, but no inspected `to-spec`, `to-tickets`, or backlog contract references it.
[Local `bare-minimum-ux`](../../skills/creative/bare-minimum-ux/SKILL.md).

### Upstream reference skills

**O6 — `batch-grill-me` schedules all currently independent decisions in rounds.** It recomputes the design-tree
frontier after every response, supplies a recommended answer for each question, looks up environmental facts,
and stops when the frontier is empty and the user confirms shared understanding. It defines neither a bounded
round size nor a persistent decision/coverage artifact.
[Matt Pocock `batch-grill-me` at the inspected commit](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/in-progress/batch-grill-me/SKILL.md).

**O7 — upstream `to-spec` and `to-tickets` rely on conversational understanding.** Upstream `to-spec` synthesizes
the existing conversation without another interview. Upstream `to-tickets` then quizzes only the proposed split,
blocking edges, and merge/split choices before applying `ready-for-agent` on a real tracker.
[Upstream `to-spec`](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/engineering/to-spec/SKILL.md),
[upstream `to-tickets`](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/engineering/to-tickets/SKILL.md).

### Requirements-elicitation evidence

**F1 — interview order, omissions, and formulation are recurring failure modes.** In a two-cohort empirical study,
the researchers classified 34 mistakes across seven themes. Participants particularly struggled with question
formulation, omission, and order; common misses included stakeholders, probing questions, the current process,
priorities, and end-of-interview summaries. The study recommends beginning with the existing process and problem,
using follow-ups, and presenting a summary for confirmation.
[Bano et al., 2019, pp. 13–14 and 27–29](https://par.nsf.gov/servlets/purl/10105611).

**F2 — interviews materially transform initial ideas, and follow-up artifacts matter.** In an empirical study of
requirements evolution, analysts conducted an interview, analyzed the result into a prototype/use cases/written
material, then used that artifact in a follow-up interview. Up to 63% of documented requirements refined initial
ideas and up to 20% introduced new features. The authors caution that they could not isolate which factor caused
the effect, but identify diagrams and mock-ups as an important possible contributor.
[Ferrari et al., 2022, method and observations](https://link.springer.com/article/10.1007/s00766-022-00383-7).

**F3 — unstructured interviewing alone underperformed structured and artifact-assisted methods in one family of
experiments.** Paper prototyping identified the most requirements and had the best observed completeness,
quality, and performance; JAD elicited the most non-functional requirements and more relevant questions;
unstructured interviews were fastest but found fewer requirements, produced more overlap, and had the lowest
quality in that experiment.
[Carrizo et al., 2020](https://www.sciencedirect.com/science/article/abs/pii/S0950584920301282).

**F4 — procedural prompts can outperform generic interrogatory prompts.** A controlled empirical investigation
reported that prompts aimed at analysts' cognitive limitations produced additional meaningful requirements and
were significantly more effective than simple question prompts.
[Pitts and Browne, 2007](https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1365-2575.2006.00240.x).

**F5 — question dependency and respondent effort matter in batch collection.** IREB's elicitation handbook says
open questions are useful for discovering new aspects, closed questions for verifying existing requirements or
hypotheses, question order should be logical and respect dependencies, and excessive cognitive effort can cause
satisficing. It also recommends testing a questionnaire before broad use.
[IREB Requirements Elicitation Handbook v2.2.0, pp. 71–75](https://cockpit-v1.ireb.org/media/pages/downloads/cpre-requirements-elicitation-handbook/c1f8973c08-1754985576/advanced_level_elicitation_handbook_en_v2.2.0.pdf).

**F6 — LLM follow-up quality improves with an explicit mistake framework.** A 2025 controlled study reports that
LLM-generated follow-up questions were no worse than minimally guided human questions on clarity, relevance, and
informativeness, and outperformed them when generation was guided by common interviewer mistake types.
[Shen, Singhal, and Breaux, 2025](https://arxiv.org/abs/2507.02858).

### UX/design capability

**O8 — Impeccable externalizes durable product and design context.** Its current public workflow writes
`PRODUCT.md` for audience, purpose, voice, anti-references, and product/brand register, and `DESIGN.md` for visual
rules. Its command surface includes shaping, critique, audit, hardening, responsiveness, UX writing, and polish,
rather than treating UI quality as a single build-time instruction.
[Impeccable repository at the inspected commit](https://github.com/pbakaus/impeccable/tree/8967edc988ee146823bca3c51fcf51296e9dec18),
[Impeccable command documentation](https://impeccable.style/docs/impeccable/).

## Inferences

**I1 — the concern is a control-plane mismatch (high confidence; O3, O4).** A state called
`ready-for-agent` cannot simultaneously mean “safe for unattended execution” and “safe to begin a process that
may require product approval.” The planning gate is therefore an architectural boundary error, not merely an
annoying interaction.

**I2 — `batch-grill-me` is necessary but insufficient (high confidence; O6, F1–F6).** Frontier scheduling fixes
dependency order and reduces turn overhead. It does not guarantee coverage, good formulation, accurate recording,
artifact-assisted correction, or a verifiable stopping condition. A reliable interviewer needs those separate
contracts.

**I3 — recommendations should be hypotheses, not defaults the user is nudged to accept (medium-high confidence;
O6, F1, F5).** Proposed answers reduce response effort, but can also turn a discovery question into a leading
question. The safe form is: show the current evidence, label the recommendation as a provisional hypothesis,
state the trade-off, and make `accept / modify / defer / unknown` equally easy.

**I4 — “shared understanding” should be an approval gate, not the coverage test (high confidence; O6, F1, F4,
F6).** The interview should stop when a surface-aware coverage ledger has no material unclassified gaps; the user
then confirms the playback. Otherwise both interviewer and user can feel aligned while entire categories remain
unasked.

**I5 — a spec is a compression and coordination artifact, not a mandatory stage (high confidence; O1, O2).** One
small settled slice can be represented faithfully by one ticket. A spec becomes useful when several tickets need
shared decisions, the work has multiple actors/journeys, or the rationale would otherwise be duplicated and drift.

**I6 — the durable record before tickets matters more than its name (high confidence; F1, F2).** Even when no spec
is warranted, the system needs a compact record of facts, decisions, assumptions, unknowns, rejected alternatives,
and authority. Without it, `to-spec` and `to-tickets` can only infer from lossy conversation context.

**I7 — `plan` is overloaded (high confidence; O1, O4).** Strategic shaping and per-ticket tactical planning have
different authorities and freshness requirements. Strategic decisions should be settled upstream. Tactical plans
may be produced just in time inside execution without a human gate when they stay within delegated authority.
Requiring detailed implementation plans for every future slice up front risks staleness as earlier slices change
the codebase.

**I8 — UX is missing as lifecycle wiring, not merely as a longer checklist (high confidence; O5, O8).** Adding more
rules to `bare-minimum-ux` alone would not ensure design context reaches specs, tickets, builders, and verification.
The lifecycle needs a surface-aware capability binding and durable design context.

## Recommended lifecycle contract

### 1. Elicit into a decision ledger

Use batch frontier rounds, but make each round bounded and explicitly skippable. Each question should carry:

- a stable decision ID and category;
- the evidence already known from the repository or conversation;
- the dependency or downstream choice it unlocks;
- a clearly labelled recommended hypothesis and its trade-off;
- compact response affordances: `accept`, `modify`, `defer`, or `unknown`.

After every round, update a durable ledger with facts, decisions, assumptions, unknowns, conflicts, rejected
alternatives, and candidate acceptance statements. Play back the delta and contradictions before recomputing the
frontier. Use procedural coverage prompts selected by surface and risk rather than a universal giant checklist.

Relevant prompt families include problem/current workflow, actors and permissions, desired outcomes, scenarios and
failure states, data and privacy, non-functional qualities, rollout/migration, operations, UX/design, testing and
evidence, dependencies, and non-goals. Repository facts are researched, not asked.

### 2. Route to a ticket or optional spec

Create a ticket directly when there is one independently demonstrable outcome, no shared cross-ticket decision,
and all material strategic questions are settled or explicitly delegated.

Create a spec when the direction spans multiple tickets, carries decisions every slice must inherit, has multiple
actors/journeys, contains irreversible or high-risk product/architecture choices, or needs a stable review surface.
The spec is not the parent merely because the work is large; it is the canonical home for shared direction.

`to-spec` may remain a pure synthesizer, but its caller must supply a completed decision ledger. Unresolved Notes
must be classified as blocking, explicitly delegated, or safely deferred. A spec with unclassified material Notes
cannot feed execution-ready tickets.

### 3. Slice and admit tickets

`to-tickets` should preserve tracer-bullet slicing and dependency review, while adding a per-ticket readiness audit:

- intended user-visible or operational outcome;
- inherited decision/spec references and relevant rationale;
- observable acceptance criteria and failure/edge states;
- true blocking edges and sequencing;
- UX/design context for UI surfaces;
- required capabilities and verification surface;
- explicit authority boundary and no unresolved blocking decision.

`backlog groom` should become an admission controller for this contract, not a substitute design interview. It may
repair small omissions with the user, but substantial shaping returns upstream.

### 4. Execute AFK with an explicit handback

`backlog run` owns scheduling, staffing, implementation, verification, review, and evidence. It may make tactical
implementation plans within the ticket's authority without another expected human gate. If execution reveals a
missing or invalid strategic decision, it records the finding, releases the claim, applies a specific handback
state, and continues independent work.

### 5. Make UX/UI a cross-cutting lane

For UI work:

- **Elicitation:** capture user tasks, contexts, journey states, design register, references, and anti-references.
- **Spec:** record shared interaction and visual direction without duplicating a full design system.
- **Tickets:** inherit the relevant journey/state and link durable `PRODUCT.md`/`DESIGN.md`-style context.
- **Implementation:** always load `bare-minimum-ux` as Asher's policy overlay; load Impeccable as a declared
  external capability when installed and approved for the project.
- **Verification:** inspect happy, empty, loading, error, disabled, and responsive states; check accessibility,
  interaction feedback, copy, and visual-system alignment. Use critique/audit/polish as distinct gates where the
  surface warrants them.

Do not copy Impeccable's large rule set into `bare-minimum-ux`. Keep the latter personal, small, and authoritative;
integrate the former by declared external requirement or setup-selected capability so versions and provenance stay
explicit.

## Architectural shape

The cleanest ownership model is three layers plus one cross-cutting lane:

1. **Discovery/shaping:** interview primitive + decision ledger + optional spec.
2. **Work formation:** ticket slicing + dependency graph + readiness audit.
3. **Execution:** backlog queue and AFK dev tail.
4. **Cross-cutting capabilities:** UX/design, research, prototype, security, or other surface-specific disciplines
   selected during shaping and carried through verification.

This means `backlog` is not “the next document.” It is the stateful organization and execution mechanism that
receives admitted tickets.

## Contradictions and tensions

- Matt's single-question `grilling` argues that multiple simultaneous questions are bewildering, while
  `batch-grill-me` asks the entire dependency frontier. The sources do not establish one universally superior
  batch size. The defensible adaptation is a bounded, user-configurable frontier round with dependency ordering,
  not an unbounded questionnaire or mandatory one-question cadence.
- Recommendation-anchored questions make answering easier but can lead the user. No inspected source directly
  evaluates this exact LLM interaction pattern. The hypothesis/trade-off framing above is a risk-control inference,
  not an established result.
- Detailed plans prepared long before execution improve human review but can go stale. The lifecycle should front-load
  strategic decisions while allowing just-in-time tactical planning under delegated authority.
- Impeccable is a rich external design system, but making it a hard dependency would burden non-UI work and violate
  this repository's explicit external-dependency consent model. Bind it conditionally by surface and setup choice.

## Unknowns

- The ideal default number of questions in one batch round for Asher's actual interaction style requires a local
  usability eval; the literature inspected supports bounded effort and dependency order, not a precise number.
- The exact name and storage location of the decision ledger are product decisions.
- Whether the optional spec should be represented as a repository document, tracker parent, or both needs a
  prototype against the real review and slicing workflow.
- The best tracker state name for an invalidated strategic decision has not been selected.
- Impeccable's project-level installation and update policy has not been reviewed for inclusion as a declared
  external requirement; only its public workflow and current repository were inspected.

## Method and coverage

The investigation inspected local skill sources and tracker issues, fetched upstream skill sources at a recorded
commit, and used professional/empirical requirements-elicitation sources plus the public Impeccable workflow.
No subagents or parallel research shards were used. Recommendations are separated from observations and inferences.

## Claim audit

- Every material factual statement above is linked to a local source or primary/first-party external source.
- Inferences name their supporting observation/fact IDs and are confidence-bounded.
- Mutable repositories carry inspected commit SHAs; web research has an as-of date in `brief.md`.
- The tensions and unsupported precision (batch size, exact state/artifact names) are explicit unknowns.
- No parallel shards remain outstanding.
- Audit result: **pass with the named design unknowns remaining intentionally unresolved**.

## Source index

1. Local `to-spec`, `to-tickets`, `backlog`, and `bare-minimum-ux` sources linked above.
2. [`mattpocock/skills` at `9603c1c`](https://github.com/mattpocock/skills/tree/9603c1cc8118d08bc1b3bf34cf714f62178dea3b).
3. Bano et al., “Teaching requirements elicitation interviews,” 2019.
4. Ferrari et al., “How do requirements evolve during elicitation?”, 2022.
5. Carrizo et al., “Requirements elicitation methods based on interviews in comparison,” 2020.
6. Pitts and Browne, “Improving requirements elicitation,” 2007.
7. IREB, *Requirements Elicitation Handbook*, v2.2.0.
8. Shen, Singhal, and Breaux, “Requirements Elicitation Follow-Up Question Generation,” 2025.
9. [`pbakaus/impeccable` at `8967edc`](https://github.com/pbakaus/impeccable/tree/8967edc988ee146823bca3c51fcf51296e9dec18).
