Dependencies And Extras
=======================

The base install depends on the four component libraries:

- ``design-research-problems``
- ``design-research-agents``
- ``design-research-experiments``
- ``design-research-analysis``

The umbrella pins their exact base distributions. Provider SDKs, model
backends, and package-specific feature dependencies remain optional extras of
the component that uses them. See the `Agents extras
<https://cmudrc.github.io/design-research-agents/dependencies_and_extras.html>`_
and the other component documentation linked from :doc:`installation`.

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

   python -m pip install -e ".[dev]"

Maintainer workflows target Python ``3.12`` from ``.python-version``.
CI enforces a strict 95% total line coverage floor through ``make coverage`` and
``make ci``.
Release packaging validation is exposed via ``make release-check``.
