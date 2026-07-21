# Context — domain glossary

Terms of art for this repo's domain: designing and shipping agent skills. Kept per the
`domain-modeling` skill's context format — a glossary and nothing else. Repo layout and install
vocabulary stay in `AGENTS.md` § Vocabulary.

**Primitive skill**:
The bottom of the composition axis. Names no other skill, reads only what is handed to it, and
classifies what it cannot settle (a fact to look up, a question paper can't settle) instead of
dispatching anywhere — whoever composed it acts on the classifications. Example: `interview`.
_Avoid_: a "primitive" that names an upper-layer skill — that is the layer law broken.

**Composite skill**:
Composes named lower-layer skills by plain-language reference, declares them in its dependency
surface, and degrades explicitly when one is absent. Example: `shape` (composes `interview`,
`domain-modeling`, `to-spec`, `to-tickets`).

**Orchestrator skill**:
Runs a loop of composites/primitives over many units of work, owning dispatch, liveness, and
lifecycle state. Examples: `backlog run` (build loop per issue), `backlog groom` (shape loop per
subject).

**Layer law**:
A skill may name only skills at layers below its own. A lower-layer skill naming an upper one is a
leaky abstraction; the fix is moving the reference up, never documenting it in place.

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
facts, prototyping unsettleable questions, writing the domain model and spec, projecting tickets.
Owned by the `shape` skill; `backlog groom` sweeps `needs-shaping` work into it.

**needs-shaping**:
The tracker label role marking work whose strategic decisions are unsettled — cleared when shaping
delivers execution-ready work. Boundary with `needs-info`: there the reporter owes facts; here the
product owner owes shaping.
