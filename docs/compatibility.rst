Compatibility And Package Status
================================

``design-research`` is an optional umbrella package, not the only supported
way to use the component libraries. This page records the exact package family
tested by the current umbrella release and separates those compatibility facts
from broader maturity policy.

Tested Package Combination
--------------------------

.. list-table:: Exact umbrella pins and current package metadata
   :header-rows: 1
   :widths: 54 20 26

   * - Package
     - Version
     - PyPI development classifier
   * - ``design-research``
     - ``0.5.0``
     - Alpha
   * - ``design-research-problems``
     - ``0.5.0``
     - Alpha
   * - ``design-research-agents``
     - ``0.7.0``
     - Pre-Alpha
   * - ``design-research-experiments``
     - ``0.4.0``
     - Alpha
   * - ``design-research-analysis``
     - ``0.4.0``
     - Alpha

The versions match the exact dependencies in ``pyproject.toml``. Normal
``python -m pip install design-research`` usage and pull-request CI resolve
this published combination. The table does not promise compatibility for
unlisted versions.

The status column reports each package's current ``Development Status``
classifier; it does not define stable, experimental, research, or legacy
states for the ecosystem. A shared maturity-label policy remains open in
`issue #12 <https://github.com/cmudrc/design-research/issues/12>`_. Until that
policy is decided, consult each package's release notes and documentation for
package-specific change guidance.

Artifact Contract
-----------------

The current deterministic family path writes an Experiments manifest with
artifact schema ``0.2.0``. The umbrella family smoke test passes that exported
artifact set to ``design-research-analysis==0.4.0`` and validates its event
table. This is the tested handoff:

.. code-block:: text

   Problems + Agents -> Experiments artifact set (schema 0.2.0) -> Analysis

Treat the artifact directory and its manifest schema as the cross-package data
contract. A package version, API status, and artifact schema version answer
different questions; none should be used as a substitute for the others.

Public API Scope
----------------

The umbrella root exports ``__version__`` plus ``problems``, ``agents``,
``experiments``, and ``analysis``. For the exact pins above, each wrapper
mirrors its component package's public ``__all__`` exports. This provides one
consistent import route for the tested family without claiming that every
component symbol is permanently stable across future releases.

The no-network :doc:`canonical_artifact_flow` exercises those public wrappers:
it resolves a packaged problem, runs the public seeded baseline agent, exports
canonical experiment artifacts, and validates them through top-level Analysis
helpers. The live :doc:`prompt_framing_study` adds a prompt-built Agents
workflow while retaining the same artifact handoff.

Start With The Umbrella Or Go Direct
------------------------------------

.. list-table:: Choosing an install path
   :header-rows: 1

   * - Start with ``design-research``
     - Install a component directly
   * - You want one import route across Problems, Agents, Experiments, and
       Analysis for the tested combination.
     - You need only one package or a narrower dependency surface.
   * - You want the shared learning path, composed examples, and compatibility
       record.
     - You need component-specific optional backends, internals, or detailed
       API guidance.
   * - You are composing the complete artifact handoff.
     - You already know which package owns the behavior you need.

Direct component use remains supported by each owning package:

- `Problems <https://cmudrc.github.io/design-research-problems/>`__
- `Agents <https://cmudrc.github.io/design-research-agents/>`__
- `Experiments <https://cmudrc.github.io/design-research-experiments/>`__
- `Analysis <https://cmudrc.github.io/design-research-analysis/>`__

Next Step
---------

Start with :doc:`canonical_artifact_flow` for the deterministic all-package
handoff, then continue to :doc:`prompt_framing_study` only when you want the
optional local-model runtime.
