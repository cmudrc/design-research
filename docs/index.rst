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
- ``Examples Passing`` reports checked-in example scripts that execute
  successfully in the examples workflow.
- ``API in Examples`` reports curated top-level ``__all__`` exports referenced
  by runnable examples. ``N/N`` means every supported top-level export appears
  in at least one example, and CI requires 100%.

Run ``make coverage``, ``make examples-test``, and ``make examples-coverage``
to reproduce these checks locally.

.. container:: drc-home-callout

   .. note::

      **Start with** :doc:`compatibility` to choose between the umbrella package
      and direct sibling installs, then run :doc:`canonical_artifact_flow` for
      the deterministic all-layer handoff.

Guides
------

Use these pages to understand the umbrella package, the shared namespace, and
the recommended path through the ecosystem.

- :doc:`compatibility`
- :doc:`canonical_artifact_flow`
- :doc:`prompt_framing_study`
- :doc:`vscode_start`
- :doc:`quickstart`
- :doc:`installation`
- :doc:`concepts`
- :doc:`typical_workflow`
- :doc:`philosophy`

Reference
---------

Look up the stable re-export surface and the extras that shape development and
documentation workflows.

- :doc:`api`
- :doc:`dependencies_and_extras`

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

Start Here
----------

- :doc:`compatibility`
- :doc:`canonical_artifact_flow`
- :doc:`prompt_framing_study`
- :doc:`vscode_start`
- :doc:`quickstart`
- :doc:`installation`
- :doc:`concepts`
- :doc:`typical_workflow`
- :doc:`api`
- :doc:`philosophy`
- `CONTRIBUTING.md <https://github.com/cmudrc/design-research/blob/HEAD/CONTRIBUTING.md>`_

.. toctree::
   :maxdepth: 2
   :hidden:

   compatibility
   canonical_artifact_flow
   prompt_framing_study
   vscode_start
   quickstart
   installation
   concepts
   typical_workflow
   philosophy
   api
   dependencies_and_extras
