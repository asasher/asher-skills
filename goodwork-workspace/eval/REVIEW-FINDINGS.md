# Review Findings

- blocker: Agent calls could hang, return empty output, or fail without a run-level ERROR distinct from skill FAIL; added timeout wrappers, empty-output checks, actor private-scaffold leakage detection, ERROR metadata, and ERROR assertions payloads.
- major: Actor turns re-sent the full transcript every time; changed actor prompts to include only a bounded recent transcript tail.
- major: Judge grading did not explicitly include `personas/README.md` binary gates or emit persona-specific gate results; added README gate context, PASS/FAIL gate instructions, `persona_gates`, and aggregate persona-gate reporting.
- major: Outbound hard checks scanned the whole transcript, so actor text could create false passes or false failures; restricted sent-claim and approval/refusal checks to subject turns while leaving semantic safety gates to the judge.
- major: Suite reporting could treat judge infrastructure placeholder recall as a zero skill score and did not surface ERROR runs clearly; added run status, excluded unscoreable ERROR runs from recall statistics, and surfaced infra notes.
- minor: The one-question assertion counted raw question marks, including code, URLs, and quoted text; changed it to count cleaned question units and documented the remaining semantic limitation.
- minor: Codex invocation and CLI continuation flags were uncertain and raw Codex stdout could be noisy; verified `claude --help` and `codex exec --help`, documented the valid flags, and switched Codex calls to `--output-last-message` with `--color never`.

## Open questions

None.
