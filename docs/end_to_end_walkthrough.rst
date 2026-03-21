End-To-End Walkthrough
======================

This walkthrough demonstrates the umbrella package doing real work with a live
model-backed agent. It uses a real packaged problem from
``design_research.problems``, a ``design_research.agents.Workflow`` compatible
with ``design_research.experiments``, canonical artifact export, and
``design_research.analysis.validate_unified_table`` on the resulting events
table.

.. image:: _static/walkthrough-flow.svg
   :alt: Flow diagram showing a packaged problem feeding a live workflow agent, then study execution, artifact export, and event-table validation.
   :width: 100%
   :align: center

What This Covers
----------------

- selects a real packaged problem through ``design_research.problems``
- runs one live study through ``design_research.experiments``
- exports ``study.yaml``, ``manifest.json``, ``conditions.csv``, ``runs.csv``,
  ``events.csv``, and ``evaluations.csv``
- validates the exported event rows through ``design_research.analysis``
- keeps the example umbrella-only while wiring the real workflow pieces through
  ``design_research.agents``

Run It
------

.. code-block:: bash

   python -m pip install llama-cpp-python
   make run-example

Optionally point the walkthrough at a specific local GGUF file:

.. code-block:: bash

   export LLAMA_CPP_MODEL=/path/to/model.gguf
   make run-example

The example writes artifacts to
``artifacts/examples/umbrella_end_to_end_walkthrough`` and prints the exported
paths plus the event-table validation summary. The script intentionally has no
deterministic fallback path: it expects a real ``llama.cpp`` runtime.

If ``LLAMA_CPP_MODEL`` is not set, the client falls back to its built-in model
defaults and Hugging Face repo settings. The first run may therefore download a
model before the walkthrough executes.

The script is intentionally written in a linear, step-by-step style so it can
double as training material and as the literal-included documentation example.
The only local callbacks left in place are the small adapters required by the
workflow and experiment APIs.

Code
----

.. literalinclude:: ../examples/end_to_end_walkthrough.py
   :language: python
   :linenos:
   :caption: ``examples/end_to_end_walkthrough.py``

When To Go Direct
-----------------

Use the umbrella package when you want one stable import surface for the
ecosystem. Install a sibling package directly when you only need one layer or
want package-specific internals. See :doc:`compatibility` for the tested
version combination and install guidance.
