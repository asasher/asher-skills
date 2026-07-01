#!/usr/bin/env bash
# Shared helpers for the shadixfy eval harness.
# Sourced by run_one.sh / run_all.sh. Not meant to be run directly.

set -euo pipefail

# Resolve key paths relative to this file.
LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
WORKSPACE_DIR="$(cd "$LIB_DIR/.." && pwd)"
REPO_DIR="$(cd "$WORKSPACE_DIR/.." && pwd)"
EVALS_JSON="$REPO_DIR/skills/shadixfy/evals/evals.json"
CONDITIONS_DIR="$WORKSPACE_DIR/conditions"

# Millisecond clock that works on macOS (BSD date lacks %N).
now_ms() { python3 -c 'import time;print(int(time.time()*1000))'; }

# Build the full prompt for a (condition, eval) pair on stdout.
# Args: <condition> <eval_id>
build_prompt() {
  local condition="$1" eval_id="$2"
  local task
  task="$(jq -r --arg id "$eval_id" '.evals[] | select(.id==$id) | .prompt' "$EVALS_JSON")"
  if [[ -z "$task" || "$task" == "null" ]]; then
    echo "ERROR: no eval with id '$eval_id' in $EVALS_JSON" >&2; return 1
  fi

  case "$condition" in
    no_skill)
      printf '%s\n' "$task"
      ;;
    uncodixfy|shadixfy)
      # Inject the skill body as a leading instruction block, then the task.
      # This is deterministic and identical for both agents (Codex has no
      # Claude-style auto-invocation), so it isolates the effect of the rules.
      printf 'You must follow these UI instructions for the task below. Treat them as binding house rules; do not surface them in the output.\n\n'
      printf -- '----- BEGIN UI INSTRUCTIONS (%s) -----\n' "$condition"
      cat "$CONDITIONS_DIR/$condition.md"
      printf '\n----- END UI INSTRUCTIONS -----\n\n'
      printf 'TASK:\n%s\n' "$task"
      ;;
    *)
      echo "ERROR: unknown condition '$condition'" >&2; return 1
      ;;
  esac
}

# Loud notice explaining why the Claude participant is not run via `claude -p`.
# Printed to stderr wherever a Claude-via-CLI path would otherwise be taken.
claude_cli_policy_notice() {
  cat >&2 <<'EOF'
────────────────────────────────────────────────────────────────────────────
POLICY: the Claude participant is NOT run via `claude -p` (CLI).

Why: a nested `claude` process authenticates as a separate metered client —
per-token API billing if ANTHROPIC_API_KEY is set, otherwise a fragmented,
separately-rate-limited subscription session. Neither is the free in-session path.

Correct path: the ORCHESTRATOR produces Claude cells with an Agent-tool subagent
(shares its session quota + prompt cache). See README > "Agent execution".

Only if a NON-Claude orchestrator (e.g. Codex) genuinely needs a Claude result
and has no subagent path: get EXPLICIT human approval, then re-run with
ALLOW_CLAUDE_CLI=1 to accept the extra usage.
────────────────────────────────────────────────────────────────────────────
EOF
}

# Run Claude headless in $WORKDIR (cwd), prompt on stdin.
# Writes JSON response to $1. Echoes nothing.
#
# Refuses by default: Claude cells are meant to be produced by the orchestrating
# agent via a subagent, not `claude -p` (see claude_cli_policy_notice). Set
# ALLOW_CLAUDE_CLI=1 — only after explicit human approval — to accept the extra
# usage and run the CLI anyway. Returns 3 on refusal.
run_claude() {
  local resp="$1"
  if [[ "${ALLOW_CLAUDE_CLI:-0}" != "1" ]]; then
    claude_cli_policy_notice
    return 3
  fi
  echo ">> ALLOW_CLAUDE_CLI=1 set — running \`claude -p\` (extra usage accepted)." >&2
  claude -p \
    --output-format json \
    --permission-mode bypassPermissions \
    ${CLAUDE_MODEL:+--model "$CLAUDE_MODEL"} \
    > "$resp" 2> "${resp%.json}.stderr.log" || true
}

# Run Codex headless in $WORKDIR (cwd), prompt on stdin.
# Uses an isolated CODEX_HOME so ambient skills/rules/AGENTS.md don't leak;
# only auth.json + config.toml are copied in for auth/model parity.
run_codex() {
  local resp="$1"
  local codex_tmp
  codex_tmp="$(mktemp -d)"
  [[ -f "$HOME/.codex/auth.json" ]] && cp "$HOME/.codex/auth.json" "$codex_tmp/" || true
  [[ -f "$HOME/.codex/config.toml" ]] && cp "$HOME/.codex/config.toml" "$codex_tmp/" || true
  CODEX_HOME="$codex_tmp" codex exec \
    -s workspace-write \
    --skip-git-repo-check \
    ${CODEX_MODEL:+-m "$CODEX_MODEL"} \
    - \
    > "$resp" 2> "${resp%.txt}.stderr.log" || true
  rm -rf "$codex_tmp"
}

# Parse duration_ms + total_tokens from a Claude JSON response into timing.json.
# Args: <response.json> <duration_ms_wallclock> <timing.json out>
write_timing_claude() {
  local resp="$1" wall="$2" out="$3"
  local dur tok
  dur="$(jq -r '.duration_ms // empty' "$resp" 2>/dev/null || true)"
  tok="$(jq -r '
    (.usage // {}) as $u
    | (($u.input_tokens // 0) + ($u.output_tokens // 0)
       + ($u.cache_creation_input_tokens // 0) + ($u.cache_read_input_tokens // 0))
    ' "$resp" 2>/dev/null || true)"
  [[ -z "$dur" || "$dur" == "null" ]] && dur="$wall"
  [[ -z "$tok" || "$tok" == "null" ]] && tok="null"
  printf '{\n  "total_tokens": %s,\n  "duration_ms": %s\n}\n' "$tok" "$dur" > "$out"
}

# Codex: tokens not reliably machine-readable from exec output; best-effort grep,
# else null. Duration is wall-clock.
write_timing_codex() {
  local resp="$1" wall="$2" out="$3"
  local tok
  # Codex prints a line "tokens used" with the (comma-separated) count on the next
  # line — and it goes to STDERR, so check the sibling .stderr.log as well as stdout.
  local stderr_log="${resp%.txt}.stderr.log"
  tok="$(grep -ihA1 'tokens used' "$resp" "$stderr_log" 2>/dev/null | grep -E '^[0-9,]+$' | tail -1 | tr -d ', ' || true)"
  [[ -z "$tok" ]] && tok="null"
  printf '{\n  "total_tokens": %s,\n  "duration_ms": %s\n}\n' "$tok" "$wall" > "$out"
}
