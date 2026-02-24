# AISE-010: Eval Suite Gives False Confidence

## Scenario
Eval scores look strong because prompts were tuned to the benchmark examples only.

## Reproduce
- Optimize prompt against a small static test set.
- Skip adversarial or out-of-distribution cases.

## Debug
- Add unseen tasks and perturb existing test cases.
- Compare score drop and failure patterns.

## Root Cause
Benchmark overfitting and weak task diversity.

## Fix
Expand eval coverage, refresh holdout sets, and track failure categories.

## Reset
Re-baseline scores using a broader suite.
