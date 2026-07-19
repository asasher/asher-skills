# Shard VIS — the `visualize` channel (post-audit addendum, coordinator-collected 2026-07-19)

Collected after the dossier's delivery, when the user produced product evidence of inline rendering in
Claude Code desktop. These packets are coordinator observations, not a fanned-out shard.

ID: VIS-1
Class: Observation
Statement: A Claude Code desktop session on 2026-07-18 rendered an SVG diagram inline in the conversation transcript via MCP tool calls labeled "Used visualize: Read me" (`mcp__visualize__read_me`, arguments `modules: ["diagram"]`, `platform: desktop`) followed by "Widget from visualize show_widget", with the rendered frame persisting in the transcript at least 17 hours later.
Source: User-provided screenshots of the session transcript (image-cache 5.png, 6.png; provided 2026-07-19)
Scope/as-of: One session, Claude Code desktop app on this user's machine, 2026-07-18
Limitations: Primary evidence of what that session displayed; not evidence of general availability, version gating, or stability elsewhere.

ID: VIS-2
Class: Observation
Statement: The `visualize` server appears in no user-level or project-level MCP configuration on this machine — `claude mcp list` returns only claude.ai connectors and railway, and `~/.claude.json` and the project `.mcp.json` contain no visualize entry — so the session's `mcp__visualize__*` tools were provisioned by the surface itself, not installed by the user.
Source: Local commands run 2026-07-19: `claude mcp list`, JSON walk of `~/.claude.json`, grep of project `.mcp.json`
Scope/as-of: This machine, 2026-07-19
Limitations: Does not establish where the server runs (in-app vs Anthropic-hosted) or which surfaces provision it.

ID: VIS-3
Class: Observation
Statement: The string `show_widget` occurs in the Claude desktop app's bundled Claude Code front-end JavaScript (`/Applications/Claude.app/Contents/Resources/ion-dist/assets/v1/index-XoaBlZfC.js`), placing the widget-rendering pathway in the shipped first-party client.
Source: grep of the installed Claude.app bundle, 2026-07-19
Scope/as-of: Claude.app installed on this machine as of 2026-07-19
Limitations: Minified bundle; establishes presence of the renderer string only, not the feature's full architecture or server location.

ID: VIS-4
Class: Observation
Statement: Per the session's own relayed account of the tool's guidance (`read_me`), the channel works by passing raw markup in the `show_widget` tool's `widget_code` argument (auto-detected as SVG when starting with `<svg`, else HTML), with the host injecting a design-system stylesheet (classes such as `c-teal`/`t`/`ts`/`th`, CSS variables such as `--surface-1`) for automatic light/dark adaptation, a CSP restricting external loads to a short CDN allowlist, `position: fixed` forbidden (frame sizes to in-flow content), scripts executing only after streaming completes, and a global `sendPrompt(text)` function inside the frame that sends a message back into the conversation.
Source: User-relayed explanation from the 2026-07-18 session (which had read the tool's `read_me` modules), provided 2026-07-19
Scope/as-of: The visualize tool's self-documentation as relayed; 2026-07-18
Limitations: Secondhand relay of the tool's own docs — accurate for what that session was told, unverified against the modules' actual text from this session (this session has no `mcp__visualize__*` tools).

ID: VIS-5
Class: Observation
Statement: A claude-code-guide agent (2026-07-19) reports that the visualize feature is absent from the Claude Code documentation map, and further asserts — without verifiable primary support — that it is an instance of the MCP Apps extension backed by an Anthropic-hosted server at `claudemcpcontent.com`, and that a GitHub issue (anthropics/claude-code#53030) reports widgets failing with HTTP 400 after render since 2026-04-24.
Source: claude-code-guide subagent report, 2026-07-19, citing code.claude.com/docs/en/claude_code_docs_map.md (absence verified), modelcontextprotocol.io extension docs, github.com/anthropics/claude-code issue #53030, and a dev.to post (inadmissible)
Scope/as-of: 2026-07-19
Limitations: The docs-map absence is credible; the MCP-Apps-identity and hosting claims are the agent's synthesis, not quoted primary text — and the visible mechanism (markup in tool arguments, host-injected design system, `sendPrompt`) differs from the MCP Apps spec shape (ui:// resource templates, postMessage JSON-RPC bridge), so identity is treated as unestablished; the instability report is contradicted by VIS-1's working, persisting render on 2026-07-18.

ID: VIS-6
Class: Unknown
Statement: Which surfaces and versions provision the `visualize` tools (desktop app only vs claude.ai/code web; version or flag gating), whether the server is in-app or Anthropic-hosted, whether it implements the MCP Apps extension internally, and its production stability are all unestablished — no official documentation exists (docs-map absence, VIS-5), and this session's environment does not expose the tools to probe.
Source: Search boundary = VIS-2/VIS-3/VIS-5 evidence plus this session's tool roster (no mcp__visualize__* available)
Scope/as-of: 2026-07-19
Limitations: A probe from a Claude Code desktop session (list tools, call read_me, exercise sendPrompt) would settle capability and stability questions empirically.
