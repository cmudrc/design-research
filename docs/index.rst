design-research
===============

The canonical umbrella package for the CMU Design Research Collective ecosystem.

What This Library Does
----------------------

``design-research`` provides a thin, stable entry point over the ecosystem's
component libraries. It keeps implementation in specialized packages while
improving top-level discoverability for research workflows, tutorials, and
papers.

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

.. image:: _static/ecosystem-platform.svg
   :alt: Ecosystem diagram showing experiments above agents, problems, and analysis.
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
