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

Run the deterministic all-layer example:

.. code-block:: bash

   python examples/canonical_artifact_flow.py

Run the live bundled example:

.. code-block:: bash

   python -m pip install "llama-cpp-python[server]" huggingface-hub
   make run-example
   make examples-test

``make run-example`` executes the live umbrella-level walkthrough that
uses a real packaged problem, a live model-backed workflow agent, canonical
experiment artifacts, and exported event-table validation.

The walkthrough uses a managed ``llama.cpp`` client. Install
``llama-cpp-python[server]`` before running it. If you want the default GGUF
download path to work, also install ``huggingface-hub``; otherwise set
``LLAMA_CPP_MODEL`` to a specific local GGUF file.

``make examples-test`` stays deterministic and offline-first by default. Set
``RUN_OLLAMA_EXAMPLES=1`` to include the propose/critic notebook or
``RUN_LLAMA_CPP_EXAMPLES=1`` to include the managed llama.cpp walkthrough.

Build the docs:

.. code-block:: bash

   make docs
