#!/bin/bash
# Goodwork v3 Tier-2 scripted dry-run — tool mechanics only, no model in the loop.
# Adapted from the probe-eval discipline in docs/agents/probe-evals.md (fair-deal Tier-2 pattern).
# Runs entirely in a mktemp sandbox; never touches the repo. Exits non-zero on any FAIL.
set -u
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
PASS=0; FAIL=0
ok(){ PASS=$((PASS+1)); echo "  PASS  $1"; }
bad(){ FAIL=$((FAIL+1)); echo "  FAIL  $1"; }
check(){ if eval "$2"; then ok "$1"; else bad "$1"; fi; }
cleanup(){ [ -n "${SERVER_PID:-}" ] && kill "$SERVER_PID" 2>/dev/null; rm -rf "$TMP"; }
trap cleanup EXIT

echo "== sandbox: $TMP"

# 1. init_workspace creates the v3 shape
python3 "$SKILL_DIR/scripts/init_workspace.py" --root "$TMP" >/dev/null 2>&1
check "init: goodwork/ created"                '[ -d "$TMP/goodwork" ]'
check "init: artifacts/ dir created"           '[ -d "$TMP/goodwork/artifacts" ]'
check "init: presentation.rungs defaults to markdown" \
  'python3 -c "import json,sys; c=json.load(open(\"$TMP/goodwork/capabilities.json\")); sys.exit(0 if \"markdown\" in c.get(\"presentation\",{}).get(\"rungs\",[]) else 1)"'

# 2. seed one card with a pending draft whose hash matches the artifact file bytes
cat > "$TMP/goodwork/artifacts/art_t1.md" <<'ART'
Subject: Quick question

Hi Taylor — testing the approval surface. Could I ask for 20 minutes?
ART
HASH=$(python3 -c "import hashlib;print(hashlib.sha256(open('$TMP/goodwork/artifacts/art_t1.md','rb').read()).hexdigest()[:16])")
python3 - "$TMP/goodwork/pipeline.json" "$HASH" <<'PY'
import json,sys
p,h=sys.argv[1],sys.argv[2]
d=json.load(open(p))
d["cards"]=[{"id":"pipe_t1","target_id":None,"role":"Test Role","stage":"outreach","warmth":"warm",
 "next_action":"Send intro note","due_at":"2026-07-19","owner":"agent","status":"open","thread_ids":[],
 "history":[{"at":"2026-07-18","kind":"draft","summary":"Intro note drafted for QA"}],
 "replies":[],"reply_digest":None,
 "drafts":[{"id":"draft_t1","channel":"gmail","artifact_id":"art_t1","content_hash":h,
            "created_at":"2026-07-18T10:00:00+04:00","status":"pending"}],
 "artifact_ids":["art_t1"],"approval_ids":[],"proof_ids":[]}]
json.dump(d,open(p,"w"))
PY
check "seed: pipeline card written" '[ -s "$TMP/goodwork/pipeline.json" ]'

# 3. server starts; projection injects artifact content and history
cd "$SKILL_DIR"
python3 scripts/server.py --workspace "$TMP/goodwork" --idle-timeout 300 > "$TMP/server.json" &
SERVER_PID=$!
sleep 1
PORT=$(python3 -c "import json;print(json.load(open('$TMP/server.json'))['port'])" 2>/dev/null)
TOKEN=$(python3 -c "import json;print(json.load(open('$TMP/server.json'))['token'])" 2>/dev/null)
check "server: started and printed port/token"  '[ -n "$PORT" ] && [ -n "$TOKEN" ]'
check "server: kanban bootstrap carries history summary" \
  'curl -s "http://127.0.0.1:$PORT/kanban?token=$TOKEN" | grep -q "Intro note drafted for QA"'
check "server: approval page carries the draft text" \
  'curl -s "http://127.0.0.1:$PORT/approval?token=$TOKEN" | grep -q "testing the approval surface"'
check "server: bad token is refused" \
  '[ "$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$PORT/kanban?token=wrong")" = "403" ]'

# 4. edited approval event round-trips into events.jsonl
EVT=$(curl -s -X POST "http://127.0.0.1:$PORT/event" -H "Content-Type: application/json" -d "{
  \"token\": \"$TOKEN\", \"type\": \"edit_then_approve_requested\", \"page\": \"approval\",
  \"item_id\": \"art_t1\", \"content_hash\": \"$HASH\", \"granularity\": \"item\",
  \"covers\": [{\"item_id\": \"art_t1\", \"content_hash\": \"$HASH\"}],
  \"payload\": {\"action\": \"edit_then_approve\", \"edited_content\": \"Hi Taylor — my own words.\", \"reason\": null},
  \"tags\": [\"approval\"]}")
check "event: edit_then_approve accepted"       'echo "$EVT" | grep -q "\"id\""'
check "event: landed in events.jsonl with edited_content" \
  'grep -q "edited_content" "$TMP/goodwork/events.jsonl"'

# 5. plain approval event + validate_approval both ways
curl -s -X POST "http://127.0.0.1:$PORT/event" -H "Content-Type: application/json" -d "{
  \"token\": \"$TOKEN\", \"type\": \"approval_requested\", \"page\": \"approval\",
  \"item_id\": \"art_t1\", \"content_hash\": \"$HASH\", \"granularity\": \"item\",
  \"covers\": [{\"item_id\": \"art_t1\", \"content_hash\": \"$HASH\"}],
  \"payload\": {\"action\": \"approve\", \"reason\": null}, \"tags\": [\"approval\"]}" >/dev/null
APPROVAL_EVT=$(grep approval_requested "$TMP/goodwork/events.jsonl" | tail -1)
echo "$APPROVAL_EVT" > "$TMP/evt.json"
python3 "$SKILL_DIR/scripts/validate_approval.py" --event "$TMP/evt.json" \
  --hashes "{\"art_t1\": \"$HASH\"}" --channel gmail > "$TMP/val.json" 2>&1
check "validate: matching hash passes (exit 0)"  '[ $? -eq 0 ] && grep -q "\"ok\": true" "$TMP/val.json" || grep -q "\"ok\":true" "$TMP/val.json"'
python3 "$SKILL_DIR/scripts/validate_approval.py" --event "$TMP/evt.json" \
  --hashes '{"art_t1": "deadbeefdeadbeef"}' >/dev/null 2>&1
check "validate: stale hash rejected (exit 20)"  '[ $? -eq 20 ]'

echo "== $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
