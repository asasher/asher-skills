# Sign-off gates

Spreadsheet-loop's human sign-off gates run through the **`review-loop` skill** — a sibling root primitive
invoked by name. This skill carries no review server of its own and imports no review-loop files.

The gates are on the **paper artifacts** only: `SPEC.md` (phase 1) and `MODEL.md` + `LAYOUT.md` (phase 2).
The live Univer surface is not a gated artifact — it is driven directly (see [the-loop](the-loop.md)).

## Render the deliverable

At a gate, render the current markdown deliverable to a self-contained HTML page. Each top-level section
becomes a block with a stable `id` derived from a slug of its heading; for `MODEL.md`/`LAYOUT.md`, render both
as one page or two, but keep ids stable across revisions. This is the stable-id convention review-loop
documents in its `templates/plan-skeleton.html` and `reference/review-loop.md`. Inline all styles; no external
fetches. The render is ephemeral; the markdown stays canonical.

## Serve and await

Present the rendered page through the `review-loop` skill: serve it with
`--kind spreadsheet-loop --issue <slug>`, point the human at the printed URL, and block on await. The exact
serve/await CLI, flags, and exit-code verdicts live in review-loop's `reference/scripts.md`: `serve` is
`scripts/review-server.py`, `await` is `scripts/review-await.py`; exit `0` approve, `3` approve_with_nits,
`10` request_changes, `124` timeout.

Branch on the exit code:

- **approve** — proceed to the next phase.
- **approve_with_nits** — apply the batched notes, then proceed without a re-review round.
- **request_changes** — revise the deliverable, write a ledger disposition for every annotation
  (`changed`, `kept`, or `orphaned`), re-serve, and re-await. A revision without a ledger is a contract
  violation.
- **timeout** — end the turn with the review URL and hub URL; re-await next turn.

## Surface

The presentation surface is inherited from the repo's `docs/agents/environment.md` § Presenting, exactly as
review-loop specifies: tailnet path proxy plus hub, or local fallback. This skill adds no surface knowledge of
its own. Absent surface config, review-loop degrades to local-only fallback: open the file on the machine;
remote review is unavailable.

The approve event — verdict, content hash, timestamp — is the approval record. Never build past a gate
without it.
