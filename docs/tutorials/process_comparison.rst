Compose The Libraries: Compare Design Processes
===============================================

Outcome scores alone can hide how a design process changed. This tutorial runs
two deterministic process treatments, exports their action traces, fits one
Markov chain per condition, and compares the transition matrices.

What You Will Learn
-------------------

- Use a packaged ideation problem as shared task context.
- Bind deterministic participant callables to experiment conditions.
- Export event sequences through the canonical artifact contract.
- Fit and compare condition-specific Markov chains from artifacts.
- Read process and outcome summaries from the same event table.

Install And Run
---------------

:download:`Download long_agent_markov_comparison.py <../../examples/long_agent_markov_comparison.py>`,
open its containing folder in VS Code, and use the integrated terminal:

.. code-block:: bash

   python -m pip install design-research==0.5.0
   python long_agent_markov_comparison.py

Core Orchestration
------------------

The complete runnable source includes the deterministic transition policies and
helper functions. The excerpt below shows the study, execution, artifact, and
analysis path.

.. literalinclude:: ../../examples/long_agent_markov_comparison.py
   :language: python
   :linenos:
   :start-at: def main()
   :end-before: def _agent_run(

Selected Output
---------------

The complete output also names the problem, reports each condition's mean
outcome and transition-matrix p-value, and gives the artifact directory. These
lines capture the main process-comparison checks:

.. code-block:: text

   Long agent Markov comparison: long_agent_markov_comparison
   Actions per run: 30
   Runs: 20
   Event rows valid: True (rows=600)
   States: 6
   Transition matrix delta: 0.8627

The exact p-value is deterministic for this seeded example. In a real study,
define the action vocabulary and coding reliability before interpreting process
differences.

Next, use :doc:`factorial_analysis` when predictors and interactions are more
important than transition structure.
