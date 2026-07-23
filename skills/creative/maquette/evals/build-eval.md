# Maquette — build eval

One full pipeline run against a sample brief, graded on the artifacts. Expensive; run after probes pass.
Because the pipeline is interview-gated, the eval harness plays the user: a scripted client persona with
an answer sheet, responding in character to intake questions.

## Sample brief (the persona's ground truth)

**Client:** regional freight brokerage ("Harbor & Pine Logistics") buying a custom TMS. **Demo room:**
owner (buyer), ops manager (daily user), their part-time IT consultant. **Trigger:** they run on
spreadsheets + phone calls; a competitor just won a shipper contract by quoting faster. **Demo beats the
persona reveals only if asked about the deal:** (1) quote a load in under a minute, (2) the dispatch board
updating live as carriers confirm, (3) a coding agent creating a load via MCP — the IT consultant's wow.
**Scope fence:** no accounting/invoicing, no carrier mobile app. **Magnitudes:** ~200 loads/day, 60
carriers, one shipper is 40% of volume. **Design:** no brand guidelines ("make it look professional") →
stock shadcn. **Personas:** dispatcher, ops manager.

## Hard gates (fail ⇒ eval fails)

1. **Interview conduct:** questions asked one at a time (never a batch dump); BRIEF.md and JOURNEYS.md
   produced and approved before any scaffold/build command runs. Approved means a serve-via-tailnet approve
   verdict: each deliverable is rendered, served through the `serve-via-tailnet` skill, and awaited; the eval
   harness, playing the user, submits the approve verdict through that surface.
2. **Dead-click sweep:** drive every route and rendered control; zero dead ends, zero `#` links, zero
   "coming soon".
3. **The seam:** no component imports fixtures directly (`grep` imports of `lib/fixtures` outside
   `lib/`); all reads/mutations go through `lib/api/`.
4. **Deliverables exist:** BRIEF.md, JOURNEYS.md, DEMO.md, HANDOFF.md, `mcp/server.ts`, working reset.

## Graded assertions

- Data realism: lists match stated magnitudes (loads list ≥ 30 rows and scrolls); one shipper visibly
  dominant; no "John Doe"/"Acme"/lorem; ragged currency values; all dates relative (grep for hardcoded
  year strings in fixtures = fail); seeded (two fresh runs render identical data).
- State coherence: create a load via UI → it appears on dashboard counts, dispatch board, and shipper
  detail without refresh; survives refresh (localStorage); reset returns to pristine.
- Latency feel: reads show skeletons; mutations show pending state; measured api latency within
  250–550ms.
- `@mock` coverage: markers exist for auth/permissions/search/live-carrier-confirm at minimum; HANDOFF.md
  mock-inventory table matches `grep -rn "@mock"` locations.
- MCP: `mcp/server.ts` tools mirror JOURNEYS.md agent journeys; `create_load` tool call updates the
  browser UI live (toast + board) with the dev server running.
- Design language: no gradients/glass/eyebrow labels (spot-check per design-language.md hard-no list);
  Geist; neutral base + ≤1 accent; radii ≤ 16px.
- Feel pass: `tabular-nums` on numeric columns; press states on buttons; popovers origin-aware; no
  `transition: all`.
- Console clean at every route (no hydration warnings — the relative-dates trap).
- Copy: no leaked build/internal language anywhere in rendered UI (the persona's phrase "demo beats" must
  never appear on-screen).

## Review pass

Screenshot each screen; an LLM/human reviewer judges: "would a buyer believe this is a live product?"
against the demo beats. Record verdict + the three weakest screens as findings for the next skill
iteration.
