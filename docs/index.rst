design-research
===============

The umbrella entry point for the
CMU Design Research Collective design-research ecosystem.

``design-research`` supplies one discoverable namespace, exact component
version pins, and compatibility-tested examples for the package family. Its
four wrapper submodules route to public exports owned by the specialized
component packages; the umbrella does not reimplement their research logic.

.. container:: drc-home-badges

   .. raw:: html

      <div class="drc-badge-row">
        <a class="drc-badge-link" href="https://github.com/cmudrc/design-research/actions/workflows/ci.yml">
          <img alt="CI" src="https://github.com/cmudrc/design-research/actions/workflows/ci.yml/badge.svg">
        </a>
        <a class="drc-badge-link" href="https://github.com/cmudrc/design-research/actions/workflows/ci.yml">
          <img alt="Coverage" src="https://raw.githubusercontent.com/cmudrc/design-research/HEAD/.github/badges/coverage.svg">
        </a>
        <a class="drc-badge-link" href="https://github.com/cmudrc/design-research/actions/workflows/examples.yml">
          <img alt="Examples Passing" src="https://raw.githubusercontent.com/cmudrc/design-research/HEAD/.github/badges/examples-passing.svg">
        </a>
        <a class="drc-badge-link" href="https://github.com/cmudrc/design-research/actions/workflows/examples.yml">
          <img alt="API in Examples" src="https://raw.githubusercontent.com/cmudrc/design-research/HEAD/.github/badges/examples-api-coverage.svg">
        </a>
        <a class="drc-badge-link" href="https://github.com/cmudrc/design-research/actions/workflows/docs-pages.yml">
          <img alt="Docs" src="https://github.com/cmudrc/design-research/actions/workflows/docs-pages.yml/badge.svg">
        </a>
        <a class="drc-badge-link" href="https://pypi.org/project/design-research/">
          <img alt="PyPI Version" src="https://img.shields.io/pypi/v/design-research.svg">
        </a>
        <a class="drc-badge-link" href="https://pypi.org/project/design-research/">
          <img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/design-research.svg">
        </a>
      </div>

Get Started
-----------

Python 3.12 or newer is required. A first installed-package session needs only:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install design-research

Then import the package family through the four wrapper submodules:

.. code-block:: python

   import design_research as dr

   problem_ids = dr.problems.list_problems()
   problem = dr.problems.get_problem(problem_ids[0])

   print(problem.metadata.title)
   print(dr.agents.Workflow)
   print(dr.experiments.Study)
   print(dr.analysis.validate_unified_table)

- :doc:`installation` explains the base package and component-owned extras.
- :doc:`quickstart` separates installed-package use from repository development.
- :doc:`learn` provides the guided path through runnable tutorials.
- :doc:`tutorials/study_to_paper_draft` covers the complete retained-evidence
  and explicit paper-draft handoff.
- :doc:`compatibility` records the exact tested versions, package classifiers,
  and artifact-schema contract.

.. container:: drc-home-callout

   .. important::

      **Joining the IDETC 2026 tutorial on Sunday, August 23?** Use the
      :doc:`Workshop Setup and Preflight page <workshop-setup>` to download the
      materials and verify your Python environment before the session.

Architecture: Two Complementary Views
-------------------------------------

Control Topology
~~~~~~~~~~~~~~~~

Problems and Agents are peer study inputs. Experiments owns study design and
coordinates their execution, then defines the artifact handoff to Analysis.

Runtime And Data Flow
~~~~~~~~~~~~~~~~~~~~~

Problems + Agents → Experiments artifact set → Analysis → evidence that can
refine the next study protocol.

These are two views of the same package family, not an installation order.
The umbrella routes imports and pins a tested combination; implementation stays
with the package that owns each behavior.

.. container:: drc-home-ecosystem

   .. image:: _static/ecosystem-platform.svg
      :alt: Two-view diagram showing the control topology and runtime data flow across Problems, Agents, Experiments, and Analysis.
      :class: dark-light drc-ecosystem-figure
      :width: 100%
      :align: center

Ecosystem Packages
------------------

- **Problems** — tasks, prompts, grammars, benchmarks, and evaluators:
  `documentation <https://cmudrc.github.io/design-research-problems/>`__ ·
  `source <https://github.com/cmudrc/design-research-problems>`__
- **Agents** — AI participants, workflows, tools, and traceable reasoning:
  `documentation <https://cmudrc.github.io/design-research-agents/>`__ ·
  `source <https://github.com/cmudrc/design-research-agents>`__
- **Experiments** — hypotheses, factors, conditions, replications, execution,
  and artifact export:
  `documentation <https://cmudrc.github.io/design-research-experiments/>`__ ·
  `source <https://github.com/cmudrc/design-research-experiments>`__
- **Analysis** — validation, transformation, statistics, and visualization:
  `documentation <https://cmudrc.github.io/design-research-analysis/>`__ ·
  `source <https://github.com/cmudrc/design-research-analysis>`__

Quality Signals
---------------

``Coverage`` reports the deterministic test suite's total line coverage;
``Examples Passing`` reports per-file runnable-example results; and
``API in Examples`` reports coverage of curated top-level exports. Use
``make coverage``, ``make examples-test``, and ``make examples-coverage`` to
reproduce them locally.

.. toctree::
   :maxdepth: 2
   :hidden:

   guides
   tutorials/index
   architecture
   reference
