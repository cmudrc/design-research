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
- ``pre-commit``
- ``pytest``
- ``pytest-cov``
- ``ruff``
- ``sphinx``
- ``sphinx-rtd-theme``
- ``twine``
- ``uv``

Install it with:

.. code-block:: bash

   pip install -e ".[dev]"
