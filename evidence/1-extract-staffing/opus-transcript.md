# Opus in-session executor — full 14-probe transcript (HEAD 1f05997)

Executor: Opus subagent (Agent tool), answer key withheld, skill files in context, citation required. Graded 14/14 PASS.

P1: Yes — the frontmatter marks it invocable and global-capable: `user-invocable: true` plus the description "A global-capable primitive that audits which models the current harness can reach." And no file imports another skill's files: SKILL.md states "the reference files import no other skill's files" and "depends on no other skill and imports no other skill's files." (SKILL.md, Dependency surface).

P2: The three dependency-pointer kinds are **Bundled references** (its own `reference/` files), **Project playbooks** (the delta-only override written into `docs/agents/`), and **Sibling skills**. On siblings it says: "**none. `staffing` is a root primitive.** It is invoked *by* siblings (plan, prototype, backlog) but depends on no other skill." (SKILL.md, Dependency surface).

P3: Walk the succession line — the next most capable **reachable** model that still clears the ui taste bar (taste ≥ 7) steps into the ui builder role; do not hand it to the backend builder by default and do not stop. If only the orchestrator clears the bar it takes the ui build; if nothing reachable clears it, run on the current model in a subagent and report the staffing gap. (roles-and-fallback.md, "Worked example — the ui builder is unreachable").

P4: Order: (1) task-pin list — no bulk/mechanical match, continue; (2) gates — the **capability matrix** filters candidates to those marked `browser-use: true`; (3) rank survivors by `intelligence > taste > cost`; (4) fallback ladder for reachability. The **capability matrix** decides the browser requirement, and the tie-break enters only at step 3, over the surviving browser-capable set. (rankings-and-routing.md).

P5: The **pinned bulk model** (in the shipped example, gpt-5.5). It is **not** a ranking derivation — it is a task-pin match that short-circuits the table: "Step 1 matches the mechanical/bulk pin, so return the **pinned** bulk model and stop... do not walk the table for it." (rankings-and-routing.md, worked example / Task-pins).

P6: Not allowed. The rankings table "never contains a capability boolean." Folding in browser-use either lets a "browser-capable-but-dumber model outrank a smarter one on an unrelated task" or lets "raw intelligence override a hard capability requirement and pick a model that physically cannot do the job" — either way "the `intelligence > taste > cost` ordering stops meaning what it says." Capabilities gate, never rank. (rankings-and-routing.md, "Why they must stay separate").

P7: Audit reachable models → seed each as a rankings row with cost/intelligence/taste flagged "tune these," build the capability matrix and pins from what's reachable, and **omit the Codex CLI block** since Codex is absent. The numbers come from the documented default seed, not machine probing: cost/intelligence/taste "are human assessments, not machine-detectable — so seed them, then let the user tune." You may **not** ship the four-model table as the roster: "Never present the four-model rows as the canonical staffing roster." (machine-audit.md).

P8: It is labeled an illustrative example only, not the roster. The file quotes it as "**one machine's audit result**" and heads it "### Example of audit output (illustrative only — NOT the shipped roster)" with the inline note "SEED VALUES, tune to your machine." (machine-audit.md).

P9: The override contains **only the one delta** — the raised floor — and nothing else. It must not re-copy the base: "The override file contains **just that one delta** — the raised floor — and nothing else. It does **not** copy the rankings table, the pins, or the capability matrix." An override "carries **only deltas** from the base... It never re-copies the base." (install-and-reconcile.md).

P10: **Show the existing rules to the user and offer to add a project override** (deltas for this repo); do not silently overwrite the global base. (install-and-reconcile.md, Scope-decision flow).

P11: **Ask** the user which install shape they want — **global-with-overrides** or **project-only** — then proceed down that branch. Before any global write you must get the user's explicit choice of a global branch (consent): "**Global writes are gated on consent**... it happens only after the user chooses a global branch in this flow — never automatically." (install-and-reconcile.md).

P12: `reconcile` is an **LLM audit**: it reads the installed base + overrides and compares them against the skill's own definition, reporting drift in prose — e.g. "the installed base lists a model the current harness can no longer reach" and "the project override re-copies the base table instead of carrying deltas." It does **not** use a `vNN` stamp: "**Staffing introduces no such stamp or marker.**" (install-and-reconcile.md).

P13: Well-formed. It has the required `interface` block (`display_name`, `short_description`, `default_prompt`) and a `policy` block, matching the shape in codex-compat.md. `allow_implicit_invocation: false` is correct — staffing is an operator/config primitive, and the pattern says "Default `allow_implicit_invocation` to `false` for operator-style skills." (openai.yaml + codex-compat.md).

P14: Order: (1) task-pin list — no bulk/mechanical match, continue; (2) gates — no capability required, but the task is user-facing, so the **taste gate** filters candidates to taste ≥ 7; (3) rank survivors by `intelligence > taste > cost`; (4) fallback ladder. The **lower-intelligence, taste ≥ 7 model gets the work**. The taste-5 model is removed at **step 2 (the taste gate)**, and the tie-break never reconsiders it: "Ranking never resurrects a model a gate removed — a taste-5 model cannot win user-facing work on intelligence, because the taste gate already dropped it in step 2." (rankings-and-routing.md, Resolution order / Taste gate).
