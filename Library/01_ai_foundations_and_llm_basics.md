# 01. AI Foundations and LLM Basics

## What This File Covers

The minimum theory an engineer needs before using AI coding tools seriously.

## Core Definitions

### Artificial Intelligence (AI)
A broad field focused on systems that perform tasks associated with human cognition (reasoning, language, perception, planning).

### Machine Learning (ML)
A subset of AI where models learn patterns from data rather than being programmed with fixed rules for every case.

### Large Language Model (LLM)
A model trained on large text/code corpora to predict the next token. It can produce fluent text and code, but fluency is not proof of correctness.

### Token
A chunk of text used internally by the model (often a word fragment, punctuation, or word). Context limits are measured in tokens, not sentences.

### Context Window
The maximum amount of input (and often output) the model can use at one time. If you exceed it, older context may be truncated or omitted.

## Why Engineers Must Care

- Long codebases exceed context windows.
- Missing context causes hallucinated APIs and wrong assumptions.
- Model confidence does not imply runtime correctness.
- Verification is still required (tests, logs, static checks, reviews).

## Generation vs Execution

An LLM can generate code text. It does not execute that code unless connected to tools or a runtime.

Engineering implication:
- Text-only answer = hypothesis
- Tool-verified change + tests = evidence-backed result

## Sampling and Determinism (Practical View)

- Higher randomness can help brainstorming but increases variance.
- Lower randomness improves consistency for structured outputs.
- Deterministic settings can still produce wrong answers if context is wrong.

## Common Beginner Mistakes

- Treating the model as a search engine with guaranteed facts
- Asking for code without constraints or target files
- Accepting code without running tests
- Ignoring model recency limits on external facts

## Engineer's Rule

Use AI to accelerate thinking and drafting. Use engineering controls to validate reality.
