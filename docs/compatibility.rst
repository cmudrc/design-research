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
   * - ``0.4.0``
     - ``0.4.0``
     - ``0.5.0``
     - ``0.2.1``
     - ``0.3.0``

These versions match the exact sibling pins in ``pyproject.toml`` and represent
the tested umbrella combination for the current docs baseline.

Before all four versions are published, Umbrella pull-request CI installs the
immutable source commits listed in ``requirements/release-candidates.txt``.
That file is a maintainer integration aid, not an alternate user installation
path or a replacement for the version matrix. Each source commit must declare
the same package version shown above and pass its component repository's own
quality gates. ``make release-candidates-check`` also verifies that the matrix
contains one immutable commit for every exact component dependency. Main-branch
CI and normal ``pip install design-research`` usage continue to resolve the
exact published versions from ``pyproject.toml``.

The bundled examples and smoke tests intentionally target this pinned family
through public integration points. :doc:`canonical_artifact_flow` is the no-network smoke
path: it resolves a packaged problem, runs the public seeded baseline agent,
exports canonical experiment artifacts, and validates them with
``design_research_analysis.integration``. The live walkthrough adds
``PromptWorkflowAgent`` and a prompt-built ``Workflow`` on top of that same
artifact contract. The shipped example scripts expect installed sibling
packages. The family smoke test uses those installed pins by default. Contributors
can opt into source worktrees with the documented ``DESIGN_RESEARCH_*_SRC`` or
``DESIGN_RESEARCH_*_ROOT`` environment overrides.

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
