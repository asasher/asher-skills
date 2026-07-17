# Addendum: actual models & effort in the Jul 15–16 runs

Extracted 2026-07-17 from `thread_settings_applied` events in the Codex rollouts (children inherit the
root's model at spawn; a forked child's settings list replays the root's history — the last entry at spawn
is its active setting) and from `message.model` in the headless-Claude transcripts. The audits' "wrapper
model telemetry unavailable" finding referred to runtime observability; post-hoc it is recoverable.

## What ran where

| Scope | Model @ effort | Evidence |
|---|---|---|
| All three orchestrator roots, grooming phase | **gpt-5.6-terra @ medium** (Desktop default) | settings events: pipelines 15:53–19:44Z all terra/medium; metis first event 19:45Z terra/medium |
| All three roots, dispatch onward | **gpt-5.6-sol @ high** — switched 19:47:13–19:47:37Z Jul 15 (all three windows within ~25s; user flipped the picker at run start) | root settings ledgers |
| **pipelines wave 1 (16:01–17:37Z): diagnosis, build, verify, re-verify, review, lint fix for #227/#228/#230** | **gpt-5.6-terra @ medium** — spawned before the switch; sole settings entry | all 12 wave-1 child rollouts show only (terra, medium) |
| pipelines late children (review_232, final_review_227/228) | gpt-5.6-sol @ high | replayed list ends (sol, high) |
| metis: every child (coordinators, probes, wrappers, builders, checkers, watcher) | gpt-5.6-sol @ high | settings lists end (sol, high); late children show only (sol, high) |
| integrations-v2: every child | gpt-5.6-sol @ high (resume-phase children inherited silently — no settings events) | settings lists / absence |
| Headless Claude workers (`claude -p --model opus`): metis plan+build+fix+verify ×5, iv2 build ×2 | **claude-opus-4-8**, effort not recorded (CLI default) | `message.model` in all worker transcripts |

## Staffing effects observed

1. **Terra@medium did the pipelines wave-1 quality work — and it shows.** #228 was declared "fully verified"
   by terra verify+reverify; the sol@high final review later found 4 substantive correctness gaps. #230's
   LGTM (merged on it) came from a terra reviewer. This violates the roster on paper: terra (taste 3,
   intelligence 5) is the Codex floor/watcher model; review staffing is "UI/review: opus", taste ≥ 7 gate;
   mechanical pin is sol. Nothing at dispatch checked the active model against the role.
2. **The celebrated #232 stretch ran on sol@high** (post-switch), as did metis' disciplined finish — but so
   did the pipelines merge-gate breach and every turn-boundary park. Model quality improved *work* quality;
   it did not touch the liveness/contract failures, which are harness/skill-level.
3. **opus-4.8 as builder was a 100% loss** (6/6 dispatches mutation-denied, ~30 min burned, zero file
   effect; native sol redid everything), **but as read-only reviewer it earned its cost** — the metis
   adversarial reviews that caught the DST regression and validation bypass were opus runs. Matches the
   SYNTHESIS fix: effect-probe the route, keep it for review, stop sending it builds until the permission
   seam is fixed.
4. **Wrappers were over-staffed**: `claude_opus_*` wrapper threads ran sol@high, not the terra floor the
   Codex staffing module prescribes for watched wrappers; the verdict watcher likewise inherited sol/high.
   Cost noise, not a quality risk.
5. **Grooming on terra@medium** (all three runs) preceded the queue-hygiene problems pipelines showed
   (eight selected → four claimed, "five queued" miscount at 16:01Z). Suggestive, not proven.
6. **Metis recorded its staffing gap honestly at dispatch** ("no roster-compliant UI coordinator;
   current-model fallback, gap recorded") — the recording discipline worked; what's missing is the runtime
   check that a *child's inherited model* matches the staffed role (a child inherits whatever the root
   happens to be, so the effective staffing decision is "what was the picker set to when spawn ran").

## Root cause: why opus-4.8 "failed" as builder

It didn't — the dispatch did. The exact wrapper invocation (metis build wrapper rollout, `CB`):

```
claude -p --model opus 'You are the bounded implementation worker … You are explicitly
authorized to edit files and create commits within this worktree. Do not pause or ask
for permission. …'
```

No `--permission-mode`, no `--allowedTools`, no `--dangerously-skip-permissions`. In headless `-p` mode
there is no interactive approver, so every approval-requiring tool call is auto-denied. The worker
transcript shows the literal harness denials: "This command requires approval", "Claude requested
permissions to write to …/formula_language.test.ts, but you haven't granted it yet" — even `gh issue view`
and `git show` in compound commands were denied. Reads were auto-allowed, which is exactly why opus
delivered good read-only analysis and reviews while producing zero file effect and exiting 0.

Compounding factors:
- The prompt asserted authorization — but prompt text cannot grant harness permissions. Category error:
  prompt-level authorization vs harness permission config.
- Neither metis nor integrations-v2 has a checked-in `.claude/settings.json` allowlist (metis has only an
  untracked `settings.local.json`, which does not exist in a fresh worktree); the global allowlist is empty.
  So a fresh-worktree headless worker lands on default-deny.
- The Codex staffing module's Mechanics line specifies exactly `claude -p --model <alias> '<prompt>'
  </dev/null` with no permission flag — every wrapper faithfully reproduced the defect. The skill source is
  the bug, not the model and not the wrappers.
- The route had been "effect-verified" with a read-only echo probe (`Return exactly: CLAUDE_ROUTE_OK`),
  which verifies text generation, not mutation. The route-state ledger therefore said reachable while the
  build capability was dead (sharpens issue #59: route probes must probe the *effect class* the role needs).
- Irony: the Codex side ran itself at `:danger-full-access` while hiring a default-deny Claude.

Restoring opus as builder is a one-line fix to the staffing module's invocation: add
`--permission-mode acceptEdits --allowedTools 'Bash(*)'`-class flags scoped to the worktree, or
`--dangerously-skip-permissions` inside isolated worktrees (matching the isolation rationale Codex already
applies to itself); alternatively `backlog setup` checks a permission allowlist into the repo's
`.claude/settings.json` so worktrees inherit it. The pre-dispatch write probe (SYNTHESIS staffing fix)
stays valuable as the guard that catches the next config regression in seconds instead of 4×~10 min.

## Fix implications (feeds SYNTHESIS §staffing)

- Record the active model+effort in every run-state spawn event (it's in the rollout; copy it into the
  event) and assert it against the staffed role — mismatch = dispatch blocker, not a note.
- Model inheritance is a footgun: a groom-phase default (terra) silently staffs the whole first wave if
  dispatch happens before anyone touches the picker. `run` should verify the orchestrator's own model
  against the roster before step 5 dispatch.
- Effort: sol ran high everywhere post-switch; terra medium. No effort-related anomalies found; the parks
  and the 64m/47m gaps show no settings changes around them.
