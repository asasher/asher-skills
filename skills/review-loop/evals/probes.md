# Review-loop — situated dry-run probes

Method: situated probes against the actual deployment targets — an Opus subagent (via the Agent tool) and
`codex exec --sandbox read-only` — with `SKILL.md` in context, plus the one `reference/` file named by the
probe when it names one (probes that test whether a reference stands alone withhold `SKILL.md`). Require the
executor to **cite the file and the exact sentence** that decided each answer, and to **flag ambiguity as a
valid answer** — flagged ambiguities are findings to feed back into the wording, not failures. Grade
pass/fail against the key. **The answer key is written before any runs** and graded against the plan's
acceptance criteria (`plans/2-extract-review-loop.html`, ids ac-1..ac-13) — the plan is the source of truth;
do not grade against looser criteria.

The runtime-verified criteria (ac-3, ac-4, ac-5, ac-6, ac-7, ac-13a) are confirmed by the verify step's
direct `python3` exercises of the shipped scripts — real HTTP GET/POST over loopback and through a stripping
proxy — and the file-check criteria (ac-1, ac-8b, ac-10, ac-12, ac-13b) by grep/parse against the tree, as
the staffing eval does for its structural criteria. Probes below additionally exercise the *routing and
understanding* of those invariants where a reasoning probe adds value; ac-4 is verified by the serve
exercise alone. Each probe names the criterion it exercises. Between them the 12 probes plus the runtime/file
set cover ac-1..ac-13.

## Probes

**P1 (ac-1).** Read `skills/review-loop/SKILL.md`. Does its frontmatter identify it as a user-invocable,
artifact-agnostic review/sign-off primitive? List the files the skill ships under `skills/review-loop/`
(SKILL, README, the `reference/` docs, the two scripts + `pages/chrome.{css,js}`, a `templates/` skeleton,
`agents/openai.yaml`, `evals/probes.md`). Do any of the skill's files import or read another skill's files?

**P2 (ac-2).** A composer skill (maquette) wants to depend on `review-loop`. From `SKILL.md`, list the three
kinds of dependency pointer the skill declares, and state exactly what it says about **sibling** skills.

**P3 (ac-8).** You need a human to sign off on a rendered **maquette**, not a plan. Does `review-server.py`
reject a non-plan/prototype `--kind`? Does the skill bake in any "backlog" or "plan" identity that would stop
it serving an arbitrary artifact? Cite what you checked.

**P4 (ac-3).** A sibling skill has just rendered an artifact and wants Asher to sign off on it. What does it
do — reinvent a review UI, or something else? Name the two scripts and the order, and the flag that sets the
artifact kind. Cite it.

**P5 (ac-5).** `review-await.py` exited **10** on your last block. What verdict is that, and what is the
required sequence before you re-serve and re-await? Be specific about what must be written and why. Cite the
contract.

**P6 (ac-6).** Asher opened the artifact, then you edited it, then Asher clicked Approve on the old tab. What
does the server do, and what does the human see? Give the HTTP status and the reason this invariant exists.
Cite it.

**P7 (ac-7).** You are asked to present an artifact for review but **no presentation surface is recorded**
for this repo. What do you do, and what must you **not** do? Cite the rule.

**P8 (ac-9).** You are building a **new** doc-review skill and want the annotate→revise→approve surface. Do
you copy `review-loop`'s scripts into your skill? What does `docs/patterns/review-surface.md` tell you to do
now, and on what repo convention? Cite it.

**P9 (ac-10).** Read `skills/review-loop/agents/openai.yaml`. Is it well-formed per
`docs/patterns/codex-compat.md`, and is `allow_implicit_invocation` set correctly for an operator primitive
that starts servers? State the value and why it is right.

**P10 (ac-6, explanatory).** After a revision, how do you (and the durable record) establish that an approval
covered the exact version now on disk? Do you compare a `vNN` version stamp on the artifact? Name the
mechanism and cite the sentence that says how reconciliation works.

**P11 (ac-13).** The artifact is served to Asher under a tailnet path prefix — the page's URL is
`https://host/asher-skills/2/review/`. When Asher submits a verdict, will the POST reach the server, whether
the proxy strips the prefix or preserves it? Name the two mechanisms (client-side and server-side) that make
this work. Cite them.

**P12 (ac-12).** You just extracted `review-loop`. Does `backlog` still present plans exactly as before, and
did you touch its scripts or `presenting.md`? What is explicitly deferred? Cite it.

## Answer key

- **P1 (ac-1):** Frontmatter has `name: review-loop`, `user-invocable: true`, and a `description` that reads
  as an artifact-agnostic review/sign-off primitive invoked by name by siblings and directly by users —
  **pass**. All listed files exist under `skills/review-loop/`. No file imports another skill's files (the
  dependency surface says the references and scripts "import no other skill's files" and siblings are "none —
  root primitive"); a grep for cross-skill paths finds none. Claiming a cross-skill import exists, or missing
  that the skill is user-invocable, = fail.
- **P2 (ac-2):** The three pointer kinds: **bundled references** (own `reference/` contract *plus the
  scripts*), **project playbooks** (a `docs/agents/` surface-config playbook — the tailnet root, surface dir,
  proxy commands, keep-awake), **sibling skills**. On siblings it must say **"none — `review-loop` is a root
  primitive"** (invoked by siblings such as backlog/maquette/prototype, depends on none). Missing any of the
  three, or getting the sibling answer wrong, = fail.
- **P3 (ac-8):** **No** — `--kind` is free-form (default `plan`, help says plan/prototype/maquette/doc are
  examples) and a non-plan value is not rejected; the server serves any HTML with stable ids and bakes in no
  "backlog"/"plan" identity (the docstring/hub carry no hardcoded "backlog"; the plan skeleton is a
  `templates/` example, not required). Cite `reference/scripts.md` (`--kind` "free-form … not rejected") and
  SKILL.md's "artifact-agnostic" paragraph. Claiming a non-plan kind is rejected = fail.
- **P4 (ac-3):** It does **not** reinvent a review UI — it composes `review-loop` by name: serve the rendered
  artifact with `scripts/review-server.py` (passing `--kind maquette`/whatever the artifact is), then block
  on `scripts/review-await.py`. Cite SKILL.md § Command surface / `reference/scripts.md`. Reinventing an ad
  hoc review UI, or naming only one script, = fail.
- **P5 (ac-5):** Exit **10 is request_changes.** Required sequence: **revise the artifact → write the
  response-ledger disposition (`changed`/`kept`/`orphaned`) for every prior annotation → re-serve →
  re-await.** A revision without a ledger is a contract violation. Cite `reference/review-loop.md` §§ verdict
  codes / response ledger. Omitting the ledger, or skipping the revision, = fail.
- **P6 (ac-6):** The server **refuses** the approval — the approve POST's `doc_hash` no longer matches the
  current hash, so it returns **HTTP 409 `{"error":"stale"}`** and the chrome banners "the document changed
  since you loaded it — reload latest." The invariant exists so a human can never sign off on a version they
  did not see (hash-bound approval, the load-bearing safety property). Cite `reference/review-loop.md` §
  Hash-bound approval. Answering that the approval is accepted, or omitting the 409, = fail.
- **P7 (ac-7):** **Local fallback** — open the rendered file or running app on the machine and say remote
  review is unavailable; you must **not improvise a public tunnel** (Funnel stays off). Cite
  `reference/surface-and-hub.md` § surface contract "Local fallback". Proposing a public tunnel/Funnel, or
  failing silently, = fail.
- **P8 (ac-9):** **No — do not copy the scripts.** The review surface is now an **extracted primitive**, the
  `review-loop` skill; adopt it by **composing it by name** ("present it via `review-loop`"), per
  `AGENTS.md` § Conventions "copy a pattern; extract a primitive". `docs/patterns/review-surface.md` is a
  superseded pointer to `skills/review-loop/`. Cite it. Saying "copy the canonical scripts" (the old advice)
  = fail.
- **P9 (ac-10):** Well-formed: `interface.display_name` "Review Loop", a one-line `short_description`
  matching the SKILL.md spirit, a concrete `default_prompt`, and `policy.allow_implicit_invocation: false`.
  `false` is correct because review-loop is an **operator primitive that starts servers and holds a public
  URL**, not a lightweight advisory skill — codex-compat.md says default `false` for operator-style skills
  that run loops or spend resources. Saying `true` is fine, or the YAML being malformed, = fail.
- **P10 (ac-6, explanatory):** The **approve event** — verdict, **content hash**, timestamp, appended to
  `events.jsonl` — plus the response ledger is the durable record; reconciliation is **LLM audit over that
  event log and the ledger, with no version stamps** (no `vNN`). You establish coverage by the hash bound
  into the approval, not by a stamp on the artifact. Cite `reference/review-loop.md` § "The approve event is
  the approval record". Answering "compare version numbers/stamps" = fail.
- **P11 (ac-13):** Yes. **Client-side:** the chrome builds every client→server call **mount-relative** (it
  derives a base from the served page's path, not root-absolute `/event`/`/version`), so requests resolve
  under a prefix. **Server-side:** the server matches its endpoints **suffix-tolerantly**, so it works
  whether the proxy strips the prefix (backend sees `/event`) or preserves it. Cite
  `reference/surface-and-hub.md` § Path-prefix mounts (and `reference/scripts.md` endpoints note). Naming
  only one side, or claiming submit still 404s, = fail.
- **P12 (ac-12):** **Yes, backlog presents exactly as before** — the extraction is non-breaking: backlog
  keeps its own bundled scripts and `presenting.md`, untouched. Rewiring backlog (and goodwork) to consume
  `review-loop` by name and deleting their copies is **explicitly deferred to a separate rewire issue**,
  noted in the superseded pattern doc. Cite `docs/patterns/review-surface.md` / SKILL.md dependency surface.
  Claiming backlog was modified, or that the rewire happened here, = fail.

## Scoring

12 probes × 2 executors (Opus in-session + `codex exec`). A probe passes only with the **correct action AND
a correct citation**. Ambiguity flags are recorded as findings, not failures — they are the most valuable
output and should drive wording fixes before ship. Report a verdict table mapping each probe → its criterion
→ pass/fail per executor.

The behavioral criteria are additionally confirmed outside the probes:

- **Runtime** (direct `python3` exercises of the shipped scripts): **ac-3** (non-plan `--kind` starts and
  prints JSON), **ac-4** (arbitrary HTML served with chrome injected; on-disk file byte-identical after),
  **ac-5** (the four verdict exit codes 0/3/10/124), **ac-6** (stale-hash approve → 409), **ac-7**
  (registry/index written and swept via `--sweep`), **ac-13a** (verdict POSTed through a stripping
  path-prefix proxy still fires the verdict-coded await).
- **File check** (grep/parse against the tree): **ac-1** (layout present), **ac-8b** (no hardcoded "backlog"
  in the server docstring/hub H1), **ac-10** (`agents/openai.yaml` parses), **ac-12** (backlog's scripts and
  `presenting.md` untouched), **ac-13b** (`chrome.js` has no root-absolute `fetch('/event'`/`fetch('/version'`
  and builds URLs from a mount base).

### Criterion coverage map

| criterion | probe(s) | also confirmed by |
|-----------|----------|-------------------|
| ac-1  | P1        | file check (layout) |
| ac-2  | P2        | — |
| ac-3  | P4        | runtime (non-plan kind serve) |
| ac-4  | —         | runtime (serve arbitrary HTML; file byte-identical) |
| ac-5  | P5        | runtime (verdict exit codes 0/3/10/124) |
| ac-6  | P6, P10   | runtime (stale-hash → 409) |
| ac-7  | P7        | runtime (registry/index + `--sweep`) |
| ac-8  | P3        | file check (no hardcoded "backlog") |
| ac-9  | P8        | file check (superseded pattern doc + README row) |
| ac-10 | P9        | file check (YAML parses) |
| ac-11 | this file (the eval) | — |
| ac-12 | P12       | file check (backlog untouched) |
| ac-13 | P11       | runtime (prefixed-mount POST) + file check (`chrome.js` mount-relative) |
