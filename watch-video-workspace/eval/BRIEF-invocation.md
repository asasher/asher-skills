# Brief: watch-video invocation probes

You are an agent harness deciding which skill (if any) to invoke for a user
message. Judge ONLY from the skill descriptions below — do not open any
files. For each message M1–M5, answer: the skill name that should fire, or
"none", plus one line of reasoning. If a message is a genuinely close call,
say so — that is a valid finding.

## Available skill descriptions

- **watch-video**: Watch a video by reading contact sheets — tiled,
  timestamped frame grids sized for a vision model. Use when the user shares
  a video, clip, or screen recording and asks anything about its content
  (what happens, summarize, find a moment, verify a flow or bug on screen),
  or when another skill needs to understand video.
- **eloquent**: Use when the user wants help with resumes, CVs, ATS
  optimization, resume bullets, job description analysis, resume tailoring,
  cover letters, LinkedIn profiles, interview prep, salary negotiation,
  offer comparison, references, portfolios, academic CVs, executive resumes,
  technical resumes, creative resumes, career changes, or resume version
  management.
- **dissolve**: Take a confusing question or contested concept and dissolve
  it — deconstruct the mental algorithm that makes it feel like a question,
  taboo the loaded word, and unbundle the disguised sub-questions. Use for
  "what is X really?" puzzles, definitional deadlocks, and stuck conceptual
  arguments.
- **smallbets**: Use when the user wants help with early-stage business
  ideas, founder strategy, community selection, idea validation,
  manual-first MVPs, first customers, pricing, content marketing,
  sustainable growth, or bootstrapping.
- **learn-anything**: Learn any skill — not just facts. Pairs teaching
  (knowledge into the head) with coaching (skill into the body). Decompose a
  skill, engineer honest feedback loops, build the rig, run live practice
  sessions rep by rep, schedule spaced drills. For embodied skills as much
  as cerebral ones.

## Messages

**M1.** "here's a .mov of the bug happening — can you find where it goes wrong?"
**M2.** "this demo video is 80MB, can you compress it so I can email it?"
**M3.** "summarize this podcast mp3 for me"
**M4.** "I recorded my screen while the app froze — tell me what I clicked right before it happened"
**M5.** "teach me video editing"
