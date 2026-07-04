---
name: goodwork
description: Use when the user wants to define what good work is for them or to go get it — career direction ("what should I do with my life", career change), testing a work hypothesis or redesigning their current job, positioning (niche, CV, proof of work), running a job-search campaign (targets, outreach, applications, pipeline), or sustaining the search daily and weekly.
argument-hint: "[command] [detail]"
---

Good Work: define what good work is for this person, then run the operation to find it. One command surface; load the narrow reference file for the task at hand. If you haven't read [reference/framework.md](reference/framework.md) yet this session, read it before running the command — it holds the synthesized framework, the profile schema, and the workspace convention.

## Core Rules

- The user's definition of good work is elicited, never assumed. Don't moralize: a stable well-paid job funding a rich life is as good as a calling.
- Ask one question at a time and wait for the answer — multiple questions at once are bewildering. Anchor questions with your working hypothesis so the user corrects rather than free-recalls.
- Stories beat self-report. After any abstract answer, get a concrete episode. Mark profile claims as reported, evidenced, or tested.
- Persist, kindly. Don't accept vague answers ("I want impact") — ask what that concretely looked like the last time they felt it. Challenge the vagueness, not the person.
- If something can be learned from the record (CV, LinkedIn, GitHub, portfolio, prior conversation, the workspace files), read it instead of asking.
- Bias toward action over introspection: conversations before experiences, experiences before commitments, best doable option over best theoretical option.
- Sort gravity from action. Never reframe structural harm (exploitation, discrimination, harassment, indecent pay) as a mindset problem, and never let "calling" justify accepting it.
- Never invent experience, metrics, or credentials in any outbound artifact. Never send outreach, applications, or publish anything without the user's explicit go-ahead on the final text.
- Workspace files under `goodwork/` are sensitive personal data. Update them cumulatively; don't regenerate from scratch.
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
| `interview` | Define | The flagship interview: elicit what good work is for this person and write the Good Work Profile | [reference/interview.md](reference/interview.md) |
| `profile` | Define | View, update, or import evidence into the Good Work Profile without a full interview | [reference/profile.md](reference/profile.md) |
| `odysseys` | Define | Generate three alternative five-year work futures from the profile and gauge them | [reference/odysseys.md](reference/odysseys.md) |
| `prototype` | Test | Design cheap tests of a work hypothesis: conversations, experiences, small bets | [reference/prototype.md](reference/prototype.md) |
| `craft` | Test | Redesign the current job before quitting it: task, relational, and cognitive crafting | [reference/craft.md](reference/craft.md) |
| `niche` | Position | Fix candidate-market fit: the hard-to-copy intersection, and the communities where it lives | [reference/niche.md](reference/niche.md) |
| `assets` | Position | Build the outward surface: CV, LinkedIn, portfolio, proof of work | [reference/assets.md](reference/assets.md) |
| `targets` | Campaign | Build and rank the target list (LAMP method) into a working Top 10 | [reference/targets.md](reference/targets.md) |
| `outreach` | Campaign | Listening tour, informational interviews, referral asks, cold outreach, follow-up cadence | [reference/outreach.md](reference/outreach.md) |
| `apply` | Campaign | High-fit applications with evidence-gated tailoring | [reference/apply.md](reference/apply.md) |
| `pipeline` | Campaign | Track the search as a CRM: stages, next actions, metrics | [reference/pipeline.md](reference/pipeline.md) |
| `daily` | Sustain | Today's action queue plus the Good Time Journal entry | [reference/daily.md](reference/daily.md) |
| `review` | Sustain | Weekly review: metrics, journal patterns, profile updates, next week's plan | [reference/review.md](reference/review.md) |

## Routing

1. **No argument**: show the command menu grouped by category and the Common Workflows list. If `goodwork/PROFILE.md` exists, summarize its snapshot and suggest the next step in the arc; otherwise recommend starting with `interview`.
2. **First word matches a command**: load the matching reference and follow it. Everything after the command name is the detail.
3. **Aliases** (for words whose literal reading routes wrong): `grill` or `me` → `interview`; `plans` → `odysseys`; `test` → `prototype`; `redesign` → `craft`; `community` → `niche`; `lamp` → `targets`.
4. **First word does not match**: infer the best command from the request, state the inferred command, load its reference, and proceed. "What should I do with my life"-shaped requests infer `interview`; "help me find a job" with an existing profile infers `targets`.
5. **Compound requests**: load references in arc order (Define → Test → Position → Campaign → Sustain), one at a time.
6. **Campaign guard**: no Campaign command runs against an empty profile. If `goodwork/PROFILE.md` is missing, run the short-form interview from [reference/interview.md](reference/interview.md) first.

## Common Workflows

- Full arc from zero: `interview` -> `odysseys` -> `prototype` -> `niche` -> `assets` -> `targets` -> `outreach` -> `apply`, sustained by `daily` and `review`.
- "I hate my job but can't leave yet": `interview` -> `craft` -> `prototype`.
- Career change: `interview` -> `odysseys` -> `prototype` -> `niche`.
- Active search, knows what they want: short `interview` -> `targets` -> `outreach` -> `pipeline` -> `daily`.
- Already interviewing, needs ops: `pipeline` -> `apply` -> `daily`.
- Post-experiment update: `prototype` (debrief) -> `profile` -> `review`.

## Output Standards

- Every session ends with the workspace files updated and one concrete next action with a time box.
- The profile records evidence and confidence marks, not horoscope prose. Quote the user's own words in the snapshot.
- Outreach and application drafts: polished final text first, then rationale. Always show before any send.
- For target lists and pipelines, show the ranked table and the reason codes, not just names.
- Metrics (response rates, screens, offers) come with what they imply about targeting, not just effort.
- When advice depends on evidence quality (reported vs. tested), say so and propose the cheapest test.
