---
name: bare-minimum-ux
description: Asher's non-negotiable baseline UX requirements. Use when building or reviewing user-facing UI.
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
  external: [{"name":"impeccable","kind":"skill","source":"https://github.com/pbakaus/impeccable","capability":"Durable design context (PRODUCT.md/DESIGN.md) authoring plus scored UI critique/audit gates","version":"latest"}]
---

1. Do not surface internal instructions, prompts, implementation details, design constraints, or acceptance criteria in user-facing copy unless explicitly asked to expose them.
2. Avoid using number type for numeric input instead use text and validate as numeric
3. Co-locate actions and their consequences, e.g. a table's add-row button belongs where the new row appears (bottom-insert → bottom button; top-insert → top button).
4. For microcopy don't put supporting information in brackets
  - Bad: Update supplier price info from this RFQ (all valid quote rows)
  - Good: Update supplier price from this RFQ for all valid quote rows
5. Every component has an obvious visual hierarchy.
6. Match each action's explicitness to its weight: primary actions overt (a global share button), incidental ones revealed in place (hover-to-copy on a field).
7. Disclose progressively: know the journey's steps and show each step just the information it needs.
8. When work touches notifications, alerts, badges, toasts, reminders, notification centers, or other interruption channels, load [notification rules](references/notifications.md).

A rule's non-obvious case — which hierarchy, which actions are primary, what a step needs — is settled with
the user during shaping (the interview), never invented during implementation.

## Deeper craft — the declared `impeccable` external

The deep design capability is **Impeccable**, the external declared above. When the project has consented and installed it (recorded in
`external-dependencies.lock.json`), load it on UI work per its own SKILL: its `init`/`document` write the
project's `PRODUCT.md`/`DESIGN.md`, and its `critique`/`audit` serve as scored verification gates. On a blank
project whose direction hasn't crystallised, defer `init` — don't scaffold empty `PRODUCT.md`/`DESIGN.md`;
run it once shaping (interview → spec) lands a direction. Its rules
are never copied here — a fork goes stale. **Precedence:** on any conflict, these rules win — this file
is Asher's personal policy overlay on top of whatever design system runs underneath.
