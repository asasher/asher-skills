# Architecture

"Browser-only" means **no database, no real auth, no external services** — not "no process". `next dev` is
a server and that's fine; it's what makes the live agent demo possible.

## Scaffold recipe (not a template — templates rot)

```bash
npx create-next-app@latest <name> --typescript --tailwind --eslint --app --no-src-dir
cd <name>
npx shadcn@latest init            # defaults; base color per BRIEF.md (default: neutral/zinc)
npm i zustand motion @modelcontextprotocol/sdk zod
npx shadcn@latest add button card dialog dropdown-menu input label table tabs badge avatar skeleton sonner  # + as needed
```

Fonts via `next/font` (Geist ships with create-next-app) — **no external font/CDN requests**; the demo must
survive meeting-room wifi (see demo reference).

## Layout

```
lib/schema.ts        # all domain types = future DB schema
lib/fixtures/        # seeded generators (see mock-data reference)
lib/store.ts         # the one client store, seeded, localStorage-persisted, resettable
lib/api/             # THE SEAM: async fns + latency; the only data access path
app/                 # routes per screen inventory
app/api/agent-bus/   # SSE + POST relay for the MCP bridge (agent mode)
mcp/server.ts        # the mini MCP server (run: npm run mcp)
components/          # shadcn + product components
BRIEF.md  JOURNEYS.md  HANDOFF.md
```

## The store

One Zustand store, seeded from fixtures, persisted to localStorage with a **versioned key** so a redeploy
never shows a stale schema, plus a reset action wired to the demo panel.

```ts
export const useStore = create<AppState>()(persist(
  (set, get) => ({ ...seedState(), /* mutations live here or in lib/api */ }),
  { name: "maquette-<product>-v1" }  // bump v on any schema/fixture change
));
export const resetDemo = () => { localStorage.removeItem("maquette-<product>-v1"); location.reload(); };
```

## The api seam

Every component reads and mutates through `lib/api/*.ts`. Async functions, simulated latency, one place to
tune feel. Components never touch fixtures or the store's internals directly.

```ts
// lib/api/net.ts
const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));
export const latency = async () => sleep(250 + Math.random() * 300);  // 250–550ms: never instant, never slow

// lib/api/orders.ts
export async function createOrder(input: OrderInput): Promise<Order> {
  await latency();
  // @mock: real impl = POST /orders; server assigns id, validates credit limit
  return useStore.getState().addOrder(input);
}
```

Rules:

- **`@mock` marker discipline:** every place reality is faked gets `// @mock: <what the real implementation
  needs>` — auth, permissions, search (client-side substring), file upload, email, webhooks, payments.
  `grep -rn "@mock"` must enumerate the entire gap between maquette and product; handoff is generated from it.
- **Loading states are real:** because latency is real, every fetch renders a skeleton (shadcn `Skeleton`)
  and every mutation disables its button / shows a spinner. Optimistic updates where the journey wants
  snappiness — the seam makes both trivial.
- Failure states only where `JOURNEYS.md` made them deliberate; a demo should not roll dice.

## MCP bridge (agent mode)

The demo beat: open a coding agent next to the product, say "create a purchase order for 40 units", and
the UI updates live. It also demos the *real* product's planned agent surface — the tools implemented here
are the tool list in `HANDOFF.md`.

Design: **the browser store stays the source of truth**; the MCP server is a thin relay through a Next
route handler. Mutations are defined once (in `lib/api`) and reused by both the UI and the bridge.

```
MCP client (Claude Code etc.)
  → mcp/server.ts (stdio, @modelcontextprotocol/sdk)
    → POST http://localhost:3000/api/agent-bus            (tool call, JSON)
      → SSE → browser: applies it via the same lib/api fn  (UI updates live)
      → browser POSTs updated snapshot back to the bus
    ← tool result (from ack/snapshot)
```

Implementation notes (keep it ~150 lines total):

- `app/api/agent-bus/route.ts`: module-level state = `{ snapshot, pendingCalls }`; `GET` streams SSE of
  pending tool calls; `POST` with `kind: "call"` enqueues and awaits the ack; `POST` with `kind: "snapshot"`
  stores the browser's latest state and resolves pending acks.
- A `useAgentBus()` hook (mounted in the root layout, dev only): subscribes to the SSE stream, dispatches
  each call to the matching `lib/api` function, pushes a snapshot + ack after every store change. Toast
  each applied agent action (sonner) — the audience should *see* the agent acting.
- `mcp/server.ts`: stdio server; one tool per agent journey in `JOURNEYS.md`, zod-validated inputs,
  read tools answer from the last snapshot. Add `"mcp": "tsx mcp/server.ts"` to package.json scripts and
  put the one-line client config (`claude mcp add <product> -- npm run mcp`) in the README and on the
  in-app Integrations screen.
- Queries are eventually-consistent (last snapshot) — fine for a demo; note it with `@mock`.

Also build the **Integrations screen** as a product surface: the planned MCP tool surface presented as
documentation, with the copyable connect command. In deployed/static mode (no local server), that screen
plus an optional canned agent-session transcript is the fallback story.

## Modes

- **Local demo (default for meetings):** `next dev` + agent mode. Everything works.
- **Deployed share-link (after the meeting):** static/Vercel deploy. Store + localStorage work fine per
  visitor; agent bus is absent — gate `useAgentBus` behind `NODE_ENV`/env flag so the build is clean.
