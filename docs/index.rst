design-research
===============

The umbrella entry point for the CMU Design Research Collective ecosystem.

``design-research`` provides a thin, stable, submodule-first namespace over the
sibling libraries. It keeps implementation in specialized packages while
making the ecosystem easier to discover, teach, and cite from one place.

It is intentionally lightweight. The value here is not hidden implementation,
but a coherent starting point for understanding how the package family fits
together and when to drop into the more specialized repos directly.

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
      </div>

Quality Signals
---------------

- ``Coverage`` reports total line coverage for the default deterministic test
  suite; CI requires at least 95%.
- ``Examples Passing`` reports per-file pass/fail evidence from checked-in
  scripts and notebooks in the examples workflow.
- ``API in Examples`` reports curated top-level ``__all__`` exports referenced
  by runnable examples. ``N/N`` means every supported top-level export appears
  in at least one example, and CI requires 100%.

Run ``make coverage``, ``make examples-test``, and ``make examples-coverage``
to reproduce these checks locally. ``make notebooks-check`` verifies that the
focused notebooks' displayed results still match their source.

.. container:: drc-home-callout

   .. note::

      **New to computational design research?** Follow the
      :doc:`Learning Path <learn>` from a first tutorial through a complete
      experiment and analysis workflow.

.. container:: drc-home-callout

   .. important::

      **Joining the IDETC 2026 tutorial on Sunday, August 23?** Use the
      :doc:`Workshop Setup and Preflight page <workshop-setup>` to download the
      materials and verify your Python environment before the session.

Tutorial Series
---------------

Start with one component or follow the complete progression from task selection
through study execution and analysis.

- :doc:`tutorials/problems_text_map`
- :doc:`tutorials/problems_truss_grammar`
- :doc:`tutorials/agents_propose_critic`
- :doc:`tutorials/agents_workflow`
- :doc:`tutorials/experiments_monty_hall`
- :doc:`tutorials/analysis_reliability`
- :doc:`tutorials/full_stack_study`
- :doc:`tutorials/process_comparison`
- :doc:`tutorials/factorial_analysis`

Guides
------

Use these pages to understand the umbrella package, the shared namespace, and
the recommended path through the ecosystem.

- :doc:`learn`
- :doc:`workshop-setup`
- :doc:`tutorials/index`
- :doc:`guides`

Integration With The Ecosystem
------------------------------

The Design Research Collective maintains a modular ecosystem of libraries for
studying human and AI design behavior.

- **design-research-agents** implements AI participants, workflows, and tool-using reasoning patterns.
- **design-research-problems** provides benchmark design tasks, prompts, grammars, and evaluators.
- **design-research-analysis** analyzes the traces, event tables, and outcomes generated during studies.
- **design-research-experiments** sits above the stack as the study-design and orchestration layer, defining hypotheses, factors, conditions, replications, and artifact flows across agents, problems, and analysis.

Together these libraries support end-to-end design research pipelines, from
study design through execution and interpretation.

.. container:: drc-home-ecosystem

   .. image:: _static/ecosystem-platform.svg
      :alt: Ecosystem diagram showing experiments above agents, problems, and analysis.
      :class: dark-light drc-ecosystem-figure
      :width: 100%
      :align: center

.. toctree::
   :maxdepth: 2
   :hidden:

   learn
   workshop-setup
   idetc2026
   tutorials/index
   guides
