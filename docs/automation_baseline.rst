Docs Automation Baseline
========================

This page documents the shared docs and CI baseline used by the
``design-research`` umbrella package.

The goal is consistency with the module repos without pretending the umbrella
package should own every repo-specific generator. The umbrella docs are
deliberately curation-heavy: they route readers to stable entry points,
cross-library workflows, and compatibility guidance rather than generating a
page for every example script.

Shared Baseline
---------------

.. list-table::
   :header-rows: 1

   * - Concern
     - Local utility
     - Workflow owner
     - Baseline expectation
   * - Docs consistency
     - ``scripts/check_docs_consistency.py``
     - ``ci.yml``
     - Keep README, docs landing pages, and linked workflow guidance aligned.
   * - Docstring policy
     - ``scripts/check_google_docstrings.py``
     - ``ci.yml``
     - Public-facing package, script, and example surfaces stay on the shared docstring policy.
   * - Coverage badge
     - ``scripts/generate_coverage_badge.py``
     - ``ci.yml``
     - Coverage badge stays in sync with the enforced family coverage floor.
   * - Example status badges
     - ``scripts/generate_examples_metrics.py`` and ``scripts/generate_examples_badges.py``
     - ``examples.yml``
     - The docs and README show the shared examples badge baseline used across the family.
   * - Release callout upkeep
     - ``scripts/update_release_readme.py``
     - ``update-release-readme.yml``
     - The README release callout stays aligned with the active monthly release train.

Workflow Responsibilities
-------------------------

- ``ci.yml`` owns lint, type, test, docstring, docs-consistency, and coverage-gate checks.
- ``examples.yml`` owns runnable example verification plus example-derived badge metrics.
- ``docs-pages.yml`` owns published documentation builds.
- ``update-release-readme.yml`` owns the release-callout refresh path.
- ``workflow.yml`` remains the broader workflow entry point that ties the maintainer checks together.

Intentional Umbrella-Specific Differences
-----------------------------------------

The umbrella repo intentionally omits one common module-repo utility:

- There is no generated example-docs page pipeline here.

That omission is deliberate. The umbrella docs emphasize curated entry points
such as :doc:`compatibility`, :doc:`quickstart`, and
:doc:`prompt_framing_study` rather than mirroring every checked-in example as a
documentation page. Example execution is still covered by ``examples.yml``,
``scripts/run_examples.py``, and the example-tooling tests; the docs simply
stay editorial instead of generator-first.

When To Update This Page
------------------------

Refresh this page whenever a new docs-check script, badge generator, release
automation hook, or repo-specific exception changes the expected maintainer
workflow.
