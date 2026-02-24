# Evals and Acceptance Manual

## Why Evals Matter

Prompt quality and agent behavior degrade silently when tools, repos, or instructions change.

## Core Eval Dimensions

- correctness
- completeness
- safety / policy compliance
- actionability
- formatting adherence
- evidence quality
- test pass rate

## Eval Workflow

1. Define task families.
2. Create gold expectations or rubric-based scoring.
3. Run baseline prompts/agents.
4. Record failures and categories.
5. Iterate prompts/system policies.
6. Re-run regression suite.
