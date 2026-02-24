# AISE-007: Prompt Regression After Template Update

## Scenario
A prompt template change improves one task class but breaks formatting or completeness for others.

## Reproduce
- Update shared prompt template.
- Re-run only one happy-path example.

## Debug
- Run prompt eval regression set.
- Compare scores by task family.

## Root Cause
No regression suite coverage across diverse prompt tasks.

## Fix
Maintain eval set with baseline outputs and thresholds before template rollouts.

## Reset
Rollback template revision or release a patched version after re-testing.
