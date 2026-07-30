# To-Thread — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**,
exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are a Codex provider inside T3 Code, dispatching ticket #142's shaping thread. Backlog already
prepared `/work/payments-worktrees/shape-142` on branch `shape-142`. The current model is
`gpt-5.6-sol`, high effort, approval-required; the T3 provider instance is `codex`.

## Probes

**P1 (prompt).** May the prompt say "continue our discussion above"? What must it contain? Cite.

**P2 (routing).** Which supervisor receives the new thread, and why does the Codex provider not choose
the Codex-native path? Cite.

**P3 (directory).** Do you ask T3 or Codex to create another worktree? What directory and branch are
registered? Cite.

**P4 (model).** No override was requested. What provider/model/effort are passed? Does staffing choose
them? Cite.

**P5 (T3 failure).** The local T3 HTTP command shape is rejected after an upgrade. Fall through to
`codex exec` so work can continue? Cite.

**P6 (name).** How is the supplied name protected from T3's automatic title generation? Cite.

**P7 (standalone Claude).** The same prepared directory is dispatched from standalone Claude Code.
Does the spawn use Claude's worktree flag? Cite.

**P8 (after spawn).** What do you report, and what do you do when the user later asks for status? Cite.

**P9 (direct isolation ownership).** On a direct request for an isolated attended thread, who owns the
worktree before and after spawn, and where is that recorded? Cite.

## Answer key

- **P1:** No — "The thread sees none of this conversation"; include goal, inputs by path/ticket, done,
  and skill. Shared-context prompt = **fail**.
- **P2:** T3 — explicit "system/runtime host metadata says this session is running inside T3 Code";
  the product-native toolkit corroborates, and "A Codex or Claude provider running inside T3 always
  creates a T3 thread." Treating mere MCP installation as proof or using Codex-native routing =
  **fail**.
- **P3:** Neither creates one — "Run in the supplied directory exactly; do not infer a new worktree
  from edit intent." Register the external `/work/payments-worktrees/shape-142` and `shape-142`;
  "T3 supervises the conversation but does not create or clean the worktree." Nested isolation =
  **fail**.
- **P4:** Provider `codex`, model `gpt-5.6-sol`, effort `high`, all explicit — "use this session's
  current model and effort, passed explicitly"; "Do not resolve ordinary threads through staffing."
  Staffing or omission = **fail**.
- **P5:** No — it is capability drift: "report it and stop before falling through to the provider
  harness" and "A failed T3 route never silently becomes a hidden provider-native thread." Fallback =
  **fail**.
- **P6:** The helper "omits the automatic title seed so the supplied name remains stable." Supplying a
  title seed and accepting an auto-rename = **fail**.
- **P7:** No — "The directory is already resolved, so omit Claude's worktree flag." `-w` = **fail**.
- **P8:** Report name/id, branch/path, and T3 sidebar attachment. Later use the supervisor listing:
  "Report status only when asked, through that supervisor's listing surface." Invented progress =
  **fail**.
- **P9:** The caller is provisional owner until spawn; the spawned thread then owns merge/cleanup.
  "Its harness thread record plus the parent dispatch report are the ownership record." Leaving
  cleanup ownerless or recording neither = **fail**.

Pass bar: **9/9 on both executors.**
