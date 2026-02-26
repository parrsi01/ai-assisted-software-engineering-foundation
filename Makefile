PYTHON ?= python3

.PHONY: help validate validate-quick test lint pycheck agent-demo tree

help:
	@printf "Targets:\n"
	@printf "  make validate        Run full repository validation\n"
	@printf "  make validate-quick  Run quick repository validation\n"
	@printf "  make test            Run unit tests\n"
	@printf "  make lint            Run shell/python syntax checks and index checks\n"
	@printf "  make agent-demo      Run agent starter example\n"
	@printf "  make tree            Print repo directory tree (fallback if tree missing)\n"

validate:
	./validate_repo.sh

validate-quick:
	./validate_repo.sh --quick

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

lint:
	bash -n validate_repo.sh
	find scripts -type f -name '*.sh' -exec bash -n {} \;
	$(MAKE) pycheck
	$(PYTHON) scripts/check_library_index.py

pycheck:
	$(PYTHON) -m py_compile scripts/check_library_index.py
	$(PYTHON) -m py_compile projects/agent-starter-lab/src/agent_runtime.py
	$(PYTHON) -m py_compile tests/test_agent_runtime.py

agent-demo:
	cd projects/agent-starter-lab && $(PYTHON) -m src.agent_runtime --goal "Write unit tests for a small parser" --context ../.. --mode safe

tree:
	@if command -v tree >/dev/null 2>&1; then tree -a -I '.git'; else find . -path './.git' -prune -o -print | sort; fi
