from __future__ import annotations

from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "Library" / "README.md"


def main() -> int:
    if not INDEX.exists():
        print("Library/README.md missing")
        return 1
    text = INDEX.read_text(encoding="utf-8")
    required = [
        "01_ai_foundations_and_llm_basics.md",
        "07_agent_engineering_and_orchestration.md",
        "14_enterprise_adoption_governance_and_career_paths.md",
    ]
    missing = [r for r in required if r not in text]
    if missing:
        print("Missing references:", ", ".join(missing))
        return 1
    print("Library index references required files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
