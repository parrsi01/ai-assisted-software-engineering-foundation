# Security and Governance Manual

## Primary Risks

- secret leakage in prompts or logs
- source code/IP exfiltration
- insecure generated code
- dependency/license issues
- unsafe commands and destructive automation
- audit gaps (no evidence trail)

## Minimum Controls

- secret scanning before prompt submission
- repo/path allowlists
- command approval policies
- test and lint gates before merge
- change review for AI-generated diffs
- prompt/output logging for regulated workflows
