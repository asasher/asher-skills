# Opportunities — `goodwork/opportunities.json`

One JSON array, one object per opportunity the person is working or watching. The agent is the sole writer. No sources file, no leads bench, no separate target list, no inbound-channel integration — the person forwards or pastes what arrives, and the agent records it.

## Schema

```json
{
  "id": "acme-senior-analyst",
  "company": "Acme",
  "role": "Senior Analyst",
  "url": "https://...",
  "found_via": "community job channel",
  "stage": "outreach",
  "fit": { "score": 4, "why": "feeds the analysis-heavy energizers; comp above floor; remote OK" },
  "warmth": "ex-colleague on the data team — not yet contacted",
  "next_action": { "what": "send the intro note (approved 2026-07-28)", "by": "2026-07-30" },
  "history": [
    "2026-07-25 — found posting, scored 4/5",
    "2026-07-28 — intro note drafted and approved"
  ],
  "closed_reason": null
}
```

Stages: `watching` → `outreach` → `applied` → `interviewing` → `offer` → `closed`. Not every opportunity takes every stage. `closed` always carries a `closed_reason` in plain words ("no response after two follow-ups", "comp below floor", "took another offer") — repeated reasons are profile evidence; route them to `profile`.

Every **open** opportunity has a `next_action` with a date. A missing next action is a decision waiting to be made — flag it at `checkin`. `history` is dated one-liners that read as the story of the pursuit, not bookkeeping; it is what the board shows.

## Scout — finding and scoring

Where to look: places the profile's intersection actually lives — community job channels, the specific boards for the field, employers of people the person admires, companies adjacent to past employers. Verify a posting is real and current before it enters the list; stale and ghost postings are common.

Score against the profile (1–5, with the why recorded):

- Does the actual work — tasks, not title — feed what energizes them?
- Search parameters: role match, location/visa, compensation floor, no dealbreaker.
- Evidence readiness: can roughly 70% of the must-have requirements be evidenced from the profile's proof? Below that, the honest fix is a proof artifact ([assets.md](assets.md)), not adjectives.
- Warmth: an insider, or a plausible path to one.

New finds enter at `watching`, ranked with reasons. Adding is cheap; pursuing is not — the person picks what moves forward.

## Track — working an opportunity

- **Warmth before applications.** Cold-applying to a top-choice company wastes it — it files the person into the portal pile before a human could route them. Default order: a conversation or intro first, the application with or after it.
- **Outreach drafts**: one specific true reason for contacting this person, one small clear ask, no CV attached, never mass-personalized. Polished final text first, then rationale.
- **Application packages**: mirror the posting's real keywords only where true evidence exists; simple formatting; tailoring is selection and emphasis from the same verified evidence base, never invention.
- **Follow-up cadence, pre-decided**: no reply → follow up after ~3 business days → once more ~7 days later → close with reason. Never more; anxiety doesn't get to improvise.
- **Volume**: 5–10 high-fit applications a week beats 50 sprayed.
- Every send: final text approved in chat, sent verbatim, logged to `history`, next action set.

## Checkin — the periodic review

Fifteen minutes, roughly weekly, or whenever the person asks "where am I?":

1. **What moved** — stage changes and replies since last time, in plain words.
2. **What stalled** — open opportunities with overdue or missing next actions; set them.
3. **One diagnosis** — find the narrowest point of the funnel and name the single fix: no replies to outreach → the message or the targeting; applications but no screens → targeting, then evidence, then documents, in that order; interviews but no offers → preparation; offers but wrong offers → scoring has drifted from the profile. One change per week — changing three things at once makes next week's numbers meaningless.
4. **Profile feedback** — repeated closed-reasons, energy patterns, market corrections → `profile`.
5. **Refresh the board** and end with next week's few concrete actions, time-boxed.
