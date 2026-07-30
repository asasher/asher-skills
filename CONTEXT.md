# Context — domain glossary

Terms of art for this repo's domain: designing and shipping agent skills. Kept per the
`domain-modeling` skill's context format — a glossary and nothing else. Repo layout and install
vocabulary stay in `AGENTS.md` § Vocabulary.

**Primitive skill**:
The bottom of the composition axis, and **sealed**: it names no other skill and never addresses
"the caller" — its text reads complete to an agent that knows nothing about what composed it. It
reads what is handed to it plus the environment (repo playbooks are environment, not caller), and
classifies what it cannot settle instead of naming who settles it. Example: `domain-modeling`.
_Avoid_: a primitive that names a sibling, an upper layer, or "whoever composed this" — all three
break the seal.

**Composite skill**:
Composes named lower-layer skills by plain-language reference, declares them in its dependency
surface, and degrades explicitly when one is absent. All composition knowledge lives here: the
composite knows its parts' contracts, the parts know nothing back. Example: `shape` (composes
`interview` and `domain-modeling`, dispatching `research` and `prototype` through `to-subagent`).
Even a thin edge makes a composite: `interview` names only `to-subagent` for fact lookups, and that
one edge moves it off the primitive rung.

**Orchestrator skill**:
Runs a loop over many units of work, owning dispatch, liveness, and lifecycle state. A
**dispatcher** is the thin case: it only fans units out and supervises. Human-in-the-loop work goes
to threads the user attends (`to-thread` — no result flows back); autonomous work goes to subagents
the dispatcher babysits (`to-subagent` — completion wakes it, outcomes are relayed). Examples:
`backlog groom` (a shaping thread per user-confirmed batch), `backlog build` (a worktree-isolated
build subagent per ready ticket).

**Dispatch adapter**:
A primitive owning *how* work is dispatched, not what the work is: `to-thread` spawns named,
interactive sessions the user attends through the outermost dispatching harness; `to-subagent`
spawns non-interactive subagents with a wake path. Both consume an exact supplied directory and
never infer or add isolation. Harness and staffing knowledge live only here — `to-subagent` is the
one skill permitted to name `staffing`; every other skill reaches models and wake paths solely by
saying "via `to-subagent`".

**Worktree primitive**:
The project-owned mechanical boundary for prepare, inspect, and remove. It creates one branch and
working copy from a named base without switching or updating the primary checkout, treats git's
worktree registration as ownership truth, and refuses ambiguous reuse or dirty removal. Orchestrators
decide *when* isolation is required and pass the resulting directory to dispatch adapters; harnesses
do not create another worktree.

**Layer law**:
A skill may name only skills at layers below its own — and a primitive names none at all. A
lower-layer skill naming an upper one is a leaky abstraction; the fix is moving the reference up,
never documenting it in place.

**Redundant negation**:
A prohibition on behavior no reader would otherwise assume ("this skill writes no durable
artifacts"). It is noise and a leakage tell — meaningful only to an author remembering a design
where the behavior existed. A prohibition earns its place only against demonstrated drift ("never
modify the source spec" stays; "records nothing durable" goes).

**Pure skill**:
The bottom of the persistence axis: writes nothing durable — its output lives in the conversation
and whatever the composer captures. Example: `interview`.

**Effectful skill**:
Writes durable artifacts (documents, tickets, code) but keeps no resume state of its own. Example:
`to-slices`.

**Stateful skill**:
Its durable artifacts double as resume state: a bare invocation reads them and continues exactly
where the last session stopped — no human recap. State lives with the work, never in chat context
or memory files; a session's last act is updating it. Examples: `backlog`, `shape`. Stateful skills
get extra probe-eval attention on the resume-after-a-gap path, since mistakes compound across
sessions.

**Agent decision vs shipped script**:
The two kinds of behavior a skill ships. Agent decisions are prose-guided judgment (routing, wording,
what to ask); shipped scripts are deterministic mechanics (atomic writes, hashing, serving). Keep
each on its side: never script a judgment call, never leave failure-prone mechanics to prose.

**Shaping**:
The stage between raw intent and execution-ready work: interviewing the decisions, researching
facts, prototyping unsettleable questions, maintaining the domain model as terms land. Owned by the
`shape` skill, run in interactive threads the user attends — one engine per subject, interview
rounds combined across the batch. The spec is shaping's exit: a settled subject crystallises via
`to-spec` automatically, the spec landing on its ticket (body canonical, diagram first); the thread
then watches the spec'd tickets for AFK comments until the user blesses readiness. Splitting a
spec'd ticket (`to-slices` parenting it, as capstone, over born-shaped child slices) happens only on
the user's explicit approval. `backlog groom` dispatches shaping work into these threads.

**Slice / tracer bullet**:
The unit `to-slices` cuts a decided direction into. A **slice** is vertical — a narrow-but-complete
path through every layer the change spans, demoable on its own; a **tracer bullet** is the sizing
discipline on top: one fresh context window. The anti-pattern is the horizontal layer ("all the
models"), which can't be demoed alone. The one exception is the wide refactor — mechanical and
high-blast-radius — sequenced expand → migrate-in-batches → contract instead.

**Capstone**:
The work-type a spec'd ticket converts to when `to-slices` splits it: the parent of the slices,
holding the spec they deliver in installments. Undispatchable while any child is open — the
parent/child relation itself carries the block (the backlog policy's open-children rule), never
per-slice edges — and its terminal work is the coverage check: verify the delivered children against
the spec, file gaps as new children (re-blocking it), close on a clean pass. Replaces the old
supersede semantics, which killed the parent and with it the accountability for the whole.

**Capture**:
The `to-backlog` move: sweep a conversation's loose items — bugs, ideas, follow-ups that aren't the
conversation's deliverable — into minimal tickets, work-typed (a fact the live chat knows) but
carrying no readiness role (routing is grooming's judgment), each preserving its chat context.
Capture is N undecided things into the intake queue; the opposite move — one decided thing into
ordered parts — is `to-slices`.

**Repo context files**:
The repo-owned strategic context a shaping session reads at intake: `CONTEXT.md` (the domain
glossary), plus `PRODUCT.md` and `DESIGN.md` where they exist. They carry domain and direction;
playbooks under `docs/agents/` carry operational bindings — a shaping decision consults the former,
a build step the latter.

**Subject / batch**:
The two grooming units. A **subject** is the decision unit: one ticket, or tickets whose decisions
interlock — it gets one shaping engine, never two. A **batch** is the attention unit: related
subjects sized to one thread — `backlog groom` proposes the batches and spawns nothing until the
user confirms the plan. Every approved batch, including a single batch, gets one interactive thread
and one project-owned worktree. Its readiness transition is atomic across the batch and waits for
that worktree's clean removal or its shaping change's verified merge and cleanup; a changed head is
presented before the readiness signal that authorizes it.

**needs-shaping**:
The tracker label role marking work whose strategic decisions are unsettled — cleared when shaping
delivers execution-ready work. Boundary with `needs-info`: there the reporter owes facts; here the
product owner owes shaping.
