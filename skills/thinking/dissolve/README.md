# Dissolve

`dissolve` takes a confusing question or contested concept and **dissolves** it — instead of picking a side, it
deconstructs the mental algorithm that makes the question feel unanswerable, until the confusion is gone. Based
on Yudkowsky's [*Dissolving the Question*](https://www.lesswrong.com/posts/Mc6QcrsbH5NRXbCRX/dissolving-the-question)
and Scott Alexander's [*Diseased Thinking*](https://www.lesswrong.com/posts/895quRDaK6gR2rM82/diseased-thinking-dissolving-questions-about-disease).

The five moves:

1. **Pose & find the itch** — what makes this *feel* like a hanging question.
2. **Taboo the word** — ban the loaded term; where you can't restate it, the confusion is located.
3. **Stack-trace & unbundle** — trace the algorithm generating the question; split it into its real sub-questions.
4. **Anticipate** — reduce each sub-question to what you'd expect to observe; empty ones dissolve.
5. **Resolve & gate** — check with the human that no lingering confusion remains.

## Model

You (the human) hold the confusion; the agent holds the method. It's a **stateful, resumable** practice: the
whole state — thinking, diagrams, discussion, sources — lives in **one self-contained `dissolution.html`** that
is also the shareable artifact. No build step, no separate state file.

- **One workspace, one folder per question.** Install the skill once at a workspace root. Each question is its
  own folder — `<slug>/dissolution.html` + `sources/` — self-contained and shareable on its own.
- **Sources** that can't sit inline go in `sources/` and are cited in the page as `[n]`.

## Usage

```bash
npx skills add <repo-url> --skill dissolve
```

```text
dissolve new "Is addiction a disease?"     # scaffold a folder and begin
dissolve                                    # inside a folder: resume where it stands
dissolve                                    # at the workspace root: list dissolutions
```

Open any `dissolution.html` in a browser to read or share the current state.
