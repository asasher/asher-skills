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

When a shaping record exists — `CONTEXT.md` terms, ADRs, decisions recorded on the ticket thread — start
from it and use the conversation to fill in around it. Then read back over the conversation and pull out:

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

Speak generically. A **spec** is the direction document, split downstream into **tickets**. Never call
the downstream unit an "issue" — that's one tracker's word, and the pair is deliberately tracker-agnostic.

## The diagram comes first

Every spec **opens with a diagram** of the moving parts — before any prose. Pick the form that fits the
direction: a flow of the pieces, a sequence of the actors, a state machine of the lifecycle — written
as a fenced `mermaid` block. The diagram
is the review affordance — a reader should grasp the shape of the direction before reading a sentence.
A direction too small to diagram is the only exception; say so in a line where the diagram would be.

## Where the spec lives

**The ticket body is canonical.** Given a ticket id, rewrite that ticket's body: the diagram, then the
template's sections. Given no ticket but a bound tracker (`docs/agents/platform.md`), **create the
ticket** — titled from a short kebab-case slug for the decided direction (the command argument, or
derived from the solution when omitted) — and write the spec as its body. Every revision rewrites the
body in place and posts a **short comment noting what changed** — the body stays the one current spec;
the comments are the revision trail and the notification.

**No tracker bound** — fall back to a repo doc at `docs/specs/<name>.md`: the same body a ticket would
carry — the diagram first, then the template's sections. A repo may record a different specs location
or naming rule in its `docs/agents/` conventions; honor it when present. The first fallback spec also
registers the specs location in the project instruction file's `## Context documents` index (path, what
it is, when to read — create the section if absent).

## Recommend the split, never perform it

When the decided direction is clearly bigger than one build, end the spec with a **Recommended split**
section: the proposed slices in a sentence each, and which edges would block which. It is a proposal
only — splitting is the user's call, and executing it belongs to a different move (superseding the
ticket with born-shaped children). A spec that fits one build carries no such section.

## Sign-off

The spec's approval is the **direction's gate.** Before presenting: run the **fidelity audit** — every
material decision from the conversation appears in the spec, and every Notes line carries its
blocking / delegated / deferred classification. An open **blocking** Note means the direction isn't
ready to build on — settle it first.

- **User present** — take approval inline, in the conversation. This is the default path and depends on no
  other skill.
- **User AFK, spec on a ticket** — the spec already sits where the user's comments reach it; their
  LGTM on the ticket (or in the conversation) is the approval. To-spec applies no readiness label —
  that decision travels by the tracker's label roles and belongs to whoever executes the user's call.
- **User AFK, fallback repo doc** — the committed spec waits in the repo; approval arrives in
  conversation when the user returns. Skipping sign-off still leaves a valid spec in place.
