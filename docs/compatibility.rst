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

The bundled examples and smoke tests intentionally target the April 2026 family
interop seams directly: ``design_research_experiments.resolve_problem(...)``,
public ``design_research_agents.SeededRandomBaselineAgent`` and
``design_research_agents.PromptWorkflowAgent`` participants, a prompt-built
``design_research_agents.Workflow``, and
``design_research_analysis.integration``. The shipped example scripts expect
installed sibling packages; adjacent sibling worktrees are preferred only by
the family-sync and subprocess example tests so the umbrella package can verify
current sibling ``main`` APIs during contributor workflows.

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

Choose This Package When...
---------------------------

Use the ecosystem by intent, not just by package name.

.. list-table:: Intent-first package selection
   :header-rows: 1

   * - You want to...
     - Start here
     - Why
   * - Browse canonical benchmarks, prompt packets, or packaged design tasks
     - ``design-research-problems``
     - The problems repo is the package-owned catalog and benchmark surface.
   * - Build agents, tool-using workflows, or execution traces
     - ``design-research-agents``
     - The agents repo owns executable participants, workflows, and tool/runtime contracts.
   * - Define controlled studies, conditions, and repeatable artifact exports
     - ``design-research-experiments``
     - The experiments repo owns hypotheses, factors, run orchestration, and export contracts.
   * - Validate ``events.csv`` and analyze existing study logs
     - ``design-research-analysis``
     - The analysis repo owns the unified-table contract and downstream empirical workflows.
   * - Compose an end-to-end workflow across all four layers with one stable namespace
     - ``design-research``
     - The umbrella package keeps the ecosystem discoverable and provides the tested package combination plus shared walkthroughs.

The sibling packages are fully valid independent entry points. The umbrella
package is the combined-path guide: it is best when you want one shared import
style, one docs shell, and one compatibility story across the full stack.

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

If you already know the exact layer you need, jump straight into the published
docs for the sibling library that owns that behavior and treat
``design-research`` as the ecosystem map rather than the required starting
point.
