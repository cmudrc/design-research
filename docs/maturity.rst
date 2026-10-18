Workflow Maturity
=================

Use maturity labels to choose a workflow and plan how much validation your
study needs. Labels apply to a named workflow or contract at the exact package
combination in :doc:`compatibility`, not to every capability in a package.
They do not certify a scientific method, a model's answers, or a paper's claims.

Maturity Levels
---------------

Experimental
~~~~~~~~~~~~

The capability is available for evaluation, but its interface, output format,
or operating requirements may change between releases. Pin versions, retain
the original evidence, and validate the behavior needed by your study. Passing
tests or one successful live-model smoke run does not by itself justify a
stronger label. Treat an unclassified workflow as experimental unless its
owning package explicitly documents a narrower status.

Stable for research
~~~~~~~~~~~~~~~~~~~

The named path has a documented public interface, deterministic regression
coverage, an explicit artifact contract, and a verified example for the listed
package combination. It is suitable for repeated research use within those
bounds. Researchers still own study design, assumptions, data quality,
interpretation, and validation of any extension beyond the tested path.

This label does not promise unchanged APIs across releases, universal backend
support, scientific validity, or byte-identical live-model output. Pin the
tested family and revalidate before upgrading.

Legacy
~~~~~~

The capability is retained to read older artifacts or support an existing
workflow, but is not recommended for new studies. Its owning maintainer must
name the replacement, supported versions, and migration limits before marking
it legacy. The label alone sets neither a removal date nor a support period.
No workflow in the current table is designated legacy.

Current Workflow Status
-----------------------

These assignments cover the ``design-research==0.5.0`` family, not arbitrary
combinations of component versions.

.. list-table:: Scope, evidence, and remaining limits
   :header-rows: 1
   :widths: 28 18 54

   * - Workflow or contract
     - Maturity
     - Evidence and boundary
   * - :doc:`canonical_artifact_flow`
     - Stable for research
     - Deterministic public-wrapper example and family smoke tests cover the
       packaged problem, seeded baseline, export, and Analysis handoff. This
       does not classify every component export.
   * - Canonical artifact schema ``0.2.0`` in :doc:`compatibility`
     - Stable for research
     - The pinned family exports and validates the canonical artifact set.
       Separately versioned run-evidence, analysis-result, and paper-contribution
       records are not promoted by this schema label.
   * - :doc:`tutorials/study_to_paper_draft`, including contribution records
       and verified bundles
     - Experimental
     - Two offline examples exercise fresh-process export, compilation,
       accounting, and integrity checks. Drafts require author review; the
       reporting surface may evolve. Integrity is not automatic replay or
       proof that a claim follows scientifically from its evidence.
   * - :doc:`prompt_framing_study` and other live-model tutorial paths
     - Experimental
     - Runtime-specific smoke checks establish that the tested setup can run.
       Model availability, dependencies, hardware, and nondeterministic output
       still require validation in the researcher's environment.

Compatibility And Expected Change
---------------------------------

Package versions identify software releases. PyPI development classifiers
describe package-level development status. Artifact schema versions identify
data contracts. Workflow maturity describes the evidence supporting a named
use path. These signals are independent; this policy does not change package
classifiers or grant new compatibility guarantees.

The exact pins in :doc:`compatibility` remain the supported umbrella
combination. Even for a stable-for-research path, do not infer compatibility
with unlisted versions or assume that a future patch or minor release cannot
change behavior. Read the owning package's release notes, preserve the original
artifact directory and environment record, and rerun the relevant acceptance
checks before adopting an upgrade. Missing or unsupported evidence must remain
an explicit gap, not an inferred result.

Changing A Label
----------------

The maintainer proposing a change opens a pull request that names the workflow,
package versions, contract versions, and new label. The proposal links the
regression tests and verified example, records remaining limitations, and
explains any compatibility or migration impact. For promotion to stable for
research, reviewers require the public interface, deterministic checks,
artifact contract, and verified example described above.

The owning package maintainer reviews component claims; the umbrella
maintainer reviews cross-package claims. The merged pull request records the
decision. Its author updates this table and the affected workflow pages in the
same change. If a regression invalidates an assignment, maintainers narrow the
scope or downgrade the label and link the corrective issue. A label never
substitutes for the tests or evidence behind it.
