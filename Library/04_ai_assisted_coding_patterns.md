# 04. AI-Assisted Coding Patterns

## Core Task Patterns

### Implementation
Use AI to draft code with explicit acceptance criteria and target files.

### Debugging
Use AI to reason from symptoms to evidence to hypothesis to fix.

### Refactoring
Use AI to preserve behavior while improving structure. Requires contract locking and tests.

### Test Generation
Use AI to propose test cases, but review for weak assertions and changed behavior expectations.

### Code Review
Use AI to find bugs and test gaps. Provide diff plus surrounding context for reliability.

### Documentation / Runbooks
Use AI to summarize workflows, but verify commands and path references.

## Best Practices by Pattern

- Implementation: specify non-goals
- Debugging: include exact error text and reproduction steps
- Refactoring: define invariants and performance constraints
- Test generation: require edge cases and negative cases
- Review: require severity ordering and file references

## AI Coding Loop (Reliable)

1. scope task
2. gather context
3. prompt for plan
4. implement minimal diff
5. run tests
6. review diff
7. summarize residual risk

## Common Failure Pattern

"It compiled" is treated as success. In practice, you also need behavior checks, regression tests, and sometimes security review.
