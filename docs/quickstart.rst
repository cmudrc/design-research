Quickstart
==========

This package targets Python 3.12+ and follows a standard ``src/`` layout.
See :doc:`compatibility` for the tested package combination and install-path
guidance.

Local development setup:

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   make dev
   make test

Run the bundled example:

.. code-block:: bash

   python -m pip install llama-cpp-python
   make run-example

``make run-example`` executes the canonical umbrella-level walkthrough that
uses a real packaged problem, a live model-backed workflow agent, canonical
experiment artifacts, and exported event-table validation.

The walkthrough uses a managed ``llama.cpp`` client. Install
``llama-cpp-python`` before running it, and optionally set ``LLAMA_CPP_MODEL``
if you want to point at a specific local GGUF file.

Build the docs:

.. code-block:: bash

   make docs
