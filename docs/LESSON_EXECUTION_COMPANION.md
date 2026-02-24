# AI-Assisted Software Engineering Lesson Execution Companion (Slow-Learning Edition)

Author: Simon Parris + Codex companion notes  
Date: 2026-02-24

Use this while coding in one terminal and reading in another.

## How to Use This Companion

For each module:

1. Read `What this lesson is`
2. Read `Why this matters`
3. Use the `Companion prompt`
4. Do one small task only
5. Capture evidence before continuing

## Lesson 1: Foundations (`docs/foundations/FOUNDATIONS_GUIDE.md`)

### What this lesson is

How LLMs work at the level needed by engineers: tokens, context windows, sampling, capabilities, and limits.

### Why this matters

If you do not understand model limits, you will misdiagnose failures as "bad prompting" when the issue is context or verification.

### Companion prompt

`Explain what part of the LLM pipeline matters for this task (tokens, context, sampling, tool use, or verification), and what failure I should expect if I ignore it. Use beginner definitions.`

### Do this now

- Read `Library/01_ai_foundations_and_llm_basics.md`
- Write a 5-line summary of token/context window/model/tool distinction

### Stop condition

You can explain why a model can be fluent and still wrong.

## Lesson 2: Prompt Software Engineering (`docs/prompt_engineering/PROMPT_SOFTWARE_ENGINEERING_MANUAL.md`)

### What this lesson is

Turning prompts into structured task specs with constraints and acceptance criteria.

### Why this matters

Strong prompts reduce rework, unsafe actions, and vague output.

### Companion prompt

`Rewrite my request into a production-grade engineering prompt with role, task, constraints, evidence requirements, and acceptance criteria. Explain each field.`

### Do this now

- Compare `prompts/templates/task_prompt_template.md` and `prompts/templates/code_review_prompt_template.md`
- Rewrite one vague prompt into a structured prompt

### Stop condition

You can identify what information is missing from a vague coding prompt.

## Lesson 3: Agent Engineering (`docs/agent_engineering/AGENT_ENGINEERING_MANUAL.md`)

### What this lesson is

Designing tool-using, policy-constrained coding agents.

### Why this matters

Agents fail in ways that look like coding bugs but are often planning, state, or permission bugs.

### Companion prompt

`Map this agent task into plan -> tool calls -> state updates -> verification -> final response. Identify where the agent can fail and what guardrail prevents each failure.`

### Do this now

- Run the starter agent lab
- Inspect its generated plan and safety mode behavior

### Stop condition

You can separate agent policy failures from model reasoning failures.

## Lesson 4: Evals (`docs/evals/EVALS_AND_ACCEPTANCE_MANUAL.md`)

### Companion prompt

`Design a regression eval for this coding prompt: define test cases, expected outputs, scoring dimensions, and pass/fail thresholds.`

## Lesson 5: Security & Governance (`docs/security/SECURITY_GOVERNANCE_MANUAL.md`)

### Companion prompt

`Explain the security and compliance risks in this AI-assisted coding workflow, then recommend the minimum guardrails that preserve productivity.`
