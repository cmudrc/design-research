Typical Workflow
================

1. Import ``design_research`` to anchor ecosystem discovery.
2. Select one or more wrapper submodules based on task:
   - ``design_research.problems`` for benchmark tasks and registries.
   - ``design_research.agents`` for participants and coordination patterns.
   - ``design_research.experiments`` for study definitions and orchestration.
   - ``design_research.analysis`` for downstream analysis and reporting.
3. Build end-to-end studies by composing these layers without duplicating logic.
   Start with the deterministic recipe-first examples for the smallest study
   entry points, then see :doc:`prompt_framing_study` for the canonical live
   walkthrough.
4. Keep package-specific details in component repositories.
