Learn With ``design-research``
================================

Learn computational design research by using the same open-source tools that
support work in the Design Research Collective. Start with a runnable tutorial,
change an example when you are ready, and keep what you build. Sharing a patch
or pull request is always optional.

.. container:: drc-learning-hero

   **The tutorials are the opportunity.** You do not need to apply, join a
   cohort, or contact the lab before starting.

   :doc:`Choose a tutorial <tutorials/index>` | :doc:`Set up VS Code <vscode_start>`

What This Path Is
-----------------

This is a public, self-guided learning path for anyone comfortable trying
Python. It is not an internship, supervised research placement, or admissions
process. There are no deadlines, meetings, certificates, or required
contributions.

Completing a tutorial or opening a contribution does not imply individual
feedback, mentorship, lab membership, a recommendation, or a future position.
Issues and pull requests enter the same open-source review process as every
other contribution. Review and acceptance depend on project fit and maintainer
availability.

You do not need to tell us your age, school, or reason for using the materials.
Do not include private information, credentials, school records, participant
data, or sponsor data in an issue or contribution.

Your Learning Path
------------------

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

.. list-table:: Choose by what you want to learn
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
extension and a short explanation are a complete learning outcome. You do not
need to submit them anywhere.

4. Contribute If It Helps Your Learning
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If your extension fixes a defect or improves the project for other users, you
may choose to share it:

1. Read the `contribution guide <https://github.com/cmudrc/design-research/blob/HEAD/CONTRIBUTING.md>`_.
2. Keep the change focused and explain the user-facing improvement.
3. Run the checks requested by the repository you changed.
4. Open a pull request through the repository's normal GitHub workflow.

A pull request is a proposed improvement, not an application. It may be
discussed, revised, declined, or remain unmerged. The value of the learning
path does not depend on that outcome.

Where The Libraries Fit
-----------------------

The umbrella package connects four focused libraries:

- `design-research-problems <https://github.com/cmudrc/design-research-problems>`_
  provides prompts, design tasks, grammars, benchmarks, and evaluators.
- `design-research-agents <https://github.com/cmudrc/design-research-agents>`_
  provides AI participants, workflows, tools, and traceable reasoning patterns.
- `design-research-experiments <https://github.com/cmudrc/design-research-experiments>`_
  defines hypotheses, conditions, replications, and study artifacts.
- `design-research-analysis <https://github.com/cmudrc/design-research-analysis>`_
  supports sequence, language, embedding, and statistical analysis.

Begin with the umbrella tutorials. Move into a component repository only when
you want to understand or change that layer in more detail.

.. container:: drc-learning-finish

   **A successful first step is simple:** run one tutorial, change one thing,
   and explain what you learned.
