# AI-Assisted Software Engineering Foundation

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
[![Lint](https://github.com/parrsi01/ai-assisted-software-engineering-foundation/actions/workflows/lint.yml/badge.svg)](https://github.com/parrsi01/ai-assisted-software-engineering-foundation/actions/workflows/lint.yml)
[![CI](https://github.com/parrsi01/ai-assisted-software-engineering-foundation/actions/workflows/ci.yml/badge.svg)](https://github.com/parrsi01/ai-assisted-software-engineering-foundation/actions/workflows/ci.yml)

Professional curriculum for AI-assisted coding, agent engineering, prompt software engineering, and AI-native delivery workflows.

Author: Simon Parris  
Date: 2026-02-24

## Start Here

1. Open this repo in VS Code.
2. Read `docs/PROJECT_MANUAL.md`.
3. Read `docs/LESSON_EXECUTION_COMPANION.md`.
4. Open `tickets/README.md` and pick one Jira-style incident/task drill.
5. Run `./validate_repo.sh --quick` after edits.

## Professional Terminology (Replacing "Vibe Coding")

Recommended LinkedIn / CV terms for this repo and skillset:

- AI-Assisted Software Engineer
- Agentic Software Engineering Practitioner
- Prompt Software Engineering / LLM Application Engineer
- AI Developer Productivity Engineer

This repository uses **AI-Assisted Software Engineering** as the primary professional term.

## Overview

This repository is a certification-level training lab for learning how to design, control, evaluate, and operationalize AI-assisted coding systems from beginner to advanced.

It covers:

- prompt engineering for software tasks
- context engineering and repo-aware workflows
- agent design (single-agent and multi-agent)
- tool use, guardrails, and permission boundaries
- code review, test generation, debugging, and refactoring with AI
- evaluation harnesses, quality gates, and prompt regression testing
- security, privacy, compliance, and IP risk management
- team operating models for AI-native engineering organizations

## Certification-Level Learning Tracks

- Foundation Track: LLM basics, prompt structure, safe usage, repo navigation, task decomposition
- Practitioner Track: coding prompts, debugging loops, test-first prompting, code review prompting, docs generation
- Agent Engineering Track: tool-using agents, planning, memory/context windows, orchestration, handoffs
- Reliability Track: evals, acceptance criteria, failure modes, hallucination containment, rollout gates
- Enterprise Track: governance, SDLC integration, auditability, change control, policy guardrails

## Quick Links (Mobile-Friendly)

- `docs/README.md` - docs index
- `docs/OFFLINE_INDEX.md` - offline-first learning index
- `docs/PROJECT_MANUAL.md` - repository operating manual
- `docs/PROJECT_RUNBOOKS_DETAILED.md` - detailed runbooks for each lab/project
- `docs/LESSON_EXECUTION_COMPANION.md` - slow-learning execution guide + companion prompts
- `docs/LESSON_RESEARCH_ANALYSIS_COMPANION.md` - theory/analysis companion for all modules
- `docs/REPOSITORY_STATUS_REPORT.md` - structure/status summary
- `Library/README.md` - full beginner-to-advanced theory library
- `prompts/oneshot/AISE_REPO_BUILDER_ONESHOT.md` - one-shot repo generation prompt template
- `tickets/README.md` - Jira-style drills
- `projects/README.md` - hands-on labs

## Learning Modules

- Module 1: LLM Foundations for Engineers (`docs/foundations/`)
- Module 2: Prompt Software Engineering (`docs/prompt_engineering/`)
- Module 3: Context Engineering and Repo Navigation (`projects/context-engineering-lab/`)
- Module 4: Agent Engineering Fundamentals (`docs/agent_engineering/`, `projects/agent-starter-lab/`)
- Module 5: AI-Assisted Debugging and Refactoring (`tickets/jira/`)
- Module 6: Evals and Prompt Regression Testing (`docs/evals/`, `projects/prompt-evals-lab/`)
- Module 7: RAG for Coding Assistants (`projects/rag-coding-assistant-lab/`)
- Module 8: Multi-Agent Review and Delivery Patterns (`projects/multi-agent-code-review-lab/`)
- Module 9: Security, Governance, and Enterprise Adoption (`docs/security/`, `docs/ops/`)

## Repo Layout

- `docs/` - manuals, companions, theory notes, runbooks
- `Library/` - long-form beginner-to-advanced reference sheets (course-wide)
- `library/` - lightweight alias/index for compatibility with repo family patterns
- `prompts/` - one-shot and reusable prompt templates
- `projects/` - runnable or guided hands-on AI engineering labs
- `tickets/` - Jira-style practice drills with reproduce/debug/fix/reset workflow
- `scripts/` - validators and helper scripts
- `tests/` - unit tests for example tooling / guardrails
- `.github/workflows/` - CI and lint pipelines

## Quick Start

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
./validate_repo.sh --quick
python -m unittest discover -s tests -p 'test_*.py' -v
```

## Example Lab Run (Agent Starter)

```bash
cd projects/agent-starter-lab
python3 -m src.agent_runtime \
  --goal "Write unit tests for a small parser" \
  --context ../.. \
  --mode safe
```

## Documentation Standards (Repository Quality)

This repo is maintained to match the same learning-repo standard as the existing DevOps, Data Science, and Network lab repositories:

- root README with navigation and progression
- offline-readable docs + companion guides
- structured `Library/` theory index
- ticket-style repeatable drills
- local validation + CI workflows
- mobile-friendly Markdown formatting

## Daily Commit / Push Loop

```bash
git status
git add .
git commit -m "docs: expand AI-assisted engineering notes"
git push
```
