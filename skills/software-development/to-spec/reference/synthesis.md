# Synthesis — the method

## The one rule: synthesize, never interview

To-spec is **pure synthesis.** **The table** is everything already in front of you: the current conversation and the codebase/project understanding built up in it. Every sentence of the spec traces to something on the table; anything genuinely undecided becomes a line in the spec's **Notes** — an open question, named plainly — and the run moves on. Never stall on the user: a flagged open question is the correct output; a question bounced back is not.

## What to mine

When a shaping record exists — decisions recorded on the ticket thread, terms and ADR drafts the shaping conversation crystallised — start from it and use the conversation to fill in around it. Then read back over the conversation and pull out:

- **The problem** — what's wrong, from the user's perspective. The reason the direction was needed.
- **The decided solution** — the direction that was settled, in the same perspective.
- **The decisions taken** — each real choice made, with the constraint that forced it. Capture the decision, not a survey of options that were discussed and dropped.
- **The user stories** — the actors and what each needs, across the full surface, not just the happy path.
- **What's out of scope** — anything explicitly excluded, so a later reader's question is answered in place.
- **The artifacts** — every decision-informing artifact, swept per § Sweep the artifacts.
- **The unresolved** — anything left open. These become Notes, not questions.

Lean on the codebase/project understanding on the table: name the modules, contracts, and architectural calls in prose, but keep to the no-stale-content rule below.

## Sweep the artifacts

Crystallising a subject sweeps its evidence trail onto the spec: collect every decision-informing artifact and give each one entry in the spec's **Supporting artifacts** section — entry anatomy, pointer forms, the conversation-only convention, and the omit-when-empty rule are the content contract in [template-guide](template-guide.md) § Supporting artifacts.

To-spec records where the trail ends; it never fabricates a dossier to fill the pointer slot. The sweep runs identically for every spec, dev and non-dev alike.

## Classify the work — dev or non-dev

Our work isn't all software, so the template flexes. Before writing, decide what kind of spec this is:

- **Dev spec** — the direction is a code change (a skill, a feature, a refactor). Keep the dev-only sections (**Testing decisions**, **Test split**, **Test seams**) and run the seams step below.
- **Non-dev spec** — the direction is a process, a piece of content, a decision, an operating change. **Skip** the dev-only sections entirely; use only the core sections ([template-guide](template-guide.md)).

If a spec is mostly non-dev but has one testable surface, keep the dev-only sections and scope them to that surface — the gate is "does it apply," not "is the whole thing code."

## The test split

A dev spec declares, per acceptance criterion by its AC id: a **durable suite test** (the behavior is long-standing; the test joins the maintained suite) or a **throwaway verification script** (proves this work once; its run is captured as evidence and the script is dropped before merge). The split is a shaping decision — verification executes the declaration, it never re-judges it. (Glossary terms and ADRs need no declaration: shaping commits them directly on the ticket's work branch, and the build's change request carries them to main.)

## Dev specs only — sketch the test seams

For a dev spec, name the **public seams** the work would be tested at, and **prefer the highest existing seam** — test at the outermost interface that already exists rather than reaching into internals or adding a new seam. The fewer seams, the better — keep it to the seams, in prose.

## Dev specs only — sweep the contract surface

When the direction touches an API, schema, or data contract, its surface carries decisions that hide as defaults: input strictness (optional vs required-nullable), nullability, error policy. Enumerate them — each lands settled in **Implementation decisions** or flagged in **Notes**. A contract decision the spec is silent on gets chosen by the builder and reversed by the reviewer; sweeping the surface here is what prevents that round trip.

## No stale content

The spec carries **no file paths and no code snippets.** They rot the moment the codebase moves, and a spec is direction, not implementation — describe the module, the contract, or the shape in prose instead.

Two narrow exceptions, and only these. First, a **prototype-validated snippet** that encodes a decision more precisely than prose can — a state machine, a reducer, a schema, a type shape: inline only that decision-rich fragment and note it came from a prototype. Second, the **Supporting artifacts** section's durable pointers — carrying a pointer to each artifact is that section's whole purpose (§ Sweep the artifacts). Outside Supporting artifacts and the one validated snippet, every section stays prose-only.

## Vocabulary

Speak generically. A **spec** is the direction document, split downstream into **tickets**. Never call the downstream unit an "issue" — that's one tracker's word, and the pair is deliberately tracker-agnostic.

## The diagram comes first

Every spec **opens with a diagram** of the moving parts — before any prose. Pick the form that fits the direction: a flow of the pieces, a sequence of the actors, a state machine of the lifecycle — rendered inline in the HTML (an SVG or equivalent that displays without a build step). The diagram is the review affordance — a reader should grasp the shape of the direction before reading a sentence. A direction too small to diagram is the only exception; say so in a line where the diagram would be.

## Where the spec lives

**The artifact branch file is canonical.** The spec is one self-contained HTML document, named for the subject, committed to the artifact branch — `artifact/<ticket>-<slug>` (`artifact/<slug>` when ticketless), plain shared history, never merged to main, deleted when spent. Every revision is a commit on that branch.

**The ticket holds a projection.** Given a ticket id, write onto that ticket: a writing-for-humans summary of the direction, the `to-web` render URL (absent that sibling, link the branch file and say the render was not deployed), and the **commit hash** the render was made from — a stale projection is visible by its hash lagging the branch. Each revision refreshes the projection (re-render, new hash) and posts a **short comment noting what changed** — the comments are the notification trail. Given no ticket but a bound tracker (`docs/agents/platform.md`), **create the ticket** — titled from a short kebab-case slug for the decided direction (the command argument, or derived from the solution when omitted) — and give it the projection.

**No tracker bound** — the branch and document are written the same way, and the projection (summary, render URL, hash) lands in the raising conversation. A later capture of the subject as a ticket adopts the links.

## Recommend the split, never perform it

When the decided direction is clearly bigger than one build, end the spec with a **Recommended split** section: the proposed slices in a sentence each, and which edges would block which. It is a proposal only — splitting is the user's call, and executing it belongs to a different move (the split that parents the ticket, as the `spec` work-type, over born-shaped child slices). A spec that fits one build carries no such section.

## Sign-off

The spec's approval is the **direction's gate.** Before presenting: run the **fidelity audit**, in both directions. Conversation → spec: every material decision from the conversation appears in the spec, and every Notes line carries its blocking / delegated / deferred classification ([template-guide](template-guide.md) § Notes). Spec → source: read the subject ticket's own stated requirements back against the finished spec — a requirement the ticket states that the spec neither delivers nor explicitly excludes is a fidelity failure, even when the conversation never raised it. An open **blocking** Note means the direction isn't ready to build on — say so plainly when presenting for sign-off.

- **User present** — take approval inline, in the conversation, recording the approval and its commit hash. This is the default path.
- **User AFK, projection on a ticket** — the projection already sits where the user's comments reach it; their LGTM on the ticket (or in the conversation) is the approval, binding to the carried hash — the LGTM arrives later; no waiting or polling. To-spec applies no readiness label — that decision travels by the tracker's label roles and belongs to whoever executes the user's call.
- **No tracker** — approval arrives in conversation when the user returns. Skipping sign-off still leaves a valid spec in place.

**Approval binds to a commit hash.** The user approves the spec they read, and the projection names the hash it was rendered from — so the approval records that hash; the user just says LGTM. Any later commit on the artifact branch past the approved hash mechanically invalidates the approval: the changed spec needs a fresh approval at its new hash.
