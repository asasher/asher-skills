---
name: bare-minimum-ux
description: Asher's non-negotiable baseline UX requirements. Use when building or reviewing application UX, web interfaces, or frontend flows.
---

1. Do not surface internal instructions, prompts, implementation details, design constraints, or acceptance criteria in user-facing product copy. Only write copy that an actual end user should see. Treat build guidance as private context unless explicitly asked to expose it.
2. Avoid using number type for numeric input instead use text and validate as numeric
3. Co-locate actions and their consequences e.g For a table add row button at the bottom is good cause you press and see the row added but add row button at the top is bad cause you have to scroll down to see the added row, it could be good if the row is added to the top.
4. For microcopy don't put supporting information in brackets
  - Bad: Update supplier price info from this RFQ (all valid quote rows)
  - Good: Update supplier price from this RFQ for all valid quote rows
5. When work touches notifications, alerts, badges, toasts, reminders, notification centers, or other interruption channels, load [notification rules](references/notifications.md).
