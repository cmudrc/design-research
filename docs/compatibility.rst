Compatibility And Start Here
============================

``design-research`` is an optional umbrella package for the ecosystem, not the
only supported way to use the underlying libraries.

Use the compatibility matrix below when you want the tested package
combination. Use the decision table below when you need to choose between the
umbrella package and a direct sibling install.

Tested Package Combination
--------------------------

.. list-table:: Version-first compatibility matrix
   :header-rows: 1

   * - ``design-research``
     - ``design-research-problems``
     - ``design-research-agents``
     - ``design-research-experiments``
     - ``design-research-analysis``
     - Monthly release context
   * - ``0.1.1``
     - ``0.2.1``
     - ``0.3.0``
     - ``0.1.1``
     - ``0.1.1``
     - ``Atlas Alignment - April 2026``

These versions match the exact sibling pins in ``pyproject.toml`` and represent
the tested umbrella combination for the current docs baseline.

The bundled examples and smoke tests now target the package-owned cross-library
path explicitly:

- ``design_research_problems.integration``
- ``design_research_agents.integration``
- ``design_research_experiments``
- ``design_research_analysis.integration``

``design_research_experiments`` remains the orchestration surface, so there is
intentionally no separate ``design_research_experiments.integration`` module.
The shipped example scripts expect installed sibling packages; adjacent sibling
worktrees are preferred only by the family-sync and subprocess example tests so
the umbrella package can verify current sibling ``main`` APIs during
contributor workflows.

Start Here Vs Go Direct
-----------------------

.. list-table:: Choosing an install path
   :header-rows: 1

   * - Start with ``design-research``
     - Install a sibling package directly
   * - You want one stable namespace across problems, agents, experiments, and
       analysis.
     - You only need one layer of the ecosystem for a focused workflow.
   * - You want the umbrella docs, examples, and compatibility guidance to stay
       in one place.
     - You want package-specific internals, lower-level helpers, or a narrower
       dependency surface.
   * - You plan to compose end-to-end workflows and prefer a shared import style.
     - You already know which component package owns the behavior you need.

Direct sibling use is fully supported. The umbrella package is a convenience
layer for discovery, stable imports, and composed workflow guidance.

The package root intentionally stays narrow: it exports only ``__version__``
plus the four wrapper submodules. Stable user-facing symbols remain under
``design_research.problems``, ``design_research.agents``,
``design_research.experiments``, and ``design_research.analysis`` rather than a
flattened root namespace.

Monthly Release Train
---------------------

Monthly release names coordinate ecosystem alignment work across repositories.
They are scheduling and documentation markers, not alternate install
coordinates. Use the version matrix above for tested package combinations, and
use the current release callout in the README for the active milestone and due
date.

Next Step
---------

If you want to see the umbrella package drive a real composed workflow, use the
deterministic bundled examples for the smallest recipe-first entry points and
continue to :doc:`prompt_framing_study` for the live canonical walkthrough.
