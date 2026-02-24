# 06. Prompt Debugging and Failure Analysis

## Prompt Debugging Mindset

When AI output is poor, do not assume the model is the only problem. Debug the full system:

- task definition
- context quality
- prompt structure
- tool access
- guardrails
- validation loop

## Failure Taxonomy

- Ambiguity: task unclear
- Scope bleed: model edits unrelated files/logic
- Hallucination: invented APIs or facts
- Format failure: wrong output structure
- Policy failure: unsafe or disallowed action proposed
- Verification failure: claims success without evidence

## Debug Procedure

1. Capture the exact prompt and context.
2. Classify the failure type.
3. Identify missing or conflicting instructions.
4. Add the smallest constraint that addresses the failure.
5. Re-run and compare.
6. Add to prompt regression tests if recurring.

## Retry Strategy (Disciplined)

Do not spam retries. Change one variable at a time:
- add file path
- add acceptance criteria
- add output format
- add validation requirement

## Advanced Topic: Prompt Drift

Teams often tweak templates informally. Small wording changes can degrade performance for other task families. This is why prompt versioning and evals matter.
