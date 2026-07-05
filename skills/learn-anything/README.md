# learn-anything

Learn any skill — not just facts. Based on Matt Pocock's [`teach`](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach)
skill, extended for skills that live in the body: accents, instruments, dance, voice acting.

The base skill is a knowledge-encoding engine — its atomic unit is the lesson. This skill keeps that as the
**teacher hat** and adds the **coach hat**, whose atomic unit is the **feedback loop**: target, trap, gap
measure, drill, progression. The agent works with a competent self-learner to engineer those loops
(including building the rig — scripts, third-party tools, physical setups), runs live rep-by-rep practice
sessions, and schedules drills using motor-learning science rather than flashcard intervals.

Install once per learning workspace. The skill is self-contained: all state lives in the workspace (drill
specs carry their own scheduling state and revision logs), nothing phones home.

## Layout

- `SKILL.md` — philosophy, the five-part loop, feedback-fidelity labels, commands, core rules
- `reference/loop-design.md` — the six-step loop-design method, tool triage, worked examples
- `reference/session-protocol.md` — live coaching: one cue per rep, agent-run interleaving, stop conditions
- `reference/motor-learning.md` — the science: stages, interleaving, faded feedback, external focus
- `reference/scheduling.md` — spaced practice for drills (not cards): cold checks, ratchets, retirement
- `reference/modality-audio.md` — the strong playbook (capture, praat/librosa, A/B loopback, ElevenLabs)
- `reference/modality-movement.md` — the honest playbook (body tests, physical rigs, human checkpoints)
- `templates/` — workspace scaffold: MISSION, drill spec, rubric, decomposition
