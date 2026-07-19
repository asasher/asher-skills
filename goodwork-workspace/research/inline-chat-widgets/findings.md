# Findings — inline interactive widgets in chat harnesses

**Question, use, scope, boundary:** see [brief.md](brief.md). As-of **2026-07-18**; all web sources accessed
that day. Claim IDs (CLA-*, OAI-*, INT-*) resolve in [claims/](claims/). Classes are marked inline:
(F) fact, (O) observation, (I) inference, (U) unknown.

## 1. Concise answer

There is now one cross-vendor standard for inline chat widgets — the **MCP Apps extension**
(`io.modelcontextprotocol/ui`, spec 2026-01-26, stable; ui:// HTML resources in sandboxed iframes with a
postMessage JSON-RPC bridge) — and it is **GA in Claude** (web, desktop, mobile, Cowork; since 2026-01-26)
and **fully supported in ChatGPT** (since 2026-02-22). It is exactly the right shape for goodwork's board
and approval flow: widgets can call tools, send chat messages, carry editable text, and receive pushed tool
results; Anthropic's launch Slack connector is described as letting users "generate message drafts, format
them your way, and review before you post."

The two catches for goodwork as a *local* skill: **(1)** on Claude, official docs show interactive
connectors arriving only as remote directory connectors and are silent on local servers — claude.ai web
explicitly cannot see local servers, and whether a local stdio server's widgets render in Claude Desktop is
undocumented (a one-hour experiment would settle it); **(2)** the **Codex app does not render widgets
today** — MCP Apps support exists in the codebase behind a default-off "under development" feature flag,
and its MCP docs stop at tools. On Claude Code there is likewise no inline widget rendering; its official
stories are the desktop Browser pane (which previews localhost — goodwork's existing server drops straight
in) and browser-side artifacts. So: chat-inline is achievable on claude.ai/Claude Desktop (pending the
local-server rendering question), near-term-plausible on Codex (flag exists), and out of scope on Claude
Code/Codex CLI today — where the local server + side-pane/browser remains the right fallback, which is the
architecture goodwork already has.

## 2. Support matrix (facts/observations)

| Surface | Inline widget mechanism | Status today | Key claims |
|---|---|---|---|
| claude.ai web | MCP Apps ("interactive connectors") | **GA** since 2026-01-26, all plans; remote connectors only | CLA-7, CLA-8, CLA-9, INT-3 |
| Claude desktop | MCP Apps | **GA**; docs show only remote directory connectors and are silent on local servers; local-stdio rendering **undocumented** | CLA-7, CLA-8, CLA-9 (O, corrected), INT-13 (U) |
| Claude mobile | MCP Apps | GA | CLA-8 |
| Claude Code (CLI/desktop/web) | **`visualize` (first-party, undocumented)** — see §9 addendum | Product evidence 2026-07-18: inline SVG/HTML widgets render in the desktop app via auto-provisioned `mcp__visualize__*` tools; nothing in official docs. Also: desktop Browser pane (localhost preview), Claude Code artifacts (browser-side) | VIS-1..6, CLA-19 (O), INT-14 (O), INT-17, CLA-17, CLA-18 |
| ChatGPT web/desktop/mobile | Apps SDK on MCP Apps | Fully MCP Apps compatible since 2026-02-22; dev mode for unreviewed servers; distribution via plugins | OAI-3, OAI-4, OAI-7, OAI-8, OAI-2 |
| Codex (CLI / IDE / desktop-now-merged-into-ChatGPT-desktop) | none shipped | MCP tools yes (stdio + HTTP via config.toml); widget rendering **not shipped per any official source** — `enable_mcp_apps` flag merged 2026-04-27, default-off, "under development"; a user report observes non-rendering (pre-merge build; see U-4) | OAI-9, OAI-10, OAI-11, OAI-12 (O), OAI-18, INT-15 (U) |

## 3. Facts and observations by subquestion

### The mechanism (spec level)
- MCP Apps proposed 2025-11-21 as SEP-1865 by Anthropic + OpenAI + MCP-UI authors; became the first
  official MCP extension 2026-01-26, spec marked Stable. (F: CLA-1, CLA-2)
- Servers declare UI templates as `ui://` resources, MIME `text/html;profile=mcp-app`; tools bind via
  `_meta.ui.resourceUri`. HTML-only MVP. (F: CLA-4, OAI-4)
- Bridge = MCP JSON-RPC over postMessage: `ui/initialize` (display modes inline/fullscreen/pip, theme,
  size), widget-initiated `tools/call`, host-pushed `ui/notifications/tool-input`/`tool-result`.
  (F: CLA-5, INT-7)
- Sandboxed iframes; host builds CSP from server-predeclared domain lists; default when nothing is
  declared is **no network at all** (`connect-src 'none'`); hosts must not allow undeclared domains.
  (F: CLA-6, INT-6)
- Widget vocabulary covers goodwork's verbs: `tools/call`, `ui/message` (post into chat),
  `ui/update-model-context`, display-mode requests. (F: INT-9, INT-10)
- Editable text in widgets is real, not theoretical: OpenAI's first-party `update-model-context` example
  binds user-typed text state and submits it to model context; a `textarea` also appears in the
  kitchen-sink-lite example (found via code search; its submit path unverified). (F: INT-16)
- Persistence is deferred at spec level ("no current mechanism for state restoration"); ChatGPT layers its
  own: `setWidgetState` is message-scoped — restored for the same message's widget, not across turns.
  (F: CLA-20, OAI-19)
- Refresh model: widgets re-render from pushed tool results; no documented server-push channel independent
  of a conversation tool call, on either vendor. (F: OAI-20; U: CLA-21)

### Claude surfaces
- "Interactive connectors" GA on Claude web/desktop/mobile/Cowork since 2026-01-26, default-on per
  connector, toggleable per conversation. (F: CLA-7, CLA-8)
- The shipped Slack app demonstrates exactly goodwork's approval shape in-chat: "generate message drafts,
  format them your way, and review before you post." (F: INT-12)
- **The docs document only remote connectors as interactive** — the developer path points at the
  remote-MCP submission guide and the articles are silent on local servers (an absence, not a stated
  prohibition); claude.ai web explicitly cannot see local servers at all. (O: CLA-9 as corrected; F: INT-3)
- Local stdio servers register on Claude Desktop via `claude_desktop_config.json` or one-click MCPB
  bundles — but no official source says whether their widgets render. (F: INT-1, INT-2; U: INT-13)
- Claude Code: no MCP Apps in docs or changelog; interactive in-terminal UI stops at elicitation dialogs.
  Its official rich-output paths are (a) the desktop Browser pane — opens project HTML files clicked in
  chat and previews localhost servers, even with external browsing disabled; (b) Claude Code artifacts —
  interactive browser pages on claude.ai, strict CSP (no fetch/XHR/WebSocket, 16 MiB), updatable in place
  by republish, with MCP-connector-mediated data as the only live-data path — local `.mcp.json` servers can
  supply data while the page is built, "but the published page can't call them." (O: CLA-19, INT-14; F: INT-17, CLA-17, CLA-18, CLA-22)
- claude.ai conversation artifacts (distinct feature): AI-powered apps all plans; persistent storage
  (20 MB, published artifacts, paid plans, web+desktop); MCP connections from artifacts on paid plans.
  (F: CLA-14)

### OpenAI surfaces
- Apps SDK = MCP server + HTML resource + `window.openai` bridge (toolInput/toolOutput/widgetState,
  callTool, sendFollowUpMessage, requestDisplayMode, file APIs). (F: OAI-1, OAI-4, OAI-5)
- ChatGPT fully MCP Apps compatible since 2026-02-22; legacy `text/html+skybridge` still recognized.
  (F: OAI-3, OAI-4)
- ChatGPT apps require an HTTPS-reachable MCP server — local dev goes through a tunnel; a purely local
  stdio server cannot power a ChatGPT app. Developer mode (web settings; Pro/Plus/Business/Enterprise/Edu)
  connects unreviewed servers; public distribution is via plugins with identity-verified review.
  (F: OAI-17, OAI-7, OAI-2)
- Codex: desktop app merged into ChatGPT desktop 2026-07-09; MCP docs cover stdio/HTTP servers and
  instructions only; `enable_mcp_apps` feature flag merged 2026-04-27 default-off "under development";
  open issue #21019 documents tools working but UI resources not rendered; plugins reach ChatGPT web (Work
  mode), desktop (Work/Codex), and Codex CLI — but not Chat mode, IDE extension, or mobile.
  (F: OAI-9, OAI-10, OAI-11, OAI-15; O: OAI-12)
- ChatGPT desktop's built-in Browser gives a shared in-chat view of localhost pages on the Codex surface —
  a side surface, not an inline widget. (F: INT-21)

### Shipping a local skill's UI
- Registration paths exist everywhere for *tools*: claude_desktop_config.json / MCPB (Claude Desktop),
  `claude mcp add` / `.mcp.json` (Claude Code), `config.toml` / `codex mcp add` (Codex). (F: INT-1, INT-2,
  INT-4, INT-5)
- Bundling: a Claude Code skill becomes a plugin (`.claude-plugin/plugin.json`) to carry an MCP server;
  Codex skills *declare* MCP dependencies in `agents/openai.yaml`; no bundling path exists for claude.ai /
  Claude Desktop chat — connectors are configured separately from skills. (F: INT-23, INT-24; U: INT-25)
- Data path for a widget is the bridge, not localhost: with no declared domains a widget has zero network,
  and no source documents any host honoring a localhost `connectDomains` entry. All board/approval data
  would flow through tool results; all user actions through widget-initiated tool calls. (F: INT-6, INT-7;
  U: INT-8)

## 4. Inferences

- **I-1.** Goodwork's approval flow (read exact text → edit it inline → approve/reject → agent executes) is
  expressible as an MCP Apps widget on surfaces that render them: editable text out of widgets is
  demonstrated first-party, approval verbs map to `tools/call`/`ui/message`, and Anthropic ships the same
  UX shape in its Slack connector. (From CLA-5, INT-9, INT-10, INT-16, INT-12.)
- **I-2.** The widget architecture would invert goodwork's data path but preserve its trust model: instead
  of the browser polling a localhost server, a goodwork MCP server returns board/approval data as tool
  results, and every user action arrives as an auditable widget-initiated tool call — the same
  "server/UI may only request; agent validates and writes" contract, with hashes carried in tool args.
  (From INT-6, INT-7, INT-9; goodwork state model in `reference/state.md`/`execution.md`.)
- **I-3.** On claude.ai web the whole-experience-in-chat goal conflicts with goodwork's locality: widgets
  require a remote connector, and goodwork's workspace is sensitive personal data on disk. In-chat there
  means hosting a goodwork MCP server off-machine (or tunneling), a deliberate privacy/architecture
  decision, not a packaging detail. (From INT-3, CLA-9; goodwork sensitivity rule in SKILL.md.)
- **I-4.** Claude Desktop is the one surface where "whole experience in chat, fully local" might already
  work — local stdio registration exists and the surface renders MCP Apps GA — but the coupling of the two
  is the pivotal unverified fact (INT-13). A minimal probe server (one ui:// resource, one tool) in
  claude_desktop_config.json settles it empirically in about an hour. (From CLA-7, INT-1, INT-2, INT-13.)
- **I-5.** For the harnesses goodwork actually runs in today (Claude Code, Codex CLI/desktop), no official
  source documents inline widget rendering as of 2026-07-18 — for Codex the shipped code carries a
  default-off flag, and for Claude Code the MCP docs and changelog are silent — so the current local server
  remains load-bearing; but both vendors' direction (Codex's `enable_mcp_apps` flag; MCP Apps as the shared
  standard) makes a goodwork MCP server with ui:// templates forward-compatible: build once, light up per
  harness as flags ship. (From OAI-10, OAI-11, OAI-12, CLA-19, INT-14, CLA-2, OAI-3.)
- **I-6.** Best inline-adjacent fallbacks per non-widget surface: Claude Code desktop → Browser pane
  pointed at the existing localhost kanban (clickable from chat, survives external-browsing lockdown);
  Codex on ChatGPT desktop → the built-in shared browser on the localhost board; terminal-only sessions →
  the current tailnet/browser flow. Claude Code artifacts suit read-only sharing, not the approval loop —
  no localhost reach and paste-back returns. (From INT-17, INT-21, CLA-18, INT-19, INT-22.)

## 5. Contradictions

- **Spec citation split, no conflict:** CLA packets cite `specification/2026-01-26/apps.mdx` ("Stable");
  INT packets cite `specification/draft/apps.mdx` (SEP-1865 "Final"). Same repo; the draft tree is the
  living copy of the released 2026-01-26 extension. Treated as one spec.
- **Launch-day host list vs. Anthropic's own list:** the MCP blog credits "Claude (web and desktop)" while
  Anthropic's announcement adds mobile and Cowork (CLA-11 vs CLA-7/8). Anthropic is authoritative for its
  own surfaces; noted, not material.
- **Artifacts blog date renders inconsistently** (June vs July 2025) — flagged inside CLA-13; immaterial.
- **CLA-9 over-read (caught in audit):** the worker's packet asserted the help-center article "states" that
  only remote connectors are interactive; the article actually documents only the remote developer path and
  is silent on local servers. Reclassed Fact → Observation with corrected wording (note in claims/cla.md);
  the conclusion is unchanged because the claude.ai-web restriction rests independently on INT-3 and the
  Desktop question was already quarantined as U-1.
- No material contradiction affects the decision.

## 6. Unknowns (with consequence)

- **U-1 (pivotal): local stdio widgets on Claude Desktop** (INT-13, CLA-9-limitation). Decides whether
  fully-local in-chat goodwork exists on any surface today. Settle by experiment, not more reading.
- **U-2: localhost in widget CSP allowlists** (INT-8). If ever honored, a widget could talk to goodwork's
  existing server directly; assume no — design for bridge-only data.
- **U-3: Claude-side widget refresh/persistence behavior** (CLA-21, CLA-12). Affects how the board widget
  restores after reopening a conversation; ChatGPT's message-scoped model (OAI-19) is the safe design
  assumption.
- **U-4: post-merge Codex desktop behavior** (OAI-12 limitation) — issue evidence predates the 2026-07-09
  merge into ChatGPT desktop; the flag state (OAI-11) still indicates not-shipped.
- **U-5: Apps SDK original launch dates** (OAI-21) — help/announcement pages 403'd; immaterial to the
  decision.

## 7. Method and coverage

Three parallel shards (Claude surfaces; OpenAI surfaces; integration shape + fallbacks), fable-5 workers
returning claim packets under the repo research contract; coordinator (this session) reconciled and wrote
this dossier. An independent fable-5 challenger audited before delivery: all claim IDs resolved; five
decision-critical sources re-fetched (help-center 13454812, Apps SDK changelog, codex PR #19884, ext-apps
spec, Claude Code artifacts doc) with four verbatim passes and one mismatch — the CLA-9 over-read — which
was repaired along with two overstatement fixes (I-5 scope, Codex matrix verb) and three wording nits.
Primary sources only: MCP spec repo + official MCP blog, Anthropic blog/help-center/product docs, OpenAI
developer docs/changelogs, first-party GitHub repos (openai/codex PRs+issues, apps-sdk examples), and this
repo's installed skill files. Bounded absences are recorded as Unknowns with their search boundaries;
several OpenAI help/announcement pages returned HTTP 403 (noted in OAI-21). No hands-on product experiments
were run — U-1 is deliberately left to a probe.

## 8. Source index (see also §9 addendum sources in claims/vis.md)

Spec & standard: github.com/modelcontextprotocol/ext-apps (spec 2026-01-26 + draft; SDK)
· blog.modelcontextprotocol.io 2025-11-21 & 2026-01-26 posts · modelcontextprotocol.io/seps/1865
· modelcontextprotocol.io/quickstart/user.
Anthropic: claude.com/blog/interactive-tools-in-claude · support.claude.com articles 13454812, 11175166,
9487310, 14729249 · claude.com/blog/claude-powered-artifacts · claude.com/blog/artifacts-in-claude-code
· code.claude.com/docs/en/{mcp,desktop,artifacts,skills} · claude.com/docs/connectors/building/mcpb
· github.com/anthropics/claude-code CHANGELOG.
OpenAI: developers.openai.com/apps-sdk{,/reference,/changelog,/build/chatgpt-ui,/build/state-management,
/deploy/connect-chatgpt,/deploy/submission} · developers.openai.com/blog/openai-for-developers-2025
· learn.chatgpt.com/docs/{extend/mcp,changelog,app-server,plugins,build-skills,browser}
· developers.openai.com/api/docs/guides/developer-mode · github.com/openai/codex PR #19884, issue #21019
· github.com/openai/openai-apps-sdk-examples.
Local: .agents/skills/review-loop/SKILL.md · skills/personal/goodwork (state/execution references).
All web sources accessed 2026-07-18.

## 9. Addendum (2026-07-19) — the `visualize` channel in Claude Code desktop

Product evidence arrived after delivery that revises the Claude Code row: a Claude Code **desktop** session
on 2026-07-18 rendered an SVG diagram inline in the transcript through an auto-provisioned first-party MCP
server named `visualize` (VIS-1). It appears in no user or project MCP config (VIS-2) and its renderer ships
in the desktop app's own front-end bundle (VIS-3). This is exactly the gap the original CLA-19/INT-14
limitations reserved: the *documented* absence stands (nothing in the docs map — VIS-5), but the *product*
has the capability.

Mechanism per the tool's own relayed guidance (VIS-4): raw markup travels in the `show_widget` tool's
`widget_code` argument (SVG auto-detected, else HTML); the host injects a design-system stylesheet
(class ramps, CSS variables) so widgets adapt to light/dark; CSP restricts external loads to a short CDN
allowlist; `position:fixed` is forbidden; scripts run after streaming; and a global `sendPrompt(text)`
inside the frame sends a message back into the conversation — the interactivity channel. A `read_me` tool
serves the design-system/constraint modules and is meant to be called first.

**Not established** (VIS-5 quarantine, VIS-6): whether this is the MCP Apps extension internally (the
visible shape — markup in tool arguments, no ui:// template, no postMessage JSON-RPC bridge — differs from
the spec), where the server runs, surface/version gating, and stability (a guide-agent-surfaced GitHub
issue alleges post-render 400s since April; the 2026-07-18 session rendered and persisted fine).

- **I-7.** Goodwork's in-chat story on Claude Code desktop is feasible *today* via `visualize`: the approval
  card (draft text in an editable field, Send/Edit/Don't-send buttons calling `sendPrompt` with the decision
  and content hash) and the kanban board can render inline, with every user action arriving as a visible
  chat message — weaker than `events.jsonl` as a machine gate but stronger as user-visible provenance; the
  agent still validates before acting, preserving the trust model. Where `mcp__visualize__*` tools are
  absent from a session, degrade to the existing local server + Browser pane/tailnet page. (From VIS-1,
  VIS-2, VIS-4; goodwork execution contract.) Caveat: an undocumented channel can change or vanish without
  notice — ship it as a progressive enhancement rung, never the only path.
- **Next probe:** from a Claude Code desktop session, call `read_me` (all modules), render an interactive
  HTML approval card, and exercise `sendPrompt` round-trip — settles VIS-6 empirically.
