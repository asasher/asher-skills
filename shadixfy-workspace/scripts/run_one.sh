#!/usr/bin/env bash
# Run a single eval cell: one (eval_id, agent, condition) at a given iteration.
# Executes the agent in an isolated temp dir OUTSIDE this repo so no ambient
# .claude / AGENTS.md / project skills leak in. Copies produced files into the
# workspace and records timing.
#
# Usage: run_one.sh <eval_id> <agent: claude|codex> <condition: no_skill|uncodixfy|shadixfy> [iteration=1]
#
# Env: CLAUDE_MODEL, CODEX_MODEL (optional model overrides).

set -euo pipefail
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/lib.sh"

EVAL_ID="${1:?eval_id required}"
AGENT="${2:?agent required (claude|codex)}"
CONDITION="${3:?condition required (no_skill|uncodixfy|shadixfy)}"
ITER="${4:-1}"

OUTDIR="$WORKSPACE_DIR/iteration-$ITER/$EVAL_ID/$AGENT/$CONDITION"
mkdir -p "$OUTDIR/outputs"

# Fresh, isolated working dir for the agent (system temp, not inside the repo).
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

# Build and save the exact prompt for reproducibility.
build_prompt "$CONDITION" "$EVAL_ID" > "$OUTDIR/prompt.txt"

echo ">> [$EVAL_ID | $AGENT | $CONDITION] running in $WORKDIR"
start="$(now_ms)"
(
  cd "$WORKDIR"
  case "$AGENT" in
    claude) run_claude "$OUTDIR/agent_response.json" < "$OUTDIR/prompt.txt" ;;
    codex)  run_codex  "$OUTDIR/agent_response.txt"  < "$OUTDIR/prompt.txt" ;;
    *) echo "ERROR: unknown agent '$AGENT'" >&2; exit 1 ;;
  esac
)
end="$(now_ms)"
wall=$(( end - start ))

# Collect any produced HTML (and sibling css/js) into outputs/.
found=0
while IFS= read -r f; do
  cp "$f" "$OUTDIR/outputs/"
  found=1
done < <(find "$WORKDIR" -maxdepth 2 -type f \( -name '*.html' -o -name '*.css' -o -name '*.js' \) 2>/dev/null)
[[ "$found" == 0 ]] && echo "   WARN: no html produced for $EVAL_ID/$AGENT/$CONDITION" >&2

# Timing.
if [[ "$AGENT" == "claude" ]]; then
  write_timing_claude "$OUTDIR/agent_response.json" "$wall" "$OUTDIR/timing.json"
else
  write_timing_codex "$OUTDIR/agent_response.txt" "$wall" "$OUTDIR/timing.json"
fi

echo "   done in ${wall}ms -> $OUTDIR/outputs"
