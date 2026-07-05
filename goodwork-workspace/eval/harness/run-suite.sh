#!/usr/bin/env bash
# Run the goodwork pair-loop matrix and aggregate a markdown report.

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  goodwork-workspace/eval/harness/run-suite.sh [options]

Options:
  --personas-dir DIR  Default: goodwork-workspace/eval/personas
  --seeds N          Seeds per persona. Default: 3
  --results-dir DIR  Default: goodwork-workspace/eval/harness/results
  --max-turns N      Subject turns per Good Work session. Default: 40
  --skip-judge       Do not run codex-as-judge; report hard assertions only
  --smoke            Run only the first persona and seed 1, pass --smoke to run-pair, and skip judge unless --judge-smoke is set
  --judge-smoke      With --smoke, still run judge.sh
  --fake-agents      Pass --fake-agents to run-pair
  -h, --help         Show this help

Environment:
  CLAUDE_MODEL       Optional model passed through to run-pair.sh
  CODEX_MODEL        Optional model passed through to actor and judge codex exec
EOF
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PERSONAS_DIR="$SCRIPT_DIR/../personas"
RESULTS_DIR="$SCRIPT_DIR/results"
SEEDS=3
MAX_TURNS=40
SKIP_JUDGE=0
SMOKE=0
JUDGE_SMOKE=0
FAKE_AGENTS=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --personas-dir) PERSONAS_DIR="${2:?--personas-dir requires a path}"; shift 2 ;;
    --seeds) SEEDS="${2:?--seeds requires a value}"; shift 2 ;;
    --results-dir) RESULTS_DIR="${2:?--results-dir requires a path}"; shift 2 ;;
    --max-turns) MAX_TURNS="${2:?--max-turns requires a value}"; shift 2 ;;
    --skip-judge) SKIP_JUDGE=1; shift ;;
    --smoke) SMOKE=1; MAX_TURNS=2; SEEDS=1; shift ;;
    --judge-smoke) JUDGE_SMOKE=1; shift ;;
    --fake-agents) FAKE_AGENTS=1; shift ;;
    -h|--help) usage; exit 0 ;;
    --*) echo "ERROR: unknown option $1" >&2; usage >&2; exit 2 ;;
    *) echo "ERROR: unexpected argument $1" >&2; usage >&2; exit 2 ;;
  esac
done

if ! [[ "$SEEDS" =~ ^[0-9]+$ && "$MAX_TURNS" =~ ^[0-9]+$ ]]; then
  echo "ERROR: seeds and max-turns must be positive integers" >&2
  exit 2
fi
if [[ "$SEEDS" -lt 1 || "$MAX_TURNS" -lt 1 ]]; then
  echo "ERROR: seeds and max-turns must be >= 1" >&2
  exit 2
fi

mkdir -p "$RESULTS_DIR"

PERSONAS=()
while IFS= read -r persona_file; do
  PERSONAS+=("$persona_file")
done < <(find "$PERSONAS_DIR" -maxdepth 1 -type f -name '*.md' ! -name 'README.md' | sort)
if [[ "${#PERSONAS[@]}" -eq 0 ]]; then
  echo "ERROR: no persona .md files found in $PERSONAS_DIR" >&2
  exit 1
fi
if [[ "$SMOKE" == "1" ]]; then
  PERSONAS=("${PERSONAS[0]}")
  if [[ "$JUDGE_SMOKE" != "1" ]]; then
    SKIP_JUDGE=1
  fi
fi

LOG="$RESULTS_DIR/run-suite.log"
: > "$LOG"

for persona in "${PERSONAS[@]}"; do
  slug="$(python3 - "$persona" <<'PY'
import re, sys
from pathlib import Path
print(re.sub(r'[^A-Za-z0-9._-]+', '-', Path(sys.argv[1]).stem).strip('-') or 'persona')
PY
)"
  for seed in $(seq 1 "$SEEDS"); do
    run_dir="$RESULTS_DIR/runs/$slug/seed-$seed"
    echo ">> run $slug seed $seed" | tee -a "$LOG"
    pair_args=(--persona "$persona" --seed "$seed" --outdir "$run_dir" --max-turns "$MAX_TURNS" --force)
    if [[ "$SMOKE" == "1" ]]; then
      pair_args+=(--smoke)
    fi
    if [[ "$FAKE_AGENTS" == "1" ]]; then
      pair_args+=(--fake-agents)
    fi

    set +e
    "$SCRIPT_DIR/run-pair.sh" "${pair_args[@]}" >> "$LOG" 2>&1
    pair_status=$?
    set -e
    if [[ "$pair_status" -ne 0 ]]; then
      echo "   WARN: run-pair failed for $slug seed $seed with status $pair_status" | tee -a "$LOG"
      continue
    fi

    if [[ "$SKIP_JUDGE" == "1" ]]; then
      echo "   judge skipped" | tee -a "$LOG"
      continue
    fi

    set +e
    "$SCRIPT_DIR/judge.sh" --run-dir "$run_dir" --persona "$persona" >> "$LOG" 2>&1
    judge_status=$?
    set -e
    if [[ "$judge_status" -ne 0 ]]; then
      echo "   WARN: judge failed for $slug seed $seed with status $judge_status" | tee -a "$LOG"
    fi
  done
done

python3 - "$RESULTS_DIR" "$RESULTS_DIR/report.md" <<'PY'
import json
import math
import statistics
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

results_dir = Path(sys.argv[1])
report_path = Path(sys.argv[2])
run_dirs = sorted((results_dir / "runs").glob("*/seed-*"))


def load_json(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"error": f"could not parse {path.name}: {exc}"}


def pct(value):
    if value is None:
        return "n/a"
    return f"{value * 100:.1f}%"


def bool_cell(value):
    if value is None:
        return "n/a"
    return "PASS" if value else "FAIL"


def run_outcome(meta, assertions, judge):
    if meta.get("status") == "error" or judge.get("status") == "error":
        return "ERROR"
    if assertions.get("passed") is False:
        return "FAIL"
    if assertions.get("passed") is True:
        return "PASS"
    return "n/a"


def difficulty_summary(judge):
    summary = judge.get("summary") or {}
    by_diff = summary.get("recall_by_difficulty") or {}
    if by_diff:
        return {
            key: pct((val or {}).get("recall")) if isinstance(val, dict) else "n/a"
            for key, val in by_diff.items()
        }

    facts = judge.get("facts") or []
    buckets = defaultdict(lambda: [0, 0])
    for fact in facts:
        diff = fact.get("difficulty") or "unknown"
        buckets[diff][0] += 1
        if fact.get("recovered"):
            buckets[diff][1] += 1
    return {key: pct(recovered / total if total else None) for key, (total, recovered) in buckets.items()}


def assertion_map(assertions_json):
    return {row.get("id"): row for row in assertions_json.get("assertions", [])}


def safety_from(assertions, judge):
    amap = assertion_map(assertions)
    hard = [
        amap.get("no_outbound_action_claims", {}).get("passed"),
        amap.get("outbound_approval_gate_present", {}).get("passed"),
    ]
    gates = judge.get("safety_gates") or {}
    judge_values = [value for value in gates.values() if isinstance(value, bool)]
    values = [value for value in hard + judge_values if value is not None]
    return all(values) if values else None


def bool_map_pass(mapping):
    values = [value for value in (mapping or {}).values() if isinstance(value, bool)]
    return all(values) if values else None


runs = []
invariant_counts = defaultdict(lambda: [0, 0])
safety_counts = defaultdict(lambda: [0, 0])
persona_gate_counts = defaultdict(lambda: [0, 0])
recalls_by_persona = defaultdict(list)

for run_dir in run_dirs:
    meta = load_json(run_dir / "metadata.json")
    assertions = load_json(run_dir / "assertions.json")
    judge = load_json(run_dir / "judge.json")
    persona = Path(meta.get("persona", run_dir.parent.name)).stem
    seed = meta.get("seed", run_dir.name.replace("seed-", ""))
    summary = judge.get("summary") or {}
    recall = summary.get("recall")
    facts_total = summary.get("facts_total") or 0
    scoreable = judge.get("status") != "error" and facts_total > 0 and isinstance(recall, (int, float)) and not math.isnan(recall)
    if scoreable:
        recalls_by_persona[persona].append(float(recall))
    amap = assertion_map(assertions)
    for row in assertions.get("assertions", []):
        if row.get("skipped"):
            continue
        invariant_counts[row.get("id")][1] += 1
        if row.get("passed"):
            invariant_counts[row.get("id")][0] += 1
    for row in assertions.get("assertions", []):
        if row.get("id") in {"no_outbound_action_claims", "outbound_approval_gate_present"} and not row.get("skipped"):
            safety_counts[row.get("id")][1] += 1
            if row.get("passed"):
                safety_counts[row.get("id")][0] += 1
    for key, value in (judge.get("safety_gates") or {}).items():
        if isinstance(value, bool):
            safety_counts[f"judge:{key}"][1] += 1
            if value:
                safety_counts[f"judge:{key}"][0] += 1
    for key, value in (judge.get("persona_gates") or {}).items():
        if isinstance(value, bool):
            persona_gate_counts[key][1] += 1
            if value:
                persona_gate_counts[key][0] += 1

    diff = difficulty_summary(judge)
    runs.append({
        "persona": persona,
        "seed": seed,
        "status": run_outcome(meta, assertions, judge),
        "ended": meta.get("ended_reason", "n/a"),
        "assertions_passed": assertions.get("passed"),
        "recall": recall if scoreable else None,
        "volunteered": diff.get("volunteered", "n/a"),
        "probed": diff.get("probed", "n/a"),
        "contradiction": diff.get("contradiction", "n/a"),
        "safety": safety_from(assertions, judge),
        "persona_gates": bool_map_pass(judge.get("persona_gates")),
        "judge_error": judge.get("error"),
        "infra_error": meta.get("error_message") if meta.get("status") == "error" else None,
        "run_dir": run_dir,
    })

lines = []
lines.append("# Goodwork Eval Report")
lines.append("")
lines.append(f"Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}")
lines.append(f"Runs found: {len(runs)}")
lines.append("")

lines.append("## Persona x Seed")
lines.append("")
lines.append("| Persona | Seed | Status | Ended | Hard gates | Recall | Volunteered | Probed | Contradiction | Safety | Persona gates | Notes |")
lines.append("|---|---:|---|---|---|---:|---:|---:|---:|---|---|---|")
for row in runs:
    notes = row["infra_error"] or row["judge_error"] or ""
    lines.append(
        f"| {row['persona']} | {row['seed']} | {row['status']} | {row['ended']} | {bool_cell(row['assertions_passed'])} | "
        f"{pct(row['recall'])} | {row['volunteered']} | {row['probed']} | {row['contradiction']} | "
        f"{bool_cell(row['safety'])} | {bool_cell(row['persona_gates'])} | {notes} |"
    )
if not runs:
    lines.append("| n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | no runs found |")
lines.append("")

lines.append("## Invariant Pass Rates")
lines.append("")
lines.append("| Gate | Passes | Total | Rate |")
lines.append("|---|---:|---:|---:|")
for gate, (passed, total) in sorted(invariant_counts.items()):
    lines.append(f"| {gate} | {passed} | {total} | {pct(passed / total if total else None)} |")
if not invariant_counts:
    lines.append("| n/a | 0 | 0 | n/a |")
lines.append("")

lines.append("## Binary Safety Gates")
lines.append("")
lines.append("| Gate | Passes | Total | Rate |")
lines.append("|---|---:|---:|---:|")
for gate, (passed, total) in sorted(safety_counts.items()):
    lines.append(f"| {gate} | {passed} | {total} | {pct(passed / total if total else None)} |")
if not safety_counts:
    lines.append("| n/a | 0 | 0 | n/a |")
lines.append("")

lines.append("## Persona Binary Gates")
lines.append("")
lines.append("| Gate | Passes | Total | Rate |")
lines.append("|---|---:|---:|---:|")
for gate, (passed, total) in sorted(persona_gate_counts.items()):
    lines.append(f"| {gate} | {passed} | {total} | {pct(passed / total if total else None)} |")
if not persona_gate_counts:
    lines.append("| n/a | 0 | 0 | n/a |")
lines.append("")

lines.append("## Variance Across Seeds")
lines.append("")
lines.append("| Persona | Seeds With Judge Scores | Mean Recall | Std Dev |")
lines.append("|---|---:|---:|---:|")
for persona, values in sorted(recalls_by_persona.items()):
    mean = statistics.mean(values) if values else None
    stdev = statistics.pstdev(values) if len(values) > 1 else 0.0 if values else None
    lines.append(f"| {persona} | {len(values)} | {pct(mean)} | {pct(stdev)} |")
if not recalls_by_persona:
    lines.append("| n/a | 0 | n/a | n/a |")
lines.append("")

lines.append("## Run Artifacts")
lines.append("")
for row in runs:
    rel = row["run_dir"].relative_to(results_dir)
    lines.append(f"- `{rel}`")

report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Report: {report_path}")
PY

echo "Suite complete: $RESULTS_DIR/report.md"
