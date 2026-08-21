Compose The Libraries: Analyze A Partial Factorial Study
=========================================================

This tutorial samples model-size and design-task combinations instead of
running their full cross product. It executes deterministic ideation traces,
exports canonical events, and fits a regression directly from the artifact.

What You Will Learn
-------------------

- Define a larger factor space while materializing a deliberate partial matrix.
- Bind problem IDs and model metadata to explicit conditions.
- Return normalized custom-agent metrics and event sequences.
- Fit numeric and categorical predictors without manually loading CSV tables.
- Keep regression inputs traceable to the exported experiment artifact.

Install And Run
---------------

:download:`Download partial_factorial_ideation_regression.py <../../examples/partial_factorial_ideation_regression.py>`,
open its containing folder in VS Code, and use the integrated terminal:

.. code-block:: bash

   python -m pip install design-research==0.4.0
   python partial_factorial_ideation_regression.py

Core Orchestration
------------------

The excerpt shows the user-facing run and analysis path. The complete source
also defines the explicit condition matrix and deterministic participant.

.. literalinclude:: ../../examples/partial_factorial_ideation_regression.py
   :language: python
   :linenos:
   :start-at: def main()
   :end-before: def _study(

Selected Output
---------------

The script also lists the fitted task-family terms and artifact directory.
These lines capture the main regression checks:

.. code-block:: text

   Partial factorial ideation regression: partial_factorial_ideation_regression
   Conditions: 12
   Runs: 24
   Event rows valid: True (rows=120)
   Regression samples: 24
   Model size coefficient: 0.0098
   R2: 0.992

Use an explicit partial matrix only when its estimable effects match the
research question. For generated fractional-factorial or Latin-hypercube
designs, use the DOE helpers owned by ``design-research-experiments``.

Continue to :doc:`../prompt_framing_study` to replace deterministic participant
logic with a managed local model while preserving the same artifact boundary.
