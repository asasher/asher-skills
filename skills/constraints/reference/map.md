# map — pin the goal, draw the flow, gather the evidence

You are opening the investigation. The deliverables are the **Goal** and **Map** sections of `constraint.html`.
This is a conversation, not a form: one question at a time, anchored with your working hypothesis, and anything
the record already shows (a repo, a dashboard, a linked doc, an earlier session) is read, not asked.

## Part 1 — the goal (section: Goal)

Without a goal there is no constraint; with a vague goal, every annoyance becomes one.

1. **The system.** What are we studying, and where are its edges? One value stream per page — if the user
   describes two flows with no shared output ("the agency work and my course business"), say so and split them
   into separate systems (`new` again later).
2. **The goal.** "What is this system *for* — what should there be more of?" Push past mission-statement fog to
   direction: more revenue, more shipped features, more published essays, more closed care plans.
3. **The throughput unit.** The load-bearing question: *"What unit of valuable output could we count per week
   and both agree the number means the system got better?"* A good unit is countable, valuable at the point of
   delivery (not "PRs opened" — "PRs in production"), and moves when the goal moves. Offer a candidate rather
   than asking cold: "For this I'd count *signed engagements per month* — right, or is it something else?"
4. **Necessary conditions.** What must not be sacrificed while throughput rises — quality floor, cash floor,
   health, key relationships, compliance. These become experiment guardrails later.

*Done when:* the throughput unit is written in bold in the Goal section and the user has confirmed it in their
own words. Set Goal to `done`, Map to `active`.

**Wrong-lens check before continuing:** if the goal is genuinely contested between stakeholders, or the honest
answer is "I don't know what I'm building yet" (exploration, unknown product-market fit) — say ToC isn't the
lens yet, name what is (goal alignment; discovery/small-bets), log it, and stop gracefully.

## Part 2 — the flow map (section: Map)

Map how a unit of value actually travels from demand to done — the *real* current flow, not the org chart or
the aspirational process.

1. **Walk one item.** "Take the last [unit] that completed — walk me through every state it passed through,
   including the waits." Waits are stages: "sits in the review queue" is a node.
2. **Draw it live.** After the walk, render the Mermaid `flowchart LR` in the Map section (conventions in
   [artifact.md](artifact.md)) and show it back: "Here's the flow as I heard it — what's missing?" The diagram
   is the anchor for every correction; users spot a missing stage on a picture far faster than in prose.
3. **Typical shapes** to offer as starting skeletons, not to impose: software delivery — idea → spec/decision →
   build → review → test/CI → deploy → validated in prod. Small business — stranger → lead → conversation →
   proposal → close → fulfill → paid/renewed. Solo work — idea → committed → drafted → finished → published →
   feedback.

## Part 3 — the three scans (section: Map, scan table)

Now annotate the map with evidence. Run three scans, each a couple of questions, and convert every answer to an
observable before recording it (opinion → number/episode; the hierarchy is in
[framework.md](framework.md)):

- **Queue scan** — "Where does work wait longest? Where does it pile up? What's the oldest item right now, and
  where is it sitting? What gets expedited most often?"
- **Scarcity scan** — "What do you always run out of? Whose calendar decides whether work moves? If one person
  vanished for two weeks, what would stop? What do people avoid using because it's hard to book?"
- **Policy scan** — "What rule causes good work to wait? What approval exists because of an old failure? What
  metric rewards being busy over finishing? What decision keeps getting escalated?"

For each hit: a scan-table row (finding · observable · source cite) and, where it's a queue, the count/wait
annotated onto the flow-map node with `:::queue`. If the user has real data (PR dashboards, CRM, analytics,
ticket ages), ask for an export into `sources/` — five minutes of data beats an hour of recollection. If data is
thin, record the concrete-episode version ("last Tuesday the release waited three days for sign-off") and mark
it accordingly.

*Done when:* the flow map renders with at least the queue scan annotated, and the scan table has entries from
all three scans (or an explicit "clean" note per scan). Set Map to `done`, Find to `active`, and hand off to
[find.md](find.md) — usually in the same session while context is warm.
