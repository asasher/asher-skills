# Cross-harness command shapes

Knowledge, not probe state: the command shapes that reliably reach a sibling harness, identical on every machine, shipped with the skill and reviewed with it. Nothing here is pre-verified — try, warn, fall back per [rankings-and-routing](rankings-and-routing.md) § Runtime fallback. Read the section for the harness you are dispatching **from**.

## The shape that works everywhere

Run the sibling CLI as a **foreground subprocess with stdin closed and output to a log**. Each clause is load-bearing:

- **Foreground, never a background shell** — backgrounded, the exec CLI hangs waiting to read stdin and dies silently with its dispatcher, leaving empty teed output while unrelated stderr noise masks the real cause.
- **Stdin closed** — redirect from `/dev/null` or close it outright.
- **Explicit timeout above the work's stated deadline** (the absolute deadline the work was dispatched with, where one exists) — the shell tool's default is never enough; without the override even a healthy worker is killed mid-task.
- **Tee output to a file as it streams** — the result survives a lost return path. Where the CLI offers a resumable session id, capture it at launch and resume **by id**, never `resume --last` — parallel workers collide on it and can silently resume a sibling's session.

The dispatch runs inside a watched native wrapper named `<external-model>:<task>`. The parent owns the prompt, the judgment, and verifying the deliverable; the wrapper owns only bounded process supervision and raw relay — it is **never repurposed to edit or build**. Staff the wrapper with the cheapest native model, at low effort. Briefs to an external-harness worker speak in goals and file paths — the parent harness's tool idioms stay out. No fire-and-forget shell may own delegated work.

## On Claude Code

Native Claude work uses the harness's own spawn paths (the Agent tool and its kin) — **never `claude -p` from Claude Code**; that is the shape a Codex parent uses to reach Claude.

Claude→Codex, from inside the target worktree:

```
codex exec --cd <worktree> --sandbox <envelope> '<self-contained prompt>' </dev/null
```

with the stdin/timeout/log discipline above.

## On Codex

Native Codex work uses watched native agent threads. Codex→Claude, from inside the target worktree:

```
claude -p --model <alias> '<self-contained prompt>' </dev/null
```

and it **never adds `--bare`**. `--bare` is not a harmless minimal mode: it forces Anthropic auth to `ANTHROPIC_API_KEY` or `apiKeyHelper` and skips keychain reads, so the child bypasses the machine's OAuth subscription and bills as API credits — paying twice for capacity the subscription already covers. It also skips `CLAUDE.md` auto-discovery, so the child loads none of the target repo's agent instructions, including the staffing playbook pointer: a `--bare` worker resolves unstaffed. Either reason alone is disqualifying.

## Names crossing into CLI arguments

A roster name is not necessarily a CLI alias — a versioned roster name written straight into a model argument can be rejected at invocation. Known pattern: some CLIs reject versioned names and accept bare ones (`sonnet`, not `sonnet-5`). A rejected name is an ordinary route failure at the point of use: warn, retry with the bare form, and fall back to the next-cheapest survivor if the route still fails. No alias table is recorded anywhere.

## Capabilities per harness

[rankings-and-routing](rankings-and-routing.md) § Declared capability routes owns the rule and the gap-report degradation. The harness delta: a declared route may live on the sibling harness — never attribute the dispatched provider's effect to the dispatching harness's model.
