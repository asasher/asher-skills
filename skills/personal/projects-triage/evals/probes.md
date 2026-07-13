# Projects Triage - situated probes

Run with `SKILL.md` and the triage protocol. Require file-and-sentence citations.

## Probes

**P1 - Opportunity repository.** `Opportunities/Acme.md` has a resolvable `workspacePath` containing a local
backlog skill. Is it dispatched?

**P2 - Project workspacePath.** A Project note has `workspacePath` but no `localPath`. Is it eligible?

**P3 - duplicate ownership.** Two Project notes name the same `localPath`. How many workers run and what is
reported?

**P4 - no isolation primitive.** The harness cannot create workers. Is a background shell acceptable, and
what is the fallback?

**P5 - no local skill.** A valid Project path lacks the `backlog` skill at both its primary and alias installed
skill mounts.
What terminal status must it receive?
