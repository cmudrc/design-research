# Contributing

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
make dev
```

The preferred maintainer interpreter is set in `.python-version` (`3.12`).

Opening the project in VS Code? Start with `docs/vscode_start.rst` for the
PyPI install path, source checkout path, interpreter selection, and first
example.

### Component Versions

The umbrella package keeps exact component version pins in `pyproject.toml`.
Those pins are the user-facing contract and must resolve from PyPI before this
umbrella release is published.

Release and validate component changes in their owning repositories first.
Then update the corresponding pin and `docs/compatibility.rst` together and run
`make dev` so local checks exercise the same published packages users receive.

## Release Publishing

Before cutting a release, run:

```bash
make release-check
```

The GitHub `Publish` workflow builds and validates distributions before any
upload:

- Publishing a GitHub Release tagged `v{package-version}` publishes to PyPI.
- A manual workflow run is build-only by default.
- A recovery publish requires selecting the release tag and explicitly setting
  `publish=true`; publishing from a branch is rejected.
- Every publishing path rejects a tag that differs from the version in
  `src/design_research/_version.py`.

## Local Quality Checks

Run these before opening a pull request:

```bash
make fmt
make lint
make type
make docstrings-check
make test
make notebooks-type
make notebooks-check
make docs-check
make docs
```

If the example or walkthrough docs changed, also run:

```bash
make examples-test
make live-smoke
```

`make run-example` is the live walkthrough path and uses a managed
`llama.cpp` client. Install `llama-cpp-python[server]` before running it. If
you want to use the default GGUF download path, also install
`huggingface-hub`; otherwise set `LLAMA_CPP_MODEL` to point at a specific local
GGUF file. Set `RUN_LLAMA_CPP_EXAMPLES=1` to include that walkthrough in
`make examples-test`. Set `RUN_OLLAMA_EXAMPLES=1` independently for the
Ollama-backed propose/critic notebook. Both remain opt-in so the default local
and CI loop stays offline-safe.

`make live-smoke` is the focused semantic gate for both live tutorials. It
runs the Ollama notebook once and uses two replicates per condition for the
managed llama.cpp study. Run `make live-smoke-ollama` or
`make live-smoke-llama-cpp` if only one runtime is provisioned. Run the
combined target periodically and before releases on model-capable
infrastructure; it is intentionally separate from offline CI.

`make examples-test` records one result per discovered file in
`artifacts/examples/example_results.json`; badge generation rejects evidence
from a different selection or inventory. When notebook source or displayed
results change, use `make notebooks-refresh` for the offline set. Refresh the
Ollama notebook with its runtime available, then run `make notebooks-check` so
source and output hashes remain synchronized.

## Coverage Policy

`design-research` follows the family-wide baseline of at least 95% total line
coverage in CI.

- Treat 95% as a strict floor for this repository, not a soft target.
- Keep new family repositories at the same baseline unless the shared policy is
  intentionally changed across the ecosystem.
- `make ci` enforces this floor through the coverage gate, so coverage-impacting
  changes should be validated there before merge.
- `make examples-test` executes the checked-in runnable examples.
- `make examples-coverage` requires every curated top-level `__all__` export
  to appear in at least one runnable example.
- `make notebooks-type` strictly checks the Python code in every focused
  tutorial, including live notebooks that default CI does not execute.

Optional but useful:

```bash
pre-commit install
pre-commit run --all-files
```

## Pull Request Guidelines

- Keep changes small enough to review quickly.
- Add or update tests for behavior changes.
- Update docs and examples when interfaces change.
- Describe what changed and how you validated it.

## Code Style

- Python 3.12+ target
- Ruff for linting and formatting
- Mypy for type checking
- Pytest for tests
- Google-style docstrings in `src/`, `examples/`, and `scripts/`
