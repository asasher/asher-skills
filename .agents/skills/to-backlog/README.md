# To-Backlog

Captures the loose items a conversation has surfaced — bugs reported in passing, enhancement ideas,
follow-ups — as **minimal tickets** in the bound tracker. Each ticket carries a **work-type** (a fact the
live conversation knows) and its **chat context** (the discipline that matters: the conversation
evaporates, and the ticket must survive being read cold), but **no readiness role** — an un-routed
ticket is exactly what `backlog groom`'s sweep takes as intake, so captured items flow into the
existing routing: clear ones straight to ready, unsettled ones to shaping.

It is capture, not decomposition: N unrelated undecided things into the intake queue. One decided thing
into ordered parts is the `to-slices` sibling.

## When to use

- **Mid-interview or mid-shaping** — the user names bugs and ideas that aren't this thread's subject;
  sweep them into the tracker instead of losing them with the chat.
- **Mid-build** — work surfaces adjacent items (or gaps in a parent's direction); `to-backlog <parent>`
  attaches them as children of that parent, which under the backlog policy's open-children rule
  re-blocks a capstone parent automatically.
- **Any conversation that accumulated work nobody wrote down.**

Not for splitting a spec (`to-slices`), not for routing or readiness (`backlog groom`), not for writing
a direction (`to-spec`).

## Shape

- **Sweep, confirm, publish.** Collect capture-worthy items, present one compact list (title, proposed
  work-type, what context the ticket carries), publish only what the user approves. A confirm, not a
  quiz — captures are not a split.
- **Work-typed, never readiness-labeled.** Type is recorded at capture; readiness stays grooming's
  judgment. Capture applying readiness would make it a second groom.
- **Context fidelity.** Symptom and repro for a bug, motivating exchange for an enhancement, links to
  artifacts the conversation named; reporter-given fragments (error text, stack traces) are evidence
  and stay verbatim.
- **Optional parentage.** With a parent argument, each capture is attached as that ticket's child via
  the platform playbook's recorded relation.

## Layout

`SKILL.md` is the whole contract — the command surface (`to-backlog [<parent ticket id>]`), the sweep →
confirm → publish → readback method, and the capture discipline. `agents/openai.yaml` is the Codex
manifest. `evals/probes.md` is the pre-deployment probe eval.

Self-contained at the file level; composes by name. The **label roles**, **parent/child relation**, and
**tracker binding** come from the repo's project playbooks (`backlog-policy.md`, `platform.md`);
`to-slices` is named only as the boundary for captures that turn out to be decided directions.

## Install

`npx skills add <repo-url> --skill to-backlog`, then invoke it (`to-backlog`) in any conversation that
accumulated work worth tracking.
