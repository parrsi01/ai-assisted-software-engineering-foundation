# AISE-009: Multi-Agent Handoff State Corruption

## Scenario
Planner and implementer agents use mismatched task schemas, causing dropped constraints during handoff.

## Reproduce
- Change planner output format without updating downstream parser.

## Debug
- Inspect serialized state between agents.
- Validate schema versioning and required fields.

## Root Cause
No schema versioning / validation on inter-agent messages.

## Fix
Version the handoff schema and enforce validation before execution.

## Reset
Replay task from the last valid checkpoint.
