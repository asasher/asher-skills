# Brief — inline interactive widgets in chat harnesses

## Question

As of 2026-07-18, what mechanisms do the Claude surfaces (claude.ai web, Claude desktop app, Claude Code)
and the OpenAI surfaces (Codex app, ChatGPT web/desktop as the Apps SDK reference) support for rendering
**interactive UI inline in a conversation**, and what are each mechanism's status, shipping model,
interactivity limits, state/refresh model, and sandbox/network constraints?

## Intended use

Decide whether the `goodwork` skill can present its kanban board, per-card history sheet, and
draft-approval flow (including user-editable draft text) as inline chat widgets per harness — keeping the
whole experience in chat — demoting the current local-server + tailnet browser page to a fallback rung.
The decision consumer is skill design work in this repo; goodwork today is a file+stdlib-script skill with
a local HTTP server, an events.jsonl request-event model, and an agent-sole-writer state contract.

## Scope

Per surface (claude.ai web, Claude desktop, Claude Code, Codex app, ChatGPT web/desktop):

1. Mechanism name(s) and status (GA / beta / flagged / unsupported), with dates.
2. How a locally-installed skill or local MCP server ships UI to that surface (packaging, config, transport).
3. Interactivity: buttons, forms, **editable text areas**, events back to the agent (tool calls, messages).
4. State and refresh: widget state persistence, re-render on new data, agent-pushed updates.
5. Sandbox and network: iframe/CSP rules, localhost reachability, external fetch policy.
6. Degradation when the mechanism is absent.

**Exclusions:** building the integration; mobile apps beyond a support-matrix note; monetization/directory
policies; non-chat surfaces (IDE panes count only where they render conversation widgets).

## Definitions

- **Inline widget** — interactive UI rendered inside the conversation transcript itself, not a separate
  browser tab/panel the chat links out to.
- **Local skill** — files + scripts installed per-project (goodwork's shape), possibly accompanied by a
  local (stdio) MCP server it provides.

## As-of boundary

2026-07-18. Mutable web sources carry accessed dates. Mechanism status is what official sources state as of
this date; roadmap talk is recorded as such, never as support.

## Sufficiency

Every scope row answered per surface from primary sources (official specs, docs, changelogs, first-party
repos/announcements) or recorded as an explicit unknown with search boundary. Feasibility mapping for
goodwork appears as inferences linked to claim IDs; the go/no-go itself stays with the caller.

## Shard map (claim-ID namespaces)

- **CLA — Claude surfaces.** MCP Apps extension in the MCP spec and Claude's support for it; artifacts as an
  alternative; which Claude surfaces render interactive UI inline, under what status and constraints.
- **OAI — OpenAI surfaces.** Apps SDK mechanism and status on ChatGPT; whether the Codex app renders Apps
  SDK/MCP UI or any inline HTML; Codex MCP support and its UI story.
- **INT — integration shape and fallbacks.** How a file-based skill ships/registers a local MCP server per
  harness (Claude desktop config, Claude Code, Codex config); whether widget sandboxes can reach localhost or
  must route data through tool results; how widget events map onto goodwork's request-event/approval model;
  non-widget inline fallbacks that keep the experience in or beside chat.

## Staffing

Coordinator/synthesizer: session orchestrator (fable-5) — sole dossier writer. Shard workers: three native
fable-5 subagents (roster rank: intelligence 9 / taste 9 / cost 1; floor respected), web-capable, returning
claim packets only. Challenger: an independent fable-5 subagent with fresh context auditing the reconciled
findings against sources. No fire-and-forget: all shards watched by the coordinator.
