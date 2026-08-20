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
- VS Code with Microsoft's `Python extension
  <https://marketplace.visualstudio.com/items?itemName=ms-python.python>`_ and
  `Jupyter extension
  <https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter>`_.
- A VS Code integrated terminal.

Run A Downloaded Tutorial Notebook
----------------------------------

Use these steps for any notebook in the :doc:`tutorial series
<tutorials/index>`:

1. Create an empty folder, open it with ``File > Open Folder`` in VS Code, and
   open ``Terminal > New Terminal``.
2. Create a virtual environment and install the notebook kernel support.

   On macOS or Linux:

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate
      python -m pip install --upgrade pip ipykernel

   On Windows PowerShell:

   .. code-block:: powershell

      py -3 -m venv .venv
      .\.venv\Scripts\Activate.ps1
      python -m pip install --upgrade pip ipykernel

3. On the tutorial page, choose **Download this notebook (.ipynb)** near the
   heading and save the file in the folder you opened in VS Code.
4. Open the downloaded ``.ipynb`` file. Read its **Setup** section, then run
   the listed ``python -m pip install ...`` command in the integrated terminal.
   Each tutorial names its own package and any plotting dependencies.
5. Use the kernel picker at the top right of the notebook, choose **Python
   Environments**, and select the interpreter inside ``.venv``. If it is not
   listed, run ``Python: Select Interpreter`` from the command palette and
   select ``.venv/bin/python`` on macOS/Linux or
   ``.venv\Scripts\python.exe`` on Windows.
6. Scan the notebook's saved results, then choose **Run All** in the notebook
   toolbar and compare them with the fresh output from your environment.

The Ollama-backed propose/critic notebook has one additional requirement: keep
``ollama serve`` running as instructed in that notebook's **Setup** section.

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

   py -3 -m venv .venv
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
  interpreter or notebook kernel, then reload the window.
- If a notebook says that no kernel is available, confirm that ``ipykernel`` is
  installed in ``.venv`` and select that environment again with the kernel
  picker.
- If ``make`` uses the wrong Python, activate ``.venv`` in the terminal or run
  ``PYTHON=.venv/bin/python make test``.
- If Windows activation is blocked, switch the terminal profile to Command
  Prompt and run ``.\.venv\Scripts\activate.bat``.
- If live walkthrough dependencies are missing, install the model-client
  dependencies only for that workflow.
- Avoid committing generated runtime output under ``artifacts/``,
  ``docs/_build/``, or local virtual environment directories.
