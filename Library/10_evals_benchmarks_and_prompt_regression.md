# 10. Evals, Benchmarks, and Prompt Regression

## Why Evals Exist

AI-assisted engineering workflows change often (prompt templates, model versions, tool configs, repos). Evals detect silent regressions.

## Eval Types

- Exact-match checks (for structured outputs)
- Rule-based checks (required fields, formatting)
- Rubric scoring (correctness, actionability, safety)
- Execution-based evals (tests compile/run)
- Human review sampling (high-risk outputs)

## Prompt Regression Testing

When a prompt template changes, re-run the same task set and compare outcomes.

Track:
- pass rate
- major failures
- safety violations
- average rework required
- formatting compliance

## Benchmark Overfitting Risk

If the team iterates only on a static prompt set, performance may improve on the benchmark while real-world quality declines.

Mitigations:
- holdout tasks
- adversarial cases
- periodic task refresh
- production telemetry sampling

## Enterprise Use

Treat prompt/eval artifacts like code:
- version them
- review changes
- record results
- gate rollouts
