design-research
===============

The canonical umbrella package for the CMU Design Research Collective ecosystem.

What This Library Does
----------------------

``design-research`` provides a thin, stable entry point over the ecosystem's
component libraries. It keeps implementation in specialized packages while
improving top-level discoverability for research workflows, tutorials, and
papers.

.. container:: drc-home-badges

   .. raw:: html

      <div class="drc-badge-row">
        <a class="drc-badge-link" href="https://github.com/cmudrc/design-research/actions/workflows/ci.yml">
          <img alt="CI" src="https://github.com/cmudrc/design-research/actions/workflows/ci.yml/badge.svg">
        </a>
        <a class="drc-badge-link" href="https://github.com/cmudrc/design-research/actions/workflows/ci.yml">
          <img alt="Coverage" src="https://raw.githubusercontent.com/cmudrc/design-research/main/.github/badges/coverage.svg">
        </a>
        <a class="drc-badge-link" href="https://github.com/cmudrc/design-research/actions/workflows/examples.yml">
          <img alt="Examples Passing" src="https://raw.githubusercontent.com/cmudrc/design-research/main/.github/badges/examples-passing.svg">
        </a>
        <a class="drc-badge-link" href="https://github.com/cmudrc/design-research/actions/workflows/examples.yml">
          <img alt="Public API In Examples" src="https://raw.githubusercontent.com/cmudrc/design-research/main/.github/badges/examples-api-coverage.svg">
        </a>
        <a class="drc-badge-link" href="https://github.com/cmudrc/design-research/actions/workflows/docs-pages.yml">
          <img alt="Docs" src="https://github.com/cmudrc/design-research/actions/workflows/docs-pages.yml/badge.svg">
        </a>
      </div>

.. container:: drc-home-callout

   .. note::

      **Start with** :doc:`quickstart` for the umbrella entry path, then use
      :doc:`typical_workflow` and :doc:`api` to see how the top-level namespace
      maps onto the sibling packages.

Highlights
----------

- Unified top-level namespace
- Thin wrapper design
- Curated stable re-exports
- Ecosystem-level framing
- Compatibility-focused packaging

Typical Workflow
----------------

1. Import ``design_research`` as the canonical ecosystem entry point.
2. Discover domain-specific capabilities via ``problems``, ``agents``, ``experiments``, and ``analysis``.
3. Compose studies across sibling libraries without rewriting underlying logic.
4. Keep package-specific behavior in component repos while using one coherent umbrella namespace.

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

- :doc:`quickstart`
- :doc:`installation`
- :doc:`concepts`
- :doc:`typical_workflow`
- :doc:`api`
- :doc:`philosophy`

.. toctree::
   :maxdepth: 2
   :caption: Documentation
   :hidden:

   quickstart
   installation
   concepts
   typical_workflow
   api

.. toctree::
   :maxdepth: 2
   :caption: Development
   :hidden:

   dependencies_and_extras
   Contributing <https://github.com/cmudrc/design-research/blob/main/CONTRIBUTING.md>

.. toctree::
   :maxdepth: 2
   :caption: Additional Guides
   :hidden:

   philosophy
