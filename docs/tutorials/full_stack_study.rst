Compose The Libraries: Run A Benchmark Study
============================================

This tutorial runs the smallest deterministic Problems to Agents to Experiments
to Analysis handoff. It is the recommended compatibility smoke test and the
best starting point for a new composed study.

What You Will Learn
-------------------

- Load a packaged design benchmark through the umbrella namespace.
- Define a study around the public seeded baseline agent.
- Execute deterministic replicates and export canonical artifacts.
- Validate event rows and compute a condition metric from those artifacts.
- Write a human-readable study summary next to the raw tables.

Install And Run
---------------

:download:`Download canonical_artifact_flow.py <../../examples/canonical_artifact_flow.py>`,
open its containing folder in VS Code, and use the integrated terminal:

.. code-block:: bash

   python -m pip install design-research==0.4.0
   python canonical_artifact_flow.py

Walkthrough
-----------

The umbrella keeps the imports coherent while each component retains ownership
of its behavior. Problems supplies the benchmark, Agents supplies the baseline
participant, Experiments owns execution and export, and Analysis consumes the
versioned event artifact.

.. literalinclude:: ../../examples/canonical_artifact_flow.py
   :language: python
   :linenos:

Selected Output
---------------

The script also prints the selected problem and agent, mean outcome, and output
directory. These lines capture the main completion checks:

.. code-block:: text

   Canonical artifact flow: canonical_artifact_flow
   Package path: problems -> agents -> experiments -> analysis
   Runs: 2 (2 success)
   Event rows valid: True (rows=2)
   Summary report: canonical_artifact_flow_summary.md

Inspect ``artifacts/examples/canonical_artifact_flow/analysis`` after the run.
Those files are the durable boundary between study execution and downstream
analysis.

Next, keep the same artifact-first boundary while comparing longer process
traces in :doc:`process_comparison`.
