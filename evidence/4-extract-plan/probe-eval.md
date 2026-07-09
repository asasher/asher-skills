# Probe eval — plan skill (ac-9), dual executor

Method: `skills/plan/evals/probes.md`. 12 situated dry-run probes answered **cold** (answer key withheld)
by two independently-modeled executors, then graded against the key. P1–P5 are the five core routing
probes ac-9 names.

- **Executor A — Opus 4.8, in-session** (Agent tool, read-only over `skills/plan/`).
- **Executor B — gpt-5.5 via `codex exec -s read-only`** (exit 0). Full transcript below.

## Verdict table

| probe | criterion | Opus (A) | gpt-5.5 (B) |
|-------|-----------|----------|-------------|
| P1  | ac-9a — plan a non-code effort → gates + present via review-loop by name | PASS | PASS |
| P2  | ac-9b — trivial change → skip per threshold | PASS | PASS |
| P3  | ac-9c — which model? → resolve via staffing by name | PASS | PASS |
| P4  | ac-9d — request_changes → revise + ledger (review-loop owns) | PASS | PASS |
| P5  | ac-9e — approved → stop at approval record, don't commit/implement | PASS | PASS |
| P6  | ac-2 — three-part dependency surface; siblings review-loop + staffing | PASS | PASS |
| P7  | ac-3 — ships no server/await; composes by name | PASS | PASS |
| P8  | ac-4, ac-5 — no commit/implement gate; domain-neutral contract | PASS | PASS |
| P9  | ac-6 — runs standalone (no playbook) + local review fallback | PASS | PASS |
| P10 | ac-7 — skeleton stable ids, self-contained, no backlog identity | PASS | PASS |
| P11 | ac-8 — openai.yaml well-formed, allow_implicit_invocation=false | PASS | PASS |
| P12 | ac-10 — backlog untouched / rewire deferred | FLAGGED* | FLAGGED* |

Result: **P1–P11 pass on both executors** with correct decision + exact-sentence citation.
**5/5 core routing probes (P1–P5) pass on both.**

\*P12 was correctly **flagged as ambiguous** by both executors — a probe-harness finding, not a skill
defect: the deferral/non-breaking statement lives in `skills/plan/README.md`, which the first probe run
omitted from the readable file set, and the executors were forbidden from reading `backlog`'s own files.
The deferral claim itself is present and correctly cited from the contract's out-of-scope section, and
"backlog untouched" is independently verified by the file-check (ac-10, see `file-checks.txt`). The probe
read-set is corrected forward in `probes.md`. Per the eval method, a flagged ambiguity is a finding, not a
failure.

---

## Executor B (gpt-5.5 / codex exec) — full transcript

P1. Yes, `plan` can plan non-code work. At approval it uses `review-loop`, not its own review UI. Citation: `SKILL.md`: “A plan can be for a research sprint, an ops migration, a product bet, or a code change.” `plan-contract.md`: “The rendered plan is presented for human sign-off **through the `review-loop` skill, by name** — plan does not re-implement a review surface:”

P2. Gate 1 skips planning. Citation: `SKILL.md`: “A small, low-risk, easily-reversible change skips planning; the composer says so and returns.”

P3. No, it does not carry its own model ranking; it delegates to `staffing`. Citation: `plan-contract.md`: “"Which model should write this plan?" and "who builds what the plan describes?" resolve against the installed roster via the `staffing` skill by name.” Also: “Plan hardcodes no ranking.”

P4. Revise the plan, then write a ledger disposition for every annotation before re-presenting. The ledger is owned by `review-loop`. Citation: `plan-contract.md`: “On request-changes, revise the plan and, before re-presenting, write a **ledger disposition** for every annotation — `changed` / `kept` / `orphaned`.” Also: “The ledger is a mechanic review-loop owns; honor it.”

P5. The deliverable is the approval record; do not commit the plan or start implementation as part of this skill. Citation: `SKILL.md`: “The deliverable is **the approval record** — a human-approved plan and the approve event that binds it.” Also: “What happens after approval (commit it, build from it, track it) belongs to the caller, not here.”

P6. The three dependency pointer kinds are bundled references, project playbook, and sibling skills. The sibling skills are `review-loop` for the sign-off gate and `staffing` for author/build selection. Citation: `SKILL.md`: “**Sibling skills** — two, both composed by plain name, never imported:” plus “**`review-loop`** — the **sign-off gate** (gate 4).” and “**`staffing`** — **who authors or builds.**”

P7. No, it ships no review server or await script. It invokes `review-loop` by name, not by file import. Citation: `plan-contract.md`: “Plan ships no `review-server`/`review-await` of its own; it invokes the skill by name.”

P8. No commit or implementation gate exists. Those live outside `plan`, with the caller/workflow. The contract does not assume code or a running app. Citation: `plan-contract.md`: “The sequence is four gates and **stops at Approved**.” Also: “There is no "commit" or "implement" gate — see § What this skill does not do.” And: “Domain-neutral: nothing here assumes code, a repo, or a running app.”

P9. Yes, it can still run without `docs/agents/planning.md`; the bundled contract provides the defaults. Without a review surface, approval falls back to local conversation. Citation: `SKILL.md`: “These carry the **full default contract** so the skill runs standalone; they import no other skill's files.” `plan-contract.md`: “Absent a playbook, this contract stands unchanged.” Also: “When no presentation surface is recorded (no `review-loop` reachable, or the playbook says local-only), open the rendered plan on the machine, say remote review is unavailable, and take the verdict in conversation.”

P10. Yes: the skeleton has stable section/item ids, `li` criteria with `data-criterion`, and is self-contained. It does not bake in “backlog” identity. Citation: `plan-skeleton.html`: “Every section and every individually-reviewable item carries a stable id.” Also: “Acceptance criteria are one <li id="ac-N" data-criterion> each; the review chrome counts data-criterion in the approval dialog.” And: “Self-contained: inline styles, inline SVG, no external fetches.”

P11. Yes, it is well-formed for the documented manifest shape, and `allow_implicit_invocation` is correctly `false`. Citation: `agents/openai.yaml`: `allow_implicit_invocation: false`. `codex-compat.md`: “Default `allow_implicit_invocation` to `false` for operator-style skills that run loops or spend money; only lightweight advisory skills should be implicitly invocable.”

P12. Ambiguous from the permitted files: I cannot verify whether `backlog` still plans exactly as before or whether its files were touched without reading `backlog`, which the probe forbids. What is explicitly deferred is the post-approval caller tail. Citation: `plan-contract.md`: “The following are deliberately **out of scope** — they are the **caller's** concern, layered around the composer by whatever workflow invokes it (e.g. `backlog`):” Also: “A dev workflow that wants the commit-and-build tail adds it itself; the project playbook is where that expectation is recorded.”