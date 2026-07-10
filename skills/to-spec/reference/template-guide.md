# Template guide — what each section holds

The scaffold is [templates/spec-skeleton.html](../templates/spec-skeleton.html) — a self-contained HTML
deliverable with stable element ids, same house style as a plan; this file says what goes in each section and which
sections are dev-only. The section set is adapted from Matt Pocock's `to-spec` and shipped as our own. Two
groups: **core** sections appear in every spec; **dev-only** sections are kept for dev specs and **skipped
when they don't apply** (see [synthesis](synthesis.md) § Classify the work).

## Core sections — always present

- **Problem** — what's wrong, from the user's perspective. One or two tight paragraphs; the reason the
  direction was needed, not the solution.
- **Solution** — the decided direction, same perspective. What we're going to do and why, at the altitude of
  direction — not an implementation walkthrough.
- **User stories** — a numbered list, "As an _actor_, I want _feature_, so that _benefit_." Cover the full
  surface, including the edges, not just the happy path.
- **Implementation decisions** — each real choice made, with the constraint that forced it. Decisions, not a
  survey of discarded options. No file paths or code snippets — describe modules, contracts, and calls in
  prose (the one exception is a prototype-validated snippet; see [synthesis](synthesis.md) § No stale content).
- **Out of scope** — what's deliberately excluded, each line saying what it is so a reader's question is
  answered in place.
- **Notes** — open questions and anything the conversation left undecided, recorded plainly. This is where the
  no-interview rule lands: unresolved points live here instead of being asked back.

## Dev-only sections — skip when N/A

Keep these for a **dev spec**; drop them entirely for a **non-dev spec** (a process, content, a decision).
Don't manufacture prose to fill a heading that doesn't apply.

- **Testing decisions** — how the work will be proven: what's worth testing and what's deliberately left
  untested, with why. Direction, not a test plan.
- **Test seams** — the public seams the work would be tested at, preferring the **highest existing seam**; the
  fewer, the better. Runs only for dev specs (see [synthesis](synthesis.md) § Dev specs only).

## Order and altitude

Sections stay in template order so `to-tickets` and any human reader find them in a predictable place. Keep
every section at the altitude of **direction**: a spec is coarser than a plan (which is per-ticket and gated
for approval before implementation). If a section is drifting into file-by-file implementation detail, pull it
back up — the tickets carry that detail, the spec sets the direction they're cut from.
