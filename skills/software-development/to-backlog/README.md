# To-Backlog

Captures the loose items a conversation has surfaced — bugs reported in passing, enhancement ideas, follow-ups — as minimal work-typed tickets in the bound tracker, each carrying its chat context but no readiness role. It is capture, not decomposition: N unrelated undecided things into the intake queue; one decided thing into ordered parts is the `to-slices` sibling.

## When to use

- **Mid-interview or mid-shaping** — the user names bugs and ideas that aren't this thread's subject; sweep them into the tracker instead of losing them with the chat.
- **Mid-build** — work surfaces adjacent items (or gaps in a parent's direction); `to-backlog <parent>` attaches them as children of that parent.
- **Any conversation that accumulated work nobody wrote down.**

Not for splitting a spec (`to-slices`), not for routing or readiness (grooming), not for writing a direction (`to-spec`).

## Shape

- **Sweep → confirm → publish → readback.** One compact list — title, work-type, context note — and nothing publishes before the user approves; with a parent argument, each captured ticket is attached as that parent's child.
- **Work-typed, un-routed, context-carrying.** The rationale for each discipline lives in `SKILL.md`.

## Layout

`SKILL.md` is the whole contract — the command surface (`to-backlog [<parent ticket id>]`), the method, and the capture discipline. `agents/openai.yaml` is the Codex manifest.

Self-contained at the file level; composes by name. The **label roles**, **parent/child relation**, and **tracker binding** come from the repo's project playbooks (`backlog-policy.md`, `platform.md`); `to-slices` is named only as the boundary for items that turn out to be decided directions.

## Install

`npx skills add <repo-url> --skill to-backlog`, then invoke it (`to-backlog`) in any conversation that accumulated work worth tracking.
