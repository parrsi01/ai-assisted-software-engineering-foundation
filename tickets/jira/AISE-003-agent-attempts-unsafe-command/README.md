# AISE-003: Agent Attempts Unsafe Command

## Scenario
Agent proposes a destructive shell command (`rm -rf`, force reset, etc.) during cleanup.

## Reproduce
- Ask the agent to "clean and reset everything" without guardrails.

## Debug
- Inspect agent policy and command allow/block rules.
- Confirm whether approval checkpoints exist.

## Root Cause
Missing execution policy and destructive command guardrails.

## Fix
Add allowlist/denylist checks and human approval for high-risk commands.

## Reset
Run recovery procedure and restore from version control/snapshot if needed.
