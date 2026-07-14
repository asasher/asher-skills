# Claude Code harness mechanics

Global pointer: `~/.claude/CLAUDE.md` § Staffing. Deferred module:
`~/.claude/asher-skills/staffing.md`. Do not use an eager `@` import.

Native Claude work uses watched Agent/Workflow children. Claude→Codex work runs only inside a watched Claude
wrapper named for the external Codex model and task, such as `gpt-5.6-sol:inspect-lock`. Staff that relay with
the cheapest native Claude model allowed by the floor through the Agent/Workflow `model` parameter. Under an
explicit timeout it runs `codex exec` read-only for investigation or workspace-write for edits, closes stdin,
and returns raw output plus separate lifecycle status. Use worktree isolation for parallel edits. Never use
`claude -p` from Claude Code.

The native child request or returned metadata must prove the wrapper model. Claude Code has no native
ChatGPT-in-Chrome, Computer Use, or image-generation provider; name any machine fallback or dispatched Codex
provider explicitly and never attribute its effect to Claude.
