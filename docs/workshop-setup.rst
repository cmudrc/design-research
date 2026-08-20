Workshop Setup and Preflight
============================

Use this page to prepare for **AI Experiments in Engineering Design: A Tutorial
on the Design Research Open-Source Ecosystem** at IDETC-CIE 2026 on Sunday,
August 23. The participant path is deterministic and runs offline after the
one-time installation.

.. container:: drc-home-callout

   .. important::

      :download:`Download the IDETC 2026 tutorial materials
      <_static/idetc2026-design-research-tutorial.zip>` and complete the
      preflight below before Sunday. Keep the extracted folder together.

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

What Is In The Download?
------------------------

The kit freezes the tested package family at ``design-research==0.4.0`` and includes a
preflight plus eight offline examples.

.. list-table:: Tutorial materials
   :header-rows: 1
   :widths: 32 50 18

   * - File
     - Purpose
     - Suggested use
   * - ``notebooks/problems_text_map.ipynb``
     - Map packaged design problems using TF-IDF and t-SNE.
     - Participant exercise
   * - ``notebooks/problems_truss_grammar.ipynb``
     - Apply design-grammar rules to a planar truss.
     - Participant exercise
   * - ``notebooks/agents_workflow.ipynb``
     - Build and trace a deterministic agent workflow.
     - Participant exercise
   * - ``notebooks/experiments_monty_hall.ipynb``
     - Define conditions and run a seeded experiment.
     - Participant exercise
   * - ``notebooks/analysis_reliability.ipynb``
     - Measure agreement among protocol coders.
     - Participant exercise
   * - ``scripts/canonical_artifact_flow.py``
     - Pass one packaged problem through agents, experiments, and analysis.
     - Optional stack check
   * - ``scripts/long_agent_markov_comparison.py``
     - Compare two scripted design processes as Markov chains.
     - Composed example
   * - ``scripts/partial_factorial_ideation_regression.py``
     - Fit a regression from a partial factorial ideation study.
     - Composed example

About ``canonical_artifact_flow.py``
------------------------------------

This is the smallest end-to-end example in the repository. It loads one
packaged design problem, runs a seeded baseline agent twice, exports the
standard experiment artifacts, and asks the analysis package to validate and
summarize them. It does not call an AI model or require network access. Think
of it as an optional plumbing check, not the first tutorial exercise.

Model-Backed Examples
---------------------

The participant kit does not require Ollama, ``llama.cpp``, a model download,
or an API key. Model-backed demonstrations are a separate facilitator path so
that model availability cannot block the offline exercises.

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
