# AISE-005: Code Review Agent Misses Regression

## Scenario
Review agent approves a patch but misses an edge-case regression because diff-only context hid related code.

## Reproduce
- Run review with only partial diff and no failing scenario description.

## Debug
- Inspect review context scope.
- Add neighboring files/tests and re-run review.

## Root Cause
Insufficient review context and no regression checklist.

## Fix
Use a review template requiring risk areas, edge cases, and test-gap analysis.

## Reset
Re-review with expanded context and rerun tests.
