---
name: goodwork
description: Define direction, test or redesign work, position the candidate, operate a campaign, or sustain/reconcile a local career search from a one-person workspace.
argument-hint: "[command] [detail]"
metadata:
  invocation: model
  execution: thread
  requires: []
  optional: []
  setup: reference/setup.md
---

Good Work defines what good work is for this person, then runs the local operation to find it. One command surface; load the narrow reference file for the task. Read [reference/framework.md](reference/framework.md) once per session before running any command.

## Core Rules

- The user's definition of good work is elicited, never assumed. Don't moralize: a stable well-paid job funding a rich life is as good as a calling.
- Ask one question at a time and wait. Anchor questions with your working hypothesis so the user corrects rather than free-recalls.
- Stories beat self-report: after any abstract answer, get a concrete episode. Mark profile claims reported, evidenced, or tested.
- Challenge vague answers ("I want impact") with concrete follow-up, not judgment.
- If the record (CV, LinkedIn, GitHub, portfolio, prior conversation, workspace files) can answer it, read it instead of asking.
- Bias to action: conversations before experiences, experiences before commitments, best doable option over best theoretical.
- Sort gravity from action. Never reframe structural harm as mindset; never let "calling" justify indecent work.
- Never invent experience, metrics, credentials, or evidence in any outbound artifact.
- Speak plainly to the user: drafts, boards, and questions — never file names, IDs, hashes, schemas, or gate mechanics. Say "waiting for your OK", not "approval record pending". Assume no technical background.
- The agent is the sole writer of workspace state. The local server may append only request events; the agent validates and applies them.
- Gate before send or submit: [reference/execution.md](reference/execution.md) owns approvals, content hashes, evidence, quotas, the execution ladder, and proof capture.
- `goodwork/` files are sensitive personal data. Update cumulatively; don't regenerate from scratch.
- If job-market, salary, company, visa, or community facts matter, verify with current sources before advising.

## Inputs To Gather

Ask only for what the command needs and the record can't provide:

- CV/resume, LinkedIn, portfolio, GitHub, or a plain history of roles and projects
- Current situation: employed/searching/redesigning, urgency, runway
- Constraints: location, visa, caregiving, health, compensation floor, industries to avoid
- Target role/field hypotheses, if any exist yet
- Existing `goodwork/` workspace files from earlier sessions

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `setup` | Connect | Create the one-person workspace, connect capabilities, and test the phone approval loop | [reference/setup.md](reference/setup.md) |
| `interview` | Define | The flagship interview: elicit what good work is for this person and write the Good Work Profile | [reference/interview.md](reference/interview.md) |
| `profile` | Define | View, update, import evidence, or drain the evidence inbox into the Good Work Profile | [reference/profile.md](reference/profile.md) |
| `odysseys` | Define | Generate three alternative five-year work futures from the profile and gauge them | [reference/odysseys.md](reference/odysseys.md) |
| `prototype` | Test | Design cheap tests of a work hypothesis: conversations, experiences, small bets | [reference/prototype.md](reference/prototype.md) |
| `craft` | Test | Redesign the current job before quitting it: task, relational, and cognitive crafting | [reference/craft.md](reference/craft.md) |
| `niche` | Position | Fix candidate-market fit: the hard-to-copy intersection, and the communities where it lives | [reference/niche.md](reference/niche.md) |
| `assets` | Position | Build the outward surface: CV, LinkedIn, portfolio, proof of work | [reference/assets.md](reference/assets.md) |
| `targets` | Campaign | Build and rank the employer target list into a working Top 10 | [reference/targets.md](reference/targets.md) |
| `scout` | Campaign | Maintain posting sources and sweep scored leads into the bench | [reference/scout.md](reference/scout.md) |
| `outreach` | Campaign | Listening tour, informational interviews, referral asks, cold outreach, follow-up cadence | [reference/outreach.md](reference/outreach.md) |
| `apply` | Campaign | High-fit applications with evidence-gated tailoring and approved execution | [reference/apply.md](reference/apply.md) |
| `pipeline` | Campaign | Track the search as a CRM: stages, next actions, metrics | [reference/pipeline.md](reference/pipeline.md) |
| `reconcile` | Sustain | Sweep inbound messages, match replies, update stages, and draft responses | [reference/reconcile.md](reference/reconcile.md) |
| `daily` | Sustain | Reconcile first, then today's action queue plus the Good Time Journal entry | [reference/daily.md](reference/daily.md) |
| `review` | Sustain | Weekly review: metrics, journal patterns, evidence inbox, profile updates, next week's plan | [reference/review.md](reference/review.md) |

## Routing

1. **No argument**: show the command menu grouped by category and the Common Workflows list. If `goodwork/PROFILE.md` exists, summarize its snapshot and suggest the next step; otherwise recommend `interview` or `setup` if operating capabilities are needed.
2. **First word matches a command**: load the matching reference and follow it. Everything after the command name is the detail.
3. **Aliases**: `grill` or `me` -> `interview`; `plans` -> `odysseys`; `test` -> `prototype`; `redesign` -> `craft`; `community` -> `niche`; `lamp` -> `targets`; `inbox` -> `reconcile`.
4. **First word does not match**: infer the best command, state the inferred command, load its reference, and proceed. "What should I do with my life" infers `interview`; "help me find a job" with a profile infers `targets`.
5. **Compound requests**: load references in arc order (Connect -> Define -> Test -> Position -> Campaign -> Sustain), one at a time.
6. **State touch**: when a command reads or writes operational JSON/JSONL, load [reference/state.md](reference/state.md). When it drafts, sends, submits, publishes, or automates, load [reference/execution.md](reference/execution.md).
7. **Campaign guard**: no Campaign command runs against an empty profile. If `goodwork/PROFILE.md` is missing, run the short-form interview from [reference/interview.md](reference/interview.md) first.

## Common Workflows

- Full arc from zero: `setup` -> `interview` -> `odysseys` -> `prototype` -> `niche` -> `assets` -> `targets` -> `scout` -> `outreach` -> `apply`, sustained by `reconcile`, `daily`, and `review`.
- "I hate my job but can't leave yet": `interview` -> `craft` -> `prototype`.
- Career change: `interview` -> `odysseys` -> `prototype` -> `niche`.
- Active search, knows what they want: short `interview` -> `setup` -> `targets` -> `scout` -> `outreach` -> `pipeline` -> `daily`.
- Already interviewing, needs ops: `setup` -> `pipeline` -> `reconcile` -> `daily`.
- Post-experiment update: `prototype` (debrief) -> `profile` -> `review`.

## Output Standards

- Every session ends with workspace files updated and one concrete next action with a time box.
- The profile records evidence and confidence marks, not horoscope prose. Quote the user's own words in the snapshot.
- Outreach and application drafts: polished final text first, then rationale.
- Target lists, lead benches, and pipelines: ranked tables with reasons, not just names.
- Metrics come with what they imply about targeting, not just effort.
- When advice depends on evidence quality, say so and propose the cheapest test.
