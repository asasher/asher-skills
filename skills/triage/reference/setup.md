# Setup

Scaffolds the project playbooks the loop depends on, then offers to install the external skills they can defer to. Run once per repo, and again to add any missing playbook.

## Steps

1. Scaffold the playbooks.
   - For each file in this skill's `templates/`, write it to `docs/agents/<name>.md` in the target repo.
   - Skip any playbook that already exists. Never overwrite without explicit confirmation.
   - Completion criterion: every template exists at `docs/agents/`, either freshly written or already present and left untouched.

2. Tailor to the repo (optional but encouraged).
   - The templates are baselines. Offer to fill each with this repo's real check commands, branch conventions, plan format, and review criteria.
   - Completion criterion: the user has chosen to tailor now or keep the baselines.

3. Offer external skills.
   - The playbooks may defer to installed skills. Offer to install the matching ones and tell the user the exact command, e.g.:
     - `diagnosing-bugs`, `tdd` — `npx skills@latest add mattpocock/skills --skill diagnosing-bugs tdd`
   - Install only what the user approves.
   - Completion criterion: the user has chosen which external skills to install, and approved installs have run.

4. Confirm readiness.
   - Report which playbooks exist and which external skills are installed.
   - Completion criterion: the user can run `triage` knowing every branch has its playbook.
