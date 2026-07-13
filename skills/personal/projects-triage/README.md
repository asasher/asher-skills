# Projects Triage

Orchestrates each eligible Project repository's own backlog workflow. Target selection is strict: only Project
known-home notes and their `localPath` field qualify. Opportunity `workspacePath` values never enter the scan.

## Source

Adapted from the installed `projects-triage` workspace skill with the Project/Opportunity boundary made
explicit.
