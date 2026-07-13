# Issue #49 — sibling harness dispatch proof

Date: 2026-07-13
Parent harness: Codex
Route: Codex → Claude Code

## Healthy Codex → Claude route

The parent launched `claude -p` through a 120-second subprocess timeout with closed stdin, explicit
`--model sonnet`, `--safe-mode`, no tools/session persistence, a $0.35 invocation ceiling, and a JSON schema.
It did **not** use `--bare`.

```text
command: claude -p --model sonnet --tools "" --safe-mode
         --no-session-persistence --max-budget-usd 0.35
         --output-format json --json-schema <schema> <prompt>
returncode: 0
elapsed: 3.33s
structured_output: {"task_id":"issue-49","reversed":"13","route":"codex-to-claude"}
independent check: reverse("31") == "13"
```

The schema-validated return is the durable task result; the parent independently checked its effect.

## Directional failure and asymmetric fallback

A deterministic invalid Claude model route failed in 2.39 seconds:

```text
route: Codex → Claude
command: claude -p --model not-a-real-model-route-49 --safe-mode <prompt>
returncode: 1
failure: selected model may not exist or be accessible
```

Only Codex→Claude was removed from the candidate set. The declared native Codex successor then ran with
closed stdin and returned the exact durable result:

```text
command: codex exec --model gpt-5.6-sol --sandbox read-only --ephemeral
         --ignore-user-config --skip-git-repo-check <prompt> </dev/null
returncode: 0
result: FALLBACK_49
```

Claude→Codex was not probed or disabled by the opposite-direction failure. No policy or credit-status monitor
participated in either decision.
