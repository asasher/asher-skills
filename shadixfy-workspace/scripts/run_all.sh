#!/usr/bin/env bash
# Run the full eval matrix for an iteration: every eval x agent x condition,
# in throttled parallel. Then screenshot + grade each cell, then aggregate.
#
# Usage: run_all.sh [iteration=1]
#   AGENTS="claude" CONDITIONS="no_skill shadixfy" run_all.sh 1   # subset
#   MAXJOBS=4 run_all.sh 1                                        # cap concurrency
#   SEQUENTIAL=1 run_all.sh 1                                     # one at a time
#
# bash 3.2 compatible (macOS default): no mapfile, no `wait -n`. Concurrency is
# capped with a `jobs -r` polling loop so we don't stampede the Claude/Codex
# rate limits. Each cell is independent; a failed cell just yields no html.

set -uo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

ITER="${1:-1}"
AGENTS="${AGENTS:-claude codex}"
CONDITIONS="${CONDITIONS:-no_skill uncodixfy shadixfy}"
MAXJOBS="${MAXJOBS:-6}"
SEQUENTIAL="${SEQUENTIAL:-0}"

EVAL_IDS=()
while IFS= read -r line; do [ -n "$line" ] && EVAL_IDS+=("$line"); done < <(jq -r '.evals[].id' "$EVALS_JSON")

echo "== iteration $ITER =="
echo "   evals:      ${EVAL_IDS[*]}"
echo "   agents:     $AGENTS"
echo "   conditions: $CONDITIONS"
echo "   parallelism: $([ "$SEQUENTIAL" = 1 ] && echo sequential || echo "$MAXJOBS-wide")"
echo

# Block until fewer than MAXJOBS background jobs are running.
throttle() {
  while [ "$(jobs -r | wc -l | tr -d ' ')" -ge "$MAXJOBS" ]; do sleep 1; done
}

started=0
for eval_id in "${EVAL_IDS[@]}"; do
  for agent in $AGENTS; do
    for cond in $CONDITIONS; do
      if [ "$SEQUENTIAL" = 1 ]; then
        "$LIB_DIR/run_one.sh" "$eval_id" "$agent" "$cond" "$ITER"
      else
        throttle
        "$LIB_DIR/run_one.sh" "$eval_id" "$agent" "$cond" "$ITER" &
      fi
      started=$((started + 1))
    done
  done
done
wait
echo
echo ">> all $started runs finished"

echo
echo "== screenshot + grade =="
for eval_id in "${EVAL_IDS[@]}"; do
  for agent in $AGENTS; do
    for cond in $CONDITIONS; do
      outdir="$WORKSPACE_DIR/iteration-$ITER/$eval_id/$agent/$cond"
      [ -f "$outdir/outputs/index.html" ] || { echo "   (no html) $eval_id/$agent/$cond"; continue; }
      bash "$LIB_DIR/screenshot.sh" "$outdir/outputs/index.html" || true
      node "$LIB_DIR/grade.mjs" "$eval_id" "$outdir" || true
    done
  done
done

echo
echo "== aggregate =="
node "$LIB_DIR/aggregate.mjs" "$ITER"

echo
echo "== dashboard =="
node "$LIB_DIR/build_dashboard.mjs"

echo
echo "Done. Open the review dashboard: $WORKSPACE_DIR/dashboard.html"
echo "Raw cells under: $WORKSPACE_DIR/iteration-$ITER/"
echo "Then fill feedback.json after human review (see workspace README)."
