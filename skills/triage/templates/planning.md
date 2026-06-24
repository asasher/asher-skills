# Playbook: Planning Enhancements

> Project playbook for this repo. The triage `plan` subskill reads this file. Tailor the threshold, format, and location to this team's conventions.

## Plan-size threshold

Write a plan when any of these hold; otherwise skip planning and implement directly:

- The change touches more than one subsystem or public interface.
- It needs new data models, migrations, or external dependencies.
- It is risky, hard to reverse, or affects more than ~1 day of work.

_Adjust these triggers to this team._

## Plan format and location

- Location: `plans/<issue-number>-<slug>.md` (or this repo's convention: _<add yours>_).
- A plan covers: user stories, definition of done, evidence required, implementation outline, risks, and test plan.
- Use diagrams or code blocks only when they make the plan clearer.

## Approval

- Plans require human approval before implementation. Note who approves and how: _<add yours>_.
- If approval changes scope, update the plan before coding.
