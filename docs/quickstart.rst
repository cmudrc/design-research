Quickstart
==========

This path starts with the package users receive from PyPI. See
:doc:`compatibility` for the exact component versions and artifact schema
tested by the current umbrella release.

Use The Installed Package
-------------------------

After following :doc:`installation`, run this offline first session:

.. code-block:: python

   import design_research as dr

   problem_ids = dr.problems.list_problems()
   problem = dr.problems.get_problem(problem_ids[0])

   print(problem.metadata.title)
   print(dr.agents.Workflow)
   print(dr.experiments.Study)
   print(dr.analysis.validate_unified_table)

The umbrella root stays narrow. Use ``design_research.problems``,
``design_research.agents``, ``design_research.experiments``, and
``design_research.analysis`` for the pinned components' public exports.

Run The Repository Compatibility Path
-------------------------------------

From a source checkout with ``make dev`` already completed, run:

.. code-block:: bash

   make test
   python examples/canonical_artifact_flow.py
   make examples-test

``canonical_artifact_flow.py`` is the deterministic, no-network handoff. It
loads a packaged problem, runs the public seeded baseline agent, exports the
Experiments artifact set, and validates the event table through Analysis.
``make examples-test`` keeps live-model examples opt-in.

Add The Optional Live Runtime
-----------------------------

The live umbrella walkthrough uses the ``llama_cpp`` extra owned by the pinned
Agents package:

.. code-block:: bash

   python -m pip install "design-research-agents[llama_cpp]==0.7.0"
   make run-example

Set ``LLAMA_CPP_MODEL`` to a local GGUF file or allow the installed Hugging
Face client to fetch the walkthrough's default model. Set
``RUN_LLAMA_CPP_EXAMPLES=1`` to include it in ``make examples-test``.
``RUN_OLLAMA_EXAMPLES=1`` independently enables the Ollama tutorial.

Validate Documentation Changes
------------------------------

.. code-block:: bash

   make docs-check
   make docs-build

``docs-check`` validates generated tutorial material and cross-file contracts;
``docs-build`` performs the strict Sphinx HTML build. Run
``make docs-linkcheck`` when public links change.
