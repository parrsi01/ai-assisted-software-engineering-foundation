# AISE-006: RAG Context Is Stale

## Scenario
Retrieved docs/snippets reference old APIs after a refactor, causing incorrect generated code.

## Reproduce
- Query a stale index after recent repository changes.

## Debug
- Compare retrieval timestamps/commit hashes with current code.
- Verify citations against HEAD.

## Root Cause
Index refresh policy missing or lagging.

## Fix
Add recency metadata and index refresh triggers; require citations with commit awareness.

## Reset
Rebuild index and rerun generation.
