#!/usr/bin/env bash
# Scripted dry run for scripts/scrub.py in a fresh temporary directory.
# sandbox, never touches the repo, exit non-zero on any FAIL.
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRUB="$SCRIPT_DIR/../scripts/scrub.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
fail=0

ok()  { echo "PASS: $1"; }
bad() { echo "FAIL: $1"; fail=1; }

cat > "$TMP/denylist.txt" <<'EOF'
# internal codenames

Acme
falconworks
EOF

cat > "$TMP/dirty.md" <<'EOF'
The ACME repo stumbled during groom.
Contact asher@example.com for details.
Paths leaked: /Users/someone/project/file.txt then ~/secrets/notes.md then C:\work\repo\a.txt
Tracker: https://tracker.internal.example/T-123
Upstream: https://github.com/asasher/asher-skills/issues/1
EOF

out="$(python3 "$SCRUB" "$TMP/dirty.md" "$TMP/denylist.txt" \
  --allow https://github.com/asasher/asher-skills 2>/dev/null)"
rc=$?

[ "$rc" -eq 1 ] && ok "dirty draft exits 1" || bad "dirty draft exits 1 (got $rc)"
grep -q "denylist: Acme" <<<"$out" && ok "denylist term, case-insensitive" || bad "denylist term, case-insensitive"
grep -q "email: asher@example.com" <<<"$out" && ok "email flagged" || bad "email flagged"
grep -q "path: /Users/someone" <<<"$out" && ok "absolute path flagged" || bad "absolute path flagged"
grep -q "path: ~/secrets" <<<"$out" && ok "home path flagged" || bad "home path flagged"
grep -q 'path: C:' <<<"$out" && ok "windows path flagged" || bad "windows path flagged"
grep -q "url: https://tracker.internal.example" <<<"$out" && ok "foreign url flagged" || bad "foreign url flagged"
grep -q "asasher/asher-skills" <<<"$out" && bad "allowed url not flagged" || ok "allowed url not flagged"

cat > "$TMP/clean.md" <<'EOF'
When a capstone ticket has one open child, the groom sweep re-proposes it every run.
Repro: split a parent into two slices, close one, run the groom twice.
EOF

python3 "$SCRUB" "$TMP/clean.md" "$TMP/denylist.txt" >/dev/null 2>&1
rc=$?
[ "$rc" -eq 0 ] && ok "clean draft exits 0 (single denylist)" || bad "clean draft exits 0 (single denylist, got $rc)"

# Multi-denylist: the scrub takes the machine-local and repo-shareable halves together; a term
# present only in the second file must still be flagged.
cat > "$TMP/denylist-shared.txt" <<'EOF'
# repo-shareable half
zephyrco
EOF

cat > "$TMP/dirty2.md" <<'EOF'
The zephyrco rollout stumbled during groom; Acme saw the same.
EOF

out2="$(python3 "$SCRUB" "$TMP/dirty2.md" "$TMP/denylist.txt" "$TMP/denylist-shared.txt" 2>/dev/null)"
rc=$?
[ "$rc" -eq 1 ] && ok "two denylists: dirty draft exits 1" || bad "two denylists: dirty draft exits 1 (got $rc)"
grep -q "denylist: zephyrco" <<<"$out2" && ok "term only in second denylist flagged" || bad "term only in second denylist flagged"
grep -q "denylist: Acme" <<<"$out2" && ok "term in first denylist still flagged" || bad "term in first denylist still flagged"

python3 "$SCRUB" "$TMP/clean.md" "$TMP/denylist.txt" "$TMP/denylist-shared.txt" >/dev/null 2>&1
rc=$?
[ "$rc" -eq 0 ] && ok "clean draft exits 0 (two denylists)" || bad "clean draft exits 0 (two denylists, got $rc)"

if [ "$fail" -ne 0 ]; then
  echo "scrub-dryrun: FAIL" >&2
  exit 1
fi
echo "scrub-dryrun: all checks passed" >&2
