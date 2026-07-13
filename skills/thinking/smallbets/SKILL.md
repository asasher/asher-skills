---
name: smallbets
description: Minimalist-entrepreneur founder workflows — community-first validation, manual MVPs, first customers, pricing, sustainable growth.
argument-hint: "[command] [business, idea, or decision]"
user-invocable: true
disable-model-invocation: true
metadata:
  internal: true
  invocation: user
  execution: thread
  requires: []
  optional: []
---

Small Bets founder workflows through one command surface. Route the user to the narrow reference file for the business stage or decision in front of them, then produce practical next actions grounded in community, manual validation, early revenue, and sustainable growth.

## Core Rules

- Start with the people being served, not with the product idea.
- Prefer manual proof before software, automation, paid acquisition, hiring, or fundraising.
- Treat payment as the clearest validation. Do not substitute compliments, surveys, or social engagement for willingness to pay.
- Keep scope small enough to ship, sell, or test this week.
- Ask for concrete evidence: named communities, real customer conversations, current workarounds, costs, prices, and constraints.
- Challenge vanity metrics, broad audiences, premature scale, speculative features, and spending money before spending time.
- If the user asks for market, competitor, legal, tax, fundraising, or platform-specific facts that may have changed, verify current sources before giving concrete guidance.
- If inputs are missing, ask for the smallest missing piece needed to proceed.

## Inputs To Gather

Ask only for missing inputs relevant to the command:

- Community or customer segment
- Problem, current workaround, and urgency
- Existing product, manual service, prototype, or offer
- Evidence from conversations, sales, waitlists, usage, churn, or support
- Price, costs, revenue, runway, and founder time constraints
- Channels where the community gathers
- Decision options and reversibility
- Desired output: checklist, plan, outreach copy, pricing recommendation, process doc, scorecard, or decision review

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `find-community` | Discovery | Identify communities the founder already belongs to and problems worth serving | [reference/find-community.md](reference/find-community.md) |
| `validate` | Discovery | Test whether a business idea is worth pursuing before building | [reference/validate.md](reference/validate.md) |
| `mvp` | Build | Define the smallest useful product, manual first and tightly scoped | [reference/mvp.md](reference/mvp.md) |
| `processize` | Build | Turn a product idea into a manual process that can be delivered today | [reference/processize.md](reference/processize.md) |
| `first-customers` | Sell | Create a plan to sell one by one toward the first 100 customers | [reference/first-customers.md](reference/first-customers.md) |
| `pricing` | Sell | Choose initial pricing, pricing model, tiers, and price tests | [reference/pricing.md](reference/pricing.md) |
| `marketing` | Scale | Build an audience and content plan after early sales prove demand | [reference/marketing.md](reference/marketing.md) |
| `grow` | Scale | Evaluate spending, hiring, fundraising, and scaling against profitability | [reference/grow.md](reference/grow.md) |
| `values` | Culture | Define practical company values before hiring or codifying culture | [reference/values.md](reference/values.md) |
| `review` | Decision Review | Gut-check any business decision through small-bet principles | [reference/review.md](reference/review.md) |

## Routing

1. **No argument**: show the command menu grouped by category, then show the Common Workflows list as quick-start hints. Ask which workflow or command the user wants to run.
2. **First word matches a command**: load the matching reference and follow it. Everything after the command name is the target.
3. **Aliases**: route `community` to `find-community`; `idea` or `validation` to `validate`; `build` to `mvp`; `manual` to `processize`; `customers` or `sales` to `first-customers`; `price` to `pricing`; `market` or `content` to `marketing`; `scale`, `hiring`, `fundraising`, or `runway` to `grow`; `culture` to `values`; `gut-check`, `decision`, or `critique` to `review`.
4. **First word does not match**: infer the best command from the user's request, state the inferred command, load its reference, and proceed.
5. **Compound requests**: load references in workflow order, not all at once. For example: `find-community` before `validate`, `validate` before `processize`, `processize` before `mvp`, `first-customers` before `marketing`, `grow` before `values` when hiring is involved.

## Common Workflows

- New founder with no idea: `find-community` -> `validate` -> `processize`.
- Idea sanity check: `validate` -> `review`.
- Manual-first product: `processize` -> `mvp` -> `pricing`.
- Launching to early users: `first-customers` -> `pricing`.
- Product has early sales: `marketing` -> `grow`.
- Hiring or team design: `grow` -> `values`.
- Strategic fork in the road: `review` -> the specific command for the weakest assumption.

## Output Standards

- Give the founder the next concrete action, not a generic strategy essay.
- Prefer short plans with named assumptions, proof needed, and a time box.
- For validation and sales, include exact people, channels, outreach scripts, and pass/fail criteria when possible.
- For processizing, produce a step-by-step manual operating procedure.
- For pricing and growth, show the simple math and state confidence.
- For reviews, lead with the sharpest risk, then the smallest test or reversible next step.
