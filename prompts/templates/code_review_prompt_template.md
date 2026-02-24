# Code Review Prompt Template

## Objective

Review changes for bugs, regressions, risks, and missing tests.

## Inputs

- Diff: <paste or file refs>
- Expected behavior: <summary>
- Constraints: <perf/security/compat>

## Review Priorities

1. correctness
2. behavioral regression
3. edge cases
4. test gaps
5. security concerns

## Output Format

- Findings ordered by severity with file references
- Open questions / assumptions
- Brief summary
