# The catalog — what to install, and the rules that bind it

Which skills fit which project, the sibling closure rules setup guarantees, and the hard invariant that every
install comes from this repo only. This file stands alone and names siblings by plain name.

## Pull only from this repo

**Every skill setup installs comes from `https://github.com/asasher/asher-skills` — the slug `asasher/asher-skills`
— and nothing else.** Every `npx skills add` command this skill emits targets that endpoint. setup **never
installs, recommends, or emits an install command for a skill from any other host or account** (not
`mattpocock/*`, not any vendor repo, not a gist).

The reason is a design stance, not a limitation: good ideas from elsewhere are **brought in, adapted, and
shipped here as our own** (for example `to-spec` is our adaptation of Matt Pocock's `to-prd`). So when a user
asks for an external skill by name — "install the TDD skill" — the move is: **offer our adapted equivalent if
we ship one, or say plainly that we don't ship it. Never reach out to the external repo.** If we have no
equivalent, that is an honest answer, not a reason to break the invariant.

## By project type — the recommendation seed

Recommend from this map, then confirm each choice one decision at a time ([interview](interview.md) § Phase 2).
The map is a starting point tuned by the project answer, not a fixed bundle.

| Project is for… | Recommend | Why |
|---|---|---|
| A shipping product / app repo, ongoing work | `backlog` (pulls its full closure) | The issue→reviewed-PR loop; brings plan, prototype, review-loop, staffing |
| A one-off feature or decision that needs sign-off | `plan` (pulls review-loop + staffing + prototype) | Reviewed plan with an approval gate, no full backlog machinery |
| A design/state question that needs to be tried | `prototype` (pulls review-loop + staffing) | Throwaway artifact that settles one question |
| A greenfield product to pitch/sell | `maquette` (pulls review-loop) | High-fidelity clickable prototype for a demo |
| Turning a decided conversation into a written spec | `to-spec` (review-loop optional) | Synthesize a spec; feeds `to-tickets` |
| Splitting a spec/plan into backlog tickets | `to-tickets` | Vertical-slice tickets with blocking edges into backlog's convention |
| Any project that will route work across models | `staffing` — offer **global** | A reusable model roster; the one skill worth installing once for every project |
| Game/asset work with sprite sheets | `to-sprites` (+ `codex-imagegen` for `--generate`) | Extract/generate sprite assets |

The single-purpose catalog skills (`bayes`, `constraints`, `dissolve`, `eloquent`, `fair-deal`, `goodwork`,
`learn-anything`, `smallbets`, `teamdrive`, `watch-video`, `shadixfy`, `bare-minimum-ux`, `skill-loop`) are
offered only when the project answer clearly calls for one; they carry no sibling closure. `fair-deal` installs
inside a deal project and is **never** global.

## The closure rules

Accepting a composer installs its **transitive sibling closure** — setup computes it at accept time and never
ships a half-wired composer. Two roots depend on nothing; everything closes over them.

- **Roots (depend on nothing):** `staffing`, `review-loop`.
- **`plan` ⇒ ensure `review-loop` + `staffing` + `prototype`.** (plan renders the artifact, review-loop signs
  it off, staffing picks who authors/builds, prototype settles logic/UI design questions — a soft edge, but
  installed with plan so gate 2 works out of the box.)
- **`prototype` ⇒ ensure `review-loop` + `staffing`.** (the two roots.)
- **`maquette` ⇒ ensure `review-loop`.** (maquette signs off its brief and journeys; it does not compose
  staffing.)
- **`backlog` ⇒ ensure ALL of `staffing`, `review-loop`, `plan`, `prototype`.** The transitive closure adds
  nothing beyond those four (plan pulls prototype and the two roots; prototype pulls only the roots).
- **Soft edges, noted not force-installed:** `to-tickets` reads backlog's `backlog-policy.md`/`platform.md`
  conventions but does not require the whole skill; `to-sprites` uses `codex-imagegen` only for `--generate`.
  Mention these; install them only if the user wants that path.

When a closure adds a sibling, **tell the user which siblings came along and why** — the pull is never silent
([interview](interview.md) § Phase 2).

## Scope — project-first

- **Project-local by default.** Every skill installs into the project unless it is `staffing`. Project installs
  never touch the user's home directory.
- **Global only for `staffing`, only with consent.** A model roster is the one genuinely cross-project thing,
  so `staffing` is the only skill offered a global install, routed through staffing's own consent gate. No
  other skill is offered global (and `fair-deal` is explicitly never global).
