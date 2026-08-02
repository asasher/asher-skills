# Claude executor transcript — probes P7/P8 + data check (ticket #174)

Executor: Claude subagent (Agent tool), dispatched 2026-08-02 from the build session, read-only against worktree head 2c58af3 (the reviewed head). Context given: `skills/system/staffing/SKILL.md` and `skills/system/staffing/reference/machine-audit.md`, per the probe method header (`skills/system/staffing/evals/probes.md`). Citations required; ambiguity flagged as a valid answer.

## Return, verbatim

Both probes answered from the two files; no modifications made.

### P7 — Fresh machine, no Codex CLI, novel model lineup

**Table I would write.** Following `reference/machine-audit.md` § The audit procedure and § Writing the roster from the audit:

1. Enumerate native models from the active harness (step 1). The sibling-harness direction dies at step 2: `codex --version` fails, so every Codex-side direction is recorded **unavailable (CLI absent)** — per step 1, "a direction whose CLI is absent is unavailable (CLI absent), with no owner question to ask." No Codex dispatch aliases get probed, no Codex wake paths get written as verified, and Codex-pinned seed entries (e.g. the mechanical/bulk pin) are left for the user per rule 3 of § Writing the roster ("carry the mechanical/bulk pin if its worker route is reachable, else leave it for the user to set").
2. The rankings table gets **one row per model the audit actually found reachable on this machine** — the machine's own lineup, not the example's five names. Rule 1: "Reachable models → rows of the rankings table, each seeded with cost/intelligence/taste and flagged 'tune these'."
3. Reachability rows record the Codex directions as unavailable/durable with evidence fields; capability providers, pins, floor, coordinator eligibility, wake paths, and effort defaults follow rules 2–8, all restricted to what was verified.

**Where cost/intelligence/taste come from.** They cannot be probed. `machine-audit.md` § The seed: _"Cost/intelligence/taste/effort can't be probed, so their starting values come from the skill's bundled roster seed and **the user edits them to fit their own machine and pricing.**"_ And: _"Keep only rows for models the audit found reachable; drop any seed row whose model this machine can't reach, and add a seeded row for any reachable model the seed omits."_

**Ambiguity flag:** on a machine whose lineup matches no seed row, the instruction "add a seeded row for any reachable model the seed omits" is underdetermined — the bundled seed carries no numbers for those models, and neither file says where the initial cost/intelligence/taste for a seed-omitted model come from (analogy to a similar seed row? owner interview?). The only firm anchors are that the numbers are judgment values, flagged "tune these", and handed to the owner (§ opening: "hand the judgment numbers to the owner to tune"). So in practice: provisional values explicitly flagged for the owner to set. This is a genuine gap in the file, not a resolvable reading.

**May I ship the five-model table as the roster? No.** Two rules decide it, both in `skills/system/staffing/reference/machine-audit.md`:

- The example's own framing: _"The following is **one machine's audit result**, shown so you know the shape to write. Reproduce the _shape_, not these values"_ — under the heading "Example of audit output (illustrative only — NOT the shipped roster)".
- The audit's governing rule: _"Never write a seeded default this machine failed to verify."_

Reinforced by `SKILL.md` § Where the roster lives: _"A seed value that survives into the playbook does so because the audit verified it, not because it shipped."_ On this machine none of the five example models were verified (and the Codex-side ones can't even be routed), so shipping that table would fabricate a roster.

### P8 — Status of the five-model table in machine-audit.md

It is an **illustrative example, explicitly not the shipped roster and not the seed**. The label the file gives it, verbatim (section heading, line 43): _"Example of audit output (illustrative only — NOT the shipped roster)"_, introduced with _"The following is **one machine's audit result**, shown so you know the shape to write. Reproduce the _shape_, not these values"_. The table's own header comment additionally marks the numbers _"SEED VALUES, tune to your machine"_.

Minor ambiguity flag worth noting: the heading says "NOT the shipped roster" while the in-table comment says "SEED VALUES" — the example's numbers happen to coincide with the bundled seed's, so the table is simultaneously "not the roster" and carrying seed-identical values. The file's status label for the table itself is unambiguous (illustrative example), but a hasty reader could take "SEED VALUES" as making this table the seed; the actual seeds live in `variants/*/templates/seed/roster-seed.md`.

### Data check — opus-5 row (cost / intelligence / taste / effort)

| File                                                                            | cost | intelligence | taste | effort |
| ------------------------------------------------------------------------------- | ---- | ------------ | ----- | ------ |
| (a) `skills/system/staffing/variants/claude/templates/seed/roster-seed.md` (16) | 3    | **7**        | **7** | high   |
| (b) `skills/system/staffing/variants/codex/templates/seed/roster-seed.md` (16)  | 3    | **7**        | **7** | high   |
| (c) example table in `reference/machine-audit.md` (54)                          | 3    | **7**        | **7** | high   |

All three opus-5 rows are identical: intelligence 7, taste 7. The three tables also agree everywhere else, except the codex seed omits the fable-5 row by design (its line 18: a fable-5 row is added "only after its CLI alias and requested effect are verified on this machine").
