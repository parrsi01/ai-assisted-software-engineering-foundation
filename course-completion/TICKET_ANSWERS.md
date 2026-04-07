# Jira Ticket Answers — AISE-001 through AISE-010

---

## AISE-001: Vague Prompt Causes Wrong File Edits

**Root Cause:** Prompt lacked scoped context and explicit file boundaries. Model inferred scope from task description and selected the wrong files.

**Exact Fix:**
```markdown
## Prompt (fixed version)
Role: Senior Python engineer
Task: Refactor the `parse_config()` function to use dataclasses instead of dicts.
Context: Target file only — `src/config/parser.py`, lines 45–87
Acceptance Criteria:
  - `parse_config()` returns a `Config` dataclass, not a dict
  - All existing callers in `src/config/parser.py` updated
  - `tests/test_config.py` passes with no changes to test file
Constraints: Do NOT modify any file other than `src/config/parser.py`
Validation: Run `python -m pytest tests/test_config.py -v` and paste output
```

**Verification Steps:**
1. Check git diff — only `src/config/parser.py` modified
2. Run test suite
3. Confirm no files outside declared scope changed

**Rollback:** `git checkout HEAD -- .` (discard all uncommitted changes) or `git revert` if committed

**Lesson:** Explicit file scope in the prompt (`do NOT modify any file other than X`) prevents the model from "improving" related code it wasn't asked to touch.

---

## AISE-002: Missing Context → Hallucinated API

**Root Cause:** No interface or file context supplied. Model generated plausible-looking API calls for methods that don't exist.

**Exact Fix:**
```markdown
## Prompt (fixed version)
Context:
  - Interface file: `src/auth/interface.py` [paste content]
  - Current implementation: `src/auth/auth.py` [paste relevant section]
Task: Add `refresh_token()` method to `AuthClient`
Constraints:
  - Use only methods defined in `src/auth/interface.py`
  - Cite the exact line number in interface.py for each method you call
  - Do not invent method signatures not present in the interface file
```

**Verification Steps:**
1. For each method the model calls: grep for it in `interface.py`
2. Run type checker: `mypy src/auth/auth.py`
3. Run tests

**Rollback:** If hallucinated API was merged: identify the non-existent method, find the correct one in the interface, fix the call.

**Lesson:** Context quality determines output quality. Without interface files, the model is guessing. Require citation of file path + line number for every API reference.

---

## AISE-003: Agent Attempts Unsafe Command

**Root Cause:** No execution policy or command filtering. Agent had unrestricted shell access and proposed `rm -rf` and `git reset --hard`.

**Exact Fix:**
```python
# In agent_runtime.py
_BLOCKED_PATTERNS = ("rm -rf", "git reset --hard", "sudo ", "chmod -R 777")

def apply_guardrails(actions, mode):
    if mode != "safe":
        return actions, []
    safe, blocked = [], []
    for action in actions:
        if action.kind == "shell" and any(p in action.content for p in _BLOCKED_PATTERNS):
            blocked.append(action)
        else:
            safe.append(action)
    return safe, blocked
```

**Additional Controls:**
- Allowlist: define exact commands the agent is permitted to run
- Approval gate: for any command not in allowlist, require human confirmation
- Dry-run mode: `--dry-run` flag logs proposed commands without executing

**Verification:** `test_safe_mode_blocks_destructive_commands()` in test suite

**Lesson:** Default should be safe mode. Permissive mode requires explicit opt-in with justification. Blocked commands should be logged, not silently skipped.

---

## AISE-004: Tests Pass but Prompt Changed the Contract

**Root Cause:** Acceptance criteria not anchored to the original behavior spec. Model rewrote both the code and the tests to match a different (subtly wrong) contract. Tests passed because they were also rewritten.

**Exact Fix:**
1. Before prompting for code changes: write (or confirm) tests that encode the spec
2. Lock those tests: `git add tests/test_feature.py && git commit -m "Add spec tests before AI edit"`
3. Prompt constraint: "Do NOT modify any test file"
4. After model applies changes: `git diff tests/` — if test files changed, reject the PR

**Process rule:** Lock behavior spec in tests before AI touches the implementation. Review test diff separately from implementation diff.

**Verification:** `git diff HEAD~1 tests/` should be empty after AI-assisted code change.

**Lesson:** Tests are the contract. If AI rewrites both code and tests, the contract changed silently. Always commit tests before prompting for implementation changes.

---

## AISE-005: Code Review Agent Misses Regression

**Root Cause:** Insufficient review context. Agent only received the diff, not the code that calls the changed function. Regression introduced in caller behavior wasn't visible in the diff alone.

**Exact Fix:**
```markdown
## Code Review Prompt (fixed)
Objective: Review this diff for bugs, regressions, and security risks
Inputs:
  - Diff: [paste diff]
  - Callers: [paste all files that call the changed function]
  - Expected behavior spec: [paste test cases or docstring]
  - Constraints: [list of invariants that must not change]
Review priorities:
  1. Behavioral regression (does this change what callers expect?)
  2. Edge cases (null inputs, empty collections, type mismatches)
  3. Security implications (input validation, auth context)
  4. Test gaps (what cases are NOT covered by existing tests?)
Output: severity-ordered findings with file:line references
```

**Verification:** For each finding: write a test that reproduces the issue, then fix it.

**Lesson:** Code review needs caller context. A diff without call sites misses interaction bugs. Provide the full blast radius of the change.

---

## AISE-006: RAG Context Is Stale (Old API After Refactor)

**Root Cause:** RAG index was not refreshed after an API refactor. Model retrieved old code chunks with deprecated method signatures.

**Exact Fix:**
1. Add recency metadata to each indexed chunk: `{"commit": "abc123", "indexed_at": "2026-01-15T10:00:00Z"}`
2. Trigger index rebuild on every merge to main
3. In the review step, verify all citations against current `HEAD` — not just index content
4. Add warning: if retrieved chunk's commit hash ≠ current HEAD for that file, flag as potentially stale

**Verification:** After index refresh, run sample queries and confirm returned code matches `git show HEAD:src/...` for the same file.

**Lesson:** RAG citations can increase confidence in wrong answers. A cited stale method looks more trustworthy than a hallucinated one — but both are wrong. Freshness metadata is mandatory.

---

## AISE-007: Prompt Regression After Template Update

**Root Cause:** No regression suite covering diverse task types. Template was updated for one use case; others broke silently.

**Exact Fix:**
1. Build eval set: ≥10 prompts covering all template use cases (implementation, review, debug, test-gen, refactor)
2. Baseline: run all 10 prompts before any template change, save outputs
3. Regression: after template change, run all 10 again, compare outputs
4. Thresholds: accept change only if pass rate ≥ baseline on critical tasks
5. Version: tag prompt template versions (`prompt-template-v1.2.0`) alongside eval baselines

**Rubric example:**
```yaml
eval:
  correctness: 0.4
  completeness: 0.2
  safety: 0.2
  actionability: 0.2
thresholds:
  pass: 0.85
  warn: 0.70
```

**Lesson:** Prompt templates are software. Version them, test them, maintain a regression suite.

---

## AISE-008: Secret Leak Risk in Prompt Context

**Root Cause:** Developer pasted `.env` file contents into a debug prompt sent to an external LLM API. Credentials potentially logged by vendor.

**Immediate Response (already happened):**
1. Rotate all credentials that appeared in the prompt — assume leaked
2. Check vendor's data retention policy — escalate if retention period active
3. Review access logs for the exposed credentials: any unauthorized use?
4. Document as AI security incident

**Process Fix:**
```python
# Pre-prompt secret scanner
import re
SECRET_PATTERNS = [
    r"[A-Za-z0-9+/]{40}",     # Base64-encoded secrets (generic)
    r"sk-[A-Za-z0-9]{48}",    # OpenAI-style API key
    r"[A-Z0-9]{20}",           # AWS access key pattern
    r"password\s*=\s*\S+",    # Password assignments
]
def scan_for_secrets(text: str) -> list:
    return [p for p in SECRET_PATTERNS if re.search(p, text)]
```

**Policy:**
- Scan all prompt context for secrets before submission
- Use local/private inference for any code that handles credentials
- Never paste `.env`, `secrets.yaml`, or credential files into any LLM context

**Lesson:** Treat prompt text as potentially public. Vendor SLAs don't guarantee prompt privacy. Automate scanning at the prompt submission layer.

---

## AISE-009: Multi-Agent Handoff State Corruption

**Root Cause:** No schema versioning or validation on inter-agent messages. Planner agent's output schema changed; implementer agent received mismatched data structure.

**Exact Fix:**
```python
# Versioned handoff schema
from dataclasses import dataclass
from typing import Literal

HANDOFF_SCHEMA_VERSION = "1.2.0"

@dataclass
class TaskHandoff:
    schema_version: str
    task_id: str
    goal: str
    context_files: list[str]
    acceptance_criteria: list[str]
    constraints: list[str]

def validate_handoff(data: dict) -> TaskHandoff:
    if data.get("schema_version") != HANDOFF_SCHEMA_VERSION:
        raise ValueError(f"Schema version mismatch: expected {HANDOFF_SCHEMA_VERSION}")
    return TaskHandoff(**data)
```

**Additional controls:**
- Validate schema on receipt, before any action
- Log schema version with every handoff
- Reject mismatched versions — do not attempt to infer intent

**Lesson:** Inter-agent messages are an API. Version them, validate them, reject mismatches explicitly.

---

## AISE-010: Eval Suite Gives False Confidence (Benchmark Overfitting)

**Root Cause:** Eval set was too small and static. Prompt was tuned against the same benchmark it was evaluated on. Tasks weren't diverse enough to catch real-world failure modes.

**Exact Fix:**
1. **Expand task diversity**: implementation, debugging, refactoring, review, test-gen — each with ≥3 variants
2. **Holdout set**: keep 20% of eval tasks unseen during prompt development; evaluate against holdout at release
3. **Refresh schedule**: rotate 10% of benchmark tasks each quarter
4. **Failure category tracking**: log not just pass/fail but which failure type (ambiguity, scope bleed, hallucination, format, policy, verification) — if one category is always passing, you may not have tasks that test it

**Signs of overfitting:**
- Pass rate on eval = 98% but rework requests from engineers remain high
- Eval tasks look similar to real prompts (no distribution gap)
- Eval set hasn't changed in >3 months

**Lesson:** Eval quality matters as much as prompt quality. A benchmark that always passes tells you nothing. Measure what engineers actually care about, not what's easy to score.
