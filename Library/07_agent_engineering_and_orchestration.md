# 07. Agent Engineering and Orchestration

## What Is an Agent (Engineering Definition)

An agent is an LLM-based system that can plan, use tools, track state, and iteratively act toward a goal under policies and constraints.

## Agent Components

- Model (reasoning/generation)
- System policy (rules/behavior)
- Tool interface (shell, file edit, search, tests)
- State store (task state, prior outputs, checkpoints)
- Planner/executor loop
- Verifier/evaluator
- Human approval gates

## Single-Agent vs Multi-Agent

### Single-Agent
Simpler to build and debug. Good for small coding tasks.

### Multi-Agent
Better role separation (planner, implementer, reviewer), but adds orchestration complexity and schema/handoff failure risks.

## Planning Patterns

- upfront plan then execute
- incremental plan per step
- plan-review-execute loops
- tool-first reactive loops

## Agent Failure Modes

- bad decomposition
- infinite/long loops
- stale state
- wrong tool choice
- missing permissions
- fake completion (done without verification)

## Engineering Controls

- max step limits
- command guardrails
- schema validation on state/handoffs
- required verification steps
- checkpoint logging

## Building Your Own Agent (Starter Roadmap)

1. Pick one narrow task
2. Add read-only tools first
3. Add explicit plan output
4. Add guarded execution
5. Add verification and tracing
6. Add evals before expanding scope
