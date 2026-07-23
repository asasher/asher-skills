# profile - view, update, import, or drain evidence

Maintains `goodwork/PROFILE.md` (schema in [framework.md](framework.md)) between interviews and drains the evidence inbox from [state.md](state.md).

## Modes

**View.** Summarize the snapshot, the confidence distribution (reported vs. evidenced vs. tested), and staleness (last update, what's changed since). Flag the weakest sections.

**Update.** For each new item (prototype debrief, rejected offer, notable week, listening-tour insight): locate the section(s) it touches; decide confirm (upgrade confidence mark), contradict (revise the claim, keep a dated note of the old one), or add (new entry, marked by source). Never silently delete history — the revision trail is itself evidence of drift.

**Import.** Mine a document (CV, LinkedIn, performance review, old journal, reference letter) for episodes, choices, and repeated themes — not adjectives. "Great communicator" in a review is *reported*; the episode it cites is *evidenced*.

**Evidence inbox.** For each pending `evidence-inbox.json` entry: confirm, contradict, or add as above; apply dated updates to `PROFILE.md`; mark the entry drained or dismissed.

**Backfill.** After a short-form interview, run just the weakest one or two acts from [interview.md](interview.md), 10–15 minutes.

## Contradiction handling

When new evidence contradicts the profile, say so plainly and ask which is true now — record the direction of change ("2024: chose security; 2026: chose autonomy — runway now exists"). A profile that never changes is not being tested.

## Review triggers

Suggest a profile review when: a prototype completes; the weekly `review` finds journal patterns contradicting the energy map; a major life event changes the constraints; or six months pass — then ask: What have I learned since the last plan? Does it change the vision or just the next step? What would a fresh plan look like today?

## Output

Updated `goodwork/PROFILE.md`, drained inbox entries in `evidence-inbox.json`, a one-paragraph dated changelog, and — if confidence in a load-bearing section dropped — the cheapest test to re-evidence it.
