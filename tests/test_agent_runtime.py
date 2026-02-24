import json
import subprocess
import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "projects" / "agent-starter-lab"

sys.path.insert(0, str(LAB))
from src.agent_runtime import build_plan, run_agent  # noqa: E402


class AgentRuntimeTests(unittest.TestCase):
    def test_build_plan_includes_test_step(self) -> None:
        plan = build_plan("Add unit tests for parser")
        self.assertTrue(any("test" in step.lower() for step in plan))

    def test_safe_mode_blocks_destructive_commands(self) -> None:
        trace = run_agent("clean and reset workspace", str(ROOT), mode="safe")
        self.assertTrue(any("rm -rf" in cmd for cmd in trace.blocked_actions))

    def test_permissive_mode_allows_destructive_commands(self) -> None:
        trace = run_agent("clean and reset workspace", str(ROOT), mode="permissive")
        self.assertFalse(trace.blocked_actions)
        self.assertTrue(any(a.content == "rm -rf build/" for a in trace.actions if a.kind == "shell"))

    def test_cli_outputs_json(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "src.agent_runtime",
                "--goal",
                "Add tests",
                "--context",
                "../..",
                "--mode",
                "safe",
            ],
            cwd=LAB,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["mode"], "safe")
        self.assertIn("plan", payload)


if __name__ == "__main__":
    unittest.main()
