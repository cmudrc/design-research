Tutorials
=========

This tutorial series starts with one library at a time, then composes the
libraries around reproducible design-research workflows. Every tutorial except
the final live-model walkthrough is deterministic and runs without network
access.

.. image:: ../_static/ecosystem-platform.svg
   :alt: Problems, agents, experiments, and analysis connected as one research workflow.
   :class: dark-light drc-ecosystem-figure
   :width: 100%
   :align: center

Choose A Starting Point
-----------------------

Install ``design-research`` to follow the complete series. Install a component
package directly when you only need its focused tutorial.
Each tutorial links its runnable source and follows the same VS Code workflow;
see :doc:`../vscode_start` for the complete editor setup.

.. list-table:: Tutorial paths
   :header-rows: 1

   * - Tutorial
     - Primary skill
     - Libraries
   * - :doc:`problems_catalog`
     - Find a task and inspect its executable contract.
     - Problems
   * - :doc:`agents_workflow`
     - Build an observable deterministic workflow.
     - Agents
   * - :doc:`experiments_factorial`
     - Define and materialize a reproducible study.
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

1. Complete the four focused tutorials in any order.
2. Run :doc:`full_stack_study` to see the shared artifact contract.
3. Choose :doc:`process_comparison` for sequence analysis or
   :doc:`factorial_analysis` for design-of-experiments analysis.
4. Continue to :doc:`../prompt_framing_study` when a local ``llama.cpp`` model
   should replace the deterministic agent.

All runnable files live under ``examples/``. ``make examples-test`` executes
the complete offline set, while ``make run-example`` runs the opt-in live
walkthrough.

.. toctree::
   :maxdepth: 1

   problems_catalog
   agents_workflow
   experiments_factorial
   analysis_reliability
   full_stack_study
   process_comparison
   factorial_analysis
