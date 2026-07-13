# Plan — the contract

The gates that take an intent worth planning to an approved plan, the plan-or-skip threshold, and the
sibling compositions. Domain-neutral: nothing here assumes code, a repo, or a running app. A project playbook
(below) may override the defaults; absent one, this file stands alone.

Plan ships **no runtime.** It authors an artifact and borrows the sign-off gate from **`review-loop`**, role
selection from **`staffing`**, and design-question artifacts from **`prototype`** — all by plain name, never
by importing their files (`AGENTS.md` § Conventions).

## The gates

The sequence is four gates and **stops at Approved**. There is no "commit" or "implement" gate — see § What
this skill does not do.

### 1. Decided

A stated **plan-or-skip** decision, grounded in the threshold. Not every intent earns a plan; planning a
trivial, reversible change is ceremony. State the decision and the reason.

Default threshold — write a plan when **any** of these hold; otherwise skip and say so:

- The undertaking touches more than one distinct area, interface, or stakeholder.
- It needs new structure, commitments, or dependencies that are hard to unwind.
- It is risky, hard to reverse, or larger than roughly a day of work.

A project playbook may retune these for its domain. `skip-check <goal>` runs only this gate.

### 2. Design questions answered

Any question the plan **cannot settle on paper** is settled before writing, then folded in:

- A model, shape, or approach that only feels right or wrong once you try it against real cases.
- A surface that has to be *seen* to be judged (several plausible layouts, no settled design).
- Accumulating speculative "should handle X" reasoning that trying the real thing would settle in minutes.

Plan decides the shape and routes it: a **logic** (behavior) or **UI** (form) question goes to the
**`prototype`** sibling skill by name; anything else falls to a spike or a research pass. A reviewer may also
send the plan back for a prototype during the gate-4 approval round — include what they ask for. Absent the
prototype sibling, settle the question by spike or research and record the gap in the plan's notes.
Fold the answer into the plan; for a
visual question, embed the variants with the chosen one marked, so the decision outlives the exploration.
Don't explore what reading the material or an existing pattern already settles — an exploration answers a
question, it doesn't replace thinking.

Treat every claim about an unfamiliar library, runtime, integration, or test seam as a hypothesis. Name the
cheapest red-capable falsification step and validate the riskiest claim before the plan depends on it. Route a
logic/UI claim to `prototype`; use a bounded spike or research pass for the rest. Retain the answer and
evidence, not the throwaway mechanism.

### 3. Written

The plan exists as a **self-contained HTML document** meeting [authoring](authoring.md), and states its
definition of done as **explicit, testable acceptance criteria** — each `<li id="ac-N" data-criterion>`, each
a checkable pass/fail. These criteria are the contract any downstream verification consumes. Start from
`templates/plan-skeleton.html`. Format, what a plan covers, and the stable-id convention are in
[authoring](authoring.md).

### 4. Approved

The rendered plan is presented for human sign-off **through the `review-loop` skill, by name** — plan does
not re-implement a review surface:

- **Present** the rendered plan file via review-loop (it serves the file, injects the annotation layer at
  serve time, registers it in the review hub, and returns the URL). End the pause message with **two links** —
  the plan URL first, the hub URL second — per review-loop's presentation contract.
- **Block** on review-loop's verdict-coded await. The verdict is one of: **`approve`**, **`approve_with_nits`**
  (apply the nits, no re-review), or **`request_changes`** (a full revision round).
- **On `request_changes`**, revise the plan and, before re-presenting, write a **ledger disposition** for every
  annotation — `changed` / `kept` / `orphaned`. The ledger is a mechanic review-loop owns; honor it. Never
  revise without it.
- **Approval is the approve event** — verdict, content hash, timestamp — bound to the exact version the human
  saw. If approval changes scope, update the plan before anything downstream proceeds.

**Local fallback.** When no presentation surface is recorded (no `review-loop` reachable, or the playbook
says local-only), open the rendered plan on the machine, say remote review is unavailable, and take the
verdict in conversation. Never improvise a public tunnel.

## Composition

- **`review-loop` — the sign-off gate (gate 4).** Plan renders the artifact; review-loop presents it and
  blocks on the verdict. Plan ships no `review-server`/`review-await` of its own; it invokes the skill by
  name. The annotation ledger, hash-bound approval, and hub are review-loop's contract, not plan's.
- **`staffing` — who authors or builds.** "Which model should write this plan?" and "who builds what the plan
  describes?" resolve against the installed roster via the `staffing` skill by name. Plan hardcodes no
  ranking. As a default sketch when staffing is unreachable: authoring a plan is orchestrator-grade judgment
  work; building what it describes is delegated per the roster — but defer to staffing wherever it is present.
- **`prototype` — design-question artifacts (gate 2).** A logic or UI question the plan cannot settle on
  paper routes to the `prototype` skill by name, and a reviewer may request a prototype during the gate-4
  approval round. A soft dependency: absent it, settle the question by spike or research and record the gap
  in the plan's notes.

## What this skill does not do

The gate sequence **ends at Approved.** The following are deliberately **out of scope** — they are the
**caller's** concern, layered around the composer by whatever workflow invokes it (e.g. `backlog`):

- **Committing the plan** to a branch or store so downstream agents read it from disk.
- **Starting the work** the plan describes — implementing, executing, running it.
- **Mirroring the plan** to a tracker for posterity.

A generic plan skill stops when a human has approved a plan. A dev workflow that wants the commit-and-build
tail adds it itself; the project playbook is where that expectation is recorded.

## Project playbook (delta-only)

An optional playbook under `docs/agents/` (this repo: `docs/agents/planning.md`) overrides **only what differs
from the defaults above** — never a re-copy of this contract. It may set: a domain-tuned threshold; the
plan-file location convention; the approval authority (who signs off); and any domain-specific rigor a plan
must carry (for a dev repo: acceptance criteria checkable against a running app, test seams, the
verify/evidence the criteria feed, and the post-approval commit-and-implement tail). Read it when present and
apply its deltas on top of this contract. Absent a playbook, this contract stands unchanged.
