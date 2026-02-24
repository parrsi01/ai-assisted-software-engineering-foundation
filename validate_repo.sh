#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

quick_mode=0
for arg in "$@"; do
  case "$arg" in
    --quick) quick_mode=1 ;;
    -h|--help)
      cat <<'USAGE'
Usage: ./validate_repo.sh [--quick]

Checks repository structure, placeholder markers, script syntax, ticket format, and unit tests.
USAGE
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg" >&2
      exit 1
      ;;
  esac
done

failures=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; failures=$((failures+1)); }
warn() { echo "WARN: $1"; }

check_file() {
  local path="$1"
  [[ -f "$path" ]] && pass "$path present" || fail "$path present"
}

check_dir() {
  local path="$1"
  [[ -d "$path" ]] && pass "$path present" || fail "$path present"
}

echo "Repository Validation"
check_file README.md
check_file docs/PROJECT_MANUAL.md
check_file docs/LESSON_EXECUTION_COMPANION.md
check_file prompts/oneshot/AISE_REPO_BUILDER_ONESHOT.md
check_dir docs
check_dir Library
check_dir library
check_dir projects
check_dir tickets
check_dir scripts
check_dir tests
check_file .github/workflows/ci.yml
check_file .github/workflows/lint.yml

if python3 - <<'PY'
from pathlib import Path
import sys
repo = Path('.')
required_sections = ["## Scenario", "## Reproduce", "## Debug", "## Root Cause", "## Fix", "## Reset"]
paths = sorted((repo / 'tickets' / 'jira').glob('AISE-*/README.md'))
if len(paths) < 10:
    print(f"Need at least 10 Jira tickets, found {len(paths)}")
    sys.exit(1)
for p in paths:
    text = p.read_text(encoding='utf-8')
    missing = [s for s in required_sections if s not in text]
    if missing:
        print(f"{p}: missing {missing}")
        sys.exit(1)
print(f"Validated {len(paths)} Jira ticket docs")
PY
then
  pass "Jira ticket structure"
else
  fail "Jira ticket structure"
fi

if python3 - <<'PY'
from pathlib import Path
import sys
lib = Path('Library')
files = sorted(lib.glob('*.md'))
if len(files) < 15:
    print(f"Expected >=15 markdown files in Library, found {len(files)}")
    sys.exit(1)
print(f"Library file count OK: {len(files)}")
PY
then
  pass "Library completeness (file count)"
else
  fail "Library completeness (file count)"
fi

if command -v rg >/dev/null 2>&1; then
  if rg -n "TODO|TBD|FIXME|PLACEHOLDER|REPLACE_WITH_|lorem ipsum" . \
      --glob '!**/.git/**' \
      --glob '!validate_repo.sh' \
      --glob '!.github/workflows/**' >/tmp/aise_placeholders.out; then
    cat /tmp/aise_placeholders.out
    fail "No placeholder/template markers remain"
  else
    pass "No placeholder/template markers remain"
  fi
else
  pass "Placeholder scan skipped (rg not installed)"
fi
rm -f /tmp/aise_placeholders.out

shell_failed=0
while IFS= read -r -d '' f; do
  if ! bash -n "$f"; then
    echo "Syntax error: $f"
    shell_failed=1
  fi
done < <(find scripts -type f -name '*.sh' -print0 2>/dev/null)

if [[ -f validate_repo.sh ]]; then
  bash -n validate_repo.sh || shell_failed=1
fi

[[ $shell_failed -eq 0 ]] && pass "Shell syntax checks" || fail "Shell syntax checks"

if python3 -m py_compile scripts/check_library_index.py projects/agent-starter-lab/src/agent_runtime.py >/dev/null 2>&1; then
  pass "Python syntax checks"
else
  fail "Python syntax checks"
fi

if python3 scripts/check_library_index.py >/dev/null 2>&1; then
  pass "Library index checker"
else
  fail "Library index checker"
fi

if [[ -d tests ]]; then
  if python3 -m unittest discover -s tests -p 'test_*.py' -v >/tmp/aise_unittest.out 2>&1; then
    pass "Unit tests"
  else
    cat /tmp/aise_unittest.out
    fail "Unit tests"
  fi
  rm -f /tmp/aise_unittest.out
else
  warn "No tests directory"
fi

if [[ $quick_mode -eq 0 ]]; then
  echo "\nRepository Metrics"
  python3 - <<'PY'
from pathlib import Path
repo = Path('.')
print(f"docs_md={sum(1 for _ in (repo/'docs').rglob('*.md'))}")
print(f"library_md={sum(1 for _ in (repo/'Library').glob('*.md'))}")
print(f"tickets={sum(1 for _ in (repo/'tickets'/'jira').glob('AISE-*'))}")
print(f"projects={sum(1 for _ in (repo/'projects').iterdir() if _.is_dir())}")
PY
fi

if [[ $failures -ne 0 ]]; then
  echo "Validation failed with $failures issue(s)." >&2
  exit 1
fi

echo "Validation passed."
