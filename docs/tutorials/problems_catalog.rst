Problems: Find And Inspect A Design Task
========================================

Use ``design-research-problems`` when a study needs a packaged prompt,
decision space, grammar, optimization benchmark, or MCP-backed task. This
tutorial searches compact catalog summaries before loading executable problem
objects.

What You Will Learn
-------------------

- Search by text and problem kind without loading every full problem.
- Narrow a loaded object to a concrete public problem type.
- Inspect a decision benchmark's best packaged evaluation.
- Read solver hints from an optimization benchmark without parsing its prose.

Install And Run
---------------

:download:`Download problems_catalog.py <../../examples/tutorials/problems_catalog.py>`,
open its containing folder in VS Code, and use the integrated terminal:

.. code-block:: bash

   python -m pip install design-research-problems==0.4.0
   python problems_catalog.py

The umbrella install also provides the component:

.. code-block:: bash

   python -m pip install design-research==0.4.0

Walkthrough
-----------

``search_problem_summaries`` returns compact metadata for routing and catalog
UIs. ``get_problem_as`` then loads one implementation and verifies the runtime
type. Optimization problems expose structured bounds, constraint counts, and a
recommended solver family through ``solver_hints``.

.. literalinclude:: ../../examples/tutorials/problems_catalog.py
   :language: python
   :linenos:

Expected Output
---------------

The catalog count can grow over time, but the selected IDs and contract fields
remain stable for this release.

.. code-block:: text

   Selected problem: decision_laptop_design_profit_maximization
   Problem kind: decision
   Best market-share proxy: 0.6353
   Optimization problem: planar_truss_span_mass_min
   Decision variables: 15
   Recommended solver: discrete or combinatorial optimizer; preserve integrality explicitly

Try changing ``text`` or ``kind`` in the search call. Add ``capabilities`` or
``study_suitability`` filters when a study requires a specific evaluator or
research use.

Next, use the selected problem in :doc:`full_stack_study`, or learn how agent
execution is structured in :doc:`agents_workflow`.
