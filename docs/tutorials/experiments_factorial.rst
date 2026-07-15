Experiments: Design A Reproducible Factorial Study
==================================================

``design-research-experiments`` owns hypotheses, factors, conditions, run
budgets, seeds, artifacts, and study execution. This tutorial stays at the
design layer and materializes a two-factor experiment without running agents.

What You Will Learn
-------------------

- Define factors and levels with stable names and values.
- Declare an outcome and a bounded run budget.
- Validate cross-object study references before execution.
- Materialize a full 2 x 2 condition table and deterministic run seeds.
- Serialize the study definition for provenance and review.

Install And Run
---------------

:download:`Download experiments_factorial.py <../../examples/tutorials/experiments_factorial.py>`,
open its containing folder in VS Code, and use the integrated terminal:

.. code-block:: bash

   python -m pip install design-research-experiments==0.2.1
   python experiments_factorial.py

Walkthrough
-----------

The study crosses prompt frame with design representation. Three replicates per
condition produce twelve planned runs. ``SeedPolicy`` derives stable per-run
seeds from study, condition, and replicate identifiers rather than global random
state.

.. literalinclude:: ../../examples/tutorials/experiments_factorial.py
   :language: python
   :linenos:

Expected Output
---------------

.. code-block:: text

   Study valid: True
   Conditions: 4
   Planned runs: 12
   - neutral / text
   - neutral / sketch
   - challenge / text
   - challenge / sketch
   Study definition: artifacts/tutorials/experiments_factorial/study.json

Add hypotheses and analysis plans when the design is ready to preregister. Add
constraints before materialization when some factor combinations are invalid.

Next, learn a focused analysis workflow in :doc:`analysis_reliability`, then
run the shared artifact handoff in :doc:`full_stack_study`.
