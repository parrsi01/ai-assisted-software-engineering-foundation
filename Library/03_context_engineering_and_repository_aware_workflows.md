# 03. Context Engineering and Repository-Aware Workflows

## Definition

Context engineering is the selection, packaging, and ordering of information that the model needs to complete a task correctly.

## Why Context Engineering Often Matters More Than Prompt Style

A perfect prompt with the wrong files still produces wrong code.
A decent prompt with the right context often performs well.

## Context Packet Components

- Task statement
- Relevant file list
- Error traces/log snippets
- Constraints (language version, style, architecture rules)
- Acceptance criteria
- Validation commands
- Risk notes (destructive commands, migration impacts)

## Repository-Aware AI Workflows

### Good Pattern

- inspect repo tree
- identify likely files
- confirm interfaces/contracts
- prompt with scoped context
- validate changes

### Bad Pattern

- prompt first
- inspect repo later
- patch generated assumptions manually

## Context Budgeting

Because context is limited:
- include only relevant files
- summarize large files
- cite exact paths and symbols
- refresh context after significant edits

## Failure Modes

- stale context after refactor
- omitted interface file
- wrong environment assumptions
- hidden constraints not stated (CI version, lint rules)

## Verification Trick

Require the model to name the files and symbols it relied on before generating changes.
