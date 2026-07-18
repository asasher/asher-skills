# Shard OAI — OpenAI surfaces (worker packets, verbatim)

ID: OAI-1
Class: Fact
Statement: The Apps SDK is OpenAI's open-source framework that extends the Model Context Protocol (MCP) so developers can build UIs alongside their MCP servers, with the UI delivered as a web component running inside an iframe in ChatGPT.
Source: OpenAI for Developers in 2025 — https://developers.openai.com/blog/openai-for-developers-2025 ("we introduced the Apps SDK—an open-source framework that extends the Model Context Protocol (MCP) to let developers build UIs alongside their MCP servers"); Build your ChatGPT UI — https://developers.openai.com/apps-sdk/build/chatgpt-ui ("Your components run inside an iframe in ChatGPT") (accessed 2026-07-18)
Scope/as-of: Apps SDK docs as published 2026-07-18; ChatGPT as host surface
Limitations: Does not establish a preview/GA label or launch date; does not cover non-ChatGPT hosts.

ID: OAI-2
Class: Fact
Statement: As of today the Apps SDK distribution model is "Apps are now submitted and published as plugins" — developer mode is used for testing, and public distribution goes through the plugin submission portal with identity verification enforced during review.
Source: Apps SDK landing — https://developers.openai.com/apps-sdk; Connect from ChatGPT — https://developers.openai.com/apps-sdk/deploy/connect-chatgpt; Prepare and maintain an app for plugin submission — https://developers.openai.com/apps-sdk/deploy/submission (accessed 2026-07-18)
Scope/as-of: 2026-07-18, ChatGPT app distribution
Limitations: Does not establish when the plugin-based model replaced the earlier app-directory submission flow, nor per-country availability.

ID: OAI-3
Class: Fact
Statement: ChatGPT has been "fully compatible with the MCP Apps spec" since the Apps SDK changelog entry dated 2026-02-22.
Source: Apps SDK Changelog — https://developers.openai.com/apps-sdk/changelog (entry 2026-02-22; accessed 2026-07-18)
Scope/as-of: ChatGPT host, as of 2026-02-22 onward
Limitations: Does not enumerate which MCP Apps spec version or which ChatGPT clients (web/desktop/mobile) attained compatibility on that date.

ID: OAI-4
Class: Fact
Statement: An app ships UI by registering an HTML resource on its MCP server (ui:// URI; mimeType "text/html;profile=mcp-app", with "text/html+skybridge" as the legacy ChatGPT form) and linking it to a tool via `_meta: { ui: { resourceUri } }` / `"openai/outputTemplate"`, which ChatGPT renders in a sandboxed iframe.
Source: Build your ChatGPT UI — https://developers.openai.com/apps-sdk/build/chatgpt-ui (registerResource example, `_meta` linking); Reference — https://developers.openai.com/apps-sdk/reference ("UI templates use `ui://` URIs or `text/html+skybridge` resources for iframe delivery") (accessed 2026-07-18)
Scope/as-of: Apps SDK docs, 2026-07-18
Limitations: Does not establish rendering behavior in any host other than ChatGPT.

ID: OAI-5
Class: Fact
Statement: The window.openai bridge lets a widget read `toolInput`, `toolOutput`, `toolResponseMetadata`, and `widgetState`; persist UI state via `setWidgetState(state)`; invoke server tools via `callTool(name, args)`; post a user-visible message via `sendFollowUpMessage({ prompt, scrollToBottom })`; and request layout changes via `requestDisplayMode` (PiP/fullscreen), plus `requestModal`, `requestClose`, `notifyIntrinsicHeight`, `openExternal`, file APIs (`uploadFile`, `selectFiles`, `getFileDownloadUrl`), and environment globals (`theme`, `displayMode`, `maxHeight`, `safeArea`, `locale`).
Source: Reference – Apps SDK — https://developers.openai.com/apps-sdk/reference (accessed 2026-07-18; window.openai API sections)
Scope/as-of: Apps SDK reference as of 2026-07-18
Limitations: Does not establish which APIs are available on every ChatGPT client version, nor rate/permission limits per API.

ID: OAI-6
Class: Fact
Statement: Widget iframes are network-restricted by CSP metadata declared on the resource template — `_meta.ui.csp` with `connectDomains`, `resourceDomains`, and optional `frameDomains` (subframes are blocked by default), legacy `_meta["openai/widgetCSP"]` snake_case keys including `redirect_domains` for allowlisting `openExternal` targets — and hosted components get a dedicated origin defaulting to https://web-sandbox.oaiusercontent.com.
Source: Reference – Apps SDK — https://developers.openai.com/apps-sdk/reference (Sandbox & Security section); Build your ChatGPT UI — https://developers.openai.com/apps-sdk/build/chatgpt-ui ("By default, widgets can't render subframes…") (accessed 2026-07-18)
Scope/as-of: Apps SDK docs, 2026-07-18
Limitations: Does not enumerate the full default CSP directive set (e.g., script-src specifics) or differences across ChatGPT clients.

ID: OAI-7
Class: Fact
Statement: ChatGPT developer mode — enabled at Settings → Security and login on ChatGPT web and available to Pro, Plus, Business, Enterprise, and Education accounts — provides full MCP client support (read and write tools) for connecting unreviewed MCP-backed apps, and is flagged by OpenAI as "Elevated risk."
Source: ChatGPT Developer mode — https://developers.openai.com/api/docs/guides/developer-mode; Connect from ChatGPT — https://developers.openai.com/apps-sdk/deploy/connect-chatgpt (accessed 2026-07-18)
Scope/as-of: 2026-07-18; developer-mode configuration is on ChatGPT web
Limitations: Does not establish per-workspace admin/RBAC details (the Help Center article on developer mode returned HTTP 403 to fetch).

ID: OAI-8
Class: Fact
Statement: The Connect-from-ChatGPT docs state that an app linked via developer mode on ChatGPT web "will be available on ChatGPT mobile apps as well," making web and mobile the surfaces the Apps SDK docs explicitly name for app availability.
Source: Connect from ChatGPT – Apps SDK — https://developers.openai.com/apps-sdk/deploy/connect-chatgpt (accessed 2026-07-18)
Scope/as-of: 2026-07-18
Limitations: This establishes app availability, not a per-surface widget-rendering guarantee; the fetched Apps SDK pages contain no explicit web/desktop/iOS/Android widget-rendering matrix (troubleshooting only implies mobile rendering via `displayMode`/`maxHeight` layout guidance).

ID: OAI-9
Class: Fact
Statement: Since 2026-07-09 the standalone Codex desktop app has been merged into the ChatGPT desktop app ("Codex joins the ChatGPT desktop app 26.707") on macOS and Windows, and the latest Codex CLI release visible in the changelog is 0.144.6 dated 2026-07-18.
Source: Codex changelog — https://learn.chatgpt.com/docs/changelog (redirect target of https://developers.openai.com/codex/changelog; entries 2026-07-09 and Codex CLI 0.144.6, 2026-07-18; accessed 2026-07-18)
Scope/as-of: Codex desktop/CLI, 2026-07-18
Limitations: Does not establish what UI capabilities the merged Codex surface inherited from ChatGPT desktop.

ID: OAI-10
Class: Fact
Statement: Codex's official MCP documentation lists its supported MCP features as STDIO servers, Streamable HTTP servers, and server instructions — shared via config.toml across "the ChatGPT desktop app, Codex CLI, and IDE extension" — and contains no mention of rendering UI resources, widgets, HTML, ui:// resources, or MCP Apps in the conversation.
Source: Model Context Protocol – Codex — https://learn.chatgpt.com/docs/extend/mcp?surface=cli and ?surface=app (redirect target of https://developers.openai.com/codex/mcp; "Supported MCP features" section; accessed 2026-07-18)
Scope/as-of: Codex CLI, IDE extension, and ChatGPT-desktop Codex surface, 2026-07-18
Limitations: Absence from this doc page is not proof of absence in the product; see OAI-11/OAI-12 for corroborating repo evidence.

ID: OAI-11
Class: Fact
Statement: openai/codex PR #19884 ("Add MCP app feature flag"), merged 2026-04-27 by an OpenAI engineer, adds an `enable_mcp_apps` flag to the codex-features registry explicitly kept "under development and disabled by default," meaning MCP Apps inline UI in Codex exists only behind a default-off feature gate.
Source: Add MCP app feature flag — https://github.com/openai/codex/pull/19884 (merged 2026-04-27; accessed 2026-07-18)
Scope/as-of: openai/codex codebase as of 2026-07-18
Limitations: Does not establish what the flag renders when enabled, whether it works end-to-end, or any timeline for default enablement.

ID: OAI-12
Class: Observation
Statement: openai/codex issue #21019 (opened 2026-05-04, still open with no maintainer resolution as of today) reports that Codex Desktop calls MCP tools successfully and logs `mcp_app_resource_uri` but "does not render MCP Apps inline UI resources," showing only the textual tool result and never fetching the resource.
Source: Codex Desktop does not render MCP Apps inline UI resources… — https://github.com/openai/codex/issues/21019 (opened 2026-05-04; accessed 2026-07-18)
Scope/as-of: Codex Desktop 26.429.30905, observed by an external reporter; issue state as of 2026-07-18
Limitations: User-filed report, not an OpenAI statement; version predates the 2026-07-09 merge into ChatGPT desktop, so behavior in ChatGPT desktop 26.707+ is not directly established.

ID: OAI-13
Class: Observation
Statement: No official Codex documentation page fetched today (MCP docs at learn.chatgpt.com/docs/extend/mcp for cli and app surfaces, config-advanced, changelog, app-server) states that any Codex surface — CLI, IDE extension, desktop, or web — renders inline interactive widgets or HTML in conversation, and the config docs expose no MCP-apps/UI setting.
Source: Search boundary — WebSearch over developers.openai.com/learn.chatgpt.com for "codex widgets / MCP Apps / ui:// / render"; WebFetch of https://learn.chatgpt.com/docs/extend/mcp?surface=cli, https://learn.chatgpt.com/docs/extend/mcp?surface=app, https://learn.chatgpt.com/docs/config-file/config-advanced, https://learn.chatgpt.com/docs/changelog, https://learn.chatgpt.com/docs/app-server (all accessed 2026-07-18)
Scope/as-of: Official Codex docs as of 2026-07-18
Limitations: Bounded absence claim — the full config reference page and every changelog entry were summarized, not read line-by-line, and undocumented product behavior could differ.

ID: OAI-14
Class: Fact
Statement: The Codex App Server is a JSON-RPC 2.0 protocol (stdio, WebSocket, or Unix-socket transports) that rich clients such as the Codex VS Code extension use to embed Codex, with the embedding application building its own UI — it is not a mechanism by which Codex renders app HTML or widgets.
Source: Codex App Server — https://learn.chatgpt.com/docs/app-server ("Codex app-server is the interface Codex uses to power rich clients (for example, the Codex VS Code extension)"; accessed 2026-07-18)
Scope/as-of: Codex integration surface, 2026-07-18
Limitations: Does not preclude a future first-party client rendering MCP UI over this protocol.

ID: OAI-15
Class: Fact
Statement: Plugins — the current distribution unit that can bundle apps, skills, connectors, and MCP servers — are available in ChatGPT web (Work mode), the ChatGPT desktop app (Work mode or Codex), and Codex CLI via `/plugins`, but "Plugins aren't available in Chat mode, the IDE extension, or mobile."
Source: Plugins – ChatGPT Learn — https://learn.chatgpt.com/docs/plugins?surface=app (accessed 2026-07-18)
Scope/as-of: 2026-07-18
Limitations: Plugin availability on a surface does not establish that apps inside a plugin render UI on that surface; the plugins and build-app pages fetched contain no statement that app widgets render inside Codex.

ID: OAI-16
Class: Observation
Statement: The Apps SDK changelog entry dated 2026-03-25 says the docs now explain that OpenAI turns approved apps into plugins for distribution, tying app distribution to the Codex plugin system.
Source: Apps SDK Changelog — https://developers.openai.com/apps-sdk/changelog (entry 2026-03-25; accessed 2026-07-18)
Scope/as-of: 2026-03-25 changelog entry, read via summarizing fetch
Limitations: The fetched paraphrase ("for now plugins are only available in Codex") may be imprecise; the exact original wording of this entry's surface-availability clause was not verified verbatim.

ID: OAI-17
Class: Fact
Statement: For ChatGPT apps the MCP server must be reachable over HTTPS — local development requires a tunnel ("use Secure MCP Tunnel… or you can expose a local server to the public internet via a tool such as ngrok or Cloudflare Tunnel") — so a purely local stdio MCP server cannot power a ChatGPT app.
Source: Connect from ChatGPT – Apps SDK — https://developers.openai.com/apps-sdk/deploy/connect-chatgpt (accessed 2026-07-18)
Scope/as-of: ChatGPT app connections, 2026-07-18
Limitations: Does not cover ChatGPT desktop's Codex mode, which reads local config (see OAI-18).

ID: OAI-18
Class: Fact
Statement: Codex natively supports local stdio MCP servers — `[mcp_servers.<name>]` in `~/.codex/config.toml` (or project `.codex/config.toml`) with `command`/`args`/`env` launches a local process, while `url` (+ optional `bearer_token_env_var`) configures a Streamable HTTP server, manageable via `codex mcp add`/`codex mcp list` — but ChatGPT web "doesn't read local Codex configuration files."
Source: Model Context Protocol – Codex — https://learn.chatgpt.com/docs/extend/mcp?surface=cli (transports and config; accessed 2026-07-18); Configuration Reference — https://developers.openai.com/codex/config-reference (per WebSearch result listing, same content family)
Scope/as-of: Codex CLI / IDE extension / ChatGPT desktop Codex host, 2026-07-18
Limitations: Establishes tool connectivity only — a local server's UI resources still are not rendered by Codex (OAI-10 to OAI-13).

ID: OAI-19
Class: Fact
Statement: Widget state is message-scoped — "Every response that returns a widget creates a fresh instance with its own UI state," state saved with `setWidgetState` (synchronous call, background persistence) is restored when the same message's widget re-renders or the chat is reopened, but it does not carry across to widgets from other messages/turns.
Source: Managing State – Apps SDK — https://developers.openai.com/apps-sdk/build/state-management; Reference — https://developers.openai.com/apps-sdk/reference (accessed 2026-07-18)
Scope/as-of: ChatGPT widget runtime, 2026-07-18
Limitations: No documented size limit for widget state was found; cross-turn continuity must instead come from server-side data or new tool calls.

ID: OAI-20
Class: Fact
Statement: Widgets re-render on new agent/tool activity by listening for MCP Apps bridge notifications over postMessage — re-rendering from `structuredContent` when `ui/notifications/tool-result` arrives (and `ui/notifications/tool-input` for approval-gated input) — and "the widget keeps its UI state and re-applies it when authoritative data is refreshed"; UI state is not model-visible unless the widget explicitly calls `ui/update-model-context`.
Source: Build your ChatGPT UI — https://developers.openai.com/apps-sdk/build/chatgpt-ui ("Listen for notifications and re-render from structuredContent"); Managing State — https://developers.openai.com/apps-sdk/build/state-management; Reference — https://developers.openai.com/apps-sdk/reference (accessed 2026-07-18)
Scope/as-of: ChatGPT widget runtime, 2026-07-18
Limitations: Documents host-pushed notifications tied to tool calls; does not establish any server-initiated push channel independent of a tool call in the conversation.

ID: OAI-21
Class: Unknown
Statement: The Apps SDK's original preview/GA milestone dates (reported elsewhere as a 2025-10-06 DevDay preview launch and 2025-12-17 opening of app submissions) could not be confirmed from primary sources today.
Source: Search boundary — https://openai.com/index/introducing-apps-in-chatgpt/, https://openai.com/index/developers-can-now-submit-apps-to-chatgpt/, and https://help.openai.com/en/articles/12584461 all returned HTTP 403 to WebFetch on 2026-07-18; the Apps SDK changelog's earliest retrievable entry was 2025-11-04 and carried no "preview"/"GA" label
Scope/as-of: Fetch attempts on 2026-07-18
Limitations: Dates above come only from secondary search snippets (VentureBeat, search-result summaries) and are not certified by this packet.
