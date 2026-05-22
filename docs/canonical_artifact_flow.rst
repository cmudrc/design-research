Canonical Artifact Flow
=======================

This is the smallest deterministic example that still crosses the full
ecosystem boundary:

- ``design_research.problems`` loads a packaged benchmark.
- ``design_research.agents`` supplies the public seeded baseline agent.
- ``design_research.experiments`` builds and runs the study, then exports
  canonical artifacts.
- ``design_research.analysis`` validates and reads those artifacts.

It is the compatibility smoke path for the examples workflow: no live model, no
network dependency, and no umbrella-owned orchestration logic.

Run it with:

.. code-block:: bash

   python examples/canonical_artifact_flow.py

Code
----

.. literalinclude:: ../examples/canonical_artifact_flow.py
   :language: python
   :linenos:
   :caption: ``examples/canonical_artifact_flow.py``
