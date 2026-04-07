# AI-Assisted Software Engineering — Full Study Notes

---

## Module 01: AI Foundations & LLM Basics

### What LLMs Are
Large Language Models predict the next token given a sequence of preceding tokens. They are:
- **Trained** on text corpora — they have learned statistical patterns, not facts
- **Stateless** — each inference is independent; the "memory" is entirely in the context window
- **Probabilistic** — the same input can produce different outputs depending on temperature/sampling

### What LLMs Are Not
- Not a database — they don't look things up; they generate text that resembles lookup results
- Not a runtime — they cannot execute code; they produce text that looks like code
- Not infallible — they will produce plausible-sounding wrong answers (hallucinations)

### Tokens vs Words
- Token ≈ 3-4 characters on average; "unrecognizable" might be 4 tokens
- Context window = maximum tokens the model processes at once (input + output combined)
- Cost and latency scale with token count — context engineering matters economically

### Generation vs Execution (Critical Distinction)
| What you see | What it actually is |
|-------------|---------------------|
| LLM wrote Python code | LLM generated text that looks like valid Python |
| LLM said "the function returns X" | LLM predicted this text is likely; it did not run the function |
| LLM "fixed a bug" | LLM produced a modified version that looks fixed; it wasn't tested |

**Engineer's rule:** text-only output = hypothesis. Tool-verified + tests passing = evidence.

### Temperature / Determinism
- `temperature=0`: nearly deterministic, greedy token selection
- `temperature>0`: sampling introduces variation — useful for creative tasks, risky for code generation
- For code and analysis: prefer low temperature to reduce variance

### Common Beginner Mistakes
- Treating LLM output as ground truth without verification
- Providing no context ("fix this bug" with no code)
- Asking for multiple unrelated things in one prompt
- No explicit acceptance criteria — how will you know if the output is correct?

---

## Module 02: Prompt Software Engineering

### Prompt as Specification
A prompt is an executable task specification. Bad prompts produce bad outputs not because the model failed, but because the spec was underspecified.

### 7 Structural Elements
1. **Role**: "You are a senior Python engineer reviewing for security issues"
2. **Task**: exactly what to do (one primary task per prompt)
3. **Context**: files, environment, constraints, relevant background
4. **Acceptance criteria**: what does success look like? (testable, observable, bounded)
5. **Constraints**: scope limits, what NOT to do, output format
6. **Safety / guardrails**: no destructive commands, minimal diffs, verify before claiming done
7. **Validation request**: "After making changes, run the test suite and report results"

### 5 Quality Dimensions
| Dimension | Definition | Anti-pattern |
|-----------|-----------|--------------|
| Specificity | Precise task description | "Improve this code" |
| Scope control | Clear boundaries on what to change | "Feel free to refactor as needed" |
| Verifiability | Testable acceptance criteria | "Make it better" |
| Safety | Guardrails on destructive actions | No constraint on file scope |
| Reusability | Template structure for similar tasks | One-off monolithic prompts |

### Prompt Layering (Advanced)
Separate concerns across prompt layers:
1. **Planning prompt**: "Analyze this problem and identify the approach" (no code changes)
2. **Implementation prompt**: "Implement the approach from step 1, targeting file X only"
3. **Review prompt**: "Review the diff from step 2 for bugs, regressions, security issues"
4. **Verification prompt**: "Run these tests and confirm they pass: [list]"

Why: mixing brainstorming with production code generation produces scope bleed and unreviewed changes.

---

## Module 03: Context Engineering & Repo-Aware Workflows

### Core Principle
Right context > polished prompt wording. A perfect prompt with wrong context produces wrong output.

### Context Packet Components
```
1. Task definition (what to do)
2. Relevant file contents (only files needed for the task)
3. Data structures / interfaces (how the code connects)
4. Environment constraints (Python version, framework, test runner)
5. Known state (what was tried before, what failed)
6. Acceptance criteria
```

### What NOT to Include
- Entire codebase when only 2 files are relevant
- Configuration files not relevant to the task
- Comment history / git log (adds tokens, reduces signal)
- Duplicate information

### Token Management
- Context window budget: reserve 30% for output, 70% for input
- Prioritize: task description > relevant code > background context
- Cut: boilerplate, generic documentation, irrelevant file sections

### Workflow: Repo-Aware Context Assembly
```
1. Read the task — what file/function/module is in scope?
2. Locate: find the relevant files (Glob/Grep)
3. Confirm: read just the relevant sections (not entire files if large)
4. Package: task + targeted file contents + interface definitions
5. Deliver: minimal, focused context prompt
6. Test: verify output against acceptance criteria
```

### Common Pitfalls
| Pitfall | Effect |
|---------|--------|
| Pasting entire repo | Model loses focus; misidentifies relevant code |
| Stale context (old API version) | Model generates code for deprecated interfaces |
| No interface definition | Model hallucates method signatures |
| Ambiguous file scope | Model edits wrong files |

---

## Module 04: AI-Assisted Coding Patterns

### 6 Core Task Patterns

**1. Implementation** — generate new code from spec
- Provide: interface signature, data types, constraints, example input/output
- Risk: model may implement a different interface than what callers expect
- Verify: run existing tests that call the new code

**2. Debugging** — find root cause of failing test or error
- Provide: error message + stack trace + minimal reproducible code snippet
- Risk: model may fix the symptom not the root cause
- Verify: original failing test now passes; no new tests broken

**3. Refactoring** — improve structure without changing behavior
- Provide: the function/module to refactor, what tests cover it
- Risk: behavior change masked as refactor
- Verify: all existing tests pass; diff reviewed manually

**4. Test Generation** — write tests for existing code
- Provide: function signature + docstring + example behavior
- Risk: tests match current (possibly buggy) behavior, not intended behavior
- Verify: tests actually test the spec, not just the implementation

**5. Code Review** — identify bugs, regressions, risks
- Provide: diff + original code + expected behavior + constraints
- Risk: model misses context about how code is called (missing correlated files)
- Verify: model's findings checked against actual test results

**6. Documentation** — generate docstrings, comments, READMEs
- Provide: function code + usage context
- Risk: technically correct doc for wrong behavior (if code is buggy)
- Verify: doc matches observed runtime behavior, not just code text

### AI Coding Loop (7 Steps)
1. Define acceptance criteria first
2. Assemble minimal context packet
3. Submit scoped prompt
4. Review output for assumptions and unsafe actions
5. Apply changes (do not accept blindly)
6. Run tests
7. Record: prompt used, files changed, test results, residual risks

---

## Module 05: Verification, Testing & Trust

### Trust Earned Through Evidence
| Evidence Type | Strength | Example |
|--------------|---------|---------|
| Tests pass on real infrastructure | Strong | CI pipeline green |
| Tests pass in isolation with mocks | Medium | Unit tests (mock can diverge from real) |
| Code review by another engineer | Medium | Peer review found no issues |
| LLM says "it looks correct" | Weak | Model predicted plausible text |
| "It compiled" | Minimal | Syntax valid; logic may be wrong |

### Verification Stack (5 Layers)
1. **Type checking**: mypy/pyright — catches type errors without running
2. **Linting**: ruff/flake8 — catches style and common logic errors
3. **Unit tests**: function-level correctness in isolation
4. **Integration tests**: component interactions against real dependencies
5. **End-to-end tests**: full user workflow validation

### Hallucination Containment
- Always cite sources: "this API exists in version X.Y, confirmed by reading the file"
- Require file path + line number citations in reviews
- Never trust LLM claims about external APIs without verification against official docs
- If in doubt: write a minimal test before trusting the claim

### Acceptance Criteria Design
Good acceptance criteria are:
- **Observable**: can be checked without ambiguity ("test_login passes" not "auth works")
- **Testable**: has a specific assertion ("returns 404 for unknown user" not "handles errors")
- **Bounded**: limited scope ("only modify auth.py" not "fix the auth system")
- **Outcome-tied**: specifies behavior, not implementation ("function completes in <100ms" not "use a cache")

---

## Module 06: Prompt Debugging & Failure Analysis

### Failure Taxonomy
| Type | Description | Fix |
|------|-------------|-----|
| Ambiguity failure | Task underspecified; model guesses intent | Add explicit constraints and examples |
| Scope bleed | Model edits files outside intended scope | Add explicit file scope constraints |
| Hallucination | Model generates confident wrong facts/APIs | Require citations; verify against source |
| Format failure | Output format wrong for downstream use | Specify exact output format with example |
| Policy failure | Model refuses or adds unwanted caveats | Clarify authorized context; adjust role |
| Verification failure | Model claims done but output wrong | Require explicit test command + output |

### Debug Procedure (5 Steps)
1. Identify which failure type occurred
2. Isolate the variable: was it context, task definition, constraints, or format?
3. Change ONE thing in the prompt
4. Re-run with the same task
5. Compare output — did the single change fix the issue?

### Retry Strategy
- Change only one variable per retry (otherwise you don't know what fixed it)
- If ambiguity failure: add one concrete example
- If scope bleed: add explicit "do NOT modify files other than X"
- If hallucination: add "cite the specific file and line number for each API you reference"
- After 2 failed retries on same approach: change the approach, not just the wording

---

## Module 07: Agent Engineering & Orchestration

### What Makes Something an Agent
An agent is an LLM system with:
1. **Goal**: a task specification it's working toward
2. **Tools**: functions it can call (file read, shell command, API call)
3. **State**: memory of what it has done (trace, context window, persistent store)
4. **Plan**: a sequence of actions toward the goal
5. **Policies**: constraints on what actions are allowed
6. **Iteration**: takes actions, observes results, updates plan

### 6 Agent Failure Modes
| Failure | Description | Mitigation |
|---------|-------------|------------|
| Wrong plan | Agent misunderstood the goal | Explicit goal + acceptance criteria |
| Wrong tool | Correct intent, used wrong function | Tool descriptions must be unambiguous |
| Stale context | Acting on outdated information | Refresh context before critical actions |
| Unsafe command | Destructive action without approval | Command guardrails + deny list |
| Silent assumption drift | Assumptions that were valid at start no longer are | Checkpoint verification steps |
| Unverified completion | Claims task done without checking | Require verification step before declaring success |

### Engineering Controls
```python
MAX_STEPS = 20           # prevent infinite loops
BLOCKED_PATTERNS = [     # deny list for shell commands
    "rm -rf",
    "git reset --hard",
    "sudo ",
    "chmod -R 777",
]
REQUIRED_VERIFICATION = True   # must run tests before claiming success
CHECKPOINT_INTERVAL = 5        # log trace every N steps
```

### Single vs Multi-Agent
| Factor | Single Agent | Multi-Agent |
|--------|-------------|-------------|
| Complexity | Simple | Higher overhead |
| Failure isolation | Single point | Per-agent failure containment |
| Parallelism | Sequential | Parallel workstreams |
| State management | Simpler | Schema versioning required |
| Use when | Most tasks | Explicitly parallel tasks with clear handoffs |

---

## Module 08: Tool Use, Permissions & Guardrails

### Tool Risk Classification
| Class | Examples | Policy |
|-------|---------|--------|
| Read-only | file read, grep, list dir | Allow by default |
| Compute-only | format, parse, calculate | Allow by default |
| Write (local) | file write, file edit | Require scope constraint |
| Write (remote) | API POST, database write | Require approval |
| Destructive | rm, reset, drop | Deny by default, explicit approval required |

### Permission Models (in order of trust)
1. **Deny by default**: everything denied unless explicitly allowed (safest)
2. **Allowlist**: only listed operations permitted
3. **Approval-required**: agent proposes, human approves
4. **Deny list**: everything allowed except explicitly blocked (riskiest)

### Practical Guardrails
- Path restrictions: only write within `/project/src/`, never `..` traversal
- Command deny list: pattern match against `_BLOCKED_PATTERNS`
- No `sudo` without explicit human approval
- Dry-run mode: show what would happen before executing
- Rate limits: prevent runaway loops
- Full trace logging: every tool call recorded

---

## Module 09: RAG & Knowledge Systems

### What RAG Does
Retrieval-Augmented Generation: retrieve relevant documents at query time → include in context → model generates answer grounded in retrieved content.

### 9-Step RAG Pipeline
1. Query received
2. Query embedding generated
3. Vector similarity search against index
4. Top-K chunks retrieved
5. Reranking (optional)
6. Context budget applied (trim to token limit)
7. Prompt assembled: query + retrieved chunks + instructions
8. Model generates response with citations
9. Citations verified against source documents

### Coding-Specific Metadata
Each chunk should carry:
- File path
- Language
- Symbol name (function/class/variable)
- Commit hash (for staleness tracking)
- Module ownership
- Test file linkage

### Failure Modes
| Failure | Cause | Fix |
|---------|-------|-----|
| Stale results | Index not refreshed after refactor | Trigger rebuild on merge to main |
| Chunking breaks functions | Chunk boundary splits function body | Chunk at AST boundaries, not line count |
| Naming mismatch | Camelcase in query, snake_case in code | Normalize at index time |
| Citation hallucination | Model cites plausible but non-existent file | Verify citations against index before output |

---

## Modules 10–14: Quick Reference

### Module 10: Evals
- **5 eval types**: functional correctness, code quality, safety, format compliance, regression
- **Regression tracking**: pass rate, major failure count, safety violations, avg rework, formatting compliance
- **Benchmark overfitting**: if you evaluate on the same set you train prompts against, you overfit
- **Rule**: version prompt + eval artifacts together; bump version when either changes

### Module 11: Security & Compliance
- **6 risk areas**: secret leakage in prompts, IP exposure to vendor models, data classification mismatch, output injection, supply chain (model provider), audit trail gaps
- **Critical rule**: never assume prompt text is private; treat as potentially logged/cached by vendor
- **Immediate rule**: rotate credentials if they appear in any prompt sent to an external model

### Module 12: Team Workflows
- AI helps most: boilerplate, test generation, documentation, code review prep, refactoring proposals
- Humans must stay in: auth changes, data migrations, prod deployments, security architecture, incident response
- CI/CD: AI output treated like any change candidate — lint + tests mandatory before merge

### Module 13: Building Agents
Build sequence: read-only tools first → add tracing → add guarded writes → add evals → add CI gate → RBAC → multi-agent only when necessary.

### Module 14: Enterprise & Career
- 5 maturity stages: ad-hoc → personal tooling → team standards → org platform → governed AI-native SDLC
- Portfolio must demonstrate: prompt structure discipline, agent guardrail design, eval methodology, team operating model understanding
