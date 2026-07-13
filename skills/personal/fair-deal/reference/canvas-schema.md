# canvas.json — schema (the shared source of truth)

`canvas.json` is the filled Fair Deal Canvas, importable into `canvas.html` (the review surface). Agents read
and write it during interview and negotiation. Keep it valid at all times.

## Shape
```json
{
  "meta": {"app":"fair-deal-canvas","version":2,"exportedAt":"<ISO date>"},
  "fields": { ... },
  "tables": { "t1":[...], "t2":[...], "t5s":[...], "t6":[...], "t7a":[...], "t7b":[...] }
}
```

## CRITICAL conventions
- In every table, the side is stored as the literal string **"Party A"** or **"Party B"** (NOT the real name
  — the app shows the name automatically). Same for owners.
- All `fields` values are strings; select fields must use EXACTLY one allowed value (below).
- Reflect what the parties actually agreed. Where a box isn't agreed yet, leave it blank or state the open
  point plainly — blank is information, not failure. The canvas reading derives from how much is filled/agreed.

## fields (all strings)
- `partyA`, `partyB`, `deal`, `date`
- Box 1: `b9_goalA`, `b9_goalB`, `b9_batnaA`, `b9_batnaB`, `b9_winA`, `b9_winB`, `b9_notes`
  - `b9_align` ∈ "Aligned — same direction" | "Compatible but different — design for both" | "Conflicting — adjust the structure"
- Box 2: `biz_customer`, `biz_offer`, `biz_channel`, `biz_edge`, `ns_metric`, `ns_track`, `biz_notes`
  - `flag_employed` (bool) — one party is also employed by the other → use two separate contracts; watch work-for-hire
  - `flag_internaluse` (bool) — a partner's own business will use what's built → price it at an internal rate through the waterfall
  - `flag_keyperson` (bool) — the venture runs on one founder's delivery skill → document/systematize it; key-person risk that bears on the split (Box 4/5) and leaver terms (Box 9)
  - **How we'll reach customers** (go-to-market):
    - `gtm_primary` ∈ "Reach out to people who already know us — 1:1" | "Publish content to an audience we build — broadcast" | "Reach out to strangers directly (cold) — 1:1" | "Pay to broadcast to strangers (ads)"
    - `gtm_owner` ∈ "Party A" | "Party B" | "Both" — who owns/runs the channel. **Whoever owns it holds the most durable contribution**; tag them "Distribution / audience" in `t2` so the keystone split reflects it.
    - `gtm_commitment` (str) — the consistent effort (e.g. "100 outreaches/day")
    - `get_referrals`, `get_team`, `get_specialists`, `get_partners` (bool) — who'll bring in customers as the venture grows
  - **How we'll fund it** (whose money):
    - `fund_needed` ∈ "No — we self-fund (savings / reinvested profit / customers pay up front)" | "Yes — we need outside capital to start"
    - `fund_kind` ∈ "Debt — a loan we repay (no ownership given up)" | "Equity — investors get ownership (dilution)" | "A mix of debt and equity"  (only when raising)
    - `fund_who` ∈ "Party A" | "Party B" | "Both" | "Outside" — who puts the money in. Capital is a contribution: feeds `t1`/`t2` (section 3/4), a preferred return in the waterfall (`b4`, section 6), and the reserved-matters list (`t6`, section 7).
- Box 3: `strengthA`, `strengthB` (each founder's highest-leverage strength + what to clear off their plate — a project/process/person), `b1_notes` · Box 4 notes: `b2_notes`
- Box 5: `b5_alloc`, `b5_vest`, `b5_notes`
  - `b5_vehicle` ∈ "Handshake / contract only" | "LLC" | "Company (Ltd / corp)" | "Partnership"
- Box 6: `b4` (waterfall text), `b4_notes`
- Box 7 notes: `b6_notes` · Box 8 notes: `b7_notes`
- Box 9: `b8_valdetail`, `b8_leaving`, `b8_stuck`, `b8_exit`, `b8_restraint_detail`, `b8_notes`
  - `b8_valmethod` ∈ "A set number, refreshed periodically" | "A formula (e.g. multiple of profit)" | "A neutral appraiser"
  - `b8_restraint` ∈ "None — neither side is restrained (encouraged default)" | "Non-solicit only — don't poach customers / staff" | "Narrow non-compete — time-boxed and paid for" | "Other — describe"
- Box 10: `b10_fail`, `b10_prevent`, `b10_notes`
- Deal shape (optional, presentation only): `dealShape` ∈ "Co-founder / JV" | "Advisory" | "Client / JV" | "Revenue-share" (blank = full canvas)
- Per-section reading (optional): `st_s1`…`st_s10`, each ∈ "open" | "pilot" | "agreed" (blank = open). These roll up to the canvas reading (any open → Keep talking; all agreed, some pilot → Pilot first; all agreed → Ready).

## tables
- `t1` (Box 3): rows `{ "what": str, "by": "Party A"|"Party B", "kind": { "asset"?: true, "task"?: true, "role"?: true, "share"?: true } }`
  - `kind` is an OBJECT of tags — a contribution can be more than one at once (e.g. an audience is `{asset:true, share:true}`). Only include keys that apply (true). Meanings: `asset` = pre-existing → license / value · `task` = one-off → fee · `role` = ongoing → salary · `share` = co-building → share.
- `t2` (Box 4): rows `{ "what": str, "by": "Party A"|"Party B", "dur": D, "lev": L }`
  - D ∈ "Distribution / audience" | "Brand & relationships" | "Proprietary data" | "Systems & judgment" | "Code / content" | "Capital" | "Labour / one-off"  (ranked most→least durable; this sets the durability-weighted share shown in Box 5)
  - L ∈ "High (scales freely)" | "Medium (buys scale)" | "Low (1:1 effort)"
- `t5s` (Box 5, optional split-by-stream): rows `{ "stream": str, "who": "Party A"|"Party B"|"Both", "split": str }`
  - Only for multi-stream deals (different splits per revenue stream). Leave the default rows' `who`/`split` blank for a single-number deal; it's treated as unused until a `who` or `split` is set.
- `t6` (Box 7): rows `{ "area": str, "owner": "Party A"|"Party B"|"Both", "reserved": bool }`
- `t7a` (Box 8 background): rows `{ "asset": str, "owner": "Party A"|"Party B", "right": str }`
- `t7b` (Box 8 foreground): rows `{ "asset": str, "owned": str, "lic": "Both"|"Party A"|"Party B"|"—" }`

After writing, validate it parses (`python3 -m json.tool canvas.json`).
