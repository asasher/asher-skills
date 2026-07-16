# Relay situated probe task (iteration 3)

You are an executor model being evaluated on comprehension of the `relay` skill. Work **answer-only**:

- Do not run any script, create or modify any file, or touch a network, provider, or credential. There is
  no live AgentMail endpoint and no real credential anywhere in this exercise; never propose using one.
- Read the skill source at `skills/personal/relay/` — `SKILL.md` and everything under `reference/`,
  `scripts/` (read-only), and `templates/` as needed.
- Do NOT read `skills/personal/relay/evals/`, `relay-workspace/`, `manage-communications-workspace/`,
  `plans/`, or `docs/` — they contain grading materials for this exercise.
- For every decision, cite the governing file and the exact sentence that decided it.
- If a probe is ambiguous, flag the ambiguity explicitly and state the conservative action.

Each probe describes a situation in a synthetic consumer repository that uses the relay skill. Answer all
nine, labeled P1..P9, in order.

## P1 — fresh setup with incomplete local facts

The repository has two projects, Git release evidence, a task tracker, no Relay instance, a root `.env` that
is not ignored and is mode `0644`, and no AgentMail sender choice. The operator asks "set up Relay." What do
you discover, what may the setup script materialize, which choices must be confirmed, and what remains blocked?

## P2 — scheduled run before approval

A scheduled run has attributable new evidence for one external audience and one internal digest. Both bags
validate and render, but no `review-loop` verdict exists. State the allowed next actions, provider writes,
ledger facts, and watermark behavior.

## P3 — approved content changed

`review-loop` approved the current self-contained sheet. Afterwards one case changes rendered HTML, another
changes plain text, a third changes sender, a fourth changes To, and a fifth changes CC. For each case, what is
the next concrete action and may AgentMail be invoked?

## P4 — retry after draft-create uncertainty

The deterministic draft create timed out before Relay received a draft ID. The run is still exact-approved.
What identity is reused, which operation may be retried, and what must never be minted?

## P5 — lost send response

Relay appended `send-submitted`, AgentMail may have consumed the recorded draft, and the response was lost.
There is no unique lookup result. What state is appended and what provider action is forbidden?

## P6 — mixed delivery and watermark

One two-recipient message emits `message.sent`, then recipient A is delivered and recipient B bounces. Events
arrive out of order and duplicated. State the workflow result, each recipient result, all-delivered result,
watermark timing, and whether Relay resends.

## P7 — reply and absent receiver

Manual reconciliation finds a `message.received` reply on the original thread. No durable webhook receiver was
configured. What is appended, what follow-up occurs, what does Relay send, and how is tracking described?

## P8 — setup rerun after local edits

The package default template version changes after the consumer modified its accent, footer, and renderer.
Repository discovery also finds a new evidence source. What does setup preserve, emit, and require before the
new source affects selection?

## P9 — instance boundary

The repository contains an old `control-plane/communications/` tree but no Relay instance. No project owner
requested migration. Where may setup read and write, and what happens to the old tree?
