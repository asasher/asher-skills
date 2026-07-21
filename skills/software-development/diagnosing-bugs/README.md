# Diagnosing Bugs

Build a tight loop that can go red on the reported defect, minimise it, test ranked falsifiable hypotheses,
instrument only their distinguishing boundaries, fix behind regression proof, and leave no debug residue.

`SKILL.md` is the compact public contract. `reference/diagnosis.md` owns the six-phase method.
`reference/setup.md` reconciles the repo-owned `docs/agents/diagnosing-bugs.md` delta without copying the
method into the project.

## Credits

- **Relationship:** adapted.
- **Source:** Matt Pocock, [`mattpocock/skills` diagnosing-bugs](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/skills/engineering/diagnosing-bugs/SKILL.md), commit [`04fee67571bc52ac58a0e59fc4924a13f61b50a6`](https://github.com/mattpocock/skills/commit/04fee67571bc52ac58a0e59fc4924a13f61b50a6).
- **Borrowed workflow:** the tight red-capable loop; reproduction and minimisation; 3–5 ranked falsifiable
  hypotheses; prediction-targeted instrumentation; correct-seam regression proof with an explicit no-seam
  outcome; cleanup and root-cause record.
- **Local changes:** compressed the method behind a narrow public contract, removed upstream repository and
  HITL-script assumptions, added a project-delta setup branch, made unattended blocking behavior explicit,
  and defined a backlog lifecycle handoff.
- **License/notices:** upstream is MIT; the preserved notice is in [LICENSE](LICENSE) and the immutable upstream
  license is [here](https://github.com/mattpocock/skills/blob/04fee67571bc52ac58a0e59fc4924a13f61b50a6/LICENSE).
