# The catalog — what to install, and the rules that bind it

Which skills fit which project and the hard invariant that every install comes from this repo only. Canonical
invocation, execution, required-sibling, optional-sibling, setup, and internal-hold declarations live under
`metadata` in each source `SKILL.md`; [`catalog.json`](catalog.json) is their generated snapshot. Internal
roots are cataloged for audit but cannot be selected or required by a public skill. Validate a
self-host checkout with `python3 skills/system/setup-asher-skills/scripts/catalog.py validate --root . --snapshot
skills/system/setup-asher-skills/reference/catalog.json` before using the snapshot.

## Pull only from this repo

**Every skill setup installs comes from `https://github.com/asasher/asher-skills` — the slug `asasher/asher-skills`
— and nothing else.** Every `npx skills add` command this skill emits targets that endpoint — or, in the
self-host case ([interview](interview.md) Phase 4), the same repo's own root as a local source: the identical
source at a local address. setup **never installs, recommends, or emits an install command for a skill from
any other host or account** (not `mattpocock/*`, not any vendor repo, not a gist).

The reason is a design stance, not a limitation: good ideas from elsewhere are **brought in, adapted, and
shipped here as our own** (for example `to-spec` is our adaptation of Matt Pocock's `to-spec`). So when a user
asks for an external skill by name — "install the TDD skill" — the move is: **offer our adapted equivalent if
we ship one, or say plainly that we don't ship it. Never reach out to the external repo.** If we have no
equivalent, that is an honest answer, not a reason to break the invariant.

## By project type — the recommendation seed

Recommend from this map, then confirm each choice one decision at a time ([interview](interview.md) § Phase 2).
The map is a starting point tuned by the project answer, not a fixed bundle.

| Project is for… | Recommend | Why |
|---|---|---|
| A shipping product / app repo, ongoing work | `backlog` (pulls its full closure) | The issue→reviewed-PR loop; brings diagnosis, plan, prototype, review-loop, staffing |
| A one-off feature or decision that needs sign-off | `plan` (requires review-loop + staffing; offer prototype for unresolved design questions) | Reviewed plan with an approval gate, no full backlog machinery |
| A design/state question that needs to be tried | `prototype` (pulls review-loop + staffing) | Throwaway artifact that settles one question |
| A greenfield product to pitch/sell | `maquette` (pulls review-loop) | High-fidelity clickable prototype for a demo |
| Turning a decided conversation into a written spec | `to-spec` (review-loop optional) | Synthesize a spec; feeds `to-tickets` |
| Splitting a spec/plan into backlog tickets | `to-tickets` | Vertical-slice tickets with blocking edges into backlog's convention |
| Any project that will route work across models | `staffing` — offer **global** | A reusable model roster; the one skill worth installing once for every project |
| Game/asset work with sprite sheets | `to-sprites` (+ `codex-imagegen` for `--generate`) | Extract/generate sprite assets |

The single-purpose catalog skills (`bayes`, `constraints`, `dissolve`, `eloquent`, `fair-deal`, `goodwork`,
`learn-anything`, `teamdrive`, `watch-video`, `shadixfy`, `bare-minimum-ux`, `skill-loop`) are
offered only when the project answer clearly calls for one; they carry no sibling closure. `fair-deal` installs
inside a deal project and is **never** global. `smallbets` is an internal provenance hold and is not offered.

## Install and setup closure

Accepting a composer installs its transitive **required** closure. Optional siblings join only when explicitly
selected or already present; joining one also brings that sibling's required closure. Required edges determine
the dependency-first setup order. The compiler rejects missing siblings, duplicate names, broken setup
pointers, and required cycles before a write plan is presented.

The current notable edges are visible in `catalog.json`: backlog requires diagnosing-bugs, plan, prototype,
review-loop, and staffing; plan requires review-loop and staffing and optionally uses prototype; prototype and spreadsheet-loop
require review-loop and staffing; maquette requires review-loop; review-loop optionally uses staffing for its
watch; setup-asher-skills requires staffing; to-spec optionally uses review-loop; and to-sprites optionally
uses codex-imagegen. Document inputs such as to-tickets consuming a spec are not sibling edges.

When closure resolution adds a sibling, **tell the user which sibling came along and why** — the pull is never
silent ([interview](interview.md) § Phase 2).

## Runtime composition

Install edges only guarantee presence; they do not say how work moves at runtime. `user` means explicit-only,
not human-only: an orchestrator or delegated prompt may name it. `model` additionally permits ambient discovery
inside any working thread. The principal runtime edges are:

| Caller | Target | Runtime reach | Condition |
|---|---|---|---|
| `backlog` | issue coordinator | explicit child dispatch | every ready issue, after `staffing route` |
| issue coordinator | step worker/reviewer/fixer | explicit child dispatch | branch and gate require it |
| `backlog` | `plan`, `prototype`, `diagnosing-bugs` | explicit named call | selected issue branch |
| `plan`, `prototype` | `review-loop` | explicit named call | artifact needs human sign-off |
| composers | `staffing route` | explicit inline named call | role/model must be resolved |
| any working thread | any installed `model` skill | ambient model invocation | the thread recognizes a matching need |

Category and execution declarations remain in the root README table; exact required/optional/setup closure
remains in generated `catalog.json`. A required install edge may support more than one runtime reach and is not
itself proof that a dispatch occurs.

## Scope — project-first

- **Project-local by default.** Every skill installs into the project unless it is `staffing`. Project installs
  never touch the user's home directory.
- **Global only for `staffing`, only with consent.** A model roster is the one genuinely cross-project thing,
  so `staffing` is the only skill offered a global install, routed through staffing's own consent gate. No
  other skill is offered global (and `fair-deal` is explicitly never global).
