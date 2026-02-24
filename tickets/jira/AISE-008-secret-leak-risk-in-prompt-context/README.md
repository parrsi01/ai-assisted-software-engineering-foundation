# AISE-008: Secret Leak Risk in Prompt Context

## Scenario
Developer pastes config files containing secrets into an external model prompt.

## Reproduce
- Include `.env` or credential-bearing config in a debug prompt.

## Debug
- Identify data classification violations.
- Review prompt logging and provider retention settings.

## Root Cause
No pre-prompt redaction process or secret scanning guardrail.

## Fix
Secret scan and redact before prompt submission; use local/private inference for sensitive code.

## Reset
Rotate exposed credentials and document incident response steps.
