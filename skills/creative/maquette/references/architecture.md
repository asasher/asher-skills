# Architecture

The maquette simulates auth, persistence, and integrations in the browser. A local Next.js server supports the live agent demo; deployed sharing works as a static app.

## Stack and layout

Use Next.js App Router with TypeScript, Tailwind, and shadcn/ui. Initialize the theme from `BRIEF.md` (neutral/zinc by default), and add components as the screen inventory needs them. Use Zustand for the client store, Motion for animation, and the MCP SDK with validated input schemas for the agent surface. Follow the project's package-manager convention and current package interfaces.

Bundle fonts through `next/font` so the demo survives meeting-room wifi.

- `lib/schema.ts` — domain types and the future database schema.
- `lib/fixtures/` — seeded generators; see [mock-data.md](mock-data.md).
- `lib/store.ts` — one client store, persisted to localStorage and resettable.
- `lib/api/` — typed async functions; the shared data-access seam.
- `app/` and `components/` — routes from the screen inventory, shadcn and product components.
- `mcp/server.ts` — local MCP server, with its launch command documented in the project.
- `BRIEF.md`, `JOURNEYS.md`, `HANDOFF.md` — intent, journeys, implementation contract.

## State and API seam

Seed one Zustand store from fixtures. Version its persistence key when schemas or fixtures change so stale data cannot survive a redeploy. Wire a reset action into the demo panel that restores the seeded state.

Every screen reads and mutates through `lib/api/*.ts`. Give each function a typed input, result, and async behavior with tunable simulated latency (250–550ms by default). Keep state coherent across lists, counts, feeds, and detail pages. The future backend replaces this seam while preserving its interfaces.

- Mark every faked behavior `@mock` with a one-line note on what production requires: auth, permissions, search, uploads, email, webhooks, payments, and integration limits. Every marker must appear in the handoff inventory.
- Render loading skeletons for pending fetches and disable or show progress on pending mutations. Use optimistic updates where the journey calls for them.
- Simulate failure only in states deliberately specified by `JOURNEYS.md`.

## MCP bridge (agent mode)

The demo beat: an agent creates a purchase order and the browser updates live. Implement one MCP tool per approved agent journey; preserve those names, input schemas, results, and behaviors in `HANDOFF.md`.

The browser store remains authoritative. A thin local relay connects the MCP server to the active browser; UI and agent mutations invoke the same `lib/api` functions. Choose the transport that fits this local setup, such as SSE plus POST acknowledgments.

Validate tool inputs and correlate each call with its browser acknowledgment. Report success only after the matching action has applied; return a clear failure for invalid input, a disconnected browser, or a timed-out call. Read tools may use the latest browser snapshot; mark its eventual consistency with `@mock`. Show each applied agent action visibly in the UI.

Document the actual server launch and client connection instructions in the README and the in-app Integrations screen. The screen also presents the planned MCP tools as product documentation.

## Modes

- **Local demo:** the Next.js app and MCP relay run together; verify a tool call updates the live browser and returns the matching result.
- **Deployed static share-link:** each visitor has browser-local state. Exclude local relay routes and subscriptions from this build. Present the Integrations documentation and, optionally, a clearly identified recorded agent-session transcript.
