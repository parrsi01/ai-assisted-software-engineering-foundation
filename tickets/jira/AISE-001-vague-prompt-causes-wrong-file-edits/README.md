# AISE-001: Vague Prompt Causes Wrong File Edits

## Scenario
A coding assistant updates the wrong module because the prompt names the feature but not the file paths.

## Reproduce
1. Give a vague request: "Add validation for user IDs".
2. Do not provide file paths or acceptance criteria.
3. Observe edits in unrelated modules.

## Debug
- Compare requested behavior vs edited files.
- Check whether the prompt defined target files and test commands.
- Identify missing constraints.

## Root Cause
Prompt lacked scoped context and explicit file boundaries.

## Fix
Use a structured task prompt with target files, acceptance criteria, and validation commands.

## Reset
Revert or discard unintended edits and rerun with a scoped prompt.
