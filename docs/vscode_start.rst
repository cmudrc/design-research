Run An Example In VS Code
=========================

Use this page when you want to try the umbrella ``design-research`` package in
VS Code. Choose the installed-package path for a first user workflow, or the
source checkout path when you want to run the repository's checked-in examples
and development checks.

The checked-in ``examples/`` directory lives in the repository source. Do not
assume those files are present inside the PyPI wheel.

Requirements
------------

- Python 3.12 or newer. Maintainer workflows target the version in
  ``.python-version``.
- VS Code with the Python extension.
- A VS Code integrated terminal.

Installed Package From PyPI
---------------------------

Open an empty folder in VS Code, then create and activate a virtual
environment from ``Terminal > New Terminal``.

On macOS or Linux:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip
   python -m pip install design-research

On Windows PowerShell:

.. code-block:: powershell

   py -3.12 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install design-research

Run ``Python: Select Interpreter`` from the command palette and choose the
interpreter inside ``.venv``. If VS Code does not list it, enter the interpreter
path manually:

- macOS/Linux: ``.venv/bin/python``
- Windows: ``.venv\Scripts\python.exe``

Create ``umbrella_example.py`` in the workspace folder:

.. code-block:: python

   import design_research as dr

   print(f"design-research: {dr.__version__}")

   problem_ids = dr.problems.list_problems()
   print(f"problem catalog size: {len(problem_ids)}")
   problem = dr.problems.get_problem("decision_laptop_design_profit_maximization")
   print(f"problem: {problem.metadata.title}")

   study = dr.experiments.build_prompt_framing_study()
   conditions = dr.experiments.build_design(study)
   print(f"study: {study.study_id}")
   print(f"conditions: {len(conditions)}")

   print(f"agent API: {dr.agents.SeededRandomBaselineAgent.__name__}")
   print(f"analysis API: {dr.analysis.validate_unified_table.__name__}")

Run the file with VS Code's ``Run Python File`` action, or run:

.. code-block:: bash

   python umbrella_example.py

Source Checkout For Repository Examples
---------------------------------------

Use this path when you want the checked-in examples, docs, tests, and optional
development tooling.

.. code-block:: bash

   git clone https://github.com/cmudrc/design-research.git
   cd design-research
   python -m venv .venv
   source .venv/bin/activate
   python -m pip install --upgrade pip setuptools wheel
   python -m pip install -e ".[dev]"

Equivalent maintainer shortcut:

.. code-block:: bash

   make dev

Run the deterministic all-layer handoff from the integrated terminal:

.. code-block:: bash

   python examples/canonical_artifact_flow.py
   make examples-test

``make run-example`` is the live model-backed walkthrough. Install
``llama-cpp-python[server]`` and ``huggingface-hub`` only when you need that
path:

.. code-block:: bash

   python -m pip install "llama-cpp-python[server]" huggingface-hub
   make run-example

First Development Checks
------------------------

Run the checks from VS Code's integrated terminal:

.. code-block:: bash

   make test
   make qa
   make docs-check

``make qa`` runs linting, formatting checks, type checks, and tests. Run
``make coverage`` before merge when changing tested behavior.

Troubleshooting
---------------

- If VS Code imports fail but the terminal works, reselect the ``.venv``
  interpreter and reload the window.
- If ``make`` uses the wrong Python, activate ``.venv`` in the terminal or run
  ``PYTHON=.venv/bin/python make test``.
- If Windows activation is blocked, switch the terminal profile to Command
  Prompt and run ``.\.venv\Scripts\activate.bat``.
- If live walkthrough dependencies are missing, install the model-client
  dependencies only for that workflow.
- Avoid committing generated runtime output under ``artifacts/``,
  ``docs/_build/``, or local virtual environment directories.
