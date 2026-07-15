Agents: Build A Deterministic Workflow
======================================

``design-research-agents`` supports local logic, tools, memory, model calls,
delegates, and reusable coordination patterns. This tutorial begins with local
logic so workflow structure and result contracts are visible without an LLM
service.

What You Will Learn
-------------------

- Define typed workflow inputs and deterministic ``LogicStep`` handlers.
- Connect steps through explicit dependencies.
- Read prior step outputs from ``dependency_results``.
- Inspect execution order, per-step results, and a Mermaid representation.

Install And Run
---------------

:download:`Download agents_workflow.py <../../examples/tutorials/agents_workflow.py>`,
open its containing folder in VS Code, and use the integrated terminal:

.. code-block:: bash

   python -m pip install design-research-agents==0.5.0
   python agents_workflow.py

Walkthrough
-----------

The first step scales three scores. The second step depends on that result and
computes a mean. ``execution_mode="dag"`` honors declared dependencies, while
the returned ``ExecutionResult`` preserves success, order, and per-step output.

.. literalinclude:: ../../examples/tutorials/agents_workflow.py
   :language: python
   :linenos:

Expected Output
---------------

.. code-block:: text

   Workflow success: True
   Execution order: scale_scores -> summarize_scores
   Scaled score count: 3
   Scaled score mean: 5.0
   Diagram starts with: flowchart LR

Replace a ``LogicStep`` with ``ToolStep``, ``ModelStep``, or ``DelegateStep``
when the workflow needs external behavior. Keep deterministic preprocessing and
validation in logic steps so model-facing work stays small and observable.

Next, define repeatable study conditions in :doc:`experiments_factorial`, or
see a packaged baseline agent participate in :doc:`full_stack_study`.
