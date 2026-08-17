# Roster seed

> **A seed, not a roster.** `staffing setup` reads this file once, when it writes the project's staffing playbook, and never again — resolution reads the playbook alone. Values here are starting points for the judgment numbers; the owner tunes them, drops models this machine cannot reach, and adds reachable models the seed omits. Never resolve from this file at runtime.
>
> Doctrine is not seeded: resolution rules live in the skill's routing reference, command shapes in its harness reference. This file carries data only.

## Models

Higher is better on every column; a higher affordability score means cheaper to run. Effort is the model's default dispatch level where the harness exposes one.

| model         | affordability | intelligence | taste | effort |
| ------------- | ------------: | -----------: | ----: | ------ |
| gpt-5.6-sol   |             4 |            9 |     5 | high   |
| gpt-5.6-terra |             6 |            5 |     3 | xhigh  |
| sonnet-5      |             5 |            5 |     5 | high   |
| opus-5        |             3 |            7 |     7 | high   |
| fable-5       |             1 |            9 |     9 | high   |

Default taste bar for user-facing UI, copy, or API design: taste ≥ 7 on this scale.

## Pins

- mechanical / bulk → gpt-5.6-sol through the sibling CLI worker route.

## Capability routes

| need | route (default declaration) | fallback / hard edge |
| --- | --- | --- |
| browser-use | scripted Playwright driving Chrome — verification is a script with artifacts, headed or headless | harness-native web bindings for interactive exploration only, never the default; a signed-in-session need is a per-use, explicit-consent handoff to the user's own browser |
| computer-use | gated: a concrete use case recorded in the project's environment playbook **and** explicit user approval | none — an unmet gate is a hard capability gap; never fall back to the user's browser or desktop |
| imagegen | the machine's installed image-generation skill/tool, named at setup | none by default — declare one at setup or report the gap |
