# Refactor

Target: a module, surface, or issue calling for behavior-preserving change. Runs standalone or as the `refactor` branch of the loop.

The technique — locking behavior with tests and refactoring under that net — lives in `docs/agents/refactoring.md`; work that playbook end to end. If it is missing, report a setup gap and stop.

## Gates

1. **Locked** — the behavior that must not change is pinned by passing tests before any implementation changes.
2. **Green throughout** — the locked tests stay green at each step of the restructuring.
3. **Scope confirmed** — the diff is structural only, or any behavior change is explicitly called out and justified.

If the target structure is itself contested — more than one plausible shape, expensive to reverse — hand that question to `reference/prototype.md` before restructuring, and record the answer on the issue.

Standalone with a PR intended: continue to `reference/verify.md`, then `reference/evidence.md`.
