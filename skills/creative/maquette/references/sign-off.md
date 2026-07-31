# Sign-off gates

Maquette's human sign-off gates run **in chat**: the user reads the deliverable and gives an explicit verdict in the conversation. Maquette carries no review server and requires no presentation infrastructure.

## Present the deliverable

At a gate, present the current markdown deliverable — `BRIEF.md` or `JOURNEYS.md` — for review:

- Summarize it in chat: the decisions it locks in, the scope fence, and anything you flagged or assumed.
- Point at the file itself as the canonical text. If the harness offers a native rendered surface (artifacts, a hosted preview), use it; otherwise the user reads the file directly.
- For a long deliverable, lead with what changed since the last round rather than re-presenting the whole document.

The markdown remains the canonical deliverable; any rendered view is ephemeral.

## Await the verdict

Ask for an explicit verdict and block on it. Three outcomes:

- **Approve** — proceed to the next phase.
- **Approve with nits** — apply the noted changes, then proceed without a re-review round.
- **Request changes** — revise the deliverable, reply in chat with how each note was addressed (`changed`, `kept` with the reason, or no longer applicable), and re-present. Never silently drop a note.

Silence, a topic change, or "looks interesting" is not a verdict. If the turn ends without one, resume by re-asking, not by building.

## The approval record

Record the approval where the pipeline can find it later: a dated `Approved` line at the top of the deliverable (who, when, any nits applied). A mid-pipeline entry (see SKILL.md operating rules) checks for these records before building on prior phases.

## Demo distribution is separate

Sign-off gates cover documents; showing the built maquette is a different act. The demo runs locally by default. When the user wants a shareable link, use the static deploy mode (e.g. Vercel) described in [architecture](architecture.md) — optional, on request, never a gate requirement.
