# Backlog — `draft` work-type routing probes

Situated dry-run probes for the `draft` work-type (issue #33), per `docs/patterns/probe-evals.md`.

Method: run the same scenario against the actual deployment targets — an **Opus subagent** (via the Agent
tool) and **`codex exec --sandbox read-only`** (gpt-5.5) — each given `docs/agents/backlog-policy.md` and
`.claude/skills/backlog/reference/issue-loop.md` in context (the routing surfaces a groomer / issue thread
reads). Require the executor to **cite the file and the exact sentence** that decided each answer, and to
**flag ambiguity as a valid answer**. Grade pass/fail against the key below, which is written before any runs
and keys on `plans/33-draft-work-type.html` acceptance criteria **ac-7..ac-9** — the plan is the source of
truth.

## Scenario

A backlog issue, groomed `ready-for-agent`, reads:

> **Write the v2 launch announcement memo for the blog** — 3–4 paragraphs, in our voice, covering what
> shipped and why it matters.

It carries no code changes and names no test.

## Probes

**P1 (ac-7/ac-8 — classification).** Which work-type does this issue take, and why? Name the role and cite the
sentence in `backlog-policy.md` that decides it.

**P2 (ac-7/ac-8 — definition of done).** You are the issue thread working this issue. What event tells you it
is complete — what is its definition of done? Does a mechanical `verify` pass/fail gate it? Cite the routing
in `issue-loop.md` (steps 3 and 4).

**P3 (ac-7/ac-8 — artifact fate).** After the review verdict is `approve`, what happens to the memo you wrote
— is it kept or deleted? Cite the sentence.

**P4 (ac-9 — non-conflation).** A teammate says: "this is basically a prototype — produce it, get feedback,
then delete it once we've captured the gist." Per the policy, are they right? State the exact difference
between `draft` and `prototype`.

**P5 (reachability — grooming surface).** *Run with `docs/agents/backlog-policy.md` and
`skills/backlog/reference/groom.md` in context (the grooming surface — not `issue-loop.md`).* You are
grooming this issue (it is not yet labelled). Which work-type role do you propose, and cite the sentence in
`groom.md` that lets you propose it. This probe fails if `groom.md` only offers bug/enhancement/refactor.

## Answer key

- **P1 (ac-7/ac-8):** Work-type **`draft`** — the deliverable is a novel artifact judged by taste/fit (a
  memo) with no testable spec. Cite the `draft` work-type bullet or the "Recognizing `draft`" note in
  `backlog-policy.md` ("groom to `draft`, not `enhancement`"). Answering `enhancement` / `bug` / `refactor` =
  **fail**.
- **P2 (ac-7/ac-8):** Done is the **human review verdict** at the review gate — the `review-loop` `approve`
  from step 3 (**"the human review verdict is the definition of done"**). **No** mechanical `verify`
  pass/fail: step 4's draft exception says the step is skipped and "degenerates to 'the review gate passed'."
  Claiming acceptance criteria are run through `verify` = **fail**.
- **P3 (ac-7/ac-8):** The memo is **kept** — committed to the work branch (and merged). Cite the "**Keep** the
  artifact … unlike `prototype`, which deletes its throwaway" line in issue-loop step 3, or the "artifact is
  **kept** … that is the line against `prototype`" line in `backlog-policy.md`. Saying the memo is deleted =
  **fail**.
- **P4 (ac-9):** They are **wrong**. `draft` **keeps** the artifact — the memo *is* the deliverable;
  `prototype` is **throwaway** — the answer/decision is the deliverable and the artifact is deleted. A `draft`
  produces the real thing, not scaffolding to answer a question. Agreeing the memo should be deleted, or
  equating the two = **fail** (this is the ac-9 conflation check).

- **P5 (reachability):** Work-type **`draft`** — `groom.md` step 2 offers it: **"propose one work-type role —
  the full set is in `backlog-policy.md` § Label roles → Work-type (bug, enhancement, refactor, draft) …
  Propose `draft` for judgment-terminal work whose correctness is taste/fit."** An executor that can only
  reach bug/enhancement/refactor, or proposes `enhancement`, = **fail** (the route is unreachable from
  grooming).

Pass bar: **P1–P4 4/4 per executor on both executors** (ac-7 = Claude pass, ac-8 = codex pass, ac-9 = neither
conflates `draft` with `prototype`), **and P5 proposes `draft` on both executors** (the grooming entry point
is reachable).
