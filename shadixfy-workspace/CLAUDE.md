# shadixfy Eval Workspace

Read and follow `AGENTS.md` in this directory before working on this eval workspace. In particular:

- Produce `claude` cells via a subagent — never `claude -p` — and get explicit approval before any
  CLI fallback (`ALLOW_CLAUDE_CLI=1`) that would incur extra usage.
- Do not report an iteration complete until `dashboard.html` has been rebuilt from the latest artifacts.
