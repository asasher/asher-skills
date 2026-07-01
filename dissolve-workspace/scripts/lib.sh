#!/usr/bin/env bash
# Shared helpers for the dissolve eval. Sourced, not run directly.
set -euo pipefail

LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
EVAL_DIR="$(cd "$LIB_DIR/.." && pwd)"
REPO_DIR="$(cd "$EVAL_DIR/.." && pwd)"
TEMPLATE="$REPO_DIR/skills/dissolve/templates/dissolution.html"

QUESTION="Is alcoholism a disease?"
DATE="2026-07-01"

# Seed a fresh dissolution.html (question pre-filled) into a target dir.
# Args: <target_dir>
seed() {
  local dir="$1"
  mkdir -p "$dir/sources"
  sed -e "s/{{QUESTION}}/$QUESTION/g" -e "s/{{DATE}}/$DATE/g" "$TEMPLATE" > "$dir/dissolution.html"
}

# Run Codex headless in a dir with an isolated CODEX_HOME so no ambient
# skills/AGENTS.md leak in. It edits files in-place in that dir.
# Args: <workdir> <prompt_file>
run_codex() {
  local workdir prompt ch
  workdir="$(cd "$1" && pwd)"                       # absolute
  prompt="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"   # absolute
  ch="$(mktemp -d)"
  [[ -f "$HOME/.codex/auth.json"   ]] && cp "$HOME/.codex/auth.json"   "$ch/" || true
  [[ -f "$HOME/.codex/config.toml" ]] && cp "$HOME/.codex/config.toml" "$ch/" || true
  ( cd "$workdir" && CODEX_HOME="$ch" codex exec -s workspace-write --skip-git-repo-check - \
      < "$prompt" > "$workdir/codex.log" 2> "$workdir/codex.stderr.log" ) || true
  rm -rf "$ch"
}
