# Project Manual

Author: Simon Parris + Codex companion notes  
Date: 2026-02-24

## Purpose

This repository trains AI-assisted software engineering as a repeatable engineering discipline, not a prompt lottery.

## Operating Principles

- Define task scope before prompting
- Preserve evidence (prompt, context, outputs, tests, diff)
- Require verification before merge
- Separate brainstorming prompts from production prompts
- Treat agents as software systems with failure modes

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
./validate_repo.sh --quick
python -m unittest discover -s tests -p 'test_*.py' -v
```

## Standard Workflow (Human + AI)

1. Read the ticket and acceptance criteria.
2. Build a minimal context package (files, constraints, commands).
3. Use a scoped prompt template from `prompts/templates/`.
4. Review AI output for assumptions and unsafe actions.
5. Run tests / validators.
6. Record findings and residual risk.

## Evidence Checklist (Required)

- Prompt used (or prompt template + parameters)
- Files inspected
- Diff summary
- Test/validation results
- Known limitations
- Follow-up tasks

## Repo Quality Gates

- `./validate_repo.sh --quick`
- `python -m unittest discover -s tests -p 'test_*.py' -v`
- no placeholder marker text (unfinished template markers)
- ticket docs use reproduce/debug/fix/reset structure
