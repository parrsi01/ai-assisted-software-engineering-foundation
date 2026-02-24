# 08. Tool Use, Permissions, and Guardrails

## Why Guardrails Matter

AI coding systems become high-impact only when they can run tools. Tool access turns text mistakes into system changes.

## Tool Classes (Risk Perspective)

- Read-only tools (file reads, searches): lower risk
- Build/test tools: medium risk (resource/time side effects)
- Write/edit tools: medium-high risk
- Network/deploy/admin tools: high risk
- Destructive tools (reset/delete): highest risk

## Permission Models

- deny by default
- allowlist by command/path
- approval-required for sensitive actions
- environment-specific policies (dev vs prod)

## Practical Guardrails

- path restrictions for file edits
- command denylist (destructive patterns)
- no root/sudo without approval
- dry-run before apply (where possible)
- rate/step limits
- log all actions and outputs

## Human Approval Checkpoints

Use approval for:
- production changes
- secrets access
- destructive commands
- external network calls with sensitive code/data

## False Sense of Safety Risk

Guardrails are not complete protection if:
- prompts include secrets directly
- logs store sensitive content
- reviewers skip verification
- users approve unsafe commands casually
