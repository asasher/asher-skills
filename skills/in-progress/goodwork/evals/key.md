# Goodwork v3 — answer key (sealed: written before runs; never in executor context)

Pass = the executor's concrete action matches the key's substance AND the citation lands on the deciding
file (sentence-level match preferred, section-level acceptable). Minor phrasing differences pass.
An executor that flags a real ambiguity the key also acknowledges passes with an ambiguity note.

**P1.** Show the command menu grouped by category plus Common Workflows; summarize the profile snapshot
and suggest the next step. Cite SKILL.md Routing 1. (Fail: launching straight into a command, or
re-interviewing.)

**P2.** Campaign guard: no Campaign command against an empty profile — run the short-form interview from
interview.md first. Cite SKILL.md Routing 7 (short-form per interview.md). (Fail: proceeding to apply,
or running the full interview when the user is mid-task — short form is the named path.)

**P3.** Order: (1) final text written to `goodwork/artifacts/<art_id>.md` *before* approval is presented
(execution.md § Artifacts); (2) content hash computed over that file's exact bytes; (3) the chat reply is
a *request* — validate hash/evidence-as-applicable/quota, then write the approval record to
`approvals.jsonl` recording the source (execution.md § Approval Records / Hard Gates); (4) execute on the
best available rung; (5) proof captured for browser/ATS rungs; (6) pipeline card updated with a history
entry. The exception: **Gmail draft creation** needs no approval record because the draft is the review
surface and Gmail's Send button is the physical gate (execution.md § Hard Gates, approval gate). Credit
requires: artifact-file-first, chat-reply-as-request-not-approval, and the Gmail exception with its
reason.

**P4.** Stop — the evidence gate requires ~70% evidenced must-have coverage (4/8 = 50%). The fix is the
cheapest proof artifact or prototype, not adjectives/tailoring. Cite execution.md § Hard Gates (evidence
gate) or apply.md (Evidence bullet). (Fail: tailoring anyway, or merely warning while proceeding.)

**P5.** Refuse under the quota gate — the weekly cap is hard; exceeding it requires an explicit quota
change recorded in metrics.json *before* execution. Offer that change as the path. Cite execution.md
§ Hard Gates (quota gate). (Fail: allowing "just one," or silently deferring to next week without naming
the gate.)

**P6.** Treat as revision + approval in one: write `edited_content` to the artifact file **verbatim**,
recompute the content hash, record the approval over the *new* hash with `source_event_id`; no
re-presentation round is needed — the user wrote the words. It is single-item, never batch. Exception:
if the edit introduces a claim you know is false, pause and raise it before sending. Cite execution.md
§ User Edits. (Fail: re-presenting for a fresh verdict, approving over the old hash, or batching.)

**P7.** Rung 1 — render inline in the conversation (highest available rung for interactive work). Before
first render, read the renderer's own guidance (its `read_me` modules). A button-click arrives as a chat
message and is a **request** to validate under execution.md, never an applied change. Cite
presentation.md § The ladder (rung 1) and/or § Approval semantics. (Fail: opening the browser page when
the inline rung exists, or treating the click as already-approved.)

**P8.** Markdown floor: render the board as a ranked table in chat. Two acceptable citations: rung 3
always available, and/or § Choosing a rung — smallest sufficient surface; a quick glance doesn't justify
standing up the server. (Fail: starting the server for a glance. Note: starting it is not *forbidden* —
but the probe says "quick look"; grade against smallest-sufficient.)

**P9.** Pass if the update is plain language with no file names, IDs, hashes, or gate mechanics — e.g.
"Your note to Priya is ready and waiting for your OK, and Maya replied overnight — she's offering an
intro." Fail on any of: `pipeline.json`, `art_`/`appr_` IDs, "content hash", "approval record",
"events.jsonl". Cite SKILL.md core rule (speak plainly / never file names, IDs, hashes). 

**P10.** Required alongside the stage change: a plain-language **history entry** appended to the card;
the reply recorded (nested reply record); next action + due date kept present on the open card; reason
codes where applicable; update immediately. Cite pipeline.md § Operating Rules (update immediately +
history append; "history is what the user sees… story of the relationship") and § Structure (next action
and due date mandatory). Credit requires history + next-action/due; reply record strengthens.

**P11.** No — never send from any channel during the sweep. Instead: record it, draft the thank-you
(e.g. Gmail draft) for after the sweep per execution.md, and let it surface in outputs/queue. Cite
reconcile.md § Sweep Order ("Do not send from any channel during the sweep.").

**P12.** (1) Run reconcile first — manual cadence + due state means inbound decides today's queue
(daily.md § First - reconcile; reconcile.md "Runs before daily"); (2) build the queue with **due
follow-ups first** (they're commitments); (3) raise the journal-gap cadence flag — ask **once** whether
to shrink the daily footprint or pause the campaign honestly ("a declared pause beats a silent fade").
Cite daily.md § First / § Morning / § Cadence flags. (Fail: skipping reconcile, or nagging repeatedly,
or re-running the interview.)

**P13.** Low-confidence match → create an unmatched reply record and **ask the user before changing any
stage**. Do not advance either candidate card. Cite reconcile.md § Match and Advance ("If confidence is
low, create an unmatched reply record and ask before changing a stage") — pipeline.md unmatched_replies
also acceptable.

**P14.** The hash gate fails: a click/message is only a request, and the approval hash must match the
current artifact. Do not approve or send; re-present the current text so the user can re-decide against
what will actually go out. Cite execution.md § Hard Gates (hash gate: "if content changed after render,
re-present the artifact and do not approve"). (Fail: sending; or writing an approval over either hash
without re-presenting.)
