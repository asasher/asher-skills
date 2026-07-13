# Categorized source layout and clean-install proof

Date: 2026-07-13

`npx skills add . --list` discovered 25 public skills at exactly
`skills/<category>/<name>/SKILL.md`; it omitted the then-internal `smallbets`. The canonical compiler
discovered all 26 sources exactly once and preserved every frontmatter name. `smallbets` was subsequently
archived at `b11bb2a` and deleted under [issue #58](https://github.com/asasher/asher-skills/issues/58), leaving
25 public sources.

Clean git fixtures then compiled the root closure and passed the ordered names to one atomic install command
per scope. Each expected flat `.agents/skills/<name>/SKILL.md` landed:

```text
system   staffing  closure=[staffing]                                      installed=1 missing=0
delivery backlog   closure=[diagnosing-bugs review-loop staffing plan
                            prototype backlog]                             installed=6 missing=0
creative maquette  closure=[review-loop maquette]                          installed=2 missing=0
thinking bayes     closure=[bayes]                                         installed=1 missing=0
personal goodwork  closure=[goodwork]                                      installed=1 missing=0
```

The backlog and maquette fixtures prove dependencies cross category boundaries while installed directories
remain flat. A preliminary sequential-command probe exposed that repeated single-skill `npx skills add`
calls can replace earlier selections from the same source; `setup-asher-skills` now batches the existing
scope plus new closure atomically and invokes owner setup branches dependency-first afterwards.

`skills/source-migration.json` accounts for every old flat source. A validator scans repository-authored text
for old flat paths outside that map and checks the root README's category/invocation/execution rows against the
generated catalog.
