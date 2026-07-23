# Shard INT — integration shape and fallbacks (worker packets, verbatim)

> Harness note: the worker's output was relayed through a pattern filter; angle brackets in a few
> statements arrived escaped and are reproduced cleaned here. Content is otherwise verbatim.

ID: INT-1
Class: Fact
Statement: The Claude Desktop app registers local MCP servers through `claude_desktop_config.json` (`~/Library/Application Support/Claude/` on macOS, `%APPDATA%\Claude\` on Windows), where each `mcpServers` entry is a stdio launch spec (`command`, `args`, `env`) that Claude Desktop starts as a local process on launch.
Source: Connect to local MCP servers — https://modelcontextprotocol.io/quickstart/user (accessed 2026-07-18; "Installing the Filesystem Server" steps)
Scope/as-of: Claude Desktop macOS/Windows, current docs as of 2026-07-18
Limitations: Does not establish whether locally configured servers can render MCP Apps widgets, only that stdio registration exists.

ID: INT-2
Class: Fact
Statement: Claude Desktop also accepts local MCP servers as one-click MCPB desktop extensions — a `.mcpb` zip archive bundling a stdio MCP server plus `manifest.json`, installed by double-click, drag-and-drop, or Settings → Extensions, with Claude Desktop auto-generating a settings UI from `user_config`.
Source: Build a desktop extension with MCPB — https://claude.com/docs/connectors/building/mcpb (accessed 2026-07-18; "What is an MCPB?", "How users install your MCPB")
Scope/as-of: Claude Desktop macOS (`darwin`) and Windows (`win32`) only; MCPB is called "the secondary distribution path"
Limitations: Per-user installation only; does not establish availability on claude.ai web, mobile, or Claude Code.

ID: INT-3
Class: Fact
Statement: claude.ai web (and Cowork) supports only remote custom connectors — the MCP server must be reachable over the public internet from Anthropic's servers — and the Help Center states explicitly that local MCP servers configured via `claude_desktop_config.json` "aren't available in Cowork or claude.ai."
Source: Get started with custom connectors using remote MCP — https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp (accessed 2026-07-18)
Scope/as-of: claude.ai web/Cowork, all plans (Free limited to one connector), as of 2026-07-18
Limitations: Does not address Claude Desktop, where the local mechanism does work; a localhost goodwork server can never be a claude.ai connector without public hosting.

ID: INT-4
Class: Fact
Statement: Claude Code registers MCP servers via `claude mcp add [--transport stdio|http|sse] ... -- <command>` or JSON config, with local stdio servers fully supported alongside HTTP, deprecated SSE, and WebSocket, at three scopes: local (`~/.claude.json`, default), project (`.mcp.json`, shared and requiring per-user approval), and user (all projects).
Source: Connect Claude Code to tools via MCP — https://code.claude.com/docs/en/mcp (accessed 2026-07-18; "Option 3: Add a local stdio server", "MCP installation scopes")
Scope/as-of: Claude Code CLI/desktop, doc references versions up to v2.1.2xx
Limitations: Establishes transport/registration only, not any inline widget rendering in Claude Code.

ID: INT-5
Class: Fact
Statement: Codex registers MCP servers in `~/.codex/config.toml` (or project-scoped `.codex/config.toml`) as `[mcp_servers.<name>]` tables — stdio entries with `command`/`args`/`env`, or streamable HTTP entries with `url` — manageable via `codex mcp add <name> -- <command>`, and this configuration is shared across Codex CLI, IDE extension, ChatGPT desktop app, and Codex cloud, while ChatGPT web instead uses plugin-supplied remote MCP tools.
Source: Model Context Protocol — https://developers.openai.com/codex/mcp (redirects to https://learn.chatgpt.com/docs/extend/mcp?surface=cli; accessed 2026-07-18)
Scope/as-of: Codex surfaces as of 2026-07-18
Limitations: Does not establish that any Codex surface renders MCP Apps/Apps SDK widgets from these servers.

ID: INT-6
Class: Fact
Statement: The MCP Apps specification requires hosts to render UI resources (`text/html;profile=mcp-app`) in sandboxed iframes under a host-constructed CSP whose restrictive default when `ui.csp` is omitted is `default-src 'none'; ... connect-src 'none'` — i.e., no network at all — with external origins allowed only if declared in `connectDomains`/`resourceDomains`/`frameDomains` metadata, and "Host MAY further restrict but MUST NOT allow undeclared domains."
Source: MCP Apps specification — https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/draft/apps.mdx (fetched via raw.githubusercontent.com; accessed 2026-07-18; CSP section)
Scope/as-of: MCP Apps extension spec draft, SEP-1865 status Final (created 2025-11-21)
Limitations: The spec does not state whether hosts will honor a `localhost`/`127.0.0.1` origin declared in `connectDomains`; see INT-8.

ID: INT-7
Class: Fact
Statement: In MCP Apps, tool data reaches the widget through the host bridge, not the network: the iframe acts as an MCP client over a `postMessage` JSON-RPC transport, performing a `ui/initialize` handshake after which the host pushes `ui/notifications/tool-input` and `ui/notifications/tool-result`, and web hosts must interpose a double-iframe sandbox proxy.
Source: MCP Apps specification — https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/draft/apps.mdx (accessed 2026-07-18; transport/handshake and sandbox-proxy sections)
Scope/as-of: MCP Apps extension spec draft as of 2026-07-18
Limitations: Does not by itself rule out declared-domain fetches (INT-6 governs those); establishes the default data path only.

ID: INT-8
Class: Unknown
Statement: Whether any shipping host (Claude web/desktop, ChatGPT) will grant a widget CSP `connectDomains` entry for `localhost`/`127.0.0.1` — which is what goodwork's local `scripts/server.py` would need to feed a widget directly — is not stated in the MCP Apps spec, the Apps SDK reference, or Anthropic's MCP Apps announcement.
Source: Searched https://github.com/modelcontextprotocol/ext-apps spec, https://developers.openai.com/apps-sdk/reference, and https://claude.com/blog/interactive-tools-in-claude (all accessed 2026-07-18) for localhost/loopback CSP language; none found.
Scope/as-of: search boundary = those three primary sources plus support.claude.com connector articles, as of 2026-07-18
Limitations: Absence of statement, not a documented prohibition; claude.ai's sandbox-proxy web architecture and remote-connector-only model make loopback delivery additionally implausible but unconfirmed.

ID: INT-9
Class: Fact
Statement: An MCP Apps widget can invoke server tools from inside the iframe via JSON-RPC `tools/call` with `{name, arguments}`, and the spec's security model lets hosts require explicit user approval for UI-initiated tool calls, with all UI-to-host traffic auditable JSON-RPC.
Source: MCP Apps specification — https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/draft/apps.mdx; SEP-1865 — https://modelcontextprotocol.io/seps/1865-mcp-apps-interactive-user-interfaces-for-mcp (accessed 2026-07-18; Security Implications)
Scope/as-of: MCP Apps spec draft as of 2026-07-18
Limitations: Approval UX is host-discretionary ("Hosts can require"), so round-trip friction per interaction is host-dependent.

ID: INT-10
Class: Fact
Statement: Beyond `tools/call`, the MCP Apps spec gives widgets `ui/message` (send message content into the host's chat), `ui/update-model-context` (inject content into the model's context for future turns), `ui/request-display-mode` (inline|fullscreen|pip), `ui/open-link`, `ui/download-file`, and `ui/notifications/size-changed` — enough vocabulary to express "approve", "send edited text", and "don't send" as distinct host-visible acts.
Source: MCP Apps specification — https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/draft/apps.mdx (accessed 2026-07-18; message reference tables)
Scope/as-of: MCP Apps spec draft as of 2026-07-18
Limitations: Spec-level capability; which of these each shipping host implements is not established here.

ID: INT-11
Class: Fact
Statement: ChatGPT's Apps SDK exposes `window.openai.callTool(name, args)`, `window.openai.sendFollowUpMessage({prompt})`, and `window.openai.setWidgetState(state)` (with `widgetState` persisted between renders and readable alongside `toolInput`/`toolOutput`), so widget interactions can trigger tool calls, post chat messages, and persist UI state such as card positions.
Source: Reference – Apps SDK — https://developers.openai.com/apps-sdk/reference (accessed 2026-07-18)
Scope/as-of: ChatGPT Apps SDK as of 2026-07-18; the same page documents both standard MCP Apps `_meta.ui.csp` and legacy `_meta["openai/widgetCSP"]` network declarations
Limitations: Documents ChatGPT the consumer surface; not evidence that Codex CLI/IDE/desktop render these widgets.

ID: INT-12
Class: Fact
Statement: Anthropic's MCP Apps launch (January 26, 2026) ships interactive connector UIs in Claude on mobile, web, and desktop for Free through Enterprise plans, connected via claude.ai/directory, with the Slack app described as letting users "generate message drafts, format them your way, and review before you post" — a shipped approve/edit-before-send widget round-trip inside Claude chat.
Source: Interactive connectors and MCP Apps — https://claude.com/blog/interactive-tools-in-claude (published 2026-01-26; accessed 2026-07-18)
Scope/as-of: claude.ai surfaces + Cowork as of launch; connection path is directory connectors (remote MCP)
Limitations: Claude Code is not mentioned as a supporting surface; does not establish that a self-built local/stdio server's widgets render in Claude Desktop (see INT-13).

ID: INT-13
Class: Unknown
Statement: No official Anthropic documentation found states whether Claude Desktop renders MCP Apps widgets from a locally configured stdio MCP server (claude_desktop_config.json or MCPB), as opposed to directory/remote connectors.
Source: Searched https://claude.com/blog/interactive-tools-in-claude, https://support.claude.com/en/articles/11175166 (custom connectors), https://modelcontextprotocol.io/quickstart/user, and https://claude.com/docs/connectors/building/mcpb (all accessed 2026-07-18); none address MCP Apps rendering for local servers.
Scope/as-of: search boundary = Anthropic blog, Help Center connector articles, MCP quickstart, MCPB docs, as of 2026-07-18
Limitations: A live experiment (local server declaring `ui://` resources in Claude Desktop) would settle this; not performed here.

ID: INT-14
Class: Observation
Statement: The full Claude Code MCP reference page contains no mention of rendering MCP Apps, `ui://` resources, or widget iframes — its only UI-adjacent surface is server-initiated elicitation dialogs ("Claude Code displays an interactive dialog and passes your response back to the server").
Source: Connect Claude Code to tools via MCP — https://code.claude.com/docs/en/mcp (full page fetched and grepped; accessed 2026-07-18)
Scope/as-of: code.claude.com MCP reference as of 2026-07-18
Limitations: Absence in one reference page, not a definitive statement that Claude Code will never render widgets; elicitation offers structured-form input but not custom HTML UI.

ID: INT-15
Class: Unknown
Statement: No official OpenAI documentation found states that any Codex surface (CLI terminal, IDE extension, or Codex in the ChatGPT desktop app) renders Apps SDK / MCP Apps widgets from a configured MCP server; Apps SDK widget rendering is documented only for ChatGPT.
Source: Searched https://developers.openai.com/codex/mcp, https://developers.openai.com/apps-sdk/reference, and https://developers.openai.com/codex/app/browser (all accessed 2026-07-18) for widget-rendering-in-Codex statements; none found.
Scope/as-of: search boundary = Codex MCP doc, Apps SDK reference, ChatGPT desktop browser doc, as of 2026-07-18
Limitations: Absence of statement; the shared config.toml across ChatGPT desktop app surfaces (INT-5) leaves room for unadvertised behavior.

ID: INT-16
Class: Fact
Statement: OpenAI's first-party Apps SDK examples repo demonstrates free-form editable text flowing out of a widget: `src/update-model-context/App.tsx` binds a user-typed text state and submits it via `app.updateModelContext({content: [{type: "text", text: text.trim()}]})` (using the `@modelcontextprotocol/ext-apps` client), and GitHub code search also finds `textarea` in `src/kitchen-sink-lite/kitchen-sink-lite.tsx`.
Source: openai/openai-apps-sdk-examples — https://github.com/openai/openai-apps-sdk-examples/blob/main/src/update-model-context/App.tsx (file content verified; accessed 2026-07-18)
Scope/as-of: Apps SDK examples repo main branch as of 2026-07-18
Limitations: Demonstrates text→model-context; a text→tool-call path (`callTool` with typed text) is API-supported (INT-11) but not verified in a specific example file here.

ID: INT-17
Class: Fact
Statement: The Claude Code desktop app's Browser pane opens static HTML files, PDFs, images, and videos from the project when their paths are clicked in chat, and also previews localhost dev servers — with localhost previews and file previews continuing to work even when enterprise settings disable external browsing.
Source: Desktop application — https://code.claude.com/docs/en/desktop (accessed 2026-07-18; "Preview your app")
Scope/as-of: Claude Code desktop app (macOS/Windows, Linux beta) as of 2026-07-18
Limitations: Side-pane rendering, not inline chat widgets; GitHub issues report stale-HTML refresh problems (#65443) and preview unavailability in remote-control sessions (#48466) — neither verified beyond titles.

ID: INT-18
Class: Fact
Statement: Claude Code artifacts publish an HTML/Markdown file as a live page at a claude.ai URL that supports inline-JavaScript interactivity (sliders, toggles, input fields, draggable cards) but sits behind a strict CSP blocking all external scripts/styles/images and all `fetch`/XHR/WebSocket calls, with the sole external-data path being declared MCP connector calls executed by claude.ai on the page's behalf.
Source: Share session output as artifacts — https://code.claude.com/docs/en/artifacts (accessed 2026-07-18; "Page constraints", "Pull live data with MCP connectors")
Scope/as-of: Claude Code CLI ≥2.1.183 / desktop ≥1.13576.0, Pro/Max/Team/Enterprise, Anthropic API provider only; connector calls need ≥2.1.209
Limitations: "Local MCP servers you configure in Claude Code, such as servers from `.mcp.json`, can supply data while Claude builds the page, but the published page can't call them" — so a viewed artifact can never reach goodwork's localhost server; no backend, no form storage.

ID: INT-19
Class: Fact
Statement: The artifacts doc officially documents an inline-adjacent approval/board fallback pattern — a "triage board artifact with each open issue as a draggable card across Now, Next, Later, and Cut columns" plus a "Copy as prompt" export button — i.e., interaction results return to the session by user paste, not by network round-trip.
Source: Share session output as artifacts — https://code.claude.com/docs/en/artifacts (accessed 2026-07-18; "Bring the result back to your session")
Scope/as-of: Claude Code artifacts as of 2026-07-18
Limitations: Manual paste-back is the documented return path; drag state does not reach the agent automatically.

ID: INT-20
Class: Unknown
Statement: Whether claude.ai conversation artifacts (the in-chat feature, distinct from Claude Code artifacts) are documented by Anthropic with the same external-network-blocking policy was not established from an official page; the Help Center artifacts article (support.claude.com article 9487310) was located but its network-policy text was not retrieved.
Source: Search boundary — WebSearch over support.claude.com for artifacts + CSP (accessed 2026-07-18)
Scope/as-of: claude.ai in-conversation artifacts as of 2026-07-18
Limitations: Widely reported to share the sandboxed `*.claudeusercontent.com` origin, but that specific claim is not cited to an official page here.

ID: INT-21
Class: Fact
Statement: For Codex, the ChatGPT desktop app's built-in browser gives "you and ChatGPT a shared view of websites and local web apps inside a chat," opening "local routes, file-backed pages, or public pages" with visual-feedback annotations and Computer-Use interaction — a side-surface (not inline-widget) way to view a local HTML board served by a session.
Source: Browser — https://developers.openai.com/codex/app/browser (redirects to https://learn.chatgpt.com/docs/browser?surface=app; accessed 2026-07-18)
Scope/as-of: ChatGPT desktop app (Codex surface) as of 2026-07-18
Limitations: Separate browser profile with no shared session state; terminal Codex CLI has no such pane documented; not a chat-inline widget.

ID: INT-22
Class: Observation
Statement: This repo's existing fallback shape, the installed `review-loop` skill, already provides browser-page sign-off around a locally served rendered HTML artifact: detached serving (`scripts/review-server.py`), anchored annotations, one batched verdict, hash-bound approval, a revision ledger and repo hub, an `await` command with verdict exit codes (0 approve / 3 nits / 10 changes / 124 timeout), and degradation to local open (never a public tunnel) when surface config is missing.
Source: /Users/asher/Projects/asher-skills/.agents/skills/review-loop/SKILL.md (read 2026-07-18; "Commands", "Loop contract")
Scope/as-of: review-loop as installed in asher-skills at 2026-07-18
Limitations: It is an approval-gate loop, not a kanban/board data channel; per its description it never authors the artifact, and serving is browser-page, not chat-inline.

ID: INT-23
Class: Fact
Statement: In Claude Code, an agent-skill package by itself does not declare MCP servers, but the plugin system does — "Plugins define MCP servers in `.mcp.json` at the plugin root or inline in `plugin.json`" — and a skill folder becomes such a plugin by adding `.claude-plugin/plugin.json`, after which "it can bundle agents, hooks, and MCP servers" (subject to the workspace trust dialog when placed in a project's `.claude/skills/`).
Source: Connect Claude Code to tools via MCP — https://code.claude.com/docs/en/mcp; Extend Claude with skills — https://code.claude.com/docs/en/skills (both accessed 2026-07-18)
Scope/as-of: Claude Code plugins/skills as of 2026-07-18; skills' documented frontmatter covers `allowed-tools`/`disallowed-tools` but no MCP field
Limitations: Plugin-bundled servers register under scoped names (`plugin:<plugin>:<server>`); this mechanism is Claude Code-only, not claude.ai or Claude Desktop chat.

ID: INT-24
Class: Fact
Statement: Codex skills can declare — but the doc does not say auto-install — MCP dependencies: a skill's optional `agents/openai.yaml` is used "to declare tool dependencies," with the documented example `dependencies: tools: - type: "mcp" value: "openaiDeveloperDocs"`, while the same doc says plugins "optionally bundle app mappings, MCP server configuration, and presentation assets in a single package."
Source: Build skills — https://developers.openai.com/codex/skills (redirects to https://learn.chatgpt.com/docs/build-skills.md; accessed 2026-07-18)
Scope/as-of: Codex skills/plugins docs as of 2026-07-18
Limitations: The declaration names a server the user must have; whether Codex prompts to install or merely warns when the dependency is missing was not established from the fetched text.

ID: INT-25
Class: Unknown
Statement: No official mechanism was found for a skill package to bundle or declare an MCP server on the claude.ai / Claude Desktop chat surfaces — there, MCP arrives only via user-configured connectors (remote) or claude_desktop_config.json/MCPB (local), separately from any skill install.
Source: Search boundary — https://code.claude.com/docs/en/skills, https://support.claude.com/en/articles/11175166, https://claude.com/docs/connectors/building/mcpb, and the Agent Skills standard pointer at https://agentskills.io referenced from the Claude Code skills doc (accessed 2026-07-18)
Scope/as-of: claude.ai web and Claude Desktop chat as of 2026-07-18
Limitations: agentskills.io standard itself was not fetched; a field added to the standard after this date would not be captured.
