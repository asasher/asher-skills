# presentation - where the user sees boards, drafts, and approvals

The presentation ladder. Detect the best rung **at present time from the session's own surface** — never
assume from config alone, because the same workspace is opened from different harnesses. Record what setup
observed in `capabilities.json` (`presentation.rungs`), but the session's live surface wins.

## The ladder

1. **Inline chat widget.** If the session exposes an inline widget renderer (tools such as
   `mcp__visualize__show_widget` in Claude Code desktop — read the renderer's own guidance, e.g. its
   `read_me` modules, before first use), render the board or approval card inline in the conversation.
   Self-contained markup only; use the host's injected design system; no external loads beyond the host's
   allowlist. Widget interactions return as chat messages (e.g. a `sendPrompt` call carrying the decision
   and content reference) — treat each as a request to validate under [execution.md](execution.md), never
   as an applied change. These renderers can be undocumented and may change without notice: on any render
   failure, drop to rung 2 without ceremony.
2. **Local server + browser.** The shipped pages (`scripts/server.py`: kanban, approval, health, diff),
   opened locally at the desk; exposed through the recorded remote layer (e.g. tailnet) for the phone loop
   when the user is away. The richest surface — drag-and-drop, batch approvals, inline draft editing.
3. **Rendered markdown in chat.** Always available; the floor. Board and bench as ranked tables; a draft as
   its full text in a quoted block with a plain ask ("Say **send it**, edit the text, or say **don't
   send**"). The typed reply is the request event; the same gates apply.

## Choosing a rung

Prefer the highest available rung for interactive work — approving a draft, working the board. But use the
smallest sufficient surface: a quick status glance is a markdown table even when the server is available;
don't stand up a page for one card. One decision per surface — never present the same approval on two rungs
at once (double-approval ambiguity).

## Approval semantics are rung-independent

Every rung produces only *requests*: a UI event, a widget message, or a typed reply. The agent validates
(hash, evidence, quota) and writes the approval record with its source, exactly as [execution.md](execution.md)
specifies. A rung change never weakens a gate — the markdown floor still shows the exact final text before
asking.

## Sensitivity

Boards and drafts are the user's own data in their own session — fine on any rung. Never route content
through an external service the rung doesn't require, and never put more on a widget than the decision
needs.
