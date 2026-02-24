from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

_BLOCKED_PATTERNS = ("rm -rf", "git reset --hard", "sudo ", "chmod -R 777")


@dataclass
class AgentAction:
    kind: str
    content: str


@dataclass
class AgentTrace:
    goal: str
    context: str
    mode: str
    plan: List[str]
    actions: List[AgentAction]
    blocked_actions: List[str]
    summary: str


def build_plan(goal: str) -> List[str]:
    goal_l = goal.lower()
    steps = [
        "Clarify scope and acceptance criteria",
        "Inspect relevant files and tests",
        "Implement minimal change",
        "Run validation/tests",
        "Summarize diff and residual risks",
    ]
    if "test" in goal_l:
        steps.insert(2, "Identify failing or missing test cases")
    if "refactor" in goal_l:
        steps.insert(3, "Preserve behavior contract before refactor")
    return steps


def propose_actions(goal: str) -> List[AgentAction]:
    actions = [
        AgentAction("note", f"Goal received: {goal}"),
        AgentAction("shell", "rg --files"),
        AgentAction("shell", "python -m unittest -q"),
    ]
    if "reset" in goal.lower() or "clean" in goal.lower():
        actions.append(AgentAction("shell", "rm -rf build/"))
    return actions


def apply_guardrails(actions: List[AgentAction], mode: str) -> tuple[List[AgentAction], List[str]]:
    if mode != "safe":
        return actions, []
    allowed: List[AgentAction] = []
    blocked: List[str] = []
    for action in actions:
        if action.kind != "shell":
            allowed.append(action)
            continue
        if any(pattern in action.content for pattern in _BLOCKED_PATTERNS):
            blocked.append(action.content)
            continue
        allowed.append(action)
    return allowed, blocked


def run_agent(goal: str, context: str, mode: str = "safe") -> AgentTrace:
    plan = build_plan(goal)
    proposed = propose_actions(goal)
    actions, blocked = apply_guardrails(proposed, mode)
    summary = (
        "Planned a bounded AI-assisted engineering workflow with guardrails. "
        f"{len(actions)} actions allowed, {len(blocked)} blocked in {mode} mode."
    )
    return AgentTrace(
        goal=goal,
        context=context,
        mode=mode,
        plan=plan,
        actions=actions,
        blocked_actions=blocked,
        summary=summary,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Minimal agent starter runtime")
    parser.add_argument("--goal", required=True, help="Goal the agent should plan for")
    parser.add_argument("--context", default=".", help="Context root path")
    parser.add_argument("--mode", choices=["safe", "permissive"], default="safe")
    args = parser.parse_args()

    ctx = str(Path(args.context).resolve())
    trace = run_agent(goal=args.goal, context=ctx, mode=args.mode)
    output = asdict(trace)
    output["actions"] = [asdict(a) for a in trace.actions]
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
