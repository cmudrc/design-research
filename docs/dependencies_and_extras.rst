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

Maintainer workflows target Python ``3.12`` from ``.python-version``.
CI enforces a strict 90% total line coverage floor through ``make coverage`` and
``make ci``.
Release packaging validation is exposed via ``make release-check``.
