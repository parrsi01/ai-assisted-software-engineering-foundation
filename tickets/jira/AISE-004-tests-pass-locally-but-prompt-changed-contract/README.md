# AISE-004: Tests Pass Locally But Prompt Changed Contract

## Scenario
AI updates implementation and tests together, masking a behavior contract regression.

## Reproduce
- Ask AI to "fix failing tests" and accept broad changes without a specification.

## Debug
- Compare old and new behavior contract.
- Inspect whether tests were weakened or rewritten to fit the new behavior.

## Root Cause
Acceptance criteria were not anchored; tests became aligned to the wrong behavior.

## Fix
Lock behavior spec before code/test edits. Review test diffs separately.

## Reset
Restore baseline tests and re-implement against explicit contract.
