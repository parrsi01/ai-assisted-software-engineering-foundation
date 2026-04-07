# Code Explanations — AI-Assisted SE Repo

---

## agent_runtime.py — Full Walkthrough

### Imports & Constants

```python
import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from typing import Literal
```

- `argparse`: stdlib CLI argument parser — cleaner than `sys.argv` manual parsing
- `asdict`: converts a dataclass instance to a plain dict — used for JSON serialization
- `Literal`: type hint that restricts values to specific strings ("safe" | "permissive")

```python
_BLOCKED_PATTERNS: tuple[str, ...] = (
    "rm -rf",
    "git reset --hard",
    "sudo ",
    "chmod -R 777",
)
```

**Why a tuple not a list?** Tuples are immutable — `_BLOCKED_PATTERNS` is a constant; a list could accidentally be modified. The underscore prefix (`_BLOCKED_PATTERNS`) is a Python convention for "module-private" (not exported).

**Why these specific patterns?** Each represents an irreversible or permission-escalating operation:
- `rm -rf`: recursive force-delete, no confirmation, no recycle bin
- `git reset --hard`: discards all uncommitted changes permanently
- `sudo `: privilege escalation — agent should never need root
- `chmod -R 777`: gives everyone read/write/execute on directory tree

---

### Dataclasses

```python
@dataclass
class AgentAction:
    kind: Literal["note", "shell", "search"]
    content: str
```

**Why a dataclass?** `@dataclass` auto-generates `__init__`, `__repr__`, `__eq__`. For a simple container like `AgentAction`, this is less boilerplate than a regular class while being more structured than a plain dict.

**`Literal["note", "shell", "search"]`**: restricts `kind` to exactly these three strings. Type checkers (mypy) will flag `AgentAction(kind="http", ...)` as an error at analysis time, before runtime.

```python
@dataclass
class AgentTrace:
    goal: str
    context: str
    mode: str
    plan: list[str]
    actions: list[AgentAction]
    blocked_actions: list[AgentAction]
    summary: str
```

**`field(default_factory=list)`** — if these fields had `default=[]`, all instances would share the same list object (a common Python gotcha with mutable defaults). `default_factory=list` creates a new list for each instance.

**Why capture `blocked_actions` separately?** The trace needs to record what was blocked, not just what ran. Audit trail: you can see that the agent tried to run `rm -rf`, and the guardrail caught it.

---

### build_plan()

```python
def build_plan(goal: str) -> list[str]:
    base_steps = [
        "Understand the goal and constraints",
        "Identify relevant files and context",
        "Propose minimal changes",
        "Validate changes against acceptance criteria",
        "Report findings and residual risks",
    ]
    if "test" in goal.lower():
        base_steps.insert(2, "Review existing test coverage")
    if "refactor" in goal.lower():
        base_steps.insert(2, "Identify refactoring scope and boundaries")
    return base_steps
```

**Keyword detection pattern:** Simple substring check on the lowercased goal string. This is intentionally naive — a production agent would use semantic understanding. For a teaching repo, this shows the concept (plan adapts to goal) without complexity.

**Why `insert(2, ...)`?** Inserts at index 2 (before "Propose minimal changes") so the additional step happens at the investigation phase, not after changes are proposed.

---

### propose_actions()

```python
def propose_actions(goal: str) -> list[AgentAction]:
    actions = [
        AgentAction("note", f"Goal: {goal}"),
        AgentAction("shell", "rg --files"),
        AgentAction("shell", "python -m unittest -q"),
    ]
    if "clean" in goal.lower():
        actions.append(AgentAction("shell", "rm -rf build/"))
    return actions
```

**Why `rg --files`?** Ripgrep file listing gives the agent a map of what exists in the project without reading file contents — minimal, fast context.

**Why `python -m unittest -q`?** Quiet mode runs tests without verbose output — checks if the baseline passes before making any changes.

**Why include `rm -rf build/` for "clean" goals?** This is deliberate: the test case `test_permissive_mode_allows_destructive_commands` checks that this action is NOT blocked in permissive mode. It demonstrates that guardrails are mode-dependent — safe mode blocks it, permissive mode allows it.

---

### apply_guardrails()

```python
def apply_guardrails(
    actions: list[AgentAction],
    mode: str,
) -> tuple[list[AgentAction], list[AgentAction]]:
    if mode != "safe":
        return actions, []
    safe_actions, blocked_actions = [], []
    for action in actions:
        if action.kind == "shell" and any(
            pattern in action.content for pattern in _BLOCKED_PATTERNS
        ):
            blocked_actions.append(action)
        else:
            safe_actions.append(action)
    return safe_actions, blocked_actions
```

**`any(pattern in action.content for pattern in _BLOCKED_PATTERNS)`**: generator expression inside `any()`. Short-circuits on first match — doesn't check all patterns if first one matches. More efficient than `for` loop with `break`.

**Why only check `kind == "shell"`?** Notes and search actions can't execute destructive commands. Only shell actions need guardrail filtering.

**Why return both lists?** The caller needs both: `safe_actions` to execute, `blocked_actions` to log in the trace. Returning only the safe list would lose the audit record.

---

### run_agent() and main()

```python
def run_agent(goal: str, context: str, mode: str) -> AgentTrace:
    plan = build_plan(goal)
    proposed_actions = propose_actions(goal)
    safe_actions, blocked_actions = apply_guardrails(proposed_actions, mode)
    summary = f"Agent completed planning phase for goal: {goal!r}"
    return AgentTrace(
        goal=goal, context=context, mode=mode,
        plan=plan, actions=safe_actions,
        blocked_actions=blocked_actions, summary=summary,
    )
```

**Composition pattern:** `run_agent` is a pure orchestrator — it calls the three building blocks and assembles the result. No logic of its own. Easy to test each building block independently.

```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--goal", required=True)
    parser.add_argument("--context", default=".")
    parser.add_argument("--mode", default="safe", choices=["safe", "permissive"])
    args = parser.parse_args()
    trace = run_agent(args.goal, args.context, args.mode)
    print(json.dumps(asdict(trace), indent=2))
```

**Why JSON output?** Composability — the agent's output can be piped to `jq`, parsed by another tool, logged, or used as input to the next step in a pipeline. JSON is the lingua franca of inter-process communication.

**`asdict(trace)`**: recursively converts the dataclass (and all nested dataclasses like `AgentAction`) to a plain dict, then `json.dumps` serializes it.

---

## check_library_index.py

```python
REQUIRED_REFS = [
    "01_ai_foundations_and_llm_basics.md",
    "07_agent_engineering_and_orchestration.md",
    "14_enterprise_adoption_governance_and_career_paths.md",
]

def check_library_index(path: Path) -> bool:
    content = path.read_text()
    return all(ref in content for ref in REQUIRED_REFS)
```

**Why these 3 specific files?** They represent the three pillars of the curriculum: foundations, agent engineering, enterprise. If all three are in the index, the index is almost certainly complete.

**Why `all()` not a loop?** `all()` returns `True` only if every element in the iterable is truthy. Short-circuits on first `False`. Clean, Pythonic, easy to read.

**Why separate validation script?** CI-composability: `make lint` can run `check_library_index.py` as a fast check without running the full test suite.

---

## test_agent_runtime.py — All 4 Tests

### test_build_plan_includes_test_step
```python
def test_build_plan_includes_test_step(self):
    plan = build_plan("Add tests for parser module")
    self.assertTrue(any("test" in step.lower() for step in plan))
```
Tests that keyword detection in `build_plan()` works: a goal containing "test" produces a plan with a test-related step. Uses `any()` to search all steps rather than checking a specific index.

### test_safe_mode_blocks_destructive_commands
```python
def test_safe_mode_blocks_destructive_commands(self):
    goal = "clean the build directory"
    actions = propose_actions(goal)
    safe, blocked = apply_guardrails(actions, "safe")
    self.assertTrue(any("rm -rf" in a.content for a in blocked))
    self.assertFalse(any("rm -rf" in a.content for a in safe))
```
Tests the guardrail's primary function: destructive commands appear in `blocked`, not `safe`. Uses two assertions: presence in blocked AND absence in safe.

### test_permissive_mode_allows_destructive_commands
```python
def test_permissive_mode_allows_destructive_commands(self):
    goal = "clean the build directory"
    actions = propose_actions(goal)
    safe, blocked = apply_guardrails(actions, "permissive")
    self.assertEqual(blocked, [])
    self.assertTrue(any("rm -rf" in a.content for a in safe))
```
Complementary test: in permissive mode, nothing is blocked and the destructive command appears in safe actions. `assertEqual(blocked, [])` confirms the list is exactly empty.

### test_cli_outputs_json
```python
def test_cli_outputs_json(self):
    result = subprocess.run(
        [sys.executable, "-m", "src.agent_runtime",
         "--goal", "Review authentication module",
         "--context", ".",
         "--mode", "safe"],
        capture_output=True, text=True, cwd=...
    )
    self.assertEqual(result.returncode, 0)
    data = json.loads(result.stdout)
    self.assertIn("plan", data)
    self.assertEqual(data["mode"], "safe")
```
Integration test: runs the CLI as a subprocess and parses the JSON output. This tests the full stack including `argparse`, `main()`, `asdict()`, and `json.dumps()`. `json.loads()` will raise an exception if the output isn't valid JSON, which becomes a test failure. Tests both structure (`"plan" in data`) and values (`data["mode"] == "safe"`).

---

## validate_repo.sh — Key Logic

**Ticket validation:**
```bash
TICKET_COUNT=$(find tickets/ -name "*.md" | wc -l)
[[ $TICKET_COUNT -ge 10 ]] || { echo "FAIL: need ≥10 tickets"; exit 1; }
```

**6 required sections check:**
```bash
for ticket in tickets/*.md; do
    for section in "Scenario" "Reproduce" "Debug" "Root Cause" "Fix" "Reset"; do
        grep -q "## $section" "$ticket" || { echo "FAIL: $ticket missing $section"; exit 1; }
    done
done
```
Iterates every ticket file and verifies all 6 sections exist by grep. If any section is missing from any ticket, validation fails with a specific message identifying which ticket and which section.

**Placeholder scan:**
```bash
grep -r "TODO\|PLACEHOLDER\|FILL_IN" docs/ Library/ tickets/ && exit 1
```
Catches incomplete content that was committed. Exits with failure if any placeholder strings are found.
