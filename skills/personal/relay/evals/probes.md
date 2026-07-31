# Relay — situated predeployment probes

Run answer-only in a synthetic repository with the Relay skill source available. Unset real credentials and
expose no live AgentMail endpoint. Require file-and-sentence citations for every decision. The answer key was
written before executor runs; grade every hard criterion pass/fail without editing it.

## P1 — fresh setup with incomplete local facts

The repository has two projects, Git release evidence, a task tracker, no Relay instance, a root `.env` that
is not ignored and is mode `0644`, and no AgentMail sender choice. The operator asks “set up Relay.” What do
you discover, what may the setup script materialize, which choices must be confirmed, and what remains blocked?

## P2 — scheduled run before approval

A scheduled run has attributable new evidence for one external audience and one internal digest. Both bags
validate and render, but no in-chat approval has been recorded and no user is present. State the allowed next
actions, provider writes, ledger facts, and watermark behavior.

## P3 — approved content changed

The user approved the current self-contained sheet in chat, and the run recorded the hash-bound approval
event. Afterwards one case changes rendered HTML, another
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

## P10 — project policy versus portable skill

A consumer uses an unfamiliar tracker whose query operations, status meanings, audience vocabulary, and
recipient-facing prose rules are unique to that repository. Which parts belong in the canonical Relay skill,
which belong in `docs/agents/relay.md`, and which must be represented in structured files under `relay/`?

## P11 — complete collection and carry-forward

The repository playbook requires three provider operations per project and says that rechecked unresolved
commercial follow-ups carry forward. A run samples only one operation, then encounters an old follow-up before
the audience watermark. What evidence-accounting work is required, and under what exact condition may the old
fact survive selection?

## P12 — same-day updates and multi-recipient draft

Two different approved updates for one audience are generated on the same day. The second has two To recipients
and two CC recipients. State how communication and draft identity avoid collision, how AgentMail receives the
recipient headers, and what verification is required before send.
