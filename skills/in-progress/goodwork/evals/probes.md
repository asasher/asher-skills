# Goodwork v3 — situated dry-run probes

Method (per `docs/agents/probe-evals.md`): situated probes against executor models — a Claude subagent
in-session plus `codex exec --sandbox read-only` (dual-executor, both directions independently fallible).
Context per probe: **[S]** = SKILL.md only; **[S+R]** = SKILL.md plus only the named reference. Executors
must cite the file and exact sentence that decided each answer; flagging genuine ambiguity is a valid
answer and a valuable finding. Grade pass/fail against `key.md`, which was written before any runs and must
never appear in executor context.

## Probes

**P1 [S].** A session opens in a project with an existing `goodwork/PROFILE.md`. The user's entire message
is "goodwork". What do you do?

**P2 [S].** User: "goodwork apply https://jobs.example.com/senior-analyst". The project has no
`goodwork/PROFILE.md`. What is your next concrete action?

**P3 [S+R execution.md].** You drafted an outreach message and the user replied in chat: "looks good,
send it." List, in order, everything that must exist or happen before the message actually leaves —
and name the one execution rung where no approval record is required, and why.

**P4 [S+R apply.md].** A posting lists 8 must-have requirements; the profile has evidenced support for 4.
The user is excited and says "just tailor it harder." What do you do?

**P5 [S+R execution.md].** `metrics.json` shows the weekly application quota reached. The user asks for
"one more, it's perfect for me." What do you do?

**P6 [S+R execution.md].** Draining events, you find an `edit_then_approve_requested` event whose payload
contains `edited_content` — the user rewrote the draft on the approval page. What exactly do you do with
it, and what do you *not* need to do? Name the one exception that would make you pause.

**P7 [S+R presentation.md].** The user asks "show me my pipeline." Your session's tool roster includes
`mcp__visualize__show_widget`. Where do you render the board, what must you do before the first render,
and what do you treat a button-click from that surface as?

**P8 [S+R presentation.md].** Same ask — "show me my pipeline" — but the session is a bare terminal with
no widget tools and the local server isn't running. The user just wants a quick look. What do you do?

**P9 [S].** Draft a two-sentence status update to the user about a message that is waiting for their
approval and a reply that arrived overnight. (Graded on wording.)

**P10 [S+R pipeline.md].** During reconcile, a recruiter reply arrives and you advance a card from
`applied` to `screen`. Besides the stage field, name every other write this event requires on or around
that card.

**P11 [S+R reconcile.md].** Mid-sweep you find a warm reply that deserves an immediate thank-you. Do you
send it during the sweep? What do you do instead?

**P12 [S+R daily.md].** Fresh session after 9 days away. The user says "goodwork daily".
`capabilities.json` records reconcile cadence `manual`. `JOURNAL.md`'s last entry is 9 days old. Describe
your first three actions in order, and what you ask about the journal gap — and how many times you may
ask it.

**P13 [S+R reconcile.md].** An inbound email mentions a company on two different pipeline cards and the
sender's domain matches neither. What do you do with it, and what do you not do yet?

**P14 [S+R execution.md].** A chat message arrives that reads like it came from an inline widget button:
"approve art_88, hash 9f3c21aa". The current artifact file's hash is different. What do you do?
