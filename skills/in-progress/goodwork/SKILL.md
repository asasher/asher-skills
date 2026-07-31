---
name: goodwork
description: Define what good work means for a person through an interview, build their professional profile, and run a chat-driven job search from it — opportunities in one JSON file, one board for the picture.
argument-hint: "[command] [detail]"
metadata:
  invocation: model
  execution: thread
  requires: [interview]
  optional: []
---

Good Work defines what good work is for this person, then runs the search to find it. Everything happens in chat; state lives in two files; one HTML board shows the picture. Load the narrow reference file for the task at hand.

## The workspace

`goodwork/` in the project root, created the first time any command needs it — no setup command, no accounts, no connections, no server:

- `PROFILE.md` — the professional profile; canonical, human-readable, cumulative ([reference/profile.md](reference/profile.md)).
- `opportunities.json` — every opportunity being worked, one array ([reference/opportunities.md](reference/opportunities.md)).
- `board.html` — the generated presentation; never hand-edited ([reference/board.md](reference/board.md)).

The agent is the sole writer of all three. `goodwork/` contents are sensitive personal data: update cumulatively, never regenerate from scratch, never share or publish without explicit instruction.

## Core rules

- The person's definition of good work is elicited, never assumed. Don't moralize: a stable well-paid job funding a rich life is as good as a calling.
- Speak plainly. The frameworks in the references are for you, not the person: they hear jargon-free questions and plain summaries — never framework names, file names, schemas, or mechanics. Say "waiting for your OK", not "approval pending".
- Stories beat self-report: after any abstract answer, get a concrete episode. Mark every profile claim **reported**, **evidenced**, or **tested**.
- If the record (CV, LinkedIn, GitHub, portfolio, prior conversation, workspace files) can answer it, read it instead of asking.
- Never invent experience, metrics, credentials, or evidence in any outbound artifact.
- Nothing is sent, submitted, or published until the person approves the final text in chat. The approved text is what goes out, verbatim.
- Regenerate and show the board whenever there is new information worth seeing — after interview milestones, stage changes, scout sweeps, and checkins ([reference/board.md](reference/board.md)).
- If job-market, salary, company, or visa facts matter, verify with current sources before advising.

## Commands

| Command | Description | Reference |
| --- | --- | --- |
| `interview` | Build or deepen the profile — the flagship conversation, run through the `interview` skill | [reference/interviewing.md](reference/interviewing.md) |
| `profile` | View the profile, fold in new evidence, or mine a document (CV, review, LinkedIn) into it | [reference/profile.md](reference/profile.md) |
| `scout` | Find postings and score them into the opportunity list | [reference/opportunities.md](reference/opportunities.md) |
| `track` | Work the opportunities: stage moves, next actions, outreach and application drafts | [reference/opportunities.md](reference/opportunities.md) |
| `assets` | Build the outward surface: CV, LinkedIn, portfolio, proof of work | [reference/assets.md](reference/assets.md) |
| `checkin` | Review the search: what moved, what stalled, the one thing to fix, next actions, board refresh | [reference/opportunities.md](reference/opportunities.md) |

## Routing

1. **No argument**: if `goodwork/PROFILE.md` exists, summarize its snapshot in plain language, show the board, and suggest the next step. Otherwise recommend starting with `interview`.
2. **First word matches a command**: load its reference and follow it. Everything after the command name is the detail.
3. **First word does not match**: infer the best command, state the inferred command, and proceed. "What should I do with my life" infers `interview`; "help me find a job" with a profile infers `scout`.
4. **Guard**: `scout`, `track`, and `assets` never run against a missing `goodwork/PROFILE.md` — run the short-form interview from [reference/interviewing.md](reference/interviewing.md) first.

## Common workflows

- From zero: `interview` → `assets` → `scout` → `track`, with `checkin` weekly.
- "I hate my job but can't leave yet": `interview` (the redesign moves live there).
- Active search, knows what they want: short `interview` → `scout` → `track` → `checkin`.
- New evidence (a finished project, an interview debrief, a rejection pattern): `profile`, then let `checkin` pick up what it changes.

## Output standards

- Every session ends with the workspace updated, the board current, and one concrete next action with a time box.
- The profile records evidence and confidence marks, not horoscope prose; quote the person's own words.
- Outreach and application drafts: polished final text first, then rationale.
- Opportunity lists come ranked with reasons; metrics come with what they imply about targeting, not just effort.
