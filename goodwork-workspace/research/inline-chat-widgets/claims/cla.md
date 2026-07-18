# Shard CLA — Claude surfaces (worker packets, verbatim)

> **Coordinator correction after challenger audit (2026-07-18):** CLA-9 is reclassed **Fact → Observation**
> and its statement corrected. The cited article contains no assertion that only remote connectors support
> interactive rendering; its only remote-related text is developer guidance ("If you are building your own
> interactive connector… See the Remote MCP Server Submission Guide for details"), and it never mentions
> local servers. Corrected statement: *the only documented developer path for interactive connectors is
> remote-connector submission; the article is silent on local servers.* The original packet below is
> preserved verbatim for provenance; findings.md cites CLA-9 in this corrected reading.

ID: CLA-1
Class: Fact
Statement: MCP Apps was proposed on November 21, 2025 as SEP-1865, co-developed by Anthropic, OpenAI, and the MCP-UI creators (Ido Salomon and Liad Yosef) to "standardize support for interactive user interfaces in the Model Context Protocol."
Source: MCP Apps: Extending servers with interactive user interfaces — https://blog.modelcontextprotocol.io/posts/2025-11-21-mcp-apps/ (published 2025-11-21; accessed 2026-07-18; whole post)
Scope/as-of: Proposal announcement, Nov 2025; official MCP project blog
Limitations: Describes the proposal-stage design only; does not establish final spec status or any host's shipped support.

ID: CLA-2
Class: Fact
Statement: MCP Apps became the first official MCP extension on January 26, 2026, with spec version 2026-01-26 marked "Stable" and identified as extension `io.modelcontextprotocol/ui`, an optional extension that must be negotiated via the extension capabilities mechanism.
Source: MCP Apps specification (2026-01-26) — https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx (accessed 2026-07-18 via raw.githubusercontent.com; Status header) and MCP Apps – Bringing UI Capabilities To MCP Clients — https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/ (published 2026-01-26; accessed 2026-07-18)
Scope/as-of: Spec status as of version 2026-01-26, current as of 2026-07-18
Limitations: "Stable" is the extension's own status label; does not establish inclusion in the core MCP spec or the feature set of any later draft revision.

ID: CLA-3
Class: Fact
Statement: The MCP Apps spec and SDK live in the official `modelcontextprotocol/ext-apps` GitHub repository, with docs at modelcontextprotocol.io/docs/extensions/apps and an npm SDK `@modelcontextprotocol/ext-apps`.
Source: GitHub – modelcontextprotocol/ext-apps — https://github.com/modelcontextprotocol/ext-apps (accessed 2026-07-18; repo description) and https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/ (Resources section)
Scope/as-of: As of 2026-07-18
Limitations: Does not establish SDK version maturity or completeness of the docs site relative to the repo spec.

ID: CLA-4
Class: Fact
Statement: In the MCP Apps spec, servers declare UI templates as resources whose URI "MUST start with `ui://`", tools bind to them via `_meta.ui.resourceUri`, and the MVP supports only HTML content with MIME type `text/html;profile=mcp-app` (other formats explicitly deferred).
Source: MCP Apps specification (2026-01-26) — https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx (accessed 2026-07-18; UI Resources / Tool-UI linkage sections)
Scope/as-of: Spec version 2026-01-26
Limitations: Spec-level requirements only; individual hosts may support a subset (e.g., a limited set of display modes).

ID: CLA-5
Class: Fact
Statement: The spec's widget-host bridge is MCP JSON-RPC carried over `postMessage` between the sandboxed iframe and the host — widgets initialize with `ui/initialize` (declaring display modes `inline`, `fullscreen`, `pip` and receiving host capabilities, theme variables, and container dimensions), can invoke server tools through the host, and receive tool input/results via `ui/notifications/tool-input` and `ui/notifications/tool-result`.
Source: MCP Apps specification (2026-01-26) — https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx (accessed 2026-07-18; Communication / lifecycle sections); corroborated by https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/ ("UIs can invoke server tools, update model context, and log debugging events")
Scope/as-of: Spec version 2026-01-26
Limitations: Does not establish which of these messages each Claude surface actually implements or permits.

ID: CLA-6
Class: Fact
Statement: The spec mandates that all MCP-app content render in sandboxed iframes with restricted permissions, that all host communication go through host-controlled `postMessage`, and that hosts build the iframe CSP from server-predeclared domain lists (`connectDomains`, `resourceDomains`, `frameDomains`, `baseUriDomains`) with a restrictive default and a rule that the "Host MUST NOT allow undeclared domains."
Source: MCP Apps specification (2026-01-26) — https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx (accessed 2026-07-18; Security model / CSP sections)
Scope/as-of: Spec version 2026-01-26
Limitations: Spec obligations on hosts; does not establish the exact CSP Claude applies in practice or any Claude-specific size limits.

ID: CLA-7
Class: Fact
Statement: Anthropic launched MCP Apps support ("interactive connectors") in Claude on January 26, 2026, generally available on Claude web, desktop, mobile, and Cowork for Free, Pro, Max, Team, and Enterprise plans, enabled by connecting apps from the "featured" section of claude.ai/directory, with nine launch partners (Amplitude, Asana, Box, Canva, Clay, Figma, Hex, monday.com, Slack).
Source: Interactive connectors and MCP Apps — https://claude.com/blog/interactive-tools-in-claude (published 2026-01-26; accessed 2026-07-18; whole post)
Scope/as-of: Launch state, 2026-01-26; first-party Anthropic announcement
Limitations: Launch-day statement; does not enumerate later-added connectors or state Claude Code support (Claude Code is not mentioned).

ID: CLA-8
Class: Fact
Statement: Per Anthropic's help center (last updated 2026-03-25), interactive connectors are available to "all users on Claude, Cowork, Claude Desktop, and Claude for iOS/Android," are default-on once the underlying connector is enabled ("No additional setup is needed"), and can be toggled per-conversation via the "Search and tools" menu or controlled by Team/Enterprise admins under Organization settings > Connectors.
Source: Use interactive connectors in Claude — https://support.claude.com/en/articles/13454812-use-interactive-connectors-in-claude (updated 2026-03-25; accessed 2026-07-18)
Scope/as-of: Claude consumer surfaces as of article update 2026-03-25, still live 2026-07-18
Limitations: Article does not mention Claude Code at all, so it establishes neither support nor non-support there.

ID: CLA-9
Class: Fact
Statement: Anthropic's help center states that only remote connectors support interactive (MCP-app) rendering in Claude — developers are directed to the Remote MCP Server Submission Guide, and local MCP servers are not offered as a path to interactive rendering.
Source: Use interactive connectors in Claude — https://support.claude.com/en/articles/13454812-use-interactive-connectors-in-claude (updated 2026-03-25; accessed 2026-07-18; developer/building section)
Scope/as-of: claude.ai/desktop interactive connectors as of 2026-03-25
Limitations: Establishes the documented path only; does not prove local stdio servers are technically blocked from rendering on desktop, only that no official doc supports it.

ID: CLA-10
Class: Fact
Statement: In Claude, interactive connectors run "in sandboxed iframes with strict Content Security Policies," all interface-to-Claude communication "uses auditable JSON-RPC messaging," servers must "predeclare which external domains they need," and purchases through third-party connectors are not supported.
Source: Use interactive connectors in Claude — https://support.claude.com/en/articles/13454812-use-interactive-connectors-in-claude (updated 2026-03-25; accessed 2026-07-18; security section)
Scope/as-of: Claude web/desktop/mobile/Cowork as of 2026-03-25
Limitations: Does not publish the concrete CSP directives, iframe allowed-origin values, or any widget payload size limit.

ID: CLA-11
Class: Observation
Statement: The official MCP blog's launch-day client list credits "Claude (web and desktop)," ChatGPT (that week), VS Code Insiders, and Goose as shipping MCP Apps hosts, with JetBrains, AWS Kiro, and Antigravity in development — Claude Code appears in no official MCP Apps host list.
Source: MCP Apps – Bringing UI Capabilities To MCP Clients — https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/ (published 2026-01-26; accessed 2026-07-18; supported clients section)
Scope/as-of: Host adoption as reported 2026-01-26
Limitations: A launch-day list; Anthropic's own Jan-26 post and Mar-25 help article additionally name mobile and Cowork, so this list understates Claude surface coverage and is not evidence about Claude Code either way.

ID: CLA-12
Class: Unknown
Statement: No official source documents MCP-app widget size limits, the concrete iframe origin Claude uses for widgets, or exact CSP directive values in Claude's implementation.
Source: Searched support.claude.com (articles 13454812, 11175166, 14503689), claude.com/blog/interactive-tools-in-claude, and the ext-apps spec (which defines domain-predeclaration semantics but leaves concrete CSP construction to hosts); web searches "support.claude.com MCP apps interactive connectors", "Claude MCP apps size limit CSP"
Scope/as-of: As of 2026-07-18
Limitations: Absence of documentation, not evidence such limits don't exist.

ID: CLA-13
Class: Fact
Statement: Anthropic announced on its official blog (dated June 25, 2025 per contemporaneous coverage; the page itself renders a July 25, 2025 date) that artifacts can "interact with Claude through an API," turning artifacts into shareable AI-powered apps where a viewer's "API usage counts against their subscription, not yours" and "no one needs to manage API keys," with launch limitations listed as "No external API calls (yet)," "No persistent storage," and "Limited to a text-based completion API."
Source: Build and share AI-powered apps with Claude — https://claude.com/blog/claude-powered-artifacts (accessed 2026-07-18; announcement + limitations sections)
Scope/as-of: AI-powered artifacts at mid-2025 launch, claude.ai
Limitations: The "no persistent storage / no external API calls" limitations are launch-era and partially superseded (see CLA-14); the post does not name the JavaScript API surface.

ID: CLA-14
Class: Fact
Statement: Per Anthropic's current help center, artifacts today support AI-powered apps on all plans (viewer authenticates with their own Claude account and usage bills to their subscription), persistent storage on Pro/Max/Team/Enterprise on web and desktop only (20 MB per artifact, text-only, personal or shared, and "only available for published artifacts"), and MCP connections to external services on Pro/Max/Team/Enterprise on web and desktop with each user authenticating MCP servers independently.
Source: What are artifacts and how do I use them? — https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them (updated ~3 weeks before access; accessed 2026-07-18; capabilities sections)
Scope/as-of: claude.ai web and Claude Desktop artifacts as of ~late June 2026
Limitations: Article does not document the general external-network/CSP policy for artifact iframes or the JS API names; "text-based input" limit applies to storage, not rendering.

ID: CLA-15
Class: Unknown
Statement: The exact `window.claude.*` JavaScript API surface for artifacts (e.g., `window.claude.complete`) is not documented in any official Anthropic public doc I could reach — only the higher-level statement that artifacts "interact with Claude through an API."
Source: Searched support.claude.com article 9487310, tutorial https://claude.com/resources/tutorials/prototype-ai-powered-apps-with-claude-artifacts (states you add AI "by simply asking Claude," no API named), https://claude.com/blog/claude-powered-artifacts; web searches "window.claude.complete site:support.claude.com", "Anthropic artifacts window.claude API docs" (hits were third-party blogs, e.g. simonwillison.net, which are not admissible support)
Scope/as-of: As of 2026-07-18
Limitations: The API demonstrably exists in third-party accounts; what's unknown is only an official specification of its names, signatures, and current capability roster.

ID: CLA-16
Class: Fact
Statement: Claude Cowork offers "live artifacts" — persistent, interactive HTML dashboards that live outside any chat, re-query connected apps on open (with a short cache and a manual refresh control), and keep version history — available on paid plans, desktop app only, with sharing restricted to Team/Enterprise.
Source: Use live artifacts in Claude Cowork — https://support.claude.com/en/articles/14729249-use-live-artifacts-in-claude-cowork (updated week of access; accessed 2026-07-18)
Scope/as-of: Claude Cowork desktop app as of 2026-07-18
Limitations: Refresh is viewer/open-triggered re-querying; the article does not describe the agent pushing updates into an already-open live artifact.

ID: CLA-17
Class: Fact
Statement: Claude Code artifacts, launched in beta on June 18, 2026, publish a session's output as "a live, interactive web page" to a private URL on claude.ai (viewer at claude.ai/code/artifact, loading content from a sandboxed `*.claudeusercontent.com` origin) that opens in a browser — the page is not rendered inline in the terminal — and per current docs are available on Pro, Max, Team, and Enterprise with a claude.ai-authenticated session, requiring CLI v2.1.183+ or Claude desktop app v1.13576.0+.
Source: Claude Code now supports artifacts — https://claude.com/blog/artifacts-in-claude-code (published 2026-06-18; accessed 2026-07-18) and Share session output as artifacts — https://code.claude.com/docs/en/artifacts (accessed 2026-07-18; Availability, Create, Allowlist sections)
Scope/as-of: Claude Code CLI and desktop app as of 2026-07-18; blog stated Team/Enterprise beta at launch, docs now list Pro/Max too
Limitations: "Not rendered inline in the terminal" is by the documented design (browser viewer, Ctrl+] reopens in browser); the docs describe no in-CLI rendering, but this packet does not cover any unreleased capability.

ID: CLA-18
Class: Fact
Statement: A published Claude Code artifact page is one self-contained page served "under a strict Content Security Policy" that "blocks scripts, stylesheets, fonts, and images loaded from any other host, along with fetch, XHR, and WebSocket calls," with a 16 MiB rendered-size cap, and the sole external-data exception is MCP connector calls that the page "hands to claude.ai, which makes the network call itself" — connector calls require v2.1.209+, run under the viewer's own account with per-viewer permission prompts, work only with claude.ai-account connectors (published pages cannot call local `.mcp.json` servers), and disqualify the artifact from public-link sharing.
Source: Share session output as artifacts — https://code.claude.com/docs/en/artifacts (accessed 2026-07-18; Page constraints, Pull live data with MCP connectors sections)
Scope/as-of: Claude Code artifacts as of 2026-07-18
Limitations: Governs Claude Code-published artifact pages; claude.ai-conversation artifacts are documented separately (CLA-14) and may differ (e.g., persistent storage is documented there, not here).

ID: CLA-19
Class: Observation
Statement: No official Anthropic source shows Claude Code (CLI, its desktop app, or claude.ai/code) rendering MCP-app `ui://` widgets or any HTML inline in the conversation: the Claude Code MCP reference documents tools, resources, OAuth, and elicitation dialogs but nothing about UI resources, iframes, or widget rendering, and the Claude Code changelog contains no MCP-apps/widget/inline-HTML entries.
Source: Connect Claude Code to tools via MCP — https://code.claude.com/docs/en/mcp (accessed 2026-07-18; full page scanned for "ui://", "widget", "iframe", "render" — no relevant hits) and CHANGELOG.md — https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md (accessed 2026-07-18 via raw; grep for artifact/mcp app/widget/html/ui resource returned only terminal-rendering bugfixes)
Scope/as-of: Claude Code as of 2026-07-18
Limitations: Absence of documentation, not proof of absence in the product; Claude Code's inline-UI story is officially the browser-side artifact (CLA-17), and elicitation dialogs are the only documented interactive in-terminal UI from MCP servers.

ID: CLA-20
Class: Fact
Statement: For pushing state into an already-rendered MCP-app widget, the spec defines host-to-widget notifications — `ui/notifications/tool-input`, `ui/notifications/tool-result`, and `ui/notifications/host-context-changed` (theme, display mode, container size) — and widget-initiated tool calls through the host, but "defers persistent state storage to future versions; no current mechanism for state restoration is defined."
Source: MCP Apps specification (2026-01-26) — https://github.com/modelcontextprotocol/ext-apps/blob/main/specification/2026-01-26/apps.mdx (accessed 2026-07-18; notifications and future-work sections)
Scope/as-of: Spec version 2026-01-26
Limitations: Spec-level; establishes neither how long Claude keeps a widget live in the transcript nor whether Claude replays state when a conversation is reopened.

ID: CLA-21
Class: Unknown
Statement: Whether, in Claude's shipped surfaces, an agent can push new data into an already-rendered MCP-app widget on a later turn, and whether widget state survives across conversation turns or reloads, is not documented in any official Anthropic source.
Source: Searched https://support.claude.com/en/articles/13454812 (fetch explicitly found no state-persistence statement), https://claude.com/blog/interactive-tools-in-claude, and the ext-apps spec (persistence deferred); web searches "Claude MCP apps widget state persist turns", "interactive connectors state refresh support.claude.com"
Scope/as-of: As of 2026-07-18
Limitations: Third-party writeups discuss behavior but are inadmissible here; hands-on product behavior was not tested.

ID: CLA-22
Class: Fact
Statement: For Claude Code artifacts, the agent can push updates into an already-rendered page across turns and sessions: republishing to the same URL means "Anyone with the page open sees the update in place," each publish creates a version, other sessions can update the page given its URL, and connector-backed pages additionally self-refresh on load, on an interval, or via an on-page refresh control with browser-cached responses.
Source: Share session output as artifacts — https://code.claude.com/docs/en/artifacts (accessed 2026-07-18; Update an artifact, Pull live data with MCP connectors sections)
Scope/as-of: Claude Code artifacts as of 2026-07-18
Limitations: Update-in-place is republish-driven (whole-page version swap), not a granular data channel into running page state; in-page JS state is not stated to survive a republish.
