Concepts
========

``design-research`` is the umbrella entry point and compatibility-tested
routing package for four specialized libraries. It does not reimplement their
research logic.

Package Roles
-------------

- **Problems** owns tasks, prompts, grammars, benchmark data, and evaluators.
- **Agents** owns AI participants, workflows, tools, and reasoning traces.
- **Experiments** owns study definitions, conditions, replication, execution
  control, and canonical artifact export.
- **Analysis** owns validation, transformation, statistics, and visualization
  of study artifacts.
- **The umbrella** owns shared discovery, the wrapper namespace, an exact
  tested version combination, and composed learning paths.

Two Architecture Views
----------------------

**Control topology** describes responsibility. Problems and Agents are peer
study inputs; Experiments coordinates their use and defines the handoff to
Analysis.

**Runtime and data flow** describes what moves during a study: Problems +
Agents → Experiments artifact set → Analysis → evidence that can refine the
next protocol.

These views are complementary. Neither is an installation order or a claim
that Experiments owns the other packages' implementations.

Contracts And Versions
----------------------

- A **package API** is the import surface owned by one package. For the exact
  pinned family, umbrella wrappers mirror the component packages' public
  ``__all__`` exports.
- A **package version** identifies released code. :doc:`compatibility` records
  the exact combination tested by the umbrella.
- An **artifact schema version** identifies the cross-package data layout and
  is recorded in the exported manifest.
- A **development classifier** is current package metadata, not an
  ecosystem-wide maturity label.
