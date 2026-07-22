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
`backlog groom` (a shaping thread per `needs-shaping` subject), `backlog build` (a worktree-isolated
build subagent per ready ticket).

**Dispatch adapter**:
A primitive owning *how* work is dispatched, not what the work is: `to-thread` spawns named,
interactive, harness-native sessions the user attends; `to-subagent` spawns non-interactive
subagents with a wake path. Harness and staffing knowledge live only here — `to-subagent` is the
one skill permitted to name `staffing`; every other skill reaches models and wake paths solely by
saying "via `to-subagent`".

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
`to-tickets`.

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
`shape` skill, run in interactive threads the user attends; crystallising the settled direction
(`to-spec`, `to-tickets`) is the user's call inside the thread, not a shape step — after which the
thread watches the published tickets for AFK comments until the user blesses readiness. `backlog
groom` dispatches `needs-shaping` work into these threads.

**needs-shaping**:
The tracker label role marking work whose strategic decisions are unsettled — cleared when shaping
delivers execution-ready work. Boundary with `needs-info`: there the reporter owes facts; here the
product owner owes shaping.
