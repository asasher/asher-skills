# Opportunity Contract

## Known home

One pursuit has one known home at `Opportunities/<Name>.md`. It remains there in terminal stages so its
commercial history and links survive promotion.

Required frontmatter:

```yaml
---
opportunity: <display name>
type: opportunity
company: "[[Company]]"
customer: "[[Customer]]"
owner: "[[Person]]"
stage: lead
opened: 2026-07-13
nextAction: aB3dE
---
```

Optional fields, only when known:

```yaml
contacts:
  - "[[Person]]"
value: 85000
currency: AED
recurringValue: 40000
probability: 40
workspacePath: /absolute/path/to/pursuit-work
outcomeDate: 2026-08-20
closeReason: <lost reason>
dormantReason: <why paused>
reviewDate: 2026-09-15
noDeliveryReason: <why a won pursuit creates no Project>
```

`probability` is an optional evidence-backed integer from 0 through 100, not a stage-derived value.
`nextAction` contains only the task ID, never task text or checkbox markdown. Active stages require it.
Terminal stages and `dormant` omit it.

Body:

```markdown
# <display name>

One-sentence orientation: customer problem, offer, and current state.

## Backlog

- [ ] Concrete commercial action 🆔 aB3dE

## Done

### 2026-07-13

- [x] Completed action 🆔 z9Yx8 ✅ 2026-07-13

## Commercial

Current scope, pricing state, offer, and explicitly labelled assumptions.

## Decision Log

- 2026-07-13 - Decision and rationale.

## Events Log

- 2026-07-13 - Material interaction, deliverable, or outcome with evidence link.

## Projects

- [[Delivery Project]] - relationship to this pursuit.

## Links

- [Working folder](...) - pursuit artifacts.
```

Keep all level-two sections present, even when they contain a concise `None yet.` marker. This gives the
validator and humans stable places to inspect.

## Stages and gates

Allowed stages: `lead`, `qualified`, `discovery`, `proposal`, `negotiation`, `closed-won`, `closed-lost`,
`dormant`.

- `lead` - named prospect/customer, need or signal, and source.
- `qualified` - plausible problem, owner or sponsor, and reason to pursue.
- `discovery` - agreed discovery action plus captured requirements or evidence.
- `proposal` - client-safe proposal exists and a concrete next action is designated.
- `negotiation` - scope, price, timing, or terms are actively discussed.
- `closed-won` - explicit acceptance or commitment, `outcomeDate`, and linked Project(s) or
  `noDeliveryReason`.
- `closed-lost` - `outcomeDate` and `closeReason`.
- `dormant` - `dormantReason` and future `reviewDate`.

A transition records evidence in `## Events Log`; artifact creation alone does not satisfy a gate.
