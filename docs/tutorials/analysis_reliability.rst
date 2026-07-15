Analysis: Measure Inter-Rater Reliability
=========================================

``design-research-analysis`` provides statistical, sequence, language,
embedding, visualization, and artifact-integration workflows. This tutorial
focuses on nominal protocol coding, where multiple researchers classify the
same design moves.

What You Will Learn
-------------------

- Represent coding data as one item per row and one rater per column.
- Choose Cohen kappa, Fleiss kappa, or Krippendorff alpha.
- Handle incomplete ratings explicitly.
- Produce reproducible item-bootstrap confidence intervals.

Install And Run
---------------

:download:`Download analysis_reliability.py <../../examples/tutorials/analysis_reliability.py>`,
open its containing folder in VS Code, and use the integrated terminal:

.. code-block:: bash

   python -m pip install design-research-analysis==0.3.0
   python analysis_reliability.py

Walkthrough
-----------

Cohen kappa uses the first two raters. Fleiss kappa uses complete rows from all
raters. Krippendorff alpha retains rows with at least two observed ratings, so
it can use the incomplete final row. A fixed seed makes each bootstrap interval
repeatable.

.. literalinclude:: ../../examples/tutorials/analysis_reliability.py
   :language: python
   :linenos:

Expected Output
---------------

.. code-block:: text

   cohen_kappa coefficient=0.500 interval=(-0.048, 1.000) items=6/6 missing=0
   fleiss_kappa coefficient=0.583 interval=(-0.211, 1.000) items=5/6 missing=1
   krippendorff_alpha coefficient=0.667 interval=(0.255, 1.000) items=6/6 missing=1

Use these estimates to audit a coding protocol before treating coded events as
study outcomes. The package currently treats these labels as nominal; do not
imply ordinal or interval disagreement costs through this API.

Next, analyze exported event sequences in :doc:`process_comparison`, or fit a
model from experiment artifacts in :doc:`factorial_analysis`.
