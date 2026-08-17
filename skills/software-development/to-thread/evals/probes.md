# To-Thread — situated dry-run probes

Pre-deployment probes per `docs/agents/probe-evals.md`: both executors, **only `SKILL.md` in context**, exact-sentence citation per answer. Ambiguity flagged with a citation is valid. Key before runs.

## Scenario

You are a Codex provider inside T3 Code, dispatching ticket #142's shaping thread. Backlog already prepared `/work/payments-worktrees/shape-142` on branch `shape-142`. The current model is `gpt-5.6-sol`, high effort, approval-required; the T3 provider instance is `codex`.

## Probes

**P1 (prompt).** May the prompt say "continue our discussion above"? What must it contain? Cite.

**P2 (routing).** Which supervisor receives the new thread, and why does the Codex provider not choose the Codex-native path? Cite.

**P3 (directory).** Do you ask T3 or Codex to create another worktree? What directory and branch are registered? Cite.

**P4 (model).** No override was requested. What provider/model/effort are passed? Does staffing choose them? Cite.

**P5 (T3 failure).** The local T3 HTTP command shape is rejected after an upgrade. Fall through to `codex exec` so work can continue? Cite.

**P6 (name).** How is the supplied name protected from T3's automatic title generation? Cite.

**P7 (standalone Claude).** The same prepared directory is dispatched from standalone Claude Code. Does the spawn use Claude's worktree flag? Cite.

**P8 (after spawn).** What do you report, and what do you do when the user later asks for status? Cite.

**P9 (direct isolation ownership).** On a direct request for an isolated attended thread, who owns the worktree before and after spawn, and where is that recorded? Cite.

**P10 (runtime mode value).** Your Codex session runs with sandbox mode `workspace-write`. What value do you pass as `--runtime-mode`? Cite.

**P11 (orphaned partial thread).** The helper created the thread, turn start failed, and the compensating delete also failed. What does the error carry for the user, and do you retry through the provider harness? Cite.

## Answer key

- **P1:** No — "The thread sees none of this conversation"; include goal, inputs by path/ticket, done, and skill. Shared-context prompt = **fail**.
- **P2:** T3 — explicit "System or runtime host metadata says this session runs inside T3 Code"; a call to the `t3-code` MCP server "reports this session's own tab or session context", and "a Codex or Claude provider running inside T3 always creates a T3 thread." Treating mere MCP installation as proof or using Codex-native routing = **fail**.
- **P3:** Neither creates one — "run in the supplied directory exactly." Register the external `/work/payments-worktrees/shape-142` and `shape-142`; "T3 supervises the conversation but does not create or clean the worktree." Nested isolation = **fail**.
- **P4:** Provider `codex`, model `gpt-5.6-sol`, effort `high`, all explicit — "the dispatching session's current model and effort, passed explicitly"; "staffing is never consulted for threads." Staffing or omission = **fail**.
- **P5:** No — it is capability drift: "report it and stop before falling through to the provider harness." Fallback = **fail**.
- **P6:** The helper "omits the automatic title seed so the supplied name remains stable." Supplying a title seed and accepting an auto-rename = **fail**.
- **P7:** No — "The directory is already resolved, so omit Claude's worktree flag." `-w` = **fail**.
- **P8:** Report per the shared contract: "give the user the name/id, the attachment path, the exact directory, and the branch." For later status, point at the attach surface: "attach-ability exists so the user can look in." Invented progress = **fail**.
- **P9:** "The caller is provisional owner until spawn, the spawned thread then owns merge/cleanup, and its standalone prompt says so." Leaving cleanup ownerless or the prompt silent on ownership = **fail**.
- **P10:** A T3 runtime mode (here the session's `approval-required`) — "`--runtime-mode` takes T3's own runtime modes ... never a provider sandbox name like `workspace-write`". Passing `workspace-write` = **fail**.
- **P11:** The error "names the orphaned thread id and title and tells the user to discard it from the T3 sidebar"; no provider-harness retry — "report it and stop before falling through to the provider harness." Silent fallback or an unnamed orphan = **fail**.

Pass bar: **11/11 on both executors.**
