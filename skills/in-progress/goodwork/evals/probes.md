# Goodwork chat-native rework — situated dry-run probes

Method (per `docs/agents/probe-evals.md`): situated probes against executor models — a Claude subagent in-session plus `codex exec --sandbox read-only` (dual-executor, both directions independently fallible). Context per probe: **[S]** = SKILL.md only; **[S+R]** = SKILL.md plus only the named reference. Executors must cite the file and exact sentence that decided each answer; flagging genuine ambiguity is a valid answer and a valuable finding. Grade pass/fail against `key.md`, which was written before any runs and must never appear in executor context.

## Probes

**P1 [S].** A session opens in a project with an existing `goodwork/PROFILE.md`. The user's entire message is "goodwork". What do you do?

**P2 [S].** User: "goodwork track — move Acme to applied". The project has no `goodwork/PROFILE.md`. What is your next concrete action?

**P3 [S].** You drafted an outreach message and the user replied in chat: "looks good, send it." What happens between that reply and the message leaving, and what gets recorded where?

**P4 [S+R opportunities.md].** A posting lists 8 must-have requirements; the profile has evidenced support for 4. The user is excited and says "just tailor it harder." What do you do?

**P5 [S+R interviewing.md].** A new user with no workspace says "I have no idea what I should do with my life." Name the command you run, the sibling skill involved and what it owns versus what this skill's reference owns, and give the first two sentences you would actually say to the user.

**P6 [S+R interviewing.md].** You are two acts into the interview; the user sounds tired but engaged. What do you do with the workspace and the board at this point, and why?

**P7 [S+R board.md].** The user asks "show me where everything stands." The session is a bare terminal with no artifact or preview surface. What do you do — and what do you never do?

**P8 [S+R profile.md].** A prototype-style debrief contradicts the profile: the person said they wanted to manage, but shadowing a manager for a week drained them badly. What exactly changes in `PROFILE.md`, and what must be preserved?

**P9 [S].** During setup the user asks: "should I connect my email and LinkedIn so you can track replies automatically?" What do you answer, and what do you offer instead?

**P10 [S+R opportunities.md].** At `checkin`: 12 applications over three weeks, zero screens, outreach replies healthy. What single change do you recommend first, and what do you explicitly not do this week?

## Scoring

10 probes × executors. A probe passes only with the correct action AND a correct citation. Ambiguity flags count as findings, not failures — they feed the next wording pass.
