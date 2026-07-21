# Synthesis — the method

The method. It imports no other skill's files.

## The one rule: synthesize, never interview

To-spec is **pure synthesis.** Everything it writes comes from what's already on the table — the current
conversation and the codebase/project understanding built up in it. Do not re-elicit requirements, do not
re-ask what the discussion already settled, and do not stop and wait on the user.

When something was genuinely left undecided, **record it as a line in the spec's Notes** — an open question,
named plainly — and move on. A flagged open question is the correct output; a question bounced back to the
user is not.

## What to mine

When the conversation ran through `interview` or the `shape` sibling, start from the crystallised record —
`CONTEXT.md` terms, ADRs, and the exit classification (settled / delegated / deferred / blocking) — and use
the conversation to fill in around it; the classification maps straight onto the Notes rule below. Then read
back over the conversation and pull out:

- **The problem** — what's wrong, from the user's perspective. The reason the direction was needed.
- **The decided solution** — the direction that was settled, in the same perspective.
- **The decisions taken** — each real choice made, with the constraint that forced it. Capture the decision,
  not a survey of options that were discussed and dropped.
- **The user stories** — the actors and what each needs, across the full surface, not just the happy path.
- **What's out of scope** — anything explicitly excluded, so a later reader's question is answered in place.
- **The unresolved** — anything left open. These become Notes, not questions.

Lean on the codebase/project understanding the conversation built: name the modules, contracts, and
architectural calls in prose, but keep to the no-stale-content rule below.

## Classify the work — dev or non-dev

Our work isn't all software, so the template flexes. Before writing, decide what kind of spec this is:

- **Dev spec** — the direction is a code change (a skill, a feature, a refactor). Keep the dev-only sections
  (**Testing decisions**, **Test seams**) and run the seams step below.
- **Non-dev spec** — the direction is a process, a piece of content, a decision, an operating change. **Skip**
  the dev-only sections entirely; use only the core sections ([template-guide](template-guide.md)).

If a spec is mostly non-dev but has one testable surface, keep the dev-only sections and scope them to that
surface — the gate is "does it apply," not "is the whole thing code."

## Dev specs only — sketch the test seams

For a dev spec, name the **public seams** the work would be tested at, and **prefer the highest existing
seam** — test at the outermost interface that already exists rather than reaching into internals or adding a
new seam. The fewer seams, the better; note what's deliberately left untested and why. This is direction for
how the work will be proven, not a test plan — keep it to the seams, in prose.

## No stale content

The spec carries **no file paths and no code snippets.** They rot the moment the codebase moves, and a spec
is direction, not implementation — describe the module, the contract, or the shape in prose instead.

The single exception: a **prototype-validated snippet** that encodes a
decision more precisely than prose can — a state machine, a reducer, a schema, a type shape. Inline only that
decision-rich fragment and note it came from a prototype. Absent that exception, everything is prose.

## Vocabulary

Speak generically. A **spec** is the direction document; `to-tickets` splits it into **tickets**. Never call
the downstream unit an "issue" — that's one tracker's word, and the pair is deliberately tracker-agnostic.

## Naming and placing the spec

Write the spec to `docs/specs/<name>.html`, where `<name>` is a short kebab-case slug for the decided
direction (given as the command argument, or derived from the solution when omitted). That path is the
contract `to-tickets` reads. The spec is a **self-contained HTML deliverable** — start from
`templates/spec-skeleton.html`; keep its stable element ids (sections, `story-N`, `dec-N`, …), inline
everything, fetch nothing. A repo may record a different specs location or naming rule in its `docs/agents/`
conventions; honor it when present, default to `docs/specs/` otherwise.

## Sign-off

The spec's approval is the **direction's gate** — the lifecycle has no separate plan stage; per-ticket
tactics are made just-in-time inside execution. Before presenting: run the **fidelity audit** — every
material decision from the conversation appears in the spec, and every Notes line carries its
blocking / delegated / deferred classification. An open **blocking** Note stops the hand-off to
`to-tickets` until shaping settles it.

- **User present** — take approval inline, in the conversation. This is the default path and depends on no
  other skill.
- **User AFK** — present the spec for sign-off through the optional `review-loop` sibling: the spec is
  already a self-contained review-ready HTML with stable element ids, so hand it to `review-loop` (composed
  by name) as-is — no render step — and it is approved from the human's own device per the repo's
  presentation-surface config.

`review-loop` is optional and never a hard dependency — if it's unavailable, fall back to inline approval or
leave the committed spec for the user to read directly. Skipping sign-off still leaves a valid spec on disk.

**On approval:** commit the spec, and — when a live tracker is bound (`docs/agents/platform.md`) — create a
**thin tracking ticket** carrying the title, a one-line gist, and a link to the canonical spec. The
projection carries links and state, never content — one source of truth, no drift. `to-tickets` wires each
slice ticket to it at publish time. The first spec also registers the specs location in the project
instruction file's `## Context documents` index (path, what it is, when to read — create the section if
absent).
