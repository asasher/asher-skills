# The catalog — what to install, and the rules that bind it

Which skills fit which project and how their dependency surface is declared. Canonical invocation, execution,
required-sibling, optional-sibling, external, setup, and internal-hold declarations live under `metadata` in
each source `SKILL.md`; schema-3 [`catalog.json`](catalog.json) is their generated snapshot and emits
`external: []` and `variants: {}` when absent. Internal roots are cataloged for audit but cannot be selected or required by a
public skill. Validate a
self-host checkout with `python3 skills/system/setup-asher-skills/scripts/catalog.py validate --root . --snapshot
skills/system/setup-asher-skills/reference/catalog.json` before using the snapshot.

## Canonical source and declared externals

**Every Asher-authored skill comes from `https://github.com/asasher/asher-skills` — the slug
`asasher/asher-skills` — or, in the self-host case, the same repo's local root.** Never substitute a fork,
mirror, gist, or similarly named external package for an Asher-authored skill.

A skill source may declare provenance-checked external requirements in one frontmatter line:

`external: [{"name":"browser-driver","kind":"codex-plugin","source":"https://github.com/owner/repo","capability":"Drive an authenticated browser","version":"v1.2.3"}]`

The value is a JSON array sorted by unique `name`. Every object requires `name`, `kind`, `source`, and
`capability`; `version` is optional. Names are lower-kebab-case, `kind` is `skill` or `codex-plugin`, and
`source` is an HTTPS GitHub repository URL. External names cannot collide with required or optional sibling
edges. The compiler merges identical declarations across the selected closure and rejects any same-name
declarations whose source, kind, capability, or version differs.

An external declaration is permission to **offer**, not permission to install. Before any external write,
follow [interview](interview.md) Phase 4: verify provenance, inspect and disclose source/version/scope/hooks,
get explicit consent, use the provider-specific installer, verify the declared capability, and record the
result in the consumer's separate `external-dependencies.lock.json`. An arbitrary external request that is
not in the selected closure is never auto-installed; offer an Asher-authored equivalent if one exists, or
state that the request needs a separate deliberate install outside this setup run.

## Opt-in provider variants

The default remains one real `.agents/skills/<name>` primary plus any harness alias symlinks. A skill opts
into real provider trees only with a sorted one-line declaration such as
`variants: {"claude":"variants/claude","codex":"variants/codex"}`. Each value must be the matching shipped
overlay directory. The catalog keeps name, invocation/execution policy, siblings, externals, and setup owner
once in the root `SKILL.md`; overlays may replace runtime files but may not contain `SKILL.md`,
`agents/openai.yaml`, or `reference/setup.md`.

For each confirmed active harness, `catalog.py materialize <skill> --provider <provider>` copies the common
runtime tree without author-only `evals/` or source-only `variants/`, applies that provider's overlay, and reports the shared-source revision plus the
effective-tree hash. `install.py publish-variant` preflights every destination and the provider lock before
publishing any tree, then atomically converts only the approved active mounts to real provider directories.
Unvaried skills never enter this path and retain their symlink behavior.

## By project type — the recommendation seed

Recommend from this map, then confirm each choice one decision at a time ([interview](interview.md) § Phase 2).
The map is a starting point tuned by the project answer, not a fixed bundle.

| Project is for… | Recommend | Why |
|---|---|---|
| A shipping product / app repo, ongoing work | `backlog` (pulls its full closure) | The issue→reviewed-PR loop; brings diagnosis, research, plan, prototype, review-loop, staffing |
| A source-backed question or investigation | `research` (requires staffing) | Primary-source dossier with facts/observations, traceable inferences, contradictions, and unknowns |
| A one-off feature or decision that needs sign-off | `plan` (requires review-loop + staffing; offer prototype/research for unresolved questions) | Reviewed plan with an approval gate, no full backlog machinery |
| A design/state question that needs to be tried | `prototype` (pulls review-loop + staffing) | Throwaway artifact that settles one question |
| A greenfield product to pitch/sell | `maquette` (pulls review-loop) | High-fidelity clickable prototype for a demo |
| Turning a decided conversation into a written spec | `to-spec` (review-loop optional) | Synthesize a spec; feeds `to-tickets` |
| Splitting a spec/plan into backlog tickets | `to-tickets` | Vertical-slice tickets with blocking edges into backlog's convention |
| Any project that will route work across models | `staffing` — offer **global** | A reusable model roster; the one skill worth installing once for every project |
| Raster, layered, or sprite-sheet asset work | `codex-imagegen` | Generate flat/layered artifacts or extract sprite assets |

The single-purpose catalog skills (`bayes`, `constraints`, `dissolve`, `eloquent`, `fair-deal`, `goodwork`,
`learn-anything`, `teamdrive`, `watch-video`, `shadixfy`, `bare-minimum-ux`, `skill-loop`) are
offered only when the project answer clearly calls for one; they carry no sibling closure. `fair-deal` installs
inside a deal project and is **never** global.

## Install and setup closure

Accepting a composer installs its transitive **required** closure. Optional siblings join only when explicitly
selected or already present; joining one also brings that sibling's required closure. Required edges determine
the dependency-first setup order. The compiler rejects missing siblings, duplicate names, broken setup
pointers, invalid provider overlays, required cycles, malformed external declarations, and conflicting external requirements before a
write plan is presented. Closure output includes the sorted, deduplicated `external` requirements merged from
every active skill.

The current notable edges are visible in `catalog.json`: backlog requires diagnosing-bugs, plan, prototype,
research, review-loop, and staffing; research requires staffing; plan requires review-loop and staffing and
optionally uses prototype and research; prototype and spreadsheet-loop
require review-loop and staffing; maquette requires review-loop; review-loop optionally uses staffing for its
watch; setup-asher-skills requires staffing; control-plane optionally uses until-zero; to-spec optionally uses
review-loop; and to-sprites optionally uses codex-imagegen. Document inputs such as to-tickets consuming a
spec are not sibling edges.

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
| `backlog` | `plan`, `prototype`, `research`, `diagnosing-bugs` | explicit named call | selected issue branch |
| `plan`, `prototype` | `review-loop` | explicit named call | artifact needs human sign-off |
| `research` | `staffing route` | explicit named call | independent source shards or claim challenger |
| `plan` | `research` | explicit named call | a source-backed fact question blocks a plan decision |
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
- **External requirements inherit the approved scope of the skill that requires them.** Disclose that scope
  separately; if the same requirement is needed in more than one scope, each provider install and lock record
  is a separate consented write.
