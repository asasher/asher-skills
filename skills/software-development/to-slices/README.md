# To-Slices

Splits a decided direction into **backlog-ready tickets** with blocking edges — only on the user's explicit call. Its primary input is a **spec'd ticket** (the spec read from its artifact branch at the blessed hash the ticket's projection names); it also accepts a **spec document**, a **plan document**, or the **raw current conversation**. It drafts vertical slices and presents the split as a **justified recommendation the user edits** — rationale per slice, every edge justified in words, a recommended landing shape, and the blessed spec hash the slices were cut from — then, on approval, publishes the tickets into the bound tracker in dependency order, blockers first. A split parent takes the **`spec` work-type** over its slices.

## When to use

- **After a spec'd ticket's recommended split is approved** — turn the direction into pickup-able tickets (a sibling invokes this by name once the user approves; a user can run it directly).
- **From a plan or a live conversation** — when no spec was written, split a plan or the current conversation the same way.

Not for writing the direction itself — that's `to-spec`. To-slices consumes a direction and cuts it into work.

## Shape

- **Tracer-bullet slices, each with rationale** — with a **wide-refactor** exception sequenced expand → migrate-in-batches → contract.
- **Recommend, then let the user edit.** The user reacts to reasons — per slice, per edge, and for the recommended landing shape (stacked default); nothing publishes before approval.
- **Publish blockers-first, in the repo's edge convention.** Readiness is left unset on a fresh split.
- **The parent keeps the whole.** A split spec'd ticket converts to the `spec` work-type over its child slices — each slice attaches as its child, the parent stays alive as the shared context, undispatchable until every child is closed or delivered, closing with a coverage check against its spec; its spec text is untouched.

## Layout

`SKILL.md` is the command surface (`to-slices [<spec'd ticket id or spec path>]`) and points into `reference/`: `slicing.md` (the split method) and `template-guide.md` (the ticket contract and the split draft). `agents/openai.yaml` is the Codex manifest.

Self-contained at the file level; composes by name. **Inputs** — consumes `to-spec`'s output, or a plan document, or a raw conversation — are read as documents, not imported. The **dependency convention**, the **`spec` work-type, `delivered` role, and open-children rule**, and the **tracker and branch bindings** come from the repo's project playbooks (`backlog-policy.md`, `platform.md`): to-slices emits _into_ the convention those playbooks record, and the playbooks are the only convention source it reads — everything else it consumes is the direction it was handed.

## Install

`npx skills add <repo-url> --skill to-slices`, then invoke it (`to-slices <spec'd ticket id>`) to split a decided direction into pickup-able tickets.

## Credits

- **Relationship:** adapted.
- **Source:** Matt Pocock's MIT-licensed [`to-tickets`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/to-tickets/SKILL.md).
- **Borrowed:** vertical slicing, granularity interview, dependency ordering, and approval-before-publish.
- **Local changes:** tracker-neutral tickets, backlog edge convention, wide-refactor lane, readiness handoff, justified-recommendation posture, landing shapes with the `delivered` role, `spec` parentage over slices, and the rename to `to-slices`.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
