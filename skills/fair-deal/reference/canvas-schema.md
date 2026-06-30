# canvas.json — schema (the shared source of truth)

`canvas.json` is the filled Fair Deal Canvas, importable into `canvas.html` (the review surface). Agents read
and write it during interview and negotiation. Keep it valid at all times.

## Shape
```json
{
  "meta": {"app":"fair-deal-canvas","version":2,"exportedAt":"<ISO date>"},
  "fields": { ... },
  "tables": { "t1":[...], "t2":[...], "t6":[...], "t7a":[...], "t7b":[...] }
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
- Box 3 notes: `b1_notes` · Box 4 notes: `b2_notes`
- Box 5: `b5_alloc`, `b5_vest`, `b5_notes`
  - `b5_vehicle` ∈ "Handshake / contract only" | "LLC" | "Company (Ltd / corp)" | "Partnership"
- Box 6: `b4` (waterfall text), `b4_notes`
- Box 7 notes: `b6_notes` · Box 8 notes: `b7_notes`
- Box 9: `b8_valdetail`, `b8_leaving`, `b8_stuck`, `b8_exit`, `b8_notes`
  - `b8_valmethod` ∈ "A set number, refreshed periodically" | "A formula (e.g. multiple of profit)" | "A neutral appraiser"
- Box 10: `b10_fail`, `b10_prevent`, `b10_notes`

## tables
- `t1` (Box 3): rows `{ "what": str, "by": "Party A"|"Party B", "kind": K }`
  - K ∈ "Pre-existing asset → license / value" | "One-off task → fee" | "Ongoing role → salary" | "Co-building → share"
- `t2` (Box 4): rows `{ "what": str, "by": "Party A"|"Party B", "dur": D, "lev": L }`
  - D ∈ "Distribution / audience" | "Brand & relationships" | "Proprietary data" | "Systems & judgment" | "Code / content" | "Capital" | "Labour / one-off"
  - L ∈ "High (scales freely)" | "Medium (buys scale)" | "Low (1:1 effort)"
- `t6` (Box 7): rows `{ "area": str, "owner": "Party A"|"Party B"|"Both", "reserved": bool }`
- `t7a` (Box 8 background): rows `{ "asset": str, "owner": "Party A"|"Party B", "right": str }`
- `t7b` (Box 8 foreground): rows `{ "asset": str, "owned": str, "lic": "Both"|"Party A"|"Party B"|"—" }`

After writing, validate it parses (`python3 -m json.tool canvas.json`).
