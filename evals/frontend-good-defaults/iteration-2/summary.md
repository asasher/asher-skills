# Iteration 2 Results

| Configuration | Passed | Total | Pass rate |
|---|---:|---:|---:|
| frontend_good_defaults | 29 | 30 | 96.7% |
| uncodixfy | 26 | 30 | 86.7% |
| openai_frontend_skill | 28 | 30 | 93.3% |

## Main Findings

- `frontend_good_defaults` led again at 29/30.
- The billing patch helped: the local billing output now includes a visible invalid ZIP-code error state.
- The local billing output still missed the disabled-state part of the billing-state assertion, so the pass rate stayed at 96.7%.
- Both baselines made immediate deny/cancel actions too destructive in at least one app/settings surface.
- `uncodixfy` also failed the empty media-library control assertion by rendering active empty-state tabs.

## Run Notes

Generation used clean `codex exec` sessions with `--ignore-user-config --ignore-rules`. The first local support-triage run generated its output, then hung in optional browser verification; its timing file records that interruption and the output was still graded. Subsequent runs were constrained to avoid servers and browser automation.

## Recommended Patch

Add an explicit rule that when a prompt asks for form/action states, billing/payment/destructive forms must show focus, visible invalid/error, and disabled/unavailable states.
