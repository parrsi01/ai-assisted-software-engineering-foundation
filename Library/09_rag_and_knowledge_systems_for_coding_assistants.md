# 09. RAG and Knowledge Systems for Coding Assistants

## RAG (Retrieval-Augmented Generation)

A pattern where relevant documents/code snippets are retrieved and included as context before generation.

## Why RAG Helps AI Coding

- reduces hallucinated APIs
- improves repo-specific accuracy
- enables citation-style answers
- supports large codebases beyond direct context limits

## Core RAG Pipeline

1. ingest docs/code
2. chunk content
3. attach metadata
4. index embeddings/keywords
5. retrieve candidates
6. rank and filter
7. assemble prompt with citations
8. generate answer/code
9. verify against current repo state

## Coding-Specific Metadata

- file path
- language
- symbol/function/class name
- commit hash or timestamp
- module ownership/domain
- test file linkage

## Failure Modes

- stale index after refactor
- over-broad chunking (too much irrelevant text)
- under-sized chunking (missing dependencies)
- retrieval misses due to naming mismatch
- no citation checking

## Safety and Governance

RAG can increase confidence without increasing correctness if citations are not validated. Always confirm retrieved snippets match current code.
