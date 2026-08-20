# AGENTS.md

## Purpose

This repository hosts `design-research`, a thin Python 3.12+ umbrella package
for the CMU Design Research Collective ecosystem. Keep changes focused,
keep the public API intentional, and avoid duplicating logic from sibling
component libraries.

## Setup

- Create and activate a virtual environment:
  - `python -m venv .venv`
  - `source .venv/bin/activate`
- The preferred interpreter target lives in `.python-version` (`3.12`).
- Install local tooling with `make dev`.

## Testing And Validation

Use the smallest useful check while iterating, then run the full gate before
merging.

- Fast local loop:
  - `make fmt`
  - `make lint`
  - `make type`
  - `make test`
- If docs changed:
  - `make docs-check`
  - `make docs`
- If the example changed:
  - `make examples-test` (live examples require their runtime-specific opt-in variable)
  - `make live-smoke` for a focused semantic check of both live tutorials (or use the runtime-specific `make live-smoke-ollama` and `make live-smoke-llama-cpp` targets)
- Pre-merge baseline:
  - `make ci`
- Pre-publish baseline:
  - `make release-check`

## Public Vs Private Boundaries

- The supported public surface is whatever is re-exported from
  `src/design_research/__init__.py` and the wrapper submodules:
  `design_research.problems`, `design_research.agents`,
  `design_research.experiments`, and `design_research.analysis`.
- Keep wrapper modules thin and trust the sibling libraries to define their own
  public surfaces. Wrapper submodules should mirror each sibling package's
  `__all__` by default rather than maintaining local allowlists.
- If internal helper modules are added, prefix them with `_` and keep them out
  of top-level exports unless there is a deliberate API decision.

## Behavioral Guardrails

- Keep tests deterministic and offline by default.
- Run `make live-smoke` periodically and before releases on model-capable infrastructure; do not make the default CI loop depend on local model services.
- Let the canonical walkthrough fail fast when the `llama.cpp` runtime is missing rather than silently falling back.
- Keep total line coverage at or above 95% in CI and local release work.
- Update tests, docs, and examples alongside behavior changes.
- Avoid broad dependency growth in the base install.
- Treat this package as an umbrella wrapper; do not duplicate implementation
  logic from sibling repositories.

## Release Planning

- Do not create monthly milestone naming tables, themed release PR names, or
  calendar release branches as default maintenance.
- Prefer small issue/PR-scoped planning and package version releases driven by
  user-facing changes.
- Use GitHub milestones only for explicit, short-lived initiatives with an
  active owner; they are optional scheduling aids, not release gates.
- Name release branches and release PRs for the version or concrete change set
  they contain.
- When publishing, update package metadata, docs, examples, and GitHub
  Releases/PyPI notes as needed. Do not add README callouts that point to
  monthly milestones.

## Keep This File Up To Date

Update this file whenever contributor workflow changes, especially setup
commands, validation commands, or public API expectations.
