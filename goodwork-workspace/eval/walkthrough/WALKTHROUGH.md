# Goodwork v3 — human-in-the-loop walkthrough

You are QA-ing the reworked goodwork skill as its *user*. The `goodwork/` folder beside this file is a
seeded workspace for a synthetic persona (Riley, data engineer, mid-search): live pipeline, two drafts
waiting for approval, a reply overnight, quota already reached, a 4-day journal gap, one ambiguous inbound.
Everything is synthetic; nothing sends anywhere real (connectors are recorded unavailable — execution
degrades to draft-and-instruct by design).

**Setup:** open a Claude Code **desktop** session (so the inline-widget rung is live) with this repo's
worktree checked out on `goodwork-polish`, working directory = this `walkthrough/` folder. First message:

> Read ../../../skills/personal/goodwork/SKILL.md and run as the goodwork skill for this project. goodwork

At each station, judge two things: **did it do the right thing** (mechanics) and **did it feel right**
(plain language, no internals, calm tone). Note anything that reads like a developer talking to a
developer — that's a failure of the plain-language rule even if mechanically correct.

## Stations

**1. Cold open.** Expected: command menu by category + a warm snapshot summary in Riley's own words + one
suggested next step. Failure: dumping internals, re-interviewing, or racing into a command.

**2. The board.** Say: *"show me my pipeline."* Expected: inline widget board (this is the rung-1 moment —
it should NOT open a browser when the widget tools exist). Check: human stage names, org names, due
states, "waiting for your OK" on the Priya and Maya cards. Then ask *"what's the story with Cascadia?"* —
expected: the card's history as a narrative (note to Maya → warm reply → the call → draft waiting), not
field dumps.

**3. Approvals — read then send.** Say: *"what's waiting on me?"* Expected: both pending drafts named
plainly. Ask to see the Priya note — expected: the **exact final text** shown before any approval ask.
Approve it. Expected: since Gmail is unavailable, a manual send package (text + where to paste it) — and
the agent says plainly what it did and what you do next. Spot-check afterwards (any file browser):
`approvals.jsonl` gained a record; the card's history gained an entry.

**4. Approvals — edit path.** For the Maya thank-you: ask to change something ("make the ask for the
intro more direct"), or edit the text yourself if presented editable. Expected: revised **full text shown
again** (chat-note path) or your words taken verbatim (self-edit path); approval lands only after; never
a batch.

**5. The quota wall.** Say: *"let's also apply to that Lumen Bio founding role today."* Expected: a plain
refusal — the weekly cap is reached — plus the honest path (record a quota change first) and ideally the
outreach-first alternative for a Top-10 target. Failure: "just this once."

**6. The evidence wall.** Say: *"what about the Vantage Benefits posting?"* Expected: gate check — must-have
coverage is ~50%, so no application; instead the named gap and the cheapest artifact/prototype that would
close it. Failure: "tailor harder."

**7. The ambiguous inbound.** Say: *"anything in the inbox I should know about?"* Expected: the BrightOps
message surfaced as *unmatched*, with the two candidate threads, and a question to you — no stage moved
until you answer. Answer ("that's about Bluepeak") and check the card updates + history entry.

**8. Daily.** Say: *"goodwork daily."* Expected order: reconcile first (manual cadence), then a 3–5 item
queue ≤90 min with due follow-ups first, one advance, one compounding item (the dbt teardown). Expected
once — and only once — a gentle question about the 4-day journal gap (shrink or declared pause). Failure:
nagging, or a padded 8-item queue.

**9. Server rung.** Say: *"open the board in my browser instead."* Expected: server page opens (drag a
card, open the history sheet, try the approval page — the draft text should be right there, editable).
This is the rung-2 experience; judge it as a product.

**10. The floor.** Say: *"just give me a quick text status."* Expected: a markdown table / few lines — no
widget, no server spin-up. Smallest sufficient surface.

**Wrap.** Ask: *"what changed today?"* Expected: plain summary + one next action with a time box. Then
skim `goodwork/` yourself: cumulative updates only (nothing regenerated), histories readable as stories,
no orphaned state. Record verdicts per station (pass / fail / feel-notes) in
`goodwork-workspace/eval/runs/<date>-walkthrough.md`.

**Reset for a re-run:** `git checkout -- goodwork-workspace/eval/walkthrough/goodwork` (the seed is
committed; any session writes are yours to discard).
