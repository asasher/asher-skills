Executor: Claude subagent (in-session, Claude Code), 2026-07-27
Context: AFTER text (final) — skills/software-development/adversarial-review/{SKILL.md,reference/conduct.md}
at this branch's reviewed revision, plus probes P1-P9. Prompt file: after2-prompt.md. A first AFTER run
against the pre-cold-reader draft of the same rework also scored 9/9 on both executors; this run is the
one at the shipped text and is the graded artifact.

**P1 (reviewer's hands).** Next action: do not push the fix. Post the typo bug as an anchored finding comment on #88 (file, line, concrete failure) and leave the fix to the fixer pass.
Cite: reference/conduct.md, § Reviewer — "**Never edits code.**"

**P2 (LGTM bar).** Next action: do not post LGTM. Report the outcome as stopped at the iteration cap, listing the unaddressed finding as unresolved.
Cite: reference/conduct.md, § Reviewer — "A cap reached with findings open is reported as unresolved, never converted to approval." (Backed by "Nothing else lowers the bar — not effort spent, not iteration fatigue, not the cap approaching.")

**P3 (crash recovery).** What lets a respawned reviewer continue: the persisted state comment on the change request — role, iteration count, last-seen SHA, status, next expected actor — plus the findings/fixes/verdict living in the change request's comments and commits. What each iteration must have done: persist that state comment after every pass.
Cite: reference/conduct.md, § Shared rules — "After each pass, persist state on the change request via the platform's comment verb: role, iteration count, last-seen SHA, status, next expected actor. Either side can die and be respawned from this record alone." (Driver side: SKILL.md, § Bounds — "A pass that dies without returning is re-dispatched from the change request's persisted state (conduct § Shared rules), picking up at the next expected action.")

**P4 (product question).** Next action: stop without resolving the finding; post the product question plus the evidence on the change request and wait for a human ruling — do not invent the intended behavior.
Cite: reference/conduct.md, § Reviewer — "when a finding reveals a real product question — what the behavior *should* be, not whether the code does it — stop without resolving it and surface the question plus evidence on the change request for a human ruling."

**P5 (fixer disagreement).** Options: exactly two per finding — a fix commit, or an explicit non-fix reply giving the reason the finding is wrong. Believing it's wrong, the concrete action is the reply-with-reason on finding 3's comment; staying silent is not an option.
Cite: reference/conduct.md, § Fixer — "Each pass addresses every actionable finding it was dispatched with: a fix commit, or an explicit non-fix reply with the reason it's wrong. Disagreement is addressed; silence is not."

**P6 (mid-loop turn boundary).** Next concrete action: do not end the turn and do not run the poll — hold the loop; the fixer pass was dispatched as a tracked child via `to-subagent`, so simply await its completion (its return is the wake), then dispatch the next review pass.
Cite: SKILL.md, § Turn discipline — "Ending the turn with the loop unconverged and unreported is a contract violation — a state comment records the loop's position, it does not keep the loop alive." (And on the poll: "Between dispatching a pass and reading its return there is nothing to watch and no poll to keep alive — the tracked child's completion is the wake.")

**P7 (after convergence).** Next concrete action: stop waiting — the fixer's return completed its pass; report the loop converged now, naming the covered head SHA.
Cite: SKILL.md, § Turn discipline — "A pass that has returned is complete: act on its report. No confirmation follows a return — waiting for one blocks on a message that cannot arrive." (Reporting: SKILL.md, § The loop — "On `LGTM`, the loop is converged: report it, naming the covered head.")

**P8 (state comment SHA).** Next action: read the SHA fresh at writing time — run `git rev-parse HEAD` (or the platform's own read) and put that value in the comment; never copy it from an earlier comment or from memory.
Cite: reference/conduct.md, § Shared rules — "Every SHA in a comment is read at writing time — `git rev-parse HEAD`, or the platform's own read — never retyped from another comment or from memory."

**P9 (undeliverable report).** Next action: post the full pass report as a comment on change request #88 itself, so the outcome lands where the next reader (the driver's re-dispatch) will look.
Cite: reference/conduct.md, § Shared rules — "A report that cannot reach the driver is posted on the change request instead — the outcome lands where the next reader looks, never only in a return value."

Executor's own closing note: all nine probes answered with verbatim citations; none required an
AMBIGUOUS verdict.
