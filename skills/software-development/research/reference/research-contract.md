# Research contract

The dossier records what the available sources establish, not what the author hopes is true. Apply this
contract to local code/document research, connected repositories and records, web research, and mixed-source
investigations.

## Source hierarchy

Prefer the source that owns the claim:

1. the observed system, raw dataset, source code, commit, specification, official documentation, first-party
   API, contract, or original record;
2. a first-party explanation or announcement when the owning artifact is unavailable;
3. a reputable secondary source, explicitly labelled, only when no primary source is reachable.

Search snippets, generated summaries, aggregators, and an article's uncited paraphrase are discovery aids,
not support. A user-provided document is primary evidence for what that document contains, not automatically
for every external-world assertion it makes.

For each source record the stable locator (URL or repo path), owner, title, publication/update date when
available, accessed date for mutable web material, and the relevant version, commit, page, section, table, or
line. Quote only the minimum words needed to identify the observation.

## Claim ledger

Give every material claim a stable ID and one class:

- **Observation** — what a source directly states or what code/data/system inspection directly shows.
- **Fact** — an observation established within the brief's scope and boundary, with no unresolved source
  conflict. State the boundary; do not universalize it.
- **Inference** — reasoning derived from named fact/observation IDs. Record the reasoning and confidence.
- **Unknown** — an in-scope question the reachable sources do not establish.

A shard returns claim packets, not a mini-essay. Each packet contains ID, class, one atomic statement,
source locators, scope/as-of qualifiers, and limitations. Inferences additionally list supporting IDs.
Recommendations are downstream judgments: keep them outside the ledger unless the user explicitly asks, and
then cite the findings they depend on.

## Contradictions and absence

Do not resolve conflicting sources by majority vote. Check whether they describe different dates, versions,
jurisdictions, populations, definitions, or authority levels. If the conflict remains, show both claims,
explain the consequence, and leave the conclusion bounded or unknown.

Do not turn failure to find a source into proof of absence. Report where and how you looked, then state the
narrow observation: no supporting primary source was found within that search boundary.

## Parallel research

Parallelize when the brief contains independent subquestions or source families whose results can be merged
without sharing mutable intermediate state. Do not fan out one small lookup or send several workers the same
vague question.

- The coordinator owns the brief, shard boundaries, claim-ID namespace, synthesis, and final file.
- Each worker receives only its question, scope, source priorities, output packet schema, and return deadline.
- Workers return packets to the coordinator or write separate shard files; they never concurrently edit the
  canonical dossier.
- Reserve at least one execution slot for the coordinator/synthesizer. When the caller is already parallel,
  choose the inner fan-out from the remaining capacity and cost of contention.
- After fan-in, deduplicate claims and reconcile cross-shard definitions and contradictions.
- Use an independent challenger for consequential conclusions, weak-source claims, or multi-shard work. The
  challenger tries to falsify material conclusions and find primary-source leakage; it does not rewrite.
- No fire-and-forget work: every shard is watched, has a named owner, and is either incorporated or reported
  as an unresolved gap before completion.

## Artifact

The project playbook sets the location. Without one, create a durable dossier under
`research/<lowercase-hyphenated-slug>/`:

- `brief.md` — question, intended use, scope, exclusions, definitions, as-of boundary, and shard map;
- `findings.md` — canonical answer and reconciled claim ledger;
- `claims/<shard>.md` — optional worker packets when fan-out is large enough to justify retaining them;
- `report.html` — optional human-facing rendering when requested; it derives from the same claims and lives
  beside them.

If research directly supports authoring a local skill and the project routes development material through a
`<skill>-workspace/`, follow its playbook and place the dossier under that workspace's `research/` directory.
Temporary executor or visualization files may remain in thread scratch, but the delivered artifact is the
canonical research file above.

When the research dossier itself is the backlog deliverable, commit it in `research/`; its citations and
audit are its intrinsic provenance.

## Dossier order

1. Question, intended use, scope, and as-of boundary.
2. Concise answer.
3. Facts and direct observations, grouped by subquestion.
4. Inferences, each linked to supporting claim IDs.
5. Contradictions and unresolved source disagreements.
6. Unknowns, search boundaries, and consequences.
7. Method and coverage.
8. Source index.

## Claim audit

Before returning, check every material sentence:

- Its class is visible: fact/observation, inference, unknown, or requested recommendation.
- A fact/observation cites the primary source that owns it, or clearly labels the source downgrade.
- The locator resolves to the cited source and identifies the relevant version/section.
- An inference names supporting claim IDs and does not exceed their scope.
- Mutable or time-sensitive material carries an as-of or accessed date.
- Contradictory sources and missing primary material are visible.
- Parallel shards are all accounted for, reconciled, and no longer writing.
- The dossier lives in the research location.

The audit passes only when every material statement is traceable or explicitly unknown. Source count alone is
not a quality signal.
