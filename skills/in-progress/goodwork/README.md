# Good Work

> **Status: in progress.** Chat-native rework: the approval server, execution ladder, and JSONL event machinery are retired; state is two files and one generated board; the interview delegates conduct to the `interview` sibling skill. Tier 1 probe evals pass 10/10 on both executors (2026-07-29, Claude subagent + gpt-5.6-sol); human field test pending. Install knowingly.

A career skill for one person, run from one folder, entirely in chat: interview the person to define what good work means for them, build the professional profile that becomes the project's state, then find, score, and work opportunities from it — with one HTML board the agent regenerates whenever the picture changes.

## Shape

- **`goodwork/PROFILE.md`** — the professional profile: track record, strengths & interests (with the positioning intersection), proof, search parameters. Every claim marked reported / evidenced / tested.
- **`goodwork/opportunities.json`** — the pipeline: one array, stages, fit scores with reasons, next actions, plain-word history.
- **`goodwork/board.html`** — a generated, self-contained projection of both; shown through the harness's native surface or opened locally. No server, ever.
- Six commands: `interview`, `profile`, `scout`, `track`, `assets`, `checkin`. Setup is implicit — the first command creates the workspace; no accounts, channels, or integrations to connect.
- The career-design frameworks (three-futures sketching, job redesign, cheap tests, positioning) inform how the agent interviews; the person hears only plain language.

## Sources

Synthesized from: Designing Your Life & Designing Your New Work Life (Burnett & Evans, Stanford Life Design Lab); Schein's Career Anchors; Holland/RIASEC & O*NET; CliftonStrengths/VIA strengths interviewing; Schwartz values; Self-Determination Theory & flow; Amabile's progress principle; the 80,000 Hours career guide; Cal Newport's _So Good They Can't Ignore You_; Gardner, Csikszentmihalyi & Damon's _Good Work_ (the three Es); Wrzesniewski's job crafting; Ibarra's _Working Identity_; ikigai (Kamiya, with the Venn-diagram caveat); Sparketype; Hendricks' Zone of Genius; Perell's personal monopoly; Kleon's _Show Your Work_; Vassallo's small bets; Dik & Duffy's calling research; _Never Search Alone_ (Terry); _The 2-Hour Job Search_ (Dalton); *What Color Is Your Parachute?\* (Bolles); weak-ties and referral evidence.

## Credits

- **Relationship:** original career-operations synthesis; interview mechanics adapted.
- **Source:** Matt Pocock's MIT-licensed [`grilling`](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/productivity/grilling/SKILL.md).
- **Borrowed:** one question at a time, hypothesis-anchored and dependency-ordered exploration, and persistent findings — now largely exercised through the `interview` sibling skill, with residual conduct rules in `reference/interviewing.md`.
- **Local changes:** built a stateful career-search operator around the interview rather than a generic grilling flow.
- **License/notices:** [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
