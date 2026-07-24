# To-Thread — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are a Claude Code session (opus, high effort) in `/work/payments`, dispatching ticket #142's shaping
as a thread. A parallel build thread is already editing this repo.

## Probes

**P1 (prompt).** Draft the thread's prompt: may it say "continue our discussion above"? What must it
contain? Cite.

**P2 (name).** Propose a name and justify its shape. Cite.

**P3 (model/effort).** Nothing was said about models. What do you pass, and how? Cite.

**P4 (isolation).** Does this spawn take `-w`? Why? Cite.

**P5 (Codex flags).** On Codex, someone suggests `--ephemeral` to keep things tidy. Response? Cite.

**P6 (after spawn).** The spawn returned. What do you report, and what do you do when the user later
asks how the thread is going? Cite.

## Answer key

- **P1:** No — "The thread sees nothing of this conversation": the prompt must "state the goal,
  reference material by path or ticket id, say what done looks like, and name any skill the thread
  should run." A prompt leaning on shared context = **fail**.
- **P2:** Something like `shape-142-driver-payouts` — "short, human, specific ... The name is how the
  user finds it in a list of twenty." A generic name = **fail**.
- **P3:** "this session's own, passed explicitly, unless told otherwise" — `--model opus --effort high`
  on the spawn. Omitting them and hoping for inheritance = **fail**.
- **P4:** Yes — "a thread that will edit a repo this session or another live thread is also editing
  gets its own worktree," and a build thread is already editing this repo. No worktree = **fail**.
- **P5:** Refuse — "Never pass `--ephemeral` — it makes the thread unresumable." Accepting = **fail**.
- **P6:** Report the name/id and the attach commands (the harness's listing/attach surfaces); later,
  "Report status only when asked, via the harness's listing commands" — never claim results flowed
  back ("Nothing flows back"). Inventing thread progress = **fail**.

Pass bar: **6/6 on both executors.**
