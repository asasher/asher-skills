# Artifact patterns

Read the section that matches the requested artifact. Use more than one section for a mixed document.

## README introduction

Answer four questions in this order:

1. What is the product or component?
2. What concrete problem does it solve?
3. How does it solve that problem at a useful level of detail?
4. What should the reader do next?

Name behavior instead of qualities. Replace claims such as easy integration or sensible defaults with the supported interface, default, or setup step.

## API reference

Give the contract before commentary:

1. Purpose and scope.
2. Signature, endpoint, or event name exactly as implemented.
3. Parameters, types, units, defaults, and constraints.
4. Return value or response shape.
5. Errors, status codes, retry behavior, and side effects.
6. one minimal valid example and one important failure example.

Keep identifiers exact. Do not rename an awkward field to improve the prose. State whether an omission, empty value, and explicit default have different behavior.

## Getting-started guide

Move the reader to one verified result:

1. State the result.
2. List prerequisites and supported versions.
3. Install.
4. Configure the minimum required values.
5. Run one command or request.
6. Show the expected result.
7. give recovery steps for the most likely failure.

Put commands in code blocks and explanations outside them. Do not hide required setup in a later note.

## Procedure or runbook

Use this order:

1. Trigger and scope.
2. Prerequisites, permissions, and hazards.
3. Numbered actions with one action in each step.
4. Expected observation after each irreversible or high-risk action.
5. Completion check.
6. rollback or escalation path.

Put each condition before its command. Do not combine separate actions with `and` unless they must occur simultaneously.

## Error message

Give the reader:

1. What failed.
2. The known cause or violated limit.
3. The current state and whether work was saved.
4. The exact recovery action.
5. the wait time, retry condition, or support reference when applicable.

Do not blame the reader. Remove generic statements about fairness, security, or reliability unless they change the recovery action.

## Deprecation notice

Name the deprecated item, the effective version or date, the replacement, and the removal behavior. Give a migration action and link to the applicable guide. Distinguish deprecated, disabled by default, and removed.

## Pull-request description

Use evidence, not ceremony:

1. Problem and affected behavior.
2. Change made.
3. Important implementation or compatibility decision.
4. Verification performed.
5. risk, rollout, migration, or follow-up.

Do not restate the title. Do not claim that the change is clean, comprehensive, or production-ready. Show the checks and remaining limits.

## Release note

State what changed, who is affected, and what action is required. Include the first affected version and any compatibility boundary. Omit implementation detail that does not change use.

## Safety instruction

Use the risk class required by the governing policy. Start with a clear command or condition, then state the hazard and possible result. Preserve approved legal wording and route any change in risk classification to the responsible subject-matter owner.
