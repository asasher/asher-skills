# Template guide — what each section holds

This file is the content contract: what a spec's body contains. The spec is one HTML document on the subject's artifact branch — the canonical file; the ticket carries only the projection (summary, render URL, commit hash). Two groups: **core** sections appear in every spec; **dev-only** sections are kept for dev specs and **skipped when they don't apply** (see [synthesis](synthesis.md) § Classify the work).

## Core sections — always present

- **Problem** — what's wrong, from the user's perspective. One or two tight paragraphs; the reason the direction was needed, not the solution.
- **Solution** — the decided direction, same perspective. What we're going to do and why, at the altitude of direction — not an implementation walkthrough.
- **User stories** — a numbered list, "As an _actor_, I want _feature_, so that _benefit_." Cover the full surface, including the edges, not just the happy path.
- **Implementation decisions** — each real choice made, with the constraint that forced it. Decisions, not a survey of discarded options. No file paths or code snippets — describe modules, contracts, and calls in prose (the one exception in this section is a prototype-validated snippet; see [synthesis](synthesis.md) § No stale content).
- **Context delta** — the glossary terms and ADR drafts this direction introduces: each term with its one-line definition, each ADR draft in the ADR format. This is the language downstream tickets and PRs use from birth; the build that makes the direction true lands it on main (see [synthesis](synthesis.md) § The two declarations). Omit the section when the direction introduces neither.
- **Out of scope** — what's deliberately excluded, each line saying what it is so a reader's question is answered in place.
- **Acceptance criteria** — a numbered list with stable ids: `AC-1`, `AC-2`, … Each criterion is one observable outcome a checker could grade pass or fail. The ids are the shared handles every downstream role keys its verdicts to — builder, verifier, reviewer, evidence — so they must stay stable across revisions: amend a criterion in place or append new ones; an id, once assigned, keeps its meaning. A spec ending in a **Recommended split** may keep its criteria at direction level — the split gives each child ticket its own numbered list.
- **Assumptions** — what the direction takes as true of the existing system, one plain line each. These are claims the build leans on, so downstream work verifies a load-bearing one before building on it. Omit the section when there are none.
- **Supporting artifacts** — the evidence trail: one entry per generated artifact that informed a decision. Research dossiers and prototype answers are the canonical cases; the rule is general, so any decision-informing artifact kind qualifies. Each entry names the artifact kind, the question it answered, its one-line takeaway, and a durable pointer — the artifact-branch file plus its render URL where one exists, a tracker-resolvable URL, or a repo-relative path. These pointers are a named exception to the no-stale-content rule, confined to this section (see [synthesis](synthesis.md) § No stale content). Never copy artifact content inline; never leave a summary without its pointer. Conversation-only evidence gets an entry stating the conclusion and marking plainly that no durable artifact exists. Omit the section when nothing was generated — the same convention as Assumptions.
- **Notes** — open questions and anything the conversation left undecided, recorded plainly. This is where the no-interview rule lands: unresolved points live here instead of being asked back.

## Dev-only sections — skip when N/A

Keep these for a **dev spec**; drop them entirely for a **non-dev spec** (a process, content, a decision). Don't manufacture prose to fill a heading that doesn't apply.

- **Testing decisions** — how the work will be proven: what's worth testing and what's deliberately left untested, with why. Direction, not a test plan.
- **Test split** — per acceptance criterion, by AC id: durable suite test or throwaway verification script (see [synthesis](synthesis.md) § The two declarations). A shaping decision downstream verification executes, never re-judges.
- **Test seams** — the public seams the work would be tested at, preferring the **highest existing seam**; the fewer, the better. Runs only for dev specs (see [synthesis](synthesis.md) § Dev specs only).

## Order and altitude

Sections stay in template order so downstream splitters and any human reader find them in a predictable place. Keep every section at the altitude of **direction**. If a section is drifting into file-by-file implementation detail, pull it back up — the tickets carry that detail, the spec sets the direction they're cut from.
