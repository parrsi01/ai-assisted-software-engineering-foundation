# Agent Starter Lab

Minimal Python stdlib example showing a safe AI coding agent runtime model:

- receives a goal
- builds a plan
- proposes actions
- blocks unsafe shell commands in `safe` mode
- records execution trace

## Run

```bash
python3 -m src.agent_runtime --goal "Add tests for parser" --context ../.. --mode safe
```

## Study Focus

- planning vs execution
- guardrails vs capability
- evidence logging and traceability
