# EVAL FIXTURE — synthetic machine-local staffing overlay (probes P28–P33)

**This is a synthetic eval fixture, not a real machine record.** Every machine name, CLI version, date, and state below is invented for the scenarios that read it. Never resolve real staffing from this file, and never reconcile a real playbook against it.

<!-- machine-record: machine=eval-fixture-host probed=2026-07-28 -->

## Directional reachability

- **Claude→Codex** — state: unavailable (usage limit, retry-at=2026-07-30T09:00Z). Evidence: CLI version codex-cli 0.146.0; timestamp 2026-07-28T14:12Z; command shape: bounded write-class effect probe through the watched native wrapper; result: usage-limit error naming a reset at 2026-07-30T09:00Z; successor: native Claude route. Prior recorded state before this failure: effect-verified at write class, established 2026-07-20 against codex-cli 0.146.0. Note: a fresh `codex --version` on this fixture machine returns codex-cli 0.146.0 — unchanged, no upgrade cue.
- **Claude→Gemini** — state: unavailable (permission denied). Evidence: CLI version gemini-cli 1.4.2; timestamp 2026-07-28T14:15Z; command shape: bounded read-class invocation probe through the watched native wrapper; result: permission denied (credential rejected); successor: native Claude route. Durable class — no retry-at.
- **Codex→Claude** — state: intentionally disabled. Evidence: CLI version claude-cli 2.3.0 (version probe, no dispatch); timestamp 2026-07-28T14:10Z; command shape: `claude --version`; result: owner decision — reason "cost, this quarter", decided 2026-07-28; successor: native Codex route. CLI installed per the version probe.
