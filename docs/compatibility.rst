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
   * - ``0.3.0``
     - ``0.3.0``
     - ``0.4.0``
     - ``0.2.0``
     - ``0.2.0``

These versions match the exact sibling pins in ``pyproject.toml`` and represent
the tested umbrella combination for the current docs baseline.

The bundled examples and smoke tests intentionally target the May 2026 family
interop seams directly. :doc:`canonical_artifact_flow` is the no-network smoke
path: it resolves a packaged problem, runs the public seeded baseline agent,
exports canonical experiment artifacts, and validates them with
``design_research_analysis.integration``. The live walkthrough adds
``PromptWorkflowAgent`` and a prompt-built ``Workflow`` on top of that same
artifact contract. The shipped example scripts expect installed sibling
packages; adjacent sibling worktrees are preferred only by the family-sync and
subprocess example tests so the umbrella package can verify current sibling
``main`` APIs during contributor workflows.

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

Release Planning
----------------

The ecosystem no longer uses monthly milestone names as the default release
coordination mechanism. Use the version matrix above for tested package
combinations, and use GitHub Releases or PyPI versions for published package
state.

Next Step
---------

If you want to see the umbrella package drive a real composed workflow, start
with :doc:`canonical_artifact_flow` and continue to :doc:`prompt_framing_study`
for the live walkthrough.
