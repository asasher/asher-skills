# Frontend Good Defaults Eval Runbook

Evaluate three configurations:

- `frontend_good_defaults`: local `skills/frontend-good-defaults`
- `uncodixfy`: `https://github.com/cyxzdev/Uncodixfy`
- `openai_frontend_skill`: OpenAI frontend skill from the GPT-5.4 frontend design blog

## Method

1. Create a fresh `iteration-N/` directory.
2. For each eval in `evals.json`, run the same prompt once per configuration in a clean context.
3. Save each run to:
   `iteration-N/<eval-id>/<configuration>/outputs/`
4. Record timing data in:
   `iteration-N/<eval-id>/<configuration>/timing.json`
5. Grade every assertion with `PASS` or `FAIL` and concrete evidence in:
   `iteration-N/<eval-id>/<configuration>/grading.json`
6. Aggregate pass counts in:
   `iteration-N/benchmark.json`
7. Human-review the actual outputs and save actionable notes in:
   `iteration-N/feedback.json`

Use separate sessions or subagents for clean-context runs. Do not let one configuration see another configuration's output.

## Run Prompt Template

```text
Execute this frontend task in a clean workspace.

Configuration: <configuration-id>
Skill: <local path or pasted skill source>
Task: <eval prompt>

Save all generated files to:
evals/frontend-good-defaults/iteration-1/<eval-id>/<configuration-id>/outputs/

When done, include:
- changed file list
- local run instructions
- any verification performed
```

## Grading Prompt Template

```text
Grade this frontend eval.

Eval id: <eval-id>
Configuration: <configuration-id>
Expected output: <expected_output>
Assertions:
<assertions>

Review the generated files and screenshots if available.
Return JSON:
{
  "eval_id": "...",
  "configuration": "...",
  "assertions": [
    {
      "assertion": "...",
      "status": "PASS|FAIL",
      "evidence": "Specific file, CSS selector, visible text, screenshot observation, or behavior."
    }
  ],
  "summary": "Short assessment."
}
```

## Benchmark Shape

```json
{
  "iteration": 1,
  "configs": {
    "frontend_good_defaults": {
      "passed": 0,
      "total": 0,
      "pass_rate": 0
    },
    "uncodixfy": {
      "passed": 0,
      "total": 0,
      "pass_rate": 0
    },
    "openai_frontend_skill": {
      "passed": 0,
      "total": 0,
      "pass_rate": 0
    }
  },
  "patterns": []
}
```
