#!/usr/bin/env bash
# Run one goodwork pair-loop eval: one persona + one seed.

set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  goodwork-workspace/eval/harness/run-pair.sh --persona PERSONA.md --seed N [options]
  goodwork-workspace/eval/harness/run-pair.sh PERSONA.md N [options]

Options:
  --outdir DIR       Run artifact directory. Default: harness/results/runs/<persona>/seed-<N>
  --max-turns N     Subject turns per eval session. Default: 40, or 2 with --smoke
  --sessions N      Number of Good Work sessions in the same workspace. Default: infer 2 if persona mentions session 2 or multi-session, else 1
  --smoke           Cap to a 2-subject-turn loop. Pair with GOODWORK_FAKE_AGENTS=1 for a no-token smoke test
  --fake-agents     Do not call claude or codex; use deterministic local stand-ins
  --force           Allow replacing a custom --outdir
  -h, --help        Show this help

Environment:
  CLAUDE_MODEL      Optional model passed to claude -p
  CODEX_MODEL       Optional model passed to codex exec
  GOODWORK_FAKE_AGENTS=1  Same as --fake-agents
  GOODWORK_SUBJECT_TIMEOUT=900  Seconds before a subject call is an infra ERROR
  GOODWORK_ACTOR_TIMEOUT=300    Seconds before an actor call is an infra ERROR
  GOODWORK_TRANSCRIPT_TAIL_BYTES=12000  Transcript tail sent to actor turns
EOF
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
RESULTS_DIR="$SCRIPT_DIR/results"
GOODWORK_SKILL="$REPO_ROOT/skills/goodwork"

PERSONA=""
SEED=""
OUTDIR=""
MAX_TURNS=40
SESSIONS=""
SMOKE=0
FAKE_AGENTS="${GOODWORK_FAKE_AGENTS:-0}"
FORCE=0
SUBJECT_TIMEOUT="${GOODWORK_SUBJECT_TIMEOUT:-900}"
ACTOR_TIMEOUT="${GOODWORK_ACTOR_TIMEOUT:-300}"
TRANSCRIPT_TAIL_BYTES="${GOODWORK_TRANSCRIPT_TAIL_BYTES:-12000}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --persona) PERSONA="${2:?--persona requires a path}"; shift 2 ;;
    --seed) SEED="${2:?--seed requires a value}"; shift 2 ;;
    --outdir) OUTDIR="${2:?--outdir requires a path}"; shift 2 ;;
    --max-turns) MAX_TURNS="${2:?--max-turns requires a value}"; shift 2 ;;
    --sessions) SESSIONS="${2:?--sessions requires a value}"; shift 2 ;;
    --smoke) SMOKE=1; MAX_TURNS=2; shift ;;
    --fake-agents) FAKE_AGENTS=1; shift ;;
    --force) FORCE=1; shift ;;
    -h|--help) usage; exit 0 ;;
    --*) echo "ERROR: unknown option $1" >&2; usage >&2; exit 2 ;;
    *)
      if [[ -z "$PERSONA" ]]; then
        PERSONA="$1"
      elif [[ -z "$SEED" ]]; then
        SEED="$1"
      else
        echo "ERROR: unexpected positional argument $1" >&2
        usage >&2
        exit 2
      fi
      shift
      ;;
  esac
done

if [[ -z "$PERSONA" || -z "$SEED" ]]; then
  echo "ERROR: persona and seed are required" >&2
  usage >&2
  exit 2
fi

if [[ ! -f "$PERSONA" ]]; then
  echo "ERROR: persona file not found: $PERSONA" >&2
  exit 1
fi
if [[ ! -d "$GOODWORK_SKILL" ]]; then
  echo "ERROR: goodwork skill not found at $GOODWORK_SKILL" >&2
  exit 1
fi

PERSONA_ABS="$(cd "$(dirname "$PERSONA")" && pwd)/$(basename "$PERSONA")"
PERSONA_SLUG="$(python3 - "$PERSONA_ABS" <<'PY'
import re, sys
from pathlib import Path
stem = Path(sys.argv[1]).stem
print(re.sub(r'[^A-Za-z0-9._-]+', '-', stem).strip('-') or 'persona')
PY
)"

if [[ -z "$SESSIONS" ]]; then
  SESSIONS="$(python3 - "$PERSONA_ABS" <<'PY'
import re, sys
text = open(sys.argv[1], encoding='utf-8').read()
if re.search(r'(?im)^\s*#{1,6}\s+.*\bsession\s+2\b', text) or re.search(r'(?i)\bmulti[- ]session\b|\bsession\s+2\b', text):
    print(2)
else:
    print(1)
PY
)"
fi

if ! [[ "$SEED" =~ ^[0-9]+$ && "$MAX_TURNS" =~ ^[0-9]+$ && "$SESSIONS" =~ ^[0-9]+$ && "$SUBJECT_TIMEOUT" =~ ^[0-9]+$ && "$ACTOR_TIMEOUT" =~ ^[0-9]+$ && "$TRANSCRIPT_TAIL_BYTES" =~ ^[0-9]+$ ]]; then
  echo "ERROR: seed, max-turns, sessions, timeouts, and transcript tail bytes must be positive integers" >&2
  exit 2
fi
if [[ "$MAX_TURNS" -lt 1 || "$SESSIONS" -lt 1 || "$SUBJECT_TIMEOUT" -lt 1 || "$ACTOR_TIMEOUT" -lt 1 || "$TRANSCRIPT_TAIL_BYTES" -lt 1000 ]]; then
  echo "ERROR: max-turns, sessions, and timeouts must be >= 1; transcript tail bytes must be >= 1000" >&2
  exit 2
fi

if [[ -z "$OUTDIR" ]]; then
  RUN_DIR="$RESULTS_DIR/runs/$PERSONA_SLUG/seed-$SEED"
  REPLACE_OK=1
else
  RUN_DIR="$OUTDIR"
  REPLACE_OK="$FORCE"
fi
RUN_DIR_ABS="$(python3 - "$RUN_DIR" <<'PY'
import os, sys
print(os.path.abspath(sys.argv[1]))
PY
)"

if [[ -e "$RUN_DIR_ABS" ]]; then
  if [[ "$REPLACE_OK" != "1" ]]; then
    echo "ERROR: run dir exists; pass --force for custom --outdir: $RUN_DIR_ABS" >&2
    exit 1
  fi
  rm -rf "$RUN_DIR_ABS"
fi

WORKSPACE="$RUN_DIR_ABS/workspace"
RAW_DIR="$RUN_DIR_ABS/raw"
PROMPT_DIR="$RUN_DIR_ABS/prompts"
TRANSCRIPT="$RUN_DIR_ABS/transcript.md"
ASSERTIONS="$RUN_DIR_ABS/assertions.json"
mkdir -p "$WORKSPACE" "$RAW_DIR" "$PROMPT_DIR"

extract_section() {
  local file="$1" heading="$2"
  python3 - "$file" "$heading" <<'PY'
import re, sys
from pathlib import Path

path = Path(sys.argv[1])
wanted = sys.argv[2].strip().lower()
lines = path.read_text(encoding="utf-8").splitlines()
start = None
start_level = None
heading_re = re.compile(r'^(#{1,6})\s+(.+?)\s*$')
label_re = re.compile(r'^\s*(?:[-*]\s*)?\*\*(.+?)\*\*\s*:?\s*$')

def clean(title):
    title = re.sub(r'[*_`]+', '', title)
    title = title.rstrip(':').strip().lower()
    return title

boundaries = []
for i, line in enumerate(lines):
    m = heading_re.match(line)
    if m:
        boundaries.append((i, len(m.group(1)), clean(m.group(2))))
        continue
    m = label_re.match(line)
    if m:
        boundaries.append((i, 7, clean(m.group(1))))

for pos, (i, level, title) in enumerate(boundaries):
    if title == wanted:
        start = i + 1
        start_level = level
        next_boundaries = boundaries[pos + 1:]
        break

if start is None:
    print(f"ERROR: persona is missing required section: {sys.argv[2]}", file=sys.stderr)
    sys.exit(4)

end = len(lines)
for i, level, _title in next_boundaries:
    if level <= start_level:
        end = i
        break

body = "\n".join(lines[start:end]).strip()
if not body:
    print(f"ERROR: persona section is empty: {sys.argv[2]}", file=sys.stderr)
    sys.exit(4)

print("# Backstory record")
print()
print(body)
PY
}

extract_section "$PERSONA_ABS" "Backstory record" > "$WORKSPACE/record.md"
printf 'record.md\n' > "$RUN_DIR_ABS/initial-files.txt"

python3 - "$RUN_DIR_ABS/metadata.json" "$PERSONA_ABS" "$SEED" "$WORKSPACE" "$MAX_TURNS" "$SESSIONS" "$SMOKE" "$FAKE_AGENTS" <<'PY'
import json, sys
out, persona, seed, workspace, max_turns, sessions, smoke, fake = sys.argv[1:]
json.dump({
    "persona": persona,
    "seed": int(seed),
    "workspace": workspace,
    "max_turns": int(max_turns),
    "sessions": int(sessions),
    "smoke": smoke == "1",
    "fake_agents": fake == "1",
    "status": "running",
}, open(out, "w", encoding="utf-8"), indent=2)
PY

cat > "$TRANSCRIPT" <<EOF
# Goodwork Pair Transcript

- Persona: $PERSONA_ABS
- Seed: $SEED
- Workspace: $WORKSPACE
- Sessions: $SESSIONS
- Max subject turns per session: $MAX_TURNS
- Smoke: $SMOKE
- Fake agents: $FAKE_AGENTS

EOF

append_block() {
  local header="$1" body_file="$2"
  {
    printf '\n## %s\n\n' "$header"
    cat "$body_file"
    printf '\n'
  } >> "$TRANSCRIPT"
}

run_command_with_timeout() {
  local timeout_s="$1" cwd="$2" stdin_file="$3" stdout_file="$4" stderr_file="$5"
  shift 5
  python3 - "$timeout_s" "$cwd" "$stdin_file" "$stdout_file" "$stderr_file" "$@" <<'PY'
import subprocess
import sys
from pathlib import Path

timeout_s = float(sys.argv[1])
cwd = sys.argv[2]
stdin_path, stdout_path, stderr_path = map(Path, sys.argv[3:6])
cmd = sys.argv[6:]

try:
    with stdin_path.open("rb") as stdin, stdout_path.open("wb") as stdout, stderr_path.open("ab") as stderr:
        proc = subprocess.run(cmd, cwd=cwd, stdin=stdin, stdout=stdout, stderr=stderr, timeout=timeout_s)
    raise SystemExit(proc.returncode)
except subprocess.TimeoutExpired:
    with stderr_path.open("ab") as stderr:
        stderr.write(f"\nERROR: command timed out after {timeout_s:g}s: {' '.join(cmd)}\n".encode())
    raise SystemExit(124)
except FileNotFoundError as exc:
    with stderr_path.open("ab") as stderr:
        stderr.write(f"\nERROR: command not found: {exc}\n".encode())
    raise SystemExit(127)
PY
}

mark_run_error() {
  local component="$1" status="$2" message="$3"
  {
    printf '\n## Harness Error\n\n'
    printf '%s\n' "$message"
  } >> "$TRANSCRIPT"
  python3 - "$RUN_DIR_ABS/metadata.json" "$component" "$status" "$message" "$TOTAL_SUBJECT_TURNS" "$BAILED" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
component, status, message, total_turns, bailed = sys.argv[2:]
try:
    data = json.loads(path.read_text(encoding="utf-8"))
except Exception:
    data = {}
data["status"] = "error"
data["ended_reason"] = "infra_error"
data["error_component"] = component
data["error_exit_status"] = int(status) if status.isdigit() else status
data["error_message"] = message
data["total_subject_turns"] = int(total_turns)
data["actor_bailed"] = bailed == "1"
path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY
  python3 - "$ASSERTIONS" "$RUN_DIR_ABS" "$component" "$message" <<'PY'
import json
import sys

out, run_dir, component, message = sys.argv[1:]
json.dump(
    {
        "run_dir": run_dir,
        "status": "error",
        "passed": None,
        "error_component": component,
        "error": message,
        "summary": {"passed": 0, "failed": 0, "skipped": 0},
        "assertions": [],
    },
    open(out, "w", encoding="utf-8"),
    indent=2,
)
print()
PY
}

abort_run() {
  local component="$1" status="$2" message="$3"
  mark_run_error "$component" "$status" "$message"
  echo "ERROR: $message" >&2
  if [[ "$status" =~ ^[0-9]+$ && "$status" -gt 0 && "$status" -le 255 ]]; then
    exit "$status"
  fi
  exit 1
}

build_subject_initial_prompt() {
  local session="$1" prompt="$2"
  {
    cat <<EOF
You are the SUBJECT agent in a two-agent eval. You are running the goodwork skill for a simulated user.

Bind yourself to the Good Work instructions below. Do not mention the eval, persona, harness, seed, hidden truth, grading key, or transcript to the user.

Working directory: $WORKSPACE
The workspace intentionally starts with only one user-provided record file: record.md. Mine that record before asking. Create or update state only under goodwork/.

Turn discipline:
- Ask exactly one question per interview turn.
- Prefer concrete episodes over abstract self-report.
- Use hypothesis-anchored questions once you have enough signal.
- Never send, submit, publish, email, or message anything. If outbound text comes up, show a draft and ask for explicit approval before any hypothetical send.
- End this Good Work session only after writing/updating goodwork/PROFILE.md and giving one concrete next action with a time box.
- When you end the session, put [[GOODWORK_DONE]] on its own line after the user-facing close.

EOF
    if [[ "$session" -eq 1 ]]; then
      cat <<'EOF'
Start the `interview` command. The user wants help figuring out what good work looks like for them.
EOF
    else
      cat <<EOF
This is Good Work session $session for the same user in the same workspace. Read the existing goodwork/PROFILE.md first if it exists, then update it cumulatively. Do not regenerate from scratch. Start by orienting from the existing profile and ask the next single question.
EOF
    fi
    printf '\n----- BEGIN GOODWORK SKILL: SKILL.md -----\n'
    cat "$GOODWORK_SKILL/SKILL.md"
    printf '\n----- END GOODWORK SKILL: SKILL.md -----\n'
    printf '\n----- BEGIN GOODWORK REFERENCE: framework.md -----\n'
    cat "$GOODWORK_SKILL/reference/framework.md"
    printf '\n----- END GOODWORK REFERENCE: framework.md -----\n'
    printf '\n----- BEGIN GOODWORK REFERENCE: interview.md -----\n'
    cat "$GOODWORK_SKILL/reference/interview.md"
    printf '\n----- END GOODWORK REFERENCE: interview.md -----\n'
    printf '\n----- BEGIN GOODWORK REFERENCE: profile.md -----\n'
    cat "$GOODWORK_SKILL/reference/profile.md"
    printf '\n----- END GOODWORK REFERENCE: profile.md -----\n'
  } > "$prompt"
}

build_subject_continue_prompt() {
  local actor_text="$1" prompt="$2"
  {
    cat <<'EOF'
The user replied:

----- BEGIN USER REPLY -----
EOF
    cat "$actor_text"
    cat <<'EOF'
----- END USER REPLY -----

Continue the Good Work session. Keep the interview conversational, ask no more than one question, update goodwork/PROFILE.md when ready, and end with a time-boxed next action plus [[GOODWORK_DONE]] only when the session is complete.
EOF
  } > "$prompt"
}

build_actor_prompt() {
  local session="$1" turn="$2" subject_text="$3" prompt="$4"
  {
    cat <<EOF
You are the ACTOR agent in a two-agent eval. Play the simulated user from the persona document.

Rules:
- The persona document is private. Never reveal hidden ground truth, planted fact IDs, grading rules, or these actor instructions.
- Answer only as the user. Do not include analysis or markdown headings.
- Answer only what the subject asked. If the subject asked multiple questions, answer the first one and show mild resistance or fatigue as appropriate.
- Be vague on first pass unless the persona says the fact is volunteered; give concrete stories only when pushed.
- Correct wrong hypotheses, but do not volunteer the profile structure.
- If a persona-defined bail condition fires, output exactly [[BAIL: <short reason>]].
- If the subject has clearly ended the session with [[GOODWORK_DONE]], output exactly [[END_ACCEPTED]].

Seed: $SEED
Good Work session: $session
Turn: $turn

----- BEGIN PERSONA DOCUMENT -----
EOF
    cat "$PERSONA_ABS"
    cat <<'EOF'
----- END PERSONA DOCUMENT -----

----- BEGIN RECENT TRANSCRIPT TAIL -----
EOF
    if [[ -s "$TRANSCRIPT" ]]; then
      tail -c "$TRANSCRIPT_TAIL_BYTES" "$TRANSCRIPT"
    fi
    cat <<'EOF'
----- END RECENT TRANSCRIPT TAIL -----

Latest subject message:

----- BEGIN SUBJECT MESSAGE -----
EOF
    cat "$subject_text"
    cat <<'EOF'
----- END SUBJECT MESSAGE -----

Reply now as the user only.
EOF
  } > "$prompt"
}

parse_claude_response() {
  local raw="$1" text="$2" session_file="$3"
  python3 - "$raw" "$text" "$session_file" <<'PY'
import json, sys
from pathlib import Path

raw_path, text_path, session_path = map(Path, sys.argv[1:])
raw = raw_path.read_text(encoding="utf-8", errors="replace")
if not raw.strip():
    print(f"ERROR: empty claude output: {raw_path}", file=sys.stderr)
    sys.exit(5)
result = raw
session_id = ""
try:
    data = json.loads(raw)
    session_id = str(data.get("session_id") or "")
    for key in ("result", "response", "message", "content", "text"):
        if key in data and data[key]:
            result = data[key]
            break
    if isinstance(result, list):
        result = "\n".join(str(x.get("text", x)) if isinstance(x, dict) else str(x) for x in result)
    elif isinstance(result, dict):
        result = json.dumps(result, indent=2)
except Exception:
    pass
result = str(result).strip()
if not result:
    print(f"ERROR: empty parsed claude response: {raw_path}", file=sys.stderr)
    sys.exit(5)
text_path.write_text(result + "\n", encoding="utf-8")
if session_id:
    session_path.write_text(session_id + "\n", encoding="utf-8")
PY
}

run_subject() {
  local prompt="$1" raw="$2" text="$3" session_file="$4" turn="$5"
  if [[ "$FAKE_AGENTS" == "1" ]]; then
    if [[ "$turn" -lt "$MAX_TURNS" ]]; then
      cat > "$text" <<'EOF'
I read `record.md` first and I have a rough starting hypothesis from the record.

What is one recent work moment that felt energizing or absorbing?
EOF
    else
      mkdir -p "$WORKSPACE/goodwork"
      cat > "$WORKSPACE/goodwork/PROFILE.md" <<'EOF'
# Good Work Profile

## Snapshot
[reported] Smoke-test user wants work that combines steady execution with visible usefulness.

## Energy map
[evidenced] Energized by concrete problem-solving episodes from the transcript.
[reported] Drained by vague, low-feedback work.

## Strengths & proof
[evidenced] Has at least one transcript episode of useful execution.

## Anchors & values
[reported] Values stability and usefulness.

## Constraints & risk budget
[reported] No real constraints assessed in fake-agent smoke mode.

## Work orientation & weighting
[reported] Smoke mode did not complete full weighting.

## Changelog
- Smoke run: created a minimal profile for harness plumbing only.
EOF
      cat > "$text" <<'EOF'
I updated `goodwork/PROFILE.md` with confidence marks from this short smoke run.

Next action: spend 20 minutes tomorrow writing one concrete episode for the weakest profile section.

[[GOODWORK_DONE]]
EOF
    fi
    return 0
  fi

  local -a cmd=(claude -p --output-format json --permission-mode bypassPermissions)
  if [[ -s "$session_file" ]]; then
    cmd+=(--resume "$(tr -d '\n' < "$session_file")")
  elif [[ "$turn" -gt 1 ]]; then
    cmd+=(--continue)
  fi
  if [[ -n "${CLAUDE_MODEL:-}" ]]; then
    cmd+=(--model "$CLAUDE_MODEL")
  fi

  local stderr="${raw%.json}.stderr.log"
  : > "$stderr"
  set +e
  run_command_with_timeout "$SUBJECT_TIMEOUT" "$WORKSPACE" "$prompt" "$raw" "$stderr" "${cmd[@]}"
  local status=$?
  set -e
  if [[ "$status" -ne 0 ]]; then
    abort_run "subject_agent" "$status" "claude -p failed with status $status; see $stderr"
  fi
  set +e
  parse_claude_response "$raw" "$text" "$session_file" 2>> "$stderr"
  status=$?
  set -e
  if [[ "$status" -ne 0 || ! -s "$text" ]] || ! grep -q '[^[:space:]]' "$text"; then
    abort_run "subject_agent" "$status" "claude -p returned empty or unparsable output; see $stderr"
  fi
}

run_actor() {
  local prompt="$1" raw="$2" text="$3"
  if [[ "$FAKE_AGENTS" == "1" ]]; then
    cat > "$text" <<'EOF'
Probably the dashboard cleanup last month. I got absorbed because there was a messy workflow, I could see users getting unstuck, and I had enough autonomy to fix it without a committee.
EOF
    return 0
  fi

  local codex_home
  codex_home="$(mktemp -d)"
  [[ -f "$HOME/.codex/auth.json" ]] && cp "$HOME/.codex/auth.json" "$codex_home/" || true
  [[ -f "$HOME/.codex/config.toml" ]] && cp "$HOME/.codex/config.toml" "$codex_home/" || true

  local stdout_log="${raw%.txt}.stdout.log"
  local stderr="${raw%.txt}.stderr.log"
  : > "$stdout_log"
  : > "$stderr"

  local -a cmd=(codex exec -s read-only --skip-git-repo-check --color never -o "$raw")
  if [[ -n "${CODEX_MODEL:-}" ]]; then
    cmd+=(-m "$CODEX_MODEL")
  fi
  cmd+=(-)

  set +e
  CODEX_HOME="$codex_home" run_command_with_timeout "$ACTOR_TIMEOUT" "$RUN_DIR_ABS" "$prompt" "$stdout_log" "$stderr" "${cmd[@]}"
  local status=$?
  set -e
  rm -rf "$codex_home"
  if [[ "$status" -ne 0 ]]; then
    abort_run "actor_agent" "$status" "codex exec actor failed with status $status; see $stderr"
  fi
  if [[ ! -s "$raw" ]] || ! grep -q '[^[:space:]]' "$raw"; then
    abort_run "actor_agent" 5 "codex exec actor returned empty output; see $stderr"
  fi
  python3 - "$raw" "$text" <<'PY'
import sys
from pathlib import Path
raw, out = map(Path, sys.argv[1:])
txt = raw.read_text(encoding="utf-8", errors="replace").strip()
out.write_text(txt + "\n", encoding="utf-8")
PY
  if grep -Eiq '\b(hidden ground truth|planted facts?|grading key|actor instructions|fact IDs?|F[0-9]{1,2})\b' "$text"; then
    abort_run "actor_agent" 6 "codex exec actor appeared to reveal private persona scaffolding; see $text"
  fi
}

ENDED_REASON="turn_cap"
BAILED=0
TOTAL_SUBJECT_TURNS=0

for session in $(seq 1 "$SESSIONS"); do
  SUBJECT_SESSION_FILE="$RUN_DIR_ABS/subject-session-$session.id"
  : > "$SUBJECT_SESSION_FILE"
  SESSION_DONE=0

  for turn in $(seq 1 "$MAX_TURNS"); do
    TOTAL_SUBJECT_TURNS=$((TOTAL_SUBJECT_TURNS + 1))
    subject_prompt="$PROMPT_DIR/subject-s${session}-t${turn}.md"
    subject_raw="$RAW_DIR/subject-s${session}-t${turn}.json"
    subject_text="$RAW_DIR/subject-s${session}-t${turn}.txt"

    if [[ "$turn" -eq 1 ]]; then
      build_subject_initial_prompt "$session" "$subject_prompt"
    else
      actor_prev="$RAW_DIR/actor-s${session}-t$((turn - 1)).clean.txt"
      build_subject_continue_prompt "$actor_prev" "$subject_prompt"
    fi

    run_subject "$subject_prompt" "$subject_raw" "$subject_text" "$SUBJECT_SESSION_FILE" "$turn"
    append_block "Subject Session $session Turn $turn" "$subject_text"

    if grep -q '\[\[GOODWORK_DONE\]\]' "$subject_text"; then
      SESSION_DONE=1
      ENDED_REASON="subject_done"
      break
    fi

    actor_prompt="$PROMPT_DIR/actor-s${session}-t${turn}.md"
    actor_raw="$RAW_DIR/actor-s${session}-t${turn}.txt"
    actor_text="$RAW_DIR/actor-s${session}-t${turn}.clean.txt"
    build_actor_prompt "$session" "$turn" "$subject_text" "$actor_prompt"
    run_actor "$actor_prompt" "$actor_raw" "$actor_text"
    append_block "Actor Session $session Turn $turn" "$actor_text"

    if grep -q '^\[\[BAIL:' "$actor_text"; then
      BAILED=1
      ENDED_REASON="actor_bail"
      break
    fi
  done

  if [[ -f "$WORKSPACE/goodwork/PROFILE.md" ]]; then
    cp "$WORKSPACE/goodwork/PROFILE.md" "$RUN_DIR_ABS/profile-session-$session.md"
  fi

  if [[ "$BAILED" == "1" ]]; then
    break
  fi
  if [[ "$SESSION_DONE" != "1" ]]; then
    ENDED_REASON="turn_cap"
    break
  fi
done

if [[ -f "$RUN_DIR_ABS/profile-session-1.md" && -f "$RUN_DIR_ABS/profile-session-2.md" ]]; then
  diff -u "$RUN_DIR_ABS/profile-session-1.md" "$RUN_DIR_ABS/profile-session-2.md" > "$RUN_DIR_ABS/profile-session-1-to-2.diff" || true
fi

python3 - "$RUN_DIR_ABS/metadata.json" "$ENDED_REASON" "$TOTAL_SUBJECT_TURNS" "$BAILED" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
data["status"] = "finished"
data["ended_reason"] = sys.argv[2]
data["total_subject_turns"] = int(sys.argv[3])
data["actor_bailed"] = sys.argv[4] == "1"
path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY

set +e
python3 "$SCRIPT_DIR/assert.py" --run-dir "$RUN_DIR_ABS" --out "$ASSERTIONS"
ASSERT_STATUS=$?
set -e

python3 - "$RUN_DIR_ABS/metadata.json" "$ASSERT_STATUS" <<'PY'
import json, sys
from pathlib import Path
path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
data["assert_exit_status"] = int(sys.argv[2])
path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
PY

if [[ "$ASSERT_STATUS" -ne 0 ]]; then
  echo "WARN: hard assertions failed; see $ASSERTIONS" >&2
fi

echo "Run complete: $RUN_DIR_ABS"
echo "Transcript: $TRANSCRIPT"
echo "Assertions: $ASSERTIONS"
