# profile — view, update, or import evidence without a full interview

The Good Work Profile (`goodwork/PROFILE.md`, schema in [framework.md](framework.md)) is a living document. This command maintains it between interviews.

## Modes

**View.** Summarize the snapshot, the confidence distribution (how much is reported vs. evidenced vs. tested), and the staleness (last updated, what's changed in their situation since). Flag the weakest sections.

**Update.** The user brings new information — a prototype debrief, a rejected offer, a great or terrible week, a listening-tour insight. For each item:
1. Locate which profile section(s) it touches.
2. Decide: does it confirm (upgrade confidence mark), contradict (revise the claim, keep a dated note of the old one), or add (new entry, marked by source)?
3. Never silently delete history — the trail of revisions is itself evidence of drift.

**Import.** Mine a document (CV, LinkedIn, performance review, old journal, reference letter) for profile evidence. Extract episodes, choices, and repeated themes — not adjectives. A performance review saying "great communicator" is *reported*; the episode it cites is *evidenced*.

**Backfill.** After a short-form interview, pick the weakest one or two sections and run just those acts from [interview.md](interview.md) — same mechanics, 10–15 minutes.

## Contradiction handling

When new evidence contradicts the profile, say so plainly and ask which is true now — people change, and the profile should record the direction of change ("2024: chose security; 2026: chose autonomy — runway now exists"). A profile that never changes is not being tested.

## Review triggers

Suggest a profile review (not necessarily a full interview) when:
- A prototype or experiment completes (`prototype` debrief).
- The weekly `review` finds journal patterns contradicting the energy map.
- A major life event changes the constraint section (move, visa, family, health, runway).
- Six months pass — run the annual-review questions: What have I learned since the last plan? Does it change the vision or just the next step? If I were making a fresh plan today, what would it be?

## Output

Updated `goodwork/PROFILE.md`, a one-paragraph changelog at the bottom of the file (dated), and — if confidence in a load-bearing section dropped — a proposed cheapest test to re-evidence it.
