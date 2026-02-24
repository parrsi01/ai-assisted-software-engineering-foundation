# 02. Prompt Software Engineering Fundamentals

## Definition

Prompt software engineering is the practice of designing prompts like executable task specifications: explicit inputs, constraints, outputs, and acceptance criteria.

## Prompt Structure (Production-Grade)

1. Role / mode
2. Objective
3. Context (files, environment, constraints)
4. Requirements / acceptance criteria
5. Safety boundaries
6. Output format
7. Validation expectations

## Why This Works

LLMs infer missing details. Strong prompts reduce the amount of missing detail.

## Prompt Quality Dimensions

- Specificity: does the model know exactly what task to perform?
- Scope control: does it know what not to touch?
- Verifiability: can the result be checked objectively?
- Safety: are risky actions constrained?
- Reusability: can the prompt template be reused with parameter changes?

## Example Transformation

Vague: "Fix my tests."

Structured:
- target file paths
- failing test output summary
- desired behavior contract
- non-goals
- command to run for validation

## Anti-Patterns

- Combining brainstorm + implementation + deployment in one prompt
- No acceptance criteria
- No file references
- No validation command
- Asking for "best" solution without constraints (performance, security, style)

## Advanced Pattern: Prompt Layering

Split prompts by purpose:
- planning prompt
- implementation prompt
- review prompt
- verification prompt

This reduces instruction conflicts and improves auditability.
