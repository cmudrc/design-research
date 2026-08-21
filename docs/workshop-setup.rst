Workshop Setup and Preflight
============================

Use this page to prepare for **AI Experiments in Engineering Design: A Tutorial
on the Design Research Open-Source Ecosystem** at IDETC-CIE 2026 on Sunday,
August 23. Complete the one-time installation before Sunday. The activity
notebooks are separate so that they can stay current without changing the
participant environment.

.. container:: drc-home-callout

   .. important::

      :download:`Download the IDETC 2026 setup kit
      <_static/idetc2026-design-research-setup.zip>` and complete the preflight
      below before Sunday. Keep the extracted folder and its ``.venv`` together.
      The activity notebooks will be provided separately at the tutorial.

Before Sunday
-------------

Install `Python 3.12 <https://www.python.org/downloads/>`_,
`VS Code <https://code.visualstudio.com/>`_, and the VS Code **Python** and
**Jupyter** extensions. Python 3.12 is the recommended tutorial version even
though the package supports newer Python releases.

Extract the download, open its folder in VS Code, and create the tutorial
environment without activating it.

On macOS or Linux:

.. code-block:: bash

   python3.12 -m venv .venv
   .venv/bin/python -m pip install --upgrade pip
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python preflight.py

On Windows PowerShell:

.. code-block:: powershell

   py -3.12 -m venv .venv
   .venv\Scripts\python -m pip install --upgrade pip
   .venv\Scripts\python -m pip install -r requirements.txt
   .venv\Scripts\python preflight.py

A successful check ends with ``Preflight passed. You are ready for the
tutorial.`` In VS Code, run ``Python: Select Interpreter`` from the command
palette and choose the interpreter inside ``.venv``. Use that same environment
as the notebook kernel.

Once the preflight passes, setup is complete. You do not need the activity
notebooks in advance.

What The Setup Prepares
-----------------------

The setup kit freezes the tested Design Research package family and installs a
broad, cross-platform tutorial environment. The preflight imports that
environment and runs a small deterministic workflow through problems, agents,
experiments, and analysis. It does not check for particular activity notebooks.

.. list-table:: Preinstalled capabilities
   :header-rows: 1
   :widths: 28 40 32

   * - Capability
     - Included surface
     - Preflight evidence
   * - Design Research ecosystem
     - Problems, agents, experiments, and analysis
     - Imports, versions, and an offline end-to-end smoke study
   * - Notebook runtime
     - IPython kernel, ``nbformat``, and ``nbclient``
     - Imports from the selected ``.venv``
   * - Data and visualization
     - NumPy, pandas, Matplotlib, SciPy, and scikit-learn
     - Imports
   * - Study and analysis methods
     - DOE, optimization, sequence analysis, graphs, and statistics
     - Imports
   * - Model-service clients
     - OpenAI, Anthropic, Gemini, and Groq client libraries
     - Imports only; no account or credential is required

At The Tutorial
---------------

The facilitator will provide the current activity pack. Extract its
``notebooks/`` and ``scripts/`` folders into the setup folder, open the activity
notebook in VS Code, and select the existing ``.venv`` kernel. The activity pack
is built independently from the setup kit, so notebook updates do not require a
second installation.

Model-Backed Examples
---------------------

The setup kit installs several hosted-model client libraries to preserve
tutorial flexibility, but it does not require an API key, local model download,
Ollama, or ``llama.cpp``. Model availability cannot block the offline exercises.

Troubleshooting
---------------

- If ``python3.12`` is not found on macOS or Linux, confirm that Python 3.12 is
  installed and available on your ``PATH``.
- If ``py -3.12`` is not found on Windows, reinstall Python 3.12 and enable the
  Python launcher option.
- If a notebook cannot import the packages but ``preflight.py`` passes, select
  the ``.venv`` notebook kernel and restart the notebook.
- If installation fails on a restricted network, save the full terminal error
  and bring it to the tutorial. The exercises themselves run offline once the
  environment is installed.

For the broader progression after the session, continue to the
:doc:`Learning Path <learn>` or the :doc:`complete tutorial index
<tutorials/index>`.
