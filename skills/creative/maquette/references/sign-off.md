# Sign-off gates

Maquette's human sign-off gates run through the **`serve-via-tailnet` skill**: a sibling root primitive invoked by
name. Maquette carries no review server of its own and imports no serve-via-tailnet files.

## Render the deliverable

At a gate, render the current markdown deliverable — `BRIEF.md` or `JOURNEYS.md` — to a self-contained HTML
page. Each top-level section becomes a block with a stable `id` derived from a slug of its heading; for
`JOURNEYS.md`, each journey and each screen entry gets the same treatment. Ids never change across
revisions. This is the stable-id convention serve-via-tailnet documents in its `templates/plan-skeleton.html`
and `reference/serve-via-tailnet.md`.

Keep the HTML self-contained: inline styles, no external fetches. The render is ephemeral, produced for the
gate; the markdown remains the canonical deliverable.

## Serve and await

Present the rendered page through the `serve-via-tailnet` skill: serve it with `--kind maquette --issue <slug>`,
point the human at the printed URL, and block on await. The exact serve/await CLI, flags, and exit-code
verdicts live in the serve-via-tailnet skill's `reference/scripts.md`: `serve` is `scripts/review-server.py`,
`await` is `scripts/review-await.py`; exit `0` approve, `3` approve_with_nits, `10` request_changes,
`124` timeout.

Branch on the exit code:

- **approve** — proceed to the next phase.
- **approve_with_nits** — apply the batched notes, then proceed without a re-review round.
- **request_changes** — revise the deliverable, write a ledger disposition for every annotation
  (`changed`, `kept`, or `orphaned`), re-serve, and re-await. A revision without a ledger is a contract
  violation.
- **timeout** — end the turn with the review URL and hub URL; re-await next turn.

## Surface

The presentation surface is inherited from the repo's `docs/agents/environment.md` § Presenting, exactly as
serve-via-tailnet specifies: tailnet path proxy plus hub, or local fallback. Maquette adds no surface knowledge of
its own. Absent surface config, serve-via-tailnet degrades to local-only fallback: open the file on the machine;
remote review is unavailable.

The approve event — verdict, content hash, timestamp — is the approval record. Never build past a gate
without it.
