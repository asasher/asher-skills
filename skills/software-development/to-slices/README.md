# To-Slices

Splits a decided direction into **backlog-ready tickets** with blocking edges — only on the user's explicit call. Its primary input is a **spec'd ticket** (the spec read from its artifact branch at the blessed hash the ticket's projection names); it also accepts a **spec document**, a **plan document**, or the **raw current conversation**. It drafts vertical slices and presents the split as a **justified recommendation the user edits** — rationale per slice, every edge justified in words, a recommended landing shape, and the blessed spec hash the slices were cut from — then, on approval, publishes the tickets into the bound tracker in dependency order, blockers first. A split parent ticket takes the **`spec` work-type** over its slices: each slice attaches as its child, and the parent stays alive as the shared context — undispatchable while any child is open and undelivered, closing with a coverage check against its spec once they're done. Its spec text is untouched.

## When to use

- **After a spec'd ticket's recommended split is approved** — turn the direction into pickup-able tickets (a sibling invokes this by name once the user approves; a user can run it directly).
- **From a plan or a live conversation** — when no spec was written, split a plan or the current conversation the same way.

Not for writing the direction itself — that's `to-spec`. To-slices consumes a direction and cuts it into work.

## Shape

- **Draft vertical slices, with rationale.** Each ticket is a tracer bullet — a narrow-but-complete path through every layer, demoable on its own, sized to one fresh context window — and carries one or two sentences of why: why this boundary, why demoable alone.
- **Wide-refactor exception.** A mechanical, high-blast-radius change is sequenced expand → migrate-in-batches → contract instead of forced into a slice.
- **Landing shape is part of the split.** **Stacked** (default for split specs): the spec ticket gets a feature branch off main whose root commit is the context delta; slices PR into it and earn the `delivered` role (applied at slice-merge time); the parent's own PR is the feature→main merge, closing the slices via its `Closes` lines. **Direct**: independent slices PR straight to main, the first carrying the context delta and blocking the rest.
- **Recommend, then let the user edit — the human-confirmation step.** The draft is a justified recommendation, not an open quiz; nothing publishes before approval.
- **Publish blockers-first, in the repo's edge convention.** Tickets are created in dependency order so every recorded edge resolves to a real earlier id.
- **Parent, don't supersede.** A split spec'd ticket keeps the whole: slices attach as children, the parent converts to the `spec` work-type, and the policy's open-children rule keeps it out of the build sweep until every child is closed or delivered. Slices discovered mid-build attach the same way and re-block it.
- **Readiness left unset.** A fresh split does not auto-apply readiness; the option to apply it on approval is noted, but the default leaves the readiness decision to the tracker's routing pass.
- **Generic vocabulary; no stale content; spec text untouched.** "Ticket" throughout; no file paths or code in tickets (prototype-validated-snippet exception); the direction itself is never rewritten — the `spec` conversion is tracker state plus a pointer comment.

## Layout

`SKILL.md` is the command surface (`to-slices [<spec'd ticket id or spec path>]`) and points into `reference/`: `slicing.md` (the split method — inputs, vertical slices, the wide-refactor exception, the justified recommendation, the landing shape, dependency ordering, the readiness default, no-stale-content, parenting the slices) and `template-guide.md` (what each ticket carries and the split draft). `agents/openai.yaml` is the Codex manifest. `evals/probes.md` is the pre-deployment probe eval.

Self-contained at the file level; composes by name. **Inputs** — consumes `to-spec`'s output, or a plan document, or a raw conversation — are read as documents, not imported. The **dependency convention**, the **`spec` work-type, `delivered` role, and open-children rule**, and the **tracker and branch bindings** come from the repo's project playbooks (`backlog-policy.md`, `platform.md`): to-slices emits _into_ the convention those playbooks record, and the playbooks are its only import.

## Install

`npx skills add <repo-url> --skill to-slices`, then invoke it (`to-slices <spec'd ticket id>`) to split a decided direction into pickup-able tickets.

## Credits

- **Relationship:** adapted.
- **Source:** Matt Pocock's MIT-licensed [`to-tickets`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/to-tickets/SKILL.md).
- **Borrowed:** vertical slicing, granularity interview, dependency ordering, and approval-before-publish.
- **Local changes:** tracker-neutral tickets, backlog edge convention, wide-refactor lane, readiness handoff, justified-recommendation posture, landing shapes with the `delivered` role, `spec` parentage over slices, and the rename to `to-slices`.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
