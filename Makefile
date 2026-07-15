PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,$(shell if command -v python3.12 >/dev/null 2>&1; then echo python3.12; else echo python3; fi))
PIP ?= $(PYTHON) -m pip
PYTEST ?= $(PYTHON) -m pytest
RUFF ?= $(PYTHON) -m ruff
MYPY ?= $(PYTHON) -m mypy
SPHINX ?= $(PYTHON) -m sphinx
BUILD ?= $(PYTHON) -m build
TWINE ?= $(PYTHON) -m twine
COVERAGE_MIN ?= 95

.PHONY: help check-python dev dev-release-candidates release-candidates-check install-dev \
	lint fmt fmt-check type test qa coverage docstrings-check \
	run-example examples-test examples-coverage examples-metrics notebooks-refresh \
	docs docs-build docs-check docs-linkcheck \
	release-check ci clean

help:
	@echo "Common targets:"
	@echo "  dev              Install the project in editable mode with dev dependencies."
	@echo "  dev-release-candidates Install reviewed component source commits for pre-release CI."
	@echo "  release-candidates-check Validate immutable component pins against project dependencies."
	@echo "  test             Run the pytest suite."
	@echo "  qa               Run lint, fmt-check, type, and test."
	@echo "  run-example      Execute the live llama.cpp strategy-comparison study example."
	@echo "  examples-test    Execute all offline example scripts and notebooks."
	@echo "  examples-coverage Require every public API export to appear in an example."
	@echo "  examples-metrics Generate example and public-API badge artifacts."
	@echo "  notebooks-refresh Execute offline tutorial notebooks and save their outputs."
	@echo "  docs             Build the HTML docs."
	@echo "  ci               Run the main local CI checks."

check-python:
	@$(PYTHON) -c "import pathlib, sys; print(f'Using Python {sys.version.split()[0]} at {pathlib.Path(sys.executable)}'); raise SystemExit(0 if sys.version_info >= (3, 12) else 1)" || (echo "Python >= 3.12 is required by pyproject.toml"; exit 1)

dev:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e ".[dev]"

dev-release-candidates:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install --force-reinstall --no-deps -r requirements/release-candidates.txt
	$(PIP) install -e ".[dev]"

release-candidates-check: check-python
	$(PYTHON) scripts/check_release_candidates.py

install-dev: dev

lint: check-python
	$(RUFF) check .

fmt: check-python
	$(RUFF) format .

fmt-check: check-python
	$(RUFF) format --check .

type: check-python
	$(MYPY) src

test: check-python
	PYTHONPATH=src $(PYTEST) -q

qa: lint fmt-check type test

coverage: check-python
	mkdir -p artifacts/coverage
	PYTHONPATH=src $(PYTEST) --cov=src/design_research --cov-fail-under=$(COVERAGE_MIN) --cov-report=term --cov-report=json:artifacts/coverage/coverage.json -q
	$(PYTHON) scripts/check_coverage_thresholds.py --coverage-json artifacts/coverage/coverage.json --minimum $(COVERAGE_MIN)

docstrings-check: check-python
	$(PYTHON) scripts/check_google_docstrings.py

run-example: check-python
	PYTHONPATH=src $(PYTHON) examples/prompt_framing_study.py

examples-test: check-python
	$(PYTHON) scripts/run_examples.py

examples-coverage: check-python examples-metrics
	$(PYTHON) scripts/check_example_api_coverage.py --minimum 100

examples-metrics: check-python examples-test
	$(PYTHON) scripts/generate_examples_metrics.py
	$(PYTHON) scripts/generate_examples_badges.py

notebooks-refresh: check-python
	$(PYTHON) scripts/run_notebooks.py --in-place

docs-build: check-python
	PYTHONPATH=src $(SPHINX) -b html docs docs/_build/html -n -W --keep-going -E

docs-check: check-python
	$(PYTHON) scripts/check_docs_consistency.py

docs-linkcheck: check-python
	PYTHONPATH=src $(SPHINX) -b linkcheck docs docs/_build/linkcheck -W --keep-going -E

docs: docs-build

release-check: check-python
	rm -rf build dist
	$(BUILD)
	$(TWINE) check dist/*

ci: release-candidates-check qa coverage docstrings-check docs-check examples-test examples-coverage release-check

clean:
	rm -rf .coverage .mypy_cache .pytest_cache .ruff_cache artifacts build dist docs/_build
	find src -maxdepth 2 -type d -name "*.egg-info" -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type f \( -name "*.pyc" -o -name ".coverage.*" \) -exec rm -f {} + 2>/dev/null || true
