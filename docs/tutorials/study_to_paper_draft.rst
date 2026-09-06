Study to Evidence to Paper Draft
================================

This workflow treats paper preparation as a deliberate continuation of study
execution. Every attempted run leaves durable evidence. No paper files appear
until a separate explicit action reads the completed study directory.

The result is a visibly labeled, author-review paper draft. It can contain
factual study structure, configured component methods, observed execution,
executed analysis prose, curated citations, tables, figures, and TODOs. It does
not make novelty claims, interpret the science, invent references, or promise
automatic computational replay.

Two Offline Examples
--------------------

.. list-table:: End-to-end acceptance examples
   :header-rows: 1

   * - Example
     - Evidence retained
     - Paper support
   * - ``ideation_evidence_to_paper.py``
     - 24 partial-factorial attempts across six packaged ideation problems,
       including ``ideation_peanut_shelling``; one intentional failure; two
       reasoned analysis exclusions; prompt and citation lineage.
     - Regression Methods and Results, coefficient table, result figure,
       deduplicated bibliography, honest failure/TODO reporting.
   * - ``computational_design_evidence_to_paper.py``
     - Eight seeded executions of the packaged student-laptop decision problem;
       raw candidates; authentic evaluator outputs; terminal run records.
     - Packaged problem and baseline-agent Methods, artifact-first dataset
       profile, evaluator table and figure.

Both examples are deterministic and offline. Running either script with no
arguments launches the study and draft phases in separate Python interpreters:

.. code-block:: bash

   python examples/ideation_evidence_to_paper.py
   python examples/computational_design_evidence_to_paper.py

Inspect the Process Boundary
----------------------------

Run the phases separately to verify that execution never creates a paper
draft implicitly:

.. code-block:: bash

   python examples/ideation_evidence_to_paper.py \
     --phase run \
     --output-dir artifacts/ideation-paper

   test ! -e artifacts/ideation-paper/paper-draft

   python examples/ideation_evidence_to_paper.py \
     --phase draft \
     --output-dir artifacts/ideation-paper \
     --require-tectonic

The first process exits after writing canonical schema 0.2.0 artifacts,
terminal ``run.json`` records, retained observations, selected analysis input,
an analysis-result record, and its table and figure. The second process loads
only that directory plus installed packages, reconstructs component-owned
paper contributions, and calls ``export_paper_draft(...)`` explicitly.

Draft Contents and Boundaries
-----------------------------

The resulting ``paper-draft/`` contains both editable formats and an auditable
manifest:

.. code-block:: text

   paper-draft/
     main.tex
     paper_draft.md
     references.bib
     paper_draft_manifest.json
     README.md
     sections/
     tables/
     figures/

``paper_draft_manifest.json`` records ``document_status: paper-draft`` and
``author_review_required: true``. Its run accounting separates planned,
attempted, terminal, successful, failed, skipped, incomplete, analyzed, and
documented excluded runs. In the ideation example those counts are 24 planned
and attempted, 23 successful, one failed, 21 analyzed, and two excluded.

TODOs are part of the contract. A normal export succeeds with an honest partial
draft. Strict completeness may write the draft and then fail when unresolved
evidence-critical TODOs remain. Author-judgment TODOs remain visible even in a
complete evidence handoff.

Compilation and Citations
-------------------------

When Tectonic is available, each example compiles ``main.tex``. Passing
``--require-tectonic`` turns a missing compiler into an acceptance failure. The
family tests also extract each verified bundle and compile the retained draft
from the extracted directory.

Only caller- or component-supplied BibTeX is emitted. Stable citation keys are
aligned with the stored BibTeX entry identifiers, every ``\\cite{...}`` key is
checked against ``references.bib``, and conflicting reference records fail
instead of being guessed or silently merged.

Verified Bundle
---------------

After compilation the Analysis package creates ``study-paper-draft.zip``. It
contains canonical study artifacts, per-run evidence, analysis records,
selected supporting data, the complete draft, tables, figures, a sanitized
environment summary, and a machine-readable inventory. SHA-256 covers every
archive member, including the inventory manifest through the ZIP comment.

Verification reads without extracting or executing. Absolute, escaping,
duplicate, and symlink members fail. Per-run attachments and unselected files
are excluded by default; the examples deliberately leave a private-note
fixture outside the bundle to exercise that boundary.

Run the Acceptance Gate
-----------------------

.. code-block:: bash

   make examples-test
   python -m pytest tests/test_paper_draft_acceptance.py

The focused test suite includes the exact release accounting fixture: 40 runs
planned and attempted, 37 successful, three failed, 35 analyzed, and two
documented exclusions.
