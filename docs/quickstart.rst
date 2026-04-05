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

   python -m pip install "design-research[examples]"
   make run-example
   make examples-test

``make run-example`` executes the canonical umbrella-level walkthrough that
uses a real packaged problem, a live model-backed workflow agent, canonical
experiment artifacts, and exported event-table validation.

The walkthrough uses a managed ``llama.cpp`` client. Install
``design-research[examples]`` before running it. That extra includes the
managed runtime client and the default GGUF download helper. If you want to
use a specific local GGUF file instead, set ``LLAMA_CPP_MODEL``.

``make examples-test`` stays deterministic and offline-first by default. It
exercises the two smaller recipe-first examples and skips the live
walkthrough unless ``RUN_LIVE_EXAMPLE=1``.

Build the docs:

.. code-block:: bash

   make docs
