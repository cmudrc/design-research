Tutorials
=========

This tutorial series starts with executable Jupyter notebooks for one library
at a time, then composes the libraries around reproducible design-research
workflows. Every notebook renders its saved results directly after the cell
that produced them. Only the Agents propose/critic notebook and final local-model
walkthrough require a running model service.

.. image:: ../_static/ecosystem-platform.svg
   :alt: Problems, agents, experiments, and analysis connected as one research workflow.
   :class: dark-light drc-ecosystem-figure
   :width: 100%
   :align: center

Choose A Starting Point
-----------------------

Install ``design-research`` to follow the complete series. Install a component
package directly when you only need its focused notebook. Each notebook page
includes its exact environment command and a source download; see
:doc:`../vscode_start` for the complete VS Code setup.

.. list-table:: Tutorial paths
   :header-rows: 1

   * - Tutorial
     - Primary skill
     - Libraries
   * - :doc:`problems_text_map`
     - Map 126 packaged word problems with TF-IDF and t-SNE.
     - Problems
   * - :doc:`problems_truss_grammar`
     - Inspect and manually apply planar-truss grammar rules.
     - Problems
   * - :doc:`agents_propose_critic`
     - Refine a design rationale with an existing LLM pattern.
     - Agents, Ollama
   * - :doc:`agents_workflow`
     - Build a deterministic workflow from logic steps.
     - Agents
   * - :doc:`experiments_monty_hall`
     - Test stay versus switch as a seeded experiment.
     - Experiments
   * - :doc:`analysis_reliability`
     - Quantify agreement among protocol coders.
     - Analysis
   * - :doc:`full_stack_study`
     - Run one benchmark through canonical artifacts.
     - All four libraries
   * - :doc:`process_comparison`
     - Compare condition-specific design-process traces.
     - Problems, Experiments, Analysis
   * - :doc:`factorial_analysis`
     - Fit a regression from a partial factorial study.
     - Problems, Experiments, Analysis

Recommended Order
-----------------

1. Start with either Problems notebook, then compare the existing Agents pattern
   with the home-built workflow.
2. Complete the Monty Hall and reliability notebooks.
3. Run :doc:`full_stack_study` to see the shared artifact contract.
4. Choose :doc:`process_comparison` for sequence analysis or
   :doc:`factorial_analysis` for design-of-experiments analysis.
5. Continue to :doc:`../prompt_framing_study` when a local ``llama.cpp`` model
   should replace the deterministic agent.

All runnable files live under ``examples/``. ``make examples-test`` executes
the complete offline set. Set ``RUN_OLLAMA_EXAMPLES=1`` to include the
propose/critic notebook after starting Ollama. Set
``RUN_LLAMA_CPP_EXAMPLES=1`` for the separate managed ``llama.cpp``
walkthrough; the two selections are independent. ``make notebooks-check``
verifies that every focused notebook page still shows results corresponding to
its committed source.

.. toctree::
   :maxdepth: 1

   problems_text_map
   problems_truss_grammar
   agents_propose_critic
   agents_workflow
   experiments_monty_hall
   analysis_reliability
   full_stack_study
   process_comparison
   factorial_analysis
