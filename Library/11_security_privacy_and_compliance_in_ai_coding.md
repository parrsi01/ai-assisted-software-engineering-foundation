# 11. Security, Privacy, and Compliance in AI Coding

## Security Questions to Ask Before Using an AI Coding Tool

- Where does prompt data go?
- Is data retained or used for training?
- What logs are stored?
- Who can access prompts/outputs?
- Can secrets or regulated data be exposed?

## Common Risks

- secrets pasted into prompts
- internal code/IP leakage
- insecure generated code patterns
- dependency or license violations
- agent executing unsafe commands
- weak audit trail for AI-generated changes

## Core Controls

- secret scanning and redaction
- data classification policy for prompt content
- provider/vendor review
- local/private model options for sensitive work
- mandatory tests and human review
- logging and retention policy

## Compliance Themes (General)

Different organizations map AI workflows to existing controls for change management, auditability, access control, and data handling. The exact policy names vary, but the engineering need is consistent: prove what changed, who approved it, and what evidence validated it.

## Secure Prompting Rule

Never assume prompt text is private unless your platform contract and configuration explicitly guarantee it.
