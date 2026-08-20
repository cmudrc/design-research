Learning Path
=============

Explore computational design research with the open-source tools developed by
the Design Research Collective. Start with a runnable tutorial, adapt an
example, and follow the parts of the ecosystem that match your interests.

.. container:: drc-learning-hero

   Start with a tutorial. Extend an example. Share an improvement if it is
   useful to others.

   :doc:`Choose a tutorial <tutorials/index>` :doc:`Set up VS Code <vscode_start>`
   :doc:`Workshop setup and preflight <workshop-setup>`

Four Steps
----------

1. Run One Example
~~~~~~~~~~~~~~~~~~

Install the published ``design-research`` package and confirm that you can load
a packaged problem. The :doc:`VS Code setup guide <vscode_start>` provides the
most direct first-user path. Python 3.12 or newer is required.

If you already work comfortably from a terminal, use the
:doc:`quickstart` instead.

2. Choose A Tutorial
~~~~~~~~~~~~~~~~~~~~

All tutorials include runnable source material and displayed results. Most run
offline. The local-model tutorial is clearly marked and can be skipped.

.. container:: drc-learning-table

   .. list-table::
      :header-rows: 1
      :widths: 22 34 30 14

      * - Track
        - Start here
        - What you will practice
        - Runtime
      * - Design problems
        - :doc:`Map packaged text problems <tutorials/problems_text_map>`
        - Loading a research corpus, representing text, and interpreting a map
        - Offline
      * - Design grammars
        - :doc:`Explore a truss grammar <tutorials/problems_truss_grammar>`
        - Applying rules and inspecting a structured design state
        - Offline
      * - Agent workflows
        - :doc:`Build a deterministic workflow <tutorials/agents_workflow>`
        - Composing and tracing a small reasoning process
        - Offline
      * - Experiments
        - :doc:`Test a Monty Hall strategy <tutorials/experiments_monty_hall>`
        - Conditions, replication, seeding, and reproducible results
        - Offline
      * - Analysis
        - :doc:`Measure coder reliability <tutorials/analysis_reliability>`
        - Preparing observations and quantifying agreement
        - Offline
      * - Complete workflow
        - :doc:`Run a full-stack study <tutorials/full_stack_study>`
        - Connecting problems, agents, experiments, and analysis
        - Offline
      * - Local AI models
        - :doc:`Try propose/critic <tutorials/agents_propose_critic>`
        - Running and comparing a model-backed agent pattern
        - Ollama

The :doc:`complete tutorial index <tutorials/index>` includes additional
process-comparison and factorial-analysis paths.

3. Make The Example Yours
~~~~~~~~~~~~~~~~~~~~~~~~~

Once an example runs unchanged, make one deliberate extension. For example:

- select a different packaged problem;
- change an experimental condition or number of replications;
- add a small deterministic agent step;
- compare another metric or visualization; or
- improve an explanation that was difficult to follow.

Record what you changed, what you expected, and what happened. A working
extension and a short explanation are a complete learning outcome.

4. Share An Improvement
~~~~~~~~~~~~~~~~~~~~~~~

If your extension could help other users, share it through the usual
open-source workflow:

1. Read the `contribution guide <https://github.com/cmudrc/design-research/blob/HEAD/CONTRIBUTING.md>`_.
2. Keep the change focused and explain the user-facing improvement.
3. Run the checks requested by the repository you changed.
4. Open a pull request through the repository's normal GitHub workflow.

Contributions are reviewed for project fit and may be revised before they are
accepted.

Where The Libraries Fit
-----------------------

The umbrella package connects four focused libraries:

- `design-research-problems documentation <https://cmudrc.github.io/design-research-problems/>`_
  (`source <https://github.com/cmudrc/design-research-problems>`__) provides
  prompts, design tasks, grammars, benchmarks, and evaluators.
- `design-research-agents documentation <https://cmudrc.github.io/design-research-agents/>`_
  (`source <https://github.com/cmudrc/design-research-agents>`__) provides AI
  participants, workflows, tools, and traceable reasoning patterns.
- `design-research-experiments documentation <https://cmudrc.github.io/design-research-experiments/>`_
  (`source <https://github.com/cmudrc/design-research-experiments>`__) defines
  hypotheses, conditions, replications, execution, and study artifacts.
- `design-research-analysis documentation <https://cmudrc.github.io/design-research-analysis/>`_
  (`source <https://github.com/cmudrc/design-research-analysis>`__) validates,
  transforms, models, and visualizes exported study data.

Begin with the umbrella tutorials. Move into a component repository only when
you want to understand or change that layer in more detail.
