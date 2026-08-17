---
name: bare-minimum-design
description: Asher's non-negotiable design baseline, and the owner of the project's DESIGN.md — the visual-system file agents read before building UI. Use when building or reviewing user-facing UI, or when a durable visual decision needs its home.
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
---

# Bare minimum design

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

A rule's non-obvious case — which hierarchy, which actions are primary, what a step needs — is settled with the user during shaping (the interview), never invented during implementation.

## DESIGN.md — the visual-system file this skill owns

The project's visual system lives in `DESIGN.md` at the repo root, in the open DESIGN.md format ([specification](https://stitch.withgoogle.com/docs/design-md/specification), Apache-2.0): YAML front-matter design tokens — hex colors, type scale, spacing, radii — followed by the format's prescribed markdown sections, from visual theme through components to do's and don'ts. Values are concrete (hex codes, not color names; patterns, not adjectives) so any agent or tool can consume them.

- **Boundary:** this file carries only how the product looks. Strategy — who the users are, what the product is, why it wins — belongs in the project's product file, never here.
- **Lazy create:** create `DESIGN.md` from the shipped [skeleton](templates/DESIGN.md) when the first durable visual decision lands, and register its line in the project instruction file's `## Context documents` index at creation — path, what it is, when to read it. Until then, no file: an empty scaffold teaches nothing.
- **Read before building UI; write as decisions land.** A visual decision made during work and absent from the file is drift — record it as part of the change that made it.
- **Precedence:** on any conflict, the numbered rules above win — they are Asher's policy overlay on whatever design system runs underneath.
