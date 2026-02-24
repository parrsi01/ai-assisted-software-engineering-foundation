# 05. Verification, Testing, and Trust

## Principle

Trust in AI-assisted coding should be earned through evidence, not intuition.

## Evidence Types (Strong to Weak)

- passing tests covering changed behavior
- integration or end-to-end validation
- static analysis / lint results
- code review findings cleared
- reasoning explanation only (weakest)

## Verification Stack

- Syntax correctness
- Type/interface correctness
- Behavioral correctness
- Regression safety
- Security and policy compliance

## Hallucination Containment Strategies

- require citations to files/symbols
- ask for uncertainty statements
- run commands/tests before finalizing
- compare outputs against known contracts
- use review prompts to challenge assumptions

## Test Risks with AI-Generated Tests

- overly broad mocking
- weak assertions
- test rewrites that hide regressions
- asserting implementation details instead of behavior

## Acceptance Criteria Design

Good acceptance criteria are:
- observable
- testable
- bounded
- tied to user/system outcomes

Example:
"Parser rejects malformed IDs with `ValueError` and existing valid IDs continue to pass current tests."
