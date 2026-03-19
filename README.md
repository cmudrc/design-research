# design-research
[![CI](https://github.com/cmudrc/design-research/actions/workflows/ci.yml/badge.svg)](https://github.com/cmudrc/design-research/actions/workflows/ci.yml)
[![Docs](https://github.com/cmudrc/design-research/actions/workflows/docs-pages.yml/badge.svg)](https://github.com/cmudrc/design-research/actions/workflows/docs-pages.yml)

<!-- release-callout:start -->
> [!IMPORTANT]
> Current monthly release: [Atlas Alignment - April 2026](https://github.com/cmudrc/design-research/milestone/1)  
> Due: April 1, 2026  
> Tracks: March 2026 work
<!-- release-callout:end -->

`design-research` is the umbrella entry-point package in the cmudrc design
research ecosystem.

It provides a thin, curated top-level import surface over the ecosystem's
specialized component libraries.

## Overview

This package focuses on discoverability and coherence rather than reimplementation:

- Submodule-first top-level API: `problems`, `agents`, `experiments`, `analysis`
- Curated re-exports of stable, user-facing APIs from component libraries
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
```

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

The full ecosystem philosophy is documented in
[`docs/philosophy.rst`](docs/philosophy.rst) and in the published docs site.

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
[CONTRIBUTING.md](https://github.com/cmudrc/design-research/blob/main/CONTRIBUTING.md).
