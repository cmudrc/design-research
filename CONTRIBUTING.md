# Contributing

## Development Setup

```bash
python -m venv .venv
source .venv/bin/activate
make dev
```

The preferred maintainer interpreter is set in `.python-version` (`3.12`).

Before cutting a release, run:

```bash
make release-check
```

## Local Quality Checks

Run these before opening a pull request:

```bash
make fmt
make lint
make type
make docstrings-check
make test
make docs-check
make docs
```

If the example or walkthrough docs changed, also run:

```bash
make run-example
make examples-test
```

`make run-example` is the live walkthrough path and uses a managed
`llama.cpp` client. Install `llama-cpp-python[server]` before running it. If
you want to use the default GGUF download path, also install
`huggingface-hub`; otherwise set `LLAMA_CPP_MODEL` to point at a specific local
GGUF file. `make examples-test` skips that walkthrough unless
`RUN_LIVE_EXAMPLE=1`, which keeps the default local and CI loop offline-safe.

## Coverage Policy

`design-research` follows the family-wide baseline of at least 90% total line
coverage in CI.

- Treat 90% as a strict floor for this repository, not a soft target.
- Keep new family repositories at the same baseline unless the shared policy is
  intentionally changed across the ecosystem.
- `make ci` enforces this floor through the coverage gate, so coverage-impacting
  changes should be validated there before merge.

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
