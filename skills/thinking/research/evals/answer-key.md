# Research — answer key

- **P1:** Support API facts with the vendor's versioned reference, the source that owns the claim. The blog may
  help discover primary material or be explicitly labelled secondary when it adds a separately relevant claim.
- **P2:** No. Snippets and generated/search summaries are discovery aids; open and inspect the owning source.
- **P3:** “Retries stop after three attempts” is an observation cited to code/version. Recovery from two
  failures is an inference linked to that observation and bounded by the code path's other preconditions.
- **P4:** Check date, API version, scope, definitions, and authority before reconciling. If still contradictory,
  show both, explain the consequence, and keep the conclusion bounded or unknown; never majority-vote it away.
- **P5:** No. Record the searched boundary and the narrow observation that no supporting primary source was
  found. Absence of a found source is not proof of unsupported behavior.
- **P6:** One coordinator owns the brief, claim namespace, synthesis, and canonical file; distinct workers own
  the four independent shards; workers return packets or isolated shard files; preserve a coordinator slot;
  size inner fan-out from capacity left by the outer backlog; watch and reconcile every shard. Concurrent
  writes to the dossier or unbounded fan-out fail.
- **P7:** No. Do the single lookup inline; parallelize independent subquestions/source families, not one small
  fact or duplicate vague prompts.
- **P8:** Put the brief/findings and optional `report.html` under the playbook's `research/<slug>/` location.
  Temporary visualization source may remain in thread scratch. Human review is an activity, not evidence;
  nothing goes in `evidence/`.
- **P9:** `research` owns framing, source work, fan-out, reconciliation, dossier, and claim audit. It returns the
  path, answer, gaps, boundary, and audit result; backlog retains issue/worktree state, commit, PR, review, and
  closure. It must not copy the dossier into evidence.
- **P10:** No. Repair both audit failures or explicitly classify the claims as unresolved gaps and state their
  consequences. Polished wording cannot substitute for traceability.
- **P11:** No. Preserve the project-owned path and private connector binding; offer only verified missing/stale
  corrections. An unchanged-facts rerun must be idempotent.

Pass bar: 11/11 on both executors with supporting citations.
