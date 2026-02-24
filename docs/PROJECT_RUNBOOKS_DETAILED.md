# Project Runbooks (Detailed)

## `projects/agent-starter-lab/`

- Objective: understand a minimal task-planning coding agent loop
- Run: `python3 -m src.agent_runtime --goal "..." --context ../.. --mode safe`
- Practice: compare vague vs scoped goals
- Evidence: generated plan, guarded command decisions, final summary

## `projects/context-engineering-lab/`

- Objective: build repo-aware context packages for coding tasks
- Practice: define file shortlist, constraints, and acceptance criteria
- Output: context packet examples + anti-patterns

## `projects/prompt-evals-lab/`

- Objective: create prompt test cases and regression checks
- Practice: score correctness, formatting, safety, and actionability
- Output: eval rubric + sample baseline prompts

## `projects/rag-coding-assistant-lab/`

- Objective: understand retrieval for code/docs assistants
- Practice: chunking strategy, metadata, citations, recency concerns
- Output: architecture notes and threat model checklist

## `projects/multi-agent-code-review-lab/`

- Objective: design planner/implementer/reviewer handoff workflows
- Practice: role prompts, shared state schema, conflict resolution
- Output: orchestration map + failure handling runbook
