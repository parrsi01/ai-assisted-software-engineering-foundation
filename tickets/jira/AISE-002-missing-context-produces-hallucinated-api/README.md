# AISE-002: Missing Context Produces Hallucinated API

## Scenario
AI generates code against functions/classes that do not exist in the repo.

## Reproduce
- Ask for integration code without providing interface definitions.

## Debug
- Search repo for referenced symbols.
- Compare generated assumptions to actual codebase contracts.

## Root Cause
No interface/context supplied; model filled gaps with likely-looking APIs.

## Fix
Provide interface files and require symbol/path citations.

## Reset
Delete invalid code and rerun with context packet.
