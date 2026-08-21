Typical Workflow
================

Use the control topology to decide who owns each step and the runtime flow to
trace the artifacts that connect those steps.

1. **Select Problems inputs.** Choose packaged tasks, prompts, grammars, or
   evaluators through ``design_research.problems``.
2. **Select Agents inputs.** Choose participants or workflows through
   ``design_research.agents``. Problems and Agents are peer inputs to the study.
3. **Define and run the study.** Use ``design_research.experiments`` for
   hypotheses, conditions, replication, execution control, and artifact export.
4. **Analyze the exported artifacts.** Use ``design_research.analysis`` to
   validate and transform the event tables, then compute or visualize results.
5. **Refine the protocol.** Feed the evidence into the next Experiments study
   definition without changing ownership of Problems, Agents, or Analysis.

The runtime handoff is therefore:

.. code-block:: text

   Problems + Agents -> Experiments artifact set -> Analysis -> protocol refinement

Start with :doc:`canonical_artifact_flow` for the smallest deterministic
all-package handoff. Continue to :doc:`prompt_framing_study` only when a live
model-backed Agents workflow is useful. Use the owning component documentation
for package-specific APIs and optional dependencies.
