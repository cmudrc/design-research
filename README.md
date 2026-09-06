# design-research
[![CI](https://github.com/cmudrc/design-research/actions/workflows/ci.yml/badge.svg)](https://github.com/cmudrc/design-research/actions/workflows/ci.yml)
[![Coverage](https://raw.githubusercontent.com/cmudrc/design-research/HEAD/.github/badges/coverage.svg)](https://github.com/cmudrc/design-research/actions/workflows/ci.yml)
[![Examples Passing](https://raw.githubusercontent.com/cmudrc/design-research/HEAD/.github/badges/examples-passing.svg)](https://github.com/cmudrc/design-research/actions/workflows/examples.yml)
[![API in Examples](https://raw.githubusercontent.com/cmudrc/design-research/HEAD/.github/badges/examples-api-coverage.svg)](https://github.com/cmudrc/design-research/actions/workflows/examples.yml)
[![Docs](https://github.com/cmudrc/design-research/actions/workflows/docs-pages.yml/badge.svg)](https://github.com/cmudrc/design-research/actions/workflows/docs-pages.yml)
[![PyPI Version](https://img.shields.io/pypi/v/design-research.svg)](https://pypi.org/project/design-research/)
[![Python Versions](https://img.shields.io/pypi/pyversions/design-research.svg)](https://pypi.org/project/design-research/)

`design-research` is the umbrella entry point for the
CMU Design Research Collective design-research ecosystem. It supplies one
discoverable namespace, exact component-version pins, and compatibility-tested
examples for the package family while leaving component implementation in the
packages that own it.

## Quickstart

Python 3.12 or newer is required.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install design-research
```

Then use the four wrapper submodules through the umbrella namespace:

```python
import design_research as dr

problem_ids = dr.problems.list_problems()
problem = dr.problems.get_problem(problem_ids[0])

print(problem.metadata.title)
print(dr.agents.Workflow)
print(dr.experiments.Study)
print(dr.analysis.validate_unified_table)
```

The package root intentionally exports only `__version__` and the four wrapper
submodules. For the pinned package family, each wrapper mirrors its component
package's public exports. Use `design_research.problems`,
`design_research.agents`, `design_research.experiments`, and
`design_research.analysis`; install a component directly when you only need
that package or its optional extras.

See the [installation guide](https://cmudrc.github.io/design-research/installation.html),
[learning path](https://cmudrc.github.io/design-research/learn.html), and
[compatibility and package status](https://cmudrc.github.io/design-research/compatibility.html)
for the next step.

## Study to Evidence to Paper Draft

Study execution always retains terminal run evidence; it does not create a
manuscript. An explicit later action can use the exported study directory and
installed component packages to create a clearly labeled `paper-draft/` in a
fresh process. The output contains evidence-backed LaTeX and Markdown,
curated references, linked tables and figures, and visible TODOs wherever
evidence or author judgment is still required.

The deterministic offline examples
[`ideation_evidence_to_paper.py`](examples/ideation_evidence_to_paper.py) and
[`computational_design_evidence_to_paper.py`](examples/computational_design_evidence_to_paper.py)
exercise that full handoff, compile the LaTeX when Tectonic is installed, and
verify `study-paper-draft.zip`. The generated material is a review-required
paper draft, not an asserted scientific interpretation or publication-ready
manuscript.

## Architecture: Two Complementary Views

The same four packages are useful to describe in two different ways:

- **Control topology:** Problems and Agents are peer study inputs. Experiments
  owns study design and coordinates their execution, then defines the artifact
  handoff to Analysis.
- **Runtime and data flow:** Problems + Agents → Experiments artifact set →
  Analysis → evidence that can refine the next study protocol.

Neither view is a package-install order. The umbrella routes imports and pins a
tested combination; it does not move implementation ownership out of the
component packages.

![Two complementary views of the design-research ecosystem](docs/_static/ecosystem-platform.svg)

## Ecosystem Packages

- **Problems** — tasks, prompts, grammars, benchmarks, and evaluators:
  [documentation](https://cmudrc.github.io/design-research-problems/) ·
  [source](https://github.com/cmudrc/design-research-problems)
- **Agents** — AI participants, workflows, tools, and traceable reasoning:
  [documentation](https://cmudrc.github.io/design-research-agents/) ·
  [source](https://github.com/cmudrc/design-research-agents)
- **Experiments** — hypotheses, factors, conditions, replications, execution,
  and artifact export:
  [documentation](https://cmudrc.github.io/design-research-experiments/) ·
  [source](https://github.com/cmudrc/design-research-experiments)
- **Analysis** — validation, transformation, statistics, and visualization of
  study artifacts:
  [documentation](https://cmudrc.github.io/design-research-analysis/) ·
  [source](https://github.com/cmudrc/design-research-analysis)

## Repository Development

For a source checkout, install contributor tooling and run the deterministic
all-layer compatibility path:

```bash
git clone https://github.com/cmudrc/design-research.git
cd design-research
python -m venv .venv
source .venv/bin/activate
make dev
make test
python examples/canonical_artifact_flow.py
make examples-test
```

`examples/canonical_artifact_flow.py` resolves a packaged problem, runs the
public seeded baseline agent, exports experiment artifacts, and validates them
through the umbrella's Analysis wrapper. The default checks remain
deterministic and offline-first.

The separate live walkthrough uses the Agents package's `llama_cpp` extra:

```bash
python -m pip install "design-research-agents[llama_cpp]==0.6.0"
make run-example
```

Set `LLAMA_CPP_MODEL` to a local GGUF file or allow the installed Hugging Face
client to fetch the walkthrough's default model. Set
`RUN_LLAMA_CPP_EXAMPLES=1` to include this path in `make examples-test`;
`RUN_OLLAMA_EXAMPLES=1` independently enables the Ollama tutorial.

## Quality Signals

- **Coverage** reports total line coverage for the default deterministic test
  suite; CI requires at least 95%.
- **Examples Passing** reports per-file pass/fail evidence from checked-in
  scripts and notebooks.
- **API in Examples** reports curated top-level `__all__` exports referenced by
  runnable examples; CI requires 100%.

Run `make coverage`, `make examples-test`, and `make examples-coverage` to
reproduce those checks. `make notebooks-check` verifies that focused
notebooks' saved outputs match their source.

For documentation changes, run:

```bash
make docs-check
make docs-build
```

`docs-check` validates generated tutorial material and cross-file contracts;
`docs-build` performs the strict Sphinx HTML build. Run `make docs-linkcheck`
when public links change.

The tested package versions and current package metadata status are documented
in the [compatibility page](https://cmudrc.github.io/design-research/compatibility.html).
Those factual classifiers are not an ecosystem-wide maturity scheme; that
separate policy remains tracked in
[issue #12](https://github.com/cmudrc/design-research/issues/12).

## Public API

The supported umbrella surface is what `design_research.__all__` and the four
wrapper modules export for the exact component versions pinned in
`pyproject.toml`. Package-specific APIs, optional dependencies, and behavior
remain documented by their owning packages.

## Contributing

See [CONTRIBUTING.md](https://github.com/cmudrc/design-research/blob/HEAD/CONTRIBUTING.md)
for the contributor workflow and release gates.
