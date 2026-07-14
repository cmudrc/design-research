# design-research
[![CI](https://github.com/cmudrc/design-research/actions/workflows/ci.yml/badge.svg)](https://github.com/cmudrc/design-research/actions/workflows/ci.yml)
[![Coverage](https://raw.githubusercontent.com/cmudrc/design-research/HEAD/.github/badges/coverage.svg)](https://github.com/cmudrc/design-research/actions/workflows/ci.yml)
[![Examples Passing](https://raw.githubusercontent.com/cmudrc/design-research/HEAD/.github/badges/examples-passing.svg)](https://github.com/cmudrc/design-research/actions/workflows/examples.yml)
[![API in Examples](https://raw.githubusercontent.com/cmudrc/design-research/HEAD/.github/badges/examples-api-coverage.svg)](https://github.com/cmudrc/design-research/actions/workflows/examples.yml)
[![Docs](https://github.com/cmudrc/design-research/actions/workflows/docs-pages.yml/badge.svg)](https://github.com/cmudrc/design-research/actions/workflows/docs-pages.yml)

`design-research` is the umbrella entry-point package in the cmudrc design
research ecosystem.

It provides a thin, submodule-first namespace over the ecosystem's
specialized component libraries.

## Quality Signals

- **Coverage** reports total line coverage for the default deterministic test suite; CI requires at least 95%.
- **Examples Passing** reports checked-in example scripts that execute successfully in the examples workflow.
- **API in Examples** reports curated top-level `__all__` exports referenced by runnable examples. `N/N` means every supported top-level export appears in at least one example, and CI requires 100%.

Run `make coverage`, `make examples-test`, and `make examples-coverage` to reproduce these checks locally.

## Overview

This package focuses on discoverability and coherence rather than reimplementation:

- Submodule-first top-level API: `problems`, `agents`, `experiments`, `analysis`
- Wrapper submodules that mirror each sibling library's public API by default
- Shared ecosystem framing and philosophy in one canonical package
- Lightweight wrapper design that preserves modular versioning boundaries

## Quickstart

Requires Python 3.12+.
Maintainer workflows target Python `3.12` (`.python-version`).

```bash
python -m venv .venv
source .venv/bin/activate
make dev
make test
python examples/canonical_artifact_flow.py
python -m pip install "llama-cpp-python[server]" huggingface-hub
make run-example
make examples-test
```

On a coordinated pre-release branch, maintainers should run
`make dev-release-candidates` before `make ci`. This installs the exact reviewed
component commits recorded in `requirements/release-candidates.txt`; normal
users and `main` continue to install the exact published versions declared in
`pyproject.toml`.

`examples/canonical_artifact_flow.py` is the deterministic compatibility smoke
path: a packaged problem, public baseline agent, experiment artifacts, and
analysis validation through the umbrella namespace.

`make run-example` is the live walkthrough. It uses a managed
`llama.cpp` client, a workflow-backed strategy comparison, canonical exports,
and downstream analysis helpers. The live workflow path now uses the sibling
public seams directly: a prompt-built `design_research.agents.Workflow`,
`design_research.agents.PromptWorkflowAgent`,
`design_research.agents.SeededRandomBaselineAgent`,
`design_research.experiments.run_study(..., agent_bindings=...)`, plus
`design_research.analysis.integration`. Install
`llama-cpp-python[server]` first. If you want the client to fetch its default
GGUF model automatically, also install `huggingface-hub`; otherwise set
`LLAMA_CPP_MODEL` to a specific local GGUF file.

`make examples-test` stays deterministic and offline-first by default. It runs
the three non-live recipe-first examples and skips the live walkthrough unless
`RUN_LIVE_EXAMPLE=1`.

Install from PyPI:

```bash
pip install design-research
```

Then start from the umbrella namespace:

```python
import design_research as dr
from design_research import problems, agents, experiments, analysis

problem_ids = problems.list_problems()
problem = problems.get_problem(problem_ids[0])

print(type(problem).__name__)
print(agents.MultiStepAgent)
print(experiments.Study)
print(analysis.validate_unified_table)
```

The package root intentionally stays small: it exports only ``__version__`` and
the four wrapper submodules. Reach the stable user-facing APIs through
`design_research.problems`, `design_research.agents`,
`design_research.experiments`, and `design_research.analysis` rather than a
flattened root namespace.

For a VS Code-oriented path that starts from PyPI and then shows the repository
example workflow, see
[Run An Example In VS Code](https://cmudrc.github.io/design-research/vscode_start.html).

## Start Here

Choose your entry point based on how much of the ecosystem you need:

- Start with `design-research` when you want one stable namespace and one set of docs across problems, agents, experiments, and analysis.
- Install a sibling package directly when you only need one layer or want package-specific internals; direct sibling use is fully supported.
- See [Compatibility and Start Here](https://cmudrc.github.io/design-research/compatibility.html) for the tested package combination and install guidance.
- See [Run An Example In VS Code](https://cmudrc.github.io/design-research/vscode_start.html) for a PyPI install path and source checkout example path.
- See [Canonical Artifact Flow](https://cmudrc.github.io/design-research/canonical_artifact_flow.html) for the deterministic all-layer handoff.
- See [Prompt-Framing Study Walkthrough](https://cmudrc.github.io/design-research/prompt_framing_study.html) for the live composed workflow.

## Ecosystem Integration

The Design Research Collective maintains a modular ecosystem of libraries for
studying human and AI design behavior.

- **design-research-agents** implements AI participants, workflows, and tool-using reasoning patterns.
- **design-research-problems** provides benchmark design tasks, prompts, grammars, and evaluators.
- **design-research-analysis** analyzes the traces, event tables, and outcomes generated during studies.
- **design-research-experiments** sits above the stack as the study-design and orchestration layer, defining hypotheses, factors, conditions, replications, and artifact flows across agents, problems, and analysis.

Together these libraries support end-to-end design research pipelines, from
study design through execution and interpretation.

## Philosophy

The full ecosystem philosophy is documented in the
[published philosophy page](https://cmudrc.github.io/design-research/philosophy.html).

## Docs

See the published documentation for quickstart, concepts, workflow framing,
philosophy, and API reference.

Build docs locally with:

```bash
make docs
```

## Public API

The supported top-level public surface is whatever is exported from
`design_research.__all__`.

Top-level exports include:

- Wrapper submodules: `problems`, `agents`, `experiments`, `analysis`
- Package metadata: `__version__`

## Contributing

Contribution workflow and quality gates are documented in
[CONTRIBUTING.md](https://github.com/cmudrc/design-research/blob/HEAD/CONTRIBUTING.md).
