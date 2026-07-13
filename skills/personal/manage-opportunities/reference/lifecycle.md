# Opportunity Lifecycle

## Create / intake

1. Search existing Opportunities and customer/company records; update an existing pursuit instead of
   duplicating it.
2. Gather only verified identity, signal/source, customer, company, owner, opened date, links, and commercial
   values. Leave optional unknowns absent.
3. Create the note from Opportunity Contract at the lowest evidenced stage.
4. Create a concrete task through `manage-tasks`, place it once in `## Backlog`, and set `nextAction` to its ID.
5. Add reciprocal links in the configured Company and Customer maps. Link known contacts both ways.
6. Validate the workspace.

Completion criterion: one valid Opportunity exists, its active next action resolves once, every asserted
fact has evidence, and configured maps reach it.

## Log event

Append one ISO-dated line to `## Events Log` describing the material interaction, deliverable, or outcome and
linking its evidence. Update commercial summary or links only where the event changes them. Do not advance
stage unless the user requested it and the next gate is independently satisfied.

## Change stage

1. Check the requested target against Opportunity Contract's evidence gate.
2. Record the evidence and transition in `## Events Log`.
3. Update `stage`; preserve history and report any gate field still missing.
4. For `closed-won`, stop and route to Close or Promote below; it has stronger ordering.
5. Validate.

## Designate next action

1. Select or create one concrete Opportunity-origin task under the `manage-tasks` contract.
2. Ensure it has a unique stable ID and exists once in this Opportunity's `## Backlog` or under this
   Opportunity in `TODO.md`.
3. Write only that ID to `nextAction`, replacing the previous reference without duplicating either task.
4. Validate.

## Close

- **Lost:** record outcome evidence, `outcomeDate`, and `closeReason`; remove `nextAction`; write
  `stage: closed-lost`; update maps; validate.
- **Dormant:** record why and a future `reviewDate`; remove `nextAction`; write `stage: dormant`; update maps;
  validate.
- **Won without delivery:** record explicit commitment, `outcomeDate`, and `noDeliveryReason`; remove
  `nextAction`; validate all fields and maps, then write `stage: closed-won` as the final write and revalidate.
- **Won with delivery:** use [promotion](promotion.md). Do not use the ordinary stage-change path.

Completion criterion: the terminal/dormant gate is evidenced, no active next-action reference remains, maps
reflect the state, and validation passes.
