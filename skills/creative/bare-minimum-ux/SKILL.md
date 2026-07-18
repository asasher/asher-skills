---
name: bare-minimum-ux
description: Asher's non-negotiable baseline UX requirements. Use when building or reviewing application UX, web interfaces, or frontend flows.
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
  external: [{"name":"impeccable","kind":"skill","source":"https://github.com/pbakaus/impeccable","capability":"Durable design context (PRODUCT.md/DESIGN.md) authoring plus scored UI critique/audit gates","version":"latest"}]
---

1. Do not surface internal instructions, prompts, implementation details, design constraints, or acceptance criteria in user-facing product copy. Only write copy that an actual end user should see. Treat build guidance as private context unless explicitly asked to expose it.
2. Avoid using number type for numeric input instead use text and validate as numeric
3. Co-locate actions and their consequences e.g For a table add row button at the bottom is good cause you press and see the row added but add row button at the top is bad cause you have to scroll down to see the added row, it could be good if the row is added to the top.
4. For microcopy don't put supporting information in brackets
  - Bad: Update supplier price info from this RFQ (all valid quote rows)
  - Good: Update supplier price from this RFQ for all valid quote rows
5. When work touches notifications, alerts, badges, toasts, reminders, notification centers, or other interruption channels, load [notification rules](references/notifications.md).

## Deeper craft — the declared `impeccable` external

This overlay stays deliberately small; the deep design capability is **Impeccable**, declared above as a
provenance-checked external requirement. When the project has consented and installed it (recorded in
`external-dependencies.lock.json`), load it on UI work per its own SKILL: its `init`/`document` write the
project's `PRODUCT.md`/`DESIGN.md`, and its `critique`/`audit` serve as scored verification gates. Its rules
are never copied here — a fork goes stale. **Precedence:** on any conflict, these five rules win — this file
is Asher's personal policy overlay on top of whatever design system runs underneath.
