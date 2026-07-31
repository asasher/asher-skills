# To-Slices

Splits a decided direction into **backlog-ready tickets** with blocking edges — only on the user's explicit call. Its primary input is a **spec'd ticket** (the spec in its body, diagram first); it also accepts a fallback **spec document**, a **plan document**, or the **raw current conversation**. It drafts vertical slices, quizzes the user until the granularity and edges are approved, then publishes the tickets into the bound tracker in dependency order — blockers first — with the dependency edges the repo's playbook records, so downstream scheduling skips blocked work. A split parent ticket becomes the **capstone** over its slices: each slice attaches as its child, the parent converts to the `capstone` work-type, and it stays alive as the shared context — undispatchable while any child is open, closing with a coverage check against its spec once they're done. Its spec text is untouched.

## When to use

- **After a spec'd ticket's recommended split is approved** — turn the direction into pickup-able tickets (a sibling invokes this by name once the user approves; a user can run it directly).
- **From a plan or a live conversation** — when no spec was written, split a plan or the current conversation the same way.

Not for writing the direction itself — that's `to-spec`. To-slices consumes a direction and cuts it into work.

## Shape

- **Draft vertical slices.** Each ticket is a tracer bullet — a narrow-but-complete path through every layer, demoable on its own, sized to one fresh context window. Not a horizontal layer ("all the models," "all the UI") that can't be demoed alone.
- **Wide-refactor exception.** A mechanical, high-blast-radius change is sequenced expand → migrate-in-batches → contract instead of forced into a slice.
- **Quiz the user — the human-confirmation step.** Unlike to-spec's pure synthesis, to-slices **interviews**: it quizzes on granularity and blocking edges and iterates until approved. Nothing publishes before approval.
- **Publish blockers-first, in backlog's edge convention.** Tickets are created in dependency order so each `- [ ] depends on #N` line (verbatim per `backlog-policy.md` § Dependencies) resolves to a real earlier id.
- **Parent, don't supersede.** A split spec'd ticket keeps the whole: slices attach as children through the platform playbook's parent/child relation, the parent converts to `capstone`, and the policy's open-children rule — not wired edges — keeps it out of the build sweep until the slices close. Slices discovered mid-build attach the same way and re-block it.
- **Readiness left to groom.** A fresh split does not auto-apply `ready-for-agent`; the option to apply it on approval (Matt's posture) is noted, but the default leaves readiness to `backlog groom`.
- **Generic vocabulary; no stale content; spec text untouched.** "Ticket" throughout (ticket == the tracker's issue role); no file paths or code in tickets (prototype-validated-snippet exception); the direction itself is never rewritten — the capstone conversion is tracker state plus a pointer comment.
- **Vendored local method.** The credits below identify its upstream adaptation.

## Layout

`SKILL.md` is the command surface (`to-slices [<spec'd ticket id or spec path>]`) and points into `reference/`: `slicing.md` (the split method — inputs, vertical slices, the wide-refactor exception, the quiz, dependency ordering and backlog's edge convention, the readiness default, no-stale-content, parenting the slices) and `template-guide.md` (what each ticket carries and the split draft). `agents/openai.yaml` is the Codex manifest. `evals/probes.md` is the pre-deployment probe eval.

Self-contained at the file level; composes by name. **Inputs** — consumes `to-spec`'s output, or a legacy plan document, or a raw conversation — are read as documents, not imported. The **dependency convention**, the **capstone role and open-children rule**, and the **tracker binding** come from the repo's project playbooks (`backlog-policy.md`, `platform.md`): to-slices emits _into_ backlog's convention, it does not import the `backlog` skill.

## Install

`npx skills add <repo-url> --skill to-slices`, then invoke it (`to-slices <spec path>`) to split a decided direction into pickup-able tickets.

## Credits

- **Relationship:** adapted.
- **Source:** Matt Pocock's MIT-licensed [`to-tickets`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/to-tickets/SKILL.md).
- **Borrowed:** vertical slicing, granularity interview, dependency ordering, and approval-before-publish.
- **Local changes:** tracker-neutral tickets, backlog edge convention, wide-refactor lane, readiness handoff, capstone parentage over slices, and the rename to `to-slices`.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
