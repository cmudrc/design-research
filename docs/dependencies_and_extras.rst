Dependencies And Extras
=======================

The base install depends on the four component libraries:

- ``design-research-problems``
- ``design-research-agents``
- ``design-research-experiments``
- ``design-research-analysis``

The ``dev`` extra installs the local contributor toolchain:

- ``build``
- ``mypy``
- ``pydata-sphinx-theme``
- ``pre-commit``
- ``pytest``
- ``pytest-cov``
- ``ruff``
- ``sphinx``
- ``sphinx-copybutton``
- ``twine``

Install it with:

.. code-block:: bash

   pip install -e ".[dev]"

The umbrella package also forwards useful sibling-library extras behind
prefixed names so the install surface stays explicit:

- ``problems_*`` mirrors curated ``design-research-problems`` extras, including
  ``problems_all`` for the currently useful problem-side add-ons.
- ``agents_*`` mirrors ``design-research-agents`` runtime/provider extras,
  including ``agents_all`` for a broad agent runtime install and ``examples``
  for the live walkthrough's ``llama.cpp`` client path.
- ``analysis_*`` mirrors the non-empty ``design-research-analysis`` extras,
  including ``analysis_all``.
- ``kitchen_sink`` installs the broad cross-ecosystem add-on set in one step.

Example installs:

.. code-block:: bash

   pip install "design-research[agents_openai]"
   pip install "design-research[problems_all,analysis_all]"
   pip install "design-research[kitchen_sink]"

Maintainer workflows target Python ``3.12`` from ``.python-version``.
CI enforces a strict 90% total line coverage floor through ``make coverage`` and
``make ci``.
Release packaging validation is exposed via ``make release-check``.
