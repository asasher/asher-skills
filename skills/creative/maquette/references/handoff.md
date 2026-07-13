# Handoff

`HANDOFF.md` is the third artifact: the contract that lets a full-stack agent (or team) implement the real
product from the repo alone — no access to this conversation, no interpretation required. Write it for a
competent stranger.

Generate it from ground truth, not memory: `lib/schema.ts`, the `lib/api/` surface, `grep -rn "@mock"`,
`mcp/server.ts`, and `JOURNEYS.md`.

## HANDOFF.md template

```markdown
# <Product> — implementation handoff

## What this repo is
A maquette: a browser-only, high-fidelity prototype. The UX, journeys, screens, and interaction design are
the approved spec — implement behind them, don't redesign them. BRIEF.md and JOURNEYS.md carry intent.

## Data model
lib/schema.ts is the schema of record. Field names follow the domain deliberately. Notes per entity:
<keys, relationships, enums that need DB representation, anything the types can't say>

## API contract
Every function in lib/api/ becomes a real endpoint/service call with the same signature and semantics.
| lib/api fn | suggested endpoint | notes (validation, side effects, authz) |

## Mock inventory (from @mock markers)
Every place the maquette fakes reality, with what the real implementation needs:
| location | what's faked | realification notes |
<auth/session · permissions · search · uploads · email/webhooks · agent-bus query consistency · …>

## Agent surface (MCP)
mcp/server.ts is the planned production tool surface. Tools, schemas, and behaviors to preserve:
<tool list with one-line contracts>

## Non-functional expectations
Perceived performance the maquette set (the latency the demo sold), volumes fixtures imply the system
must handle, locales/currency behavior, accessibility level established.

## Suggested build order
Journeys by JOURNEYS.md ranking; keep the maquette running as the reference implementation and diff
against it screen by screen.
```

## Rules

- The mock inventory must be **complete** — an unlisted fake becomes a production surprise. If
  `grep -c "@mock"` disagrees with the table, fix the table.
- State what is deliberately absent (no real-time sync, no audit trail, …) so absence reads as a decision,
  not an oversight.
- Keep `BRIEF.md`, `JOURNEYS.md`, `DEMO.md`, and `HANDOFF.md` in the repo — the maquette repo is the
  complete deliverable.
