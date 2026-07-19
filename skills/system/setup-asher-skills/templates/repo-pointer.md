<!-- Seed for the repo pointer. setup writes this alongside the `## Agent skills` block (in the same
     memory file, or as a short note the block links). It records where the skills come from and how to
     update them. No version stamp — reconciliation is the LLM audit that `setup-asher-skills` (audit
     mode) runs. -->

<!-- skills source: https://github.com/asasher/asher-skills -->

> **Skills source.** The agent skills in this project come from
> [asher-skills](https://github.com/asasher/asher-skills) and are installed with
> `npx skills add https://github.com/asasher/asher-skills --skill <name>` (add `-g` only for `staffing`).
> A selected skill may declare a provenance-checked external
> skill or Codex plugin; those require separate disclosure and consent and are recorded in the consumer's
> `external-dependencies.lock.json`. Undeclared external requests are not auto-installed. To add a skill,
> adjust scope, or reconcile drift, re-invoke `setup-asher-skills`.
