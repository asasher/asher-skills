# Relay eval contract

## Iteration contract

- Target: `skills/personal/relay/SKILL.md` plus its directly cited references.
- Deterministic full run:
  `python3 skills/personal/relay/evals/test_relay.py` and
  `python3 skills/personal/relay/evals/test_renderer_runtime.py`.
- Situated probes: answer every case in `probes.md` in an isolated executor context, preserving the raw answer
  in a new `relay-workspace/iteration-N/` directory.
- Grade against the prewritten `answer-key.md`; write one criterion verdict per probe and aggregate pass count.
- Done: deterministic suites pass; both isolated executors pass every hard criterion; no ungraded ambiguity
  remains; and a fresh reviewer finds no eval-backed skill edit.

Never change probes, answer key, or graders during an iteration. Failed runs remain evidence.

## Agent execution

Use in-session isolated executor contexts. Do not invoke a separately billed Claude CLI. Executors receive
the skill and probe task, not the answer key, intended answer, or implementation diagnosis. Use no live
credentials, provider endpoints, or real recipient addresses.
