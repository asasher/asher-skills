# Plan — authoring

What a plan covers and the house format. Domain-neutral: a plan reads the same whether the undertaking is a
research effort, an ops change, or a product build. Start from `templates/plan-skeleton.html`; this file says
what goes in it and how it should read. A project playbook may add domain-specific sections on top.

## What a plan covers

- **Problem statement** — the problem from the affected person's perspective, and the proposed solution the
  same way. One or two sentences, not a memo.
- **Stories** — a numbered, honest list: "As an _actor_, I want _outcome_, so that _benefit_." Cover the full
  surface of the undertaking, not just the happy path.
- **Definition of done** — explicit, testable **acceptance criteria**, each a checkable **pass/fail**. This is
  the contract everything downstream is judged against, so it carries the most weight. Each criterion is one
  `<li id="ac-N" data-criterion>`. Make each one something a person could independently confirm true or false
  — not a direction ("improve X") but a checkable state ("X does Y under condition Z").
- **Key decisions** — the choices the plan commits to and the constraint that forces each. Describe decisions,
  not artifacts: name what changes and why, not the exact files or code — those rot. (Exception: a snippet
  validated in a spike that pins a decision more precisely than prose can — a state machine, a schema, a
  shape — inline the decision-rich part and note where it came from.)
- **How it will be checked** — the seams the acceptance criteria will be confirmed at, and anything
  deliberately left unchecked, with why. Prefer the fewest, highest-level seams that still prove the criteria.
- **What's required, what's risky, what's out of scope** — the proof the plan owes on completion, the risks
  with their mitigations, and the exclusions that answer a reviewer's "but what about…" in place.

## House format

The plan is a document a human reviews under time pressure, then a durable reference. Optimize for the review.

- **HTML, self-contained.** Inline styles, inline SVG, no external fetches — it renders anywhere, including a
  plain browser open, and needs no server to read. Committed as a single file.
- **Visual first, minimalist.** Every screen of prose costs review attention. Lead each section with the
  diagram or table that carries it — a state machine, a sequence, a before/after shape — one sentence of prose
  beneath, secondary detail folded into `<details>`. If a diagram can carry it, a diagram does.
- **Diagrams are inline SVG**, pre-rendered at write time (e.g. `mmdc` for Mermaid sources, or hand-drawn) —
  never ship a rendering library in the document. Color by meaning, not decoration.
- **Stable anchors.** Every section and every individually-reviewable item carries a stable `id` that **never
  changes across revisions** — acceptance criteria are `<li id="ac-N" data-criterion>` rows, decisions are
  their own ids. The review layer anchors annotations to these ids, and any downstream check keys on the
  criterion ids; a renamed id orphans a comment.
- **Keep it short.** A plan is not documentation. Say the decision and the reason; drop the throat-clearing.

## Acceptance criteria — the load-bearing part

The criteria are what a reviewer scrutinizes hardest and what everything downstream is measured against, so
they earn extra care:

- **Checkable pass/fail.** Someone other than the author can confirm each one true or false. If you can't say
  how it would be checked, it isn't an acceptance criterion yet.
- **Observable, not aspirational.** "The report lists each source with its date" — not "the report is
  thorough."
- **One claim per criterion.** Split a compound criterion so a reviewer can accept or reject each half.
- **Domain-shaped by the playbook.** In a code repo the playbook may require each criterion be checkable
  against a running system and name the seam; in a research effort a criterion may be checkable against the
  produced artifact. The *form* — explicit, testable, pass/fail — is constant; what "checkable against" means
  is the playbook's to specify.
