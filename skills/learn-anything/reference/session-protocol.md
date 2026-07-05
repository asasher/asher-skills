# The live practice session

Read this when running `session`. The agent is *in the loop*: it assembles the set, runs the reps, delivers
the cues, decides the switches, and writes the log. The learner's job is to perform; yours is everything else.

## Before

1. **Assemble the set** from drill state (`reference/scheduling.md`): 2–4 drills due, interleaved, plus at
   most one stretch drill slightly past current level. Tell the learner the set and roughly how long.
2. **Rig check** — one command. Capture works, playback works, exemplar loads. A session that starts with
   ten minutes of debugging teaches the learner not to start sessions; if the rig is broken, fixing it *is*
   today's session and the practice reschedules.
3. **Warm-up** inside the skill (easy reps of a mastered drill), not beside it.

## The rep loop

```
rep → capture → score → ONE cue → rep
```

- **One cue per rep, maximum.** Working memory during motor execution holds about one item. Five corrections
  at once is the classic coaching failure; bank the others for later reps.
- **External focus beats internal.** Cue the effect in the world — "land the note on the click", "throw the
  sound at the back wall", "push the floor away" — not the body part ("tense your soft palate", "bend your
  knee more"). Reach for internal cues only when an external one has failed twice.
- **Sometimes the cue is silence.** In later reps of a block, withhold feedback deliberately and ask the
  learner to self-score first — faded feedback is how the loop transfers into their own head (see
  `reference/motor-learning.md`). Compare their score to the measure's; the gap between those two numbers is
  its own curriculum.
- **Respect the latency budget live.** If scoring a rep starts taking longer than doing one, drop to
  sampling (score every Nth rep, body-test the rest) rather than stalling the loop.

## Switching and difficulty — the agent decides

Learners left alone block-practice what already feels good. You run the interleaving:

- **Switch drills** on a schedule the learner doesn't control — after a fixed rep count or when two clean
  reps land, whichever comes first. Switching *before* it feels settled is the point.
- **Ratchet difficulty** when the criterion is met within the session (tempo up, phrase longer, context
  noisier). **Un-ratchet without ceremony** when three reps in a row fail — difficulty is a dial, not a rank.
- **Stop conditions.** Quality dropping across three consecutive reps means fatigue is now training the
  error: end the block or step down. Ending a session early with clean last reps beats grinding into a
  groove-in. Say this out loud so the learner learns the rule too.
- **Expect it to feel worse than blocked practice.** Interleaved, variable, feedback-faded sessions depress
  in-session performance and improve retention. Warn the learner once per workspace, then remind them when
  they chase the feeling of fluency.

## After

1. **Log to `practice-log/`**: date, drills run, reps, scores, cues that landed, plus **one line of
   subjective notes** from the learner ("jaw tension", "easier after the third block"). The subjective line
   catches what the metrics miss.
2. **Update drill state** in each drill file: score history, last-practiced, stage or criterion changes.
3. **Harvest if the loop itself failed** — a latency violation, a rubric that stopped discriminating, a
   drill too big. One line to `LEARNINGS.md` about the *design*, not the learner.
4. **Name the next session's likely set** in one sentence, so the learner ends knowing what's coming.
