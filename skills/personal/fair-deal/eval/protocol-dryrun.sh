#!/usr/bin/env bash
# Local dry run / eval of the fair-deal turn protocol.
# Simulates two partners (Ada=A, Ben=B) as two clones of one repo, with a bare
# local repo standing in for the private GitHub remote. One agent (me) role-plays
# both sides, following the skill's reference contracts. Asserts the protocol's
# invariants at every step. No network, no GitHub.
set -u
SK="$(cd "$(dirname "$0")/.." && pwd)"   # the skill dir (eval/ lives inside it)
TPL="$SK/templates"
ROOT="$(mktemp -d)/fair-deal-dryrun"   # scratch; never inside the repo
ORIGIN="$ROOT/origin.git"
A="$ROOT/deal-A"; B="$ROOT/deal-B"
PASS=0; FAIL=0
ok(){ echo "  PASS $1"; PASS=$((PASS+1)); }
no(){ echo "  FAIL $1"; FAIL=$((FAIL+1)); }
assert(){ if eval "$2"; then ok "$1"; else no "$1"; fi; }
hr(){ echo; echo "===== $1 ====="; }

rm -rf "$ROOT"; mkdir -p "$ROOT"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
gitq(){ git -C "$1" -c init.defaultBranch=main -c protocol.file.allow=always "${@:2}"; }

cj(){ node -e "$1" "$2" "${3:-}" "${4:-}"; }   # tiny node helper passthrough

# ---- canvas.json mutator: node helper file ----
cat > "$ROOT/cv.js" <<'NODE'
const fs=require('fs');
const [,,file,op,arg]=process.argv;
const c=JSON.parse(fs.readFileSync(file,'utf8'));
const set=(k,v)=>{c.fields[k]=v;};
if(op==='fields'){ Object.assign(c.fields, JSON.parse(arg)); }
if(op==='t1push'){ c.tables.t1.push(JSON.parse(arg)); }
if(op==='t2push'){ c.tables.t2.push(JSON.parse(arg)); }
c.meta.exportedAt='2026-06-30T00:00:00Z';
fs.writeFileSync(file, JSON.stringify(c,null,2)+'\n');
NODE

# ---- state.json mutator ----
cat > "$ROOT/st.js" <<'NODE'
const fs=require('fs');
const [,,file,patch]=process.argv;
const s=JSON.parse(fs.readFileSync(file,'utf8'));
Object.assign(s, JSON.parse(patch));
fs.writeFileSync(file, JSON.stringify(s,null,2)+'\n');
NODE

jsonok(){ node -e "JSON.parse(require('fs').readFileSync(process.argv[1]))" "$1" 2>/dev/null; }
turnof(){ node -e "console.log(JSON.parse(require('fs').readFileSync(process.argv[1])).turn)" "$1"; }
phaseof(){ node -e "console.log(JSON.parse(require('fs').readFileSync(process.argv[1])).phase)" "$1"; }

# ============================================================ origin
hr "0 · bare origin (stands in for the private GitHub repo)"
git init --bare -q -b main "$ORIGIN"
assert "bare origin created" "[ -d '$ORIGIN' ]"

# ============================================================ SETUP (Party A)
hr "1 · setup — Party A (Ada) scaffolds the deal"
mkdir -p "$A"; gitq "$A" init -q
gitq "$A" config user.name "Ada"; gitq "$A" config user.email ada@example.com
# scaffold from templates
cp "$TPL/gitignore" "$A/.gitignore"
cp "$TPL/canvas.seed.json" "$A/canvas.json"
cp "$TPL/canvas.html" "$A/canvas.html"
cp "$TPL/README-deal.md" "$A/README.md"
mkdir -p "$A/negotiation/from-A" "$A/negotiation/from-B"
cp "$TPL/state.json" "$A/negotiation/state.json"
node "$ROOT/st.js" "$A/negotiation/state.json" '{"parties":{"A":"Ada","B":"Ben"}}'
printf '# Negotiation log — Ada × Ben\n' > "$A/negotiation/log.md"
: > "$A/negotiation/from-A/.gitkeep"; : > "$A/negotiation/from-B/.gitkeep"
node "$ROOT/cv.js" "$A/canvas.json" fields '{"partyA":"Ada","partyB":"Ben","deal":"PlateAI","date":"2026-06-30"}'
# the skill itself is committed so B gets it on clone
mkdir -p "$A/.claude/skills"; cp -R "$SK" "$A/.claude/skills/fair-deal"
# private scratchpad (gitignored)
mkdir -p "$A/private/notes"; echo A > "$A/private/whoami"; cp "$TPL/solo-prep.md" "$A/private/solo-prep.md"; : > "$A/private/notes/.gitkeep"
# FIREWALL CHECK before first commit
gitq "$A" add -A
STAGED_PRIV=$(gitq "$A" diff --cached --name-only | grep -c '^private/' || true)
assert "setup: nothing under private/ is staged (firewall)" "[ '$STAGED_PRIV' -eq 0 ]"
assert "setup: canvas.json parses" "jsonok '$A/canvas.json'"
assert "setup: skill committed into the repo (clone-gets-skill)" "gitq '$A' diff --cached --name-only | grep -q '.claude/skills/personal/fair-deal/SKILL.md'"
gitq "$A" commit -q -m "fair-deal: setup A — scaffold PlateAI deal"
gitq "$A" remote add origin "$ORIGIN"; gitq "$A" push -q origin main
assert "setup: pushed to origin" "gitq '$A' rev-parse origin/main >/dev/null 2>&1"
assert "setup: origin has NO private/ files" "[ \$(gitq '$A' ls-tree -r --name-only origin/main | grep -c '^private/') -eq 0 ]"

# ============================================================ JOIN (Party B)
hr "2 · join — Party B (Ben) clones and creates his private side"
gitq "$ROOT" clone -q "$ORIGIN" "$B"
gitq "$B" config user.name "Ben"; gitq "$B" config user.email ben@example.com
assert "join: B's clone has the shared scaffold" "[ -f '$B/canvas.json' ] && [ -f '$B/negotiation/state.json' ]"
assert "join: B got the skill on clone" "[ -f '$B/.claude/skills/personal/fair-deal/SKILL.md' ]"
assert "join: B's clone carries NO private/ (A's firewall held)" "[ ! -d '$B/private' ]"
mkdir -p "$B/private/notes"; echo B > "$B/private/whoami"; cp "$TPL/solo-prep.md" "$B/private/solo-prep.md"; : > "$B/private/notes/.gitkeep"
assert "join: B's private/ is gitignored (untracked-ignored)" "gitq '$B' status --porcelain | grep -q private/ ; [ \$? -ne 0 ]"

# ============================================================ INTERVIEW (both, privately)
hr "3 · interview — each agent seeds OWN-side opening positions; floor stays private"
# Ada's private floor (NEVER committed)
cat >> "$A/private/solo-prep.md" <<'EOF'

## FILLED (dry run)
- True goal: build a durable product on top of my buyer audience; keep the audience mine.
- Floor: would accept down to 45% equity IF the audience stays licensed (not assigned).
- Won't concede: the audience list stays my property; I keep a data export on exit.
- Walk-away: license the audience to someone else and stay solo.
EOF
# CORRECT ORDER: pull on a clean tree FIRST, then edit, then commit, then push.
gitq "$A" pull -q --rebase origin main
# Ada seeds her own-side canvas fields + her contribution rows. Leaves contested split (b5_alloc) blank.
node "$ROOT/cv.js" "$A/canvas.json" fields '{"b9_goalA":"A durable product on my buyer audience","b9_batnaA":"License the audience to others, stay solo","b9_winA":"the audience stays mine and the product compounds","biz_customer":"home cooks who want plated-meal kits","biz_offer":"AI meal-plan + sourcing, $29/mo","biz_channel":"my 40k buyer email list (mine)","biz_edge":"the audience + proprietary recipe data","flag_internaluse":false}'
node "$ROOT/cv.js" "$A/canvas.json" t1push '{"what":"40k buyer audience","by":"Party A","kind":{"asset":true,"share":true}}'
node "$ROOT/cv.js" "$A/canvas.json" t2push '{"what":"buyer audience","by":"Party A","dur":"Distribution / audience","lev":"High (scales freely)"}'
node "$ROOT/st.js" "$A/negotiation/state.json" '{"ready_to_negotiate":{"A":true,"B":false}}'
gitq "$A" add canvas.json negotiation/state.json
PRIV=$(gitq "$A" diff --cached --name-only | grep -c '^private/' || true)
assert "interview A: floor/solo-prep NOT staged (firewall)" "[ '$PRIV' -eq 0 ]"
gitq "$A" commit -q -m "fair-deal: interview A — opening positions ready"
gitq "$A" push -q origin main
assert "interview A: origin still has no private/" "[ \$(gitq '$A' ls-tree -r --name-only origin/main | grep -c '^private/') -eq 0 ]"

# Ben interviews — pulls A's latest first, seeds his own-side fields + rows.
cat >> "$B/private/solo-prep.md" <<'EOF'

## FILLED (dry run)
- True goal: get paid fairly for building + a real stake in the upside.
- Floor: won't build for under market rate; needs >=40% of equity OR a build fee.
- Won't concede: my build work is paid (fee or salary), not just "sweat".
- Walk-away: take a salaried CTO role elsewhere.
EOF
gitq "$B" pull -q --rebase origin main
node "$ROOT/cv.js" "$B/canvas.json" fields '{"b9_goalB":"Fair pay for building + a real stake","b9_batnaB":"Salaried CTO role elsewhere","b9_winB":"my build is paid AND I hold meaningful equity"}'
node "$ROOT/cv.js" "$B/canvas.json" t1push '{"what":"build the product","by":"Party B","kind":{"task":true,"share":true}}'
node "$ROOT/cv.js" "$B/canvas.json" t2push '{"what":"build the app","by":"Party B","dur":"Code / content","lev":"High (scales freely)"}'
node "$ROOT/st.js" "$B/negotiation/state.json" '{"ready_to_negotiate":{"A":true,"B":true},"phase":"negotiate"}'
gitq "$B" add canvas.json negotiation/state.json
PRIVB=$(gitq "$B" diff --cached --name-only | grep -c '^private/' || true)
assert "interview B: floor/solo-prep NOT staged (firewall)" "[ '$PRIVB' -eq 0 ]"
gitq "$B" commit -q -m "fair-deal: interview B — opening positions ready; phase=negotiate"
gitq "$B" push -q origin main
assert "interview: both ready → phase=negotiate" "[ \$(phaseof '$B/negotiation/state.json') = negotiate ]"
assert "interview: canvas merged both sides' rows (t1 has 2)" "[ \$(node -e \"console.log(JSON.parse(require('fs').readFileSync('$B/canvas.json')).tables.t1.length)\") -eq 2 ]"

# ============================================================ NEGOTIATE (alternating turns)
hr "4 · negotiate — strict alternation via the turn token"
# turn is 'A' (from setup default, untouched). A moves first.
move(){  # $1=clone $2=me(A/B) $3=other $4=round $5=summary $6=canvasPatchJSON
  local C="$1" ME="$2" OT="$3" RN="$4" SUM="$5" PATCH="$6"
  gitq "$C" pull -q --rebase origin main
  local T; T=$(turnof "$C/negotiation/state.json")
  if [ "$T" != "$ME" ]; then no "negotiate r$RN: $ME tried to move out of turn (turn=$T)"; return; fi
  ok "negotiate r$RN: it is ${ME}'s turn (turn token respected)"
  node "$ROOT/cv.js" "$C/canvas.json" fields "$PATCH"
  printf '## Round %s — %s\n%s\n' "$RN" "$ME" "$SUM" > "$C/negotiation/from-$ME/round-$RN.md"
  printf '\n### r%s %s\n%s\n' "$RN" "$ME" "$SUM" >> "$C/negotiation/log.md"
  node "$ROOT/st.js" "$C/negotiation/state.json" "{\"turn\":\"$OT\",\"round\":$RN,\"last_move\":{\"by\":\"$ME\",\"at\":\"2026-06-30\",\"summary\":\"$SUM\"}}"
  gitq "$C" add canvas.json negotiation/state.json "negotiation/from-$ME/round-$RN.md" negotiation/log.md
  local PV; PV=$(gitq "$C" diff --cached --name-only | grep -c '^private/' || true)
  assert "negotiate r$RN: no private/ staged (firewall)" "[ '$PV' -eq 0 ]"
  # only this side's outbox touched (not the other's)
  assert "negotiate r$RN: $ME did not write the other side's outbox" "! gitq '$C' diff --cached --name-only | grep -q 'from-$OT/'"
  gitq "$C" commit -q -m "fair-deal: negotiate/$RN $ME — $SUM"
  gitq "$C" pull -q --rebase origin main
  gitq "$C" push -q origin main
  assert "negotiate r$RN: canvas.json still parses after push" "jsonok '$C/canvas.json'"
}
# r1: Ada proposes 55/45, anchored to her audience durability
move "$A" A B 1 "Propose Ada 55% / Ben 45%; audience licensed (stays Ada's), benchmark: distribution is top-durability" '{"b5_alloc":"Ada 55% / Ben 45%","b5_vehicle":"LLC"}'
# r2: Ben counters 50/50 with a creative third option (build fee off the top) so equity can be clean
move "$B" B A 2 "Counter Ada 50% / Ben 50%; pay Ben a market build fee off the top in the waterfall so equity is clean 50/50" '{"b5_alloc":"Ada 50% / Ben 50%","b4":"Direct costs -> tax -> Ben build fee (market) -> Ada audience licence fee -> remaining profit 50/50"}'
# r3: Ada accepts 50/50 + the fee mechanism; sets restraint=None; reverse vesting
move "$A" A B 3 "Accept 50/50 with both fees off the top; reverse vesting 4y/1y; restraint None; audience stays licensed" '{"b5_vest":"4-year reverse vesting, 1-year cliff","b8_restraint":"None — neither side is restrained (encouraged default)","b8_exit":"Ada keeps the audience + a data export; foreground product licensed back to both"}'

# convergence — B's turn now; B marks ready + accepts
hr "5 · convergence → ready, then both accept"
gitq "$B" pull -q --rebase origin main
assert "converge: it is B's turn to close" "[ \$(turnof '$B/negotiation/state.json') = B ]"
node "$ROOT/st.js" "$B/negotiation/state.json" '{"phase":"ready","accepted":{"A":false,"B":true},"turn":"A"}'
printf '\n### close B — converged: 50/50 + fees off the top, vesting, audience licensed, restraint none\n' >> "$B/negotiation/log.md"
gitq "$B" add negotiation/state.json negotiation/log.md
gitq "$B" commit -q -m "fair-deal: negotiate/4 B — converged; phase=ready; B accepts"
gitq "$B" push -q origin main
# A reviews + accepts
gitq "$A" pull -q --rebase origin main
node "$ROOT/st.js" "$A/negotiation/state.json" '{"accepted":{"A":true,"B":true}}'
gitq "$A" add negotiation/state.json; gitq "$A" commit -q -m "fair-deal: ready A — A accepts the converged canvas"; gitq "$A" push -q origin main
assert "converge: phase is ready" "[ \$(phaseof '$A/negotiation/state.json') = ready ]"
assert "converge: both accepted" "node -e \"const s=JSON.parse(require('fs').readFileSync('$A/negotiation/state.json'));process.exit(s.accepted.A&&s.accepted.B?0:1)\""

# ============================================================ DRAFT
hr "6 · draft — generate AGREEMENT.md from the shared canvas only"
gitq "$A" pull -q --rebase origin main
node -e '
const fs=require("fs");
const c=JSON.parse(fs.readFileSync(process.argv[1],"utf8"));
const f=c.fields, nm=v=>v==="Party A"?(f.partyA||"A"):v==="Party B"?(f.partyB||"B"):v;
const tagL={asset:"asset (license/value)",task:"task (fee)",role:"role (salary)",share:"co-build (share)"};
let s="# Agreement Memo — "+f.deal+" ("+f.partyA+" × "+f.partyB+")\n\n*Business terms only — not legal advice. Review together, then a lawyer formalises.*\n\n";
s+="## 1. Parties & purpose\n"+f.partyA+" and "+f.partyB+" — "+f.deal+". Vehicle: "+(f.b5_vehicle||"[ ]")+".\n\n";
s+="## 2. The business\nCustomer: "+f.biz_customer+"\nOffer: "+f.biz_offer+"\nChannel: "+f.biz_channel+"\nEdge: "+f.biz_edge+"\n\n";
s+="## 3. Contributions\n"+c.tables.t1.map(r=>"- "+r.what+" — "+nm(r.by)+": "+Object.keys(r.kind||{}).filter(k=>r.kind[k]).map(k=>tagL[k]).join(", ")).join("\n")+"\n\n";
s+="## 4. How money flows\n"+(f.b4||"[ ]")+"\n\n";
s+="## 5. The split & vesting\nHoldings: "+(f.b5_alloc||"[ ]")+"\nVesting: "+(f.b5_vest||"[ ]")+"\n\n";
s+="## 8. How it can end or change\nExit: "+(f.b8_exit||"[ ]")+"\nRestraint: "+(f.b8_restraint||"[ ]")+"\n\n";
s+="## 9. Goals & alignment\n"+f.partyA+": "+f.b9_goalA+" (alt: "+f.b9_batnaA+")\n"+f.partyB+": "+f.b9_goalB+" (alt: "+f.b9_batnaB+")\n\n";
s+="## 11. Legal step\nBusiness terms only; convert to formal documents before relying on it.\n";
fs.writeFileSync(process.argv[2], s);
' "$A/canvas.json" "$A/AGREEMENT.md"
# firewall: the memo must contain nothing from any private floor
assert "draft: AGREEMENT.md generated" "[ -s '$A/AGREEMENT.md' ]"
assert "draft: memo leaks NO private floor (no '45%' / 'walk-away' / 'won't concede')" "! grep -qiE '45%|walk-away|won.t concede|floor' '$A/AGREEMENT.md'"
gitq "$A" add AGREEMENT.md; gitq "$A" commit -q -m "fair-deal: draft A — agreement memo generated"; gitq "$A" push -q origin main

# ============================================================ FINAL INVARIANTS
hr "7 · final repo-wide invariants"
assert "FINAL: origin tree contains ZERO private/ files" "[ \$(gitq '$A' ls-tree -r --name-only origin/main | grep -c '^private/') -eq 0 ]"
assert "FINAL: both private scratchpads still exist locally" "[ -f '$A/private/solo-prep.md' ] && [ -f '$B/private/solo-prep.md' ]"
assert "FINAL: canvas.json valid at HEAD" "jsonok '$A/canvas.json'"
# alternation audit from commit log
echo; echo "  negotiate commit order (should alternate A,B,A,B):"
gitq "$A" log --format='    %an: %s' | grep -E 'negotiate/[0-9]' | tail -r
# turn-token never let the same side move twice in a row is enforced by move() asserts above.

echo; echo "================ RESULT: $PASS passed, $FAIL failed ================"
[ "$FAIL" -eq 0 ]
