# Interview

Elicits and settles the strategic decisions behind a piece of work by walking its decision tree in **batch
frontier rounds**: every currently-unblocked question asked in one numbered round, each carrying the evidence
in hand, what it unlocks, and a recommended hypothesis with its trade-off (accept / modify / defer /
unknown). Facts are looked up, never asked; provided artifacts are read, never asked about; the session ends
only when the frontier is empty **and** a surface-aware coverage sweep holds — "we feel aligned" is the
sign-off, not the test.

## When to use

- An idea, problem, PDF, or half-formed direction needs its decisions surfaced and settled before spec,
  tickets, or a build.
- A workflow skill (to-spec's caller, backlog groom, a shaping session) needs an intent sharpened.
- Use bare `interview` when nothing durable is wanted; use the `shape` skill when settled terms and
  decisions should be written down as they land.

## Shape

- **Intake first** — repo, artifacts, PRODUCT/CONTEXT/ADRs read before the first question.
- **Frontier rounds** — the whole unblocked set per round; dependency-ordered; split by cluster only if a
  round balloons. One topic per question; assert-then-confirm over option menus.
- **Facts vs decisions** — environment facts via lookup or the `research` sibling (a running lookup blocks
  only its downstream questions); decisions go to the user and wait. Paper-unsettleable questions go to the
  `prototype` sibling as probes.
- **Playback per round** — delta, unlocks, contradictions — then recompute the frontier.
- **Exit** — every open thread classified settled / delegated / deferred / blocking, plus a one-line depth
  call (implement now / tickets / spec first) for the user to confirm.

## Dependency surface

- **Bundled:** `SKILL.md` only.
- **Siblings (optional, by name):** `research`, `prototype`, `staffing`.
- **Composed by:** `shape` (adds `domain-modeling` extraction, synthesis, and projection).

## Provenance

- **Sources:** Matt Pocock's MIT-licensed
  [`batch-grill-me`](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/in-progress/batch-grill-me/SKILL.md)
  (frontier scheduling, rounds, facts-not-asked) and
  [`grilling`](https://github.com/mattpocock/skills/blob/9603c1cc8118d08bc1b3bf34cf714f62178dea3b/skills/productivity/grilling/SKILL.md)
  (decisions-are-the-user's, shared-understanding confirmation). License in `THIRD_PARTY_LICENSES.md`.
- **Local changes:** intake-first artifact ingestion; hypothesis framing with accept/modify/defer/unknown
  affordances; one-topic-per-question and assert-then-confirm (interview craft observed in
  [Impeccable](https://github.com/pbakaus/impeccable)); coverage-sweep stopping condition; open-thread
  classification and depth call at exit; requirements-elicitation grounding from the
  `research/afk-spec-ticket-lifecycle` dossier (Bano 2019; Ferrari 2022; Carrizo 2020; Pitts & Browne 2007;
  IREB v2.2.0; Shen 2025).
