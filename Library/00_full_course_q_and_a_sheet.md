# 00. Full Course Q&A Sheet

## Foundations

Q: Why can an LLM produce convincing but incorrect code?  
A: It predicts likely tokens, not runtime truth. Without verification tools/tests, correctness is not guaranteed.

Q: What usually matters more in coding tasks: prompt wording or context quality?  
A: Context quality and scope control often matter more.

## Prompt Engineering

Q: What are the minimum fields in a good coding prompt?  
A: Task, context, constraints, acceptance criteria, and validation requirements.

Q: Why are acceptance criteria important?  
A: They define observable success and prevent silent behavior changes.

## Agents

Q: What makes an AI assistant an agent?  
A: Tool use, state, iterative action, and policies/guardrails.

Q: When should humans remain in the loop?  
A: High-risk actions, destructive commands, production changes, and security-sensitive workflows.

## Evals

Q: Why do prompt templates need regression tests?  
A: Small wording changes can improve one task type but degrade others.

## Security

Q: What is the easiest serious mistake in AI coding workflows?  
A: Pasting secrets or sensitive code into prompts without controls.
