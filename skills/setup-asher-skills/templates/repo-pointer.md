<!-- Seed for the repo pointer. setup writes this alongside the `## Agent skills` block (in the same
     memory file, or as a short note the block links). It records where the skills come from and how to
     update them. No version stamp — reconciliation is the LLM audit that `setup-asher-skills` (audit
     mode) runs. -->

<!-- skills source: https://github.com/asasher/asher-skills -->

> **Skills source.** The agent skills in this project come from
> [asher-skills](https://github.com/asasher/asher-skills) and are installed with
> `npx skills add https://github.com/asasher/asher-skills --skill <name>` (add `-g` only for `staffing`).
> All skills come from this repo; external ideas are adapted and shipped here rather than installed from
> elsewhere. To add a skill, adjust scope, or reconcile drift, re-invoke `setup-asher-skills`.
