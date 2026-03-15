# AGENTS.md

## Purpose

This repository hosts `design-research`, a thin Python 3.12+ umbrella package
for the CMU Design Research Collective ecosystem. Keep changes focused,
keep the public API intentional, and avoid duplicating logic from sibling
component libraries.

## Setup

- Create and activate a virtual environment:
  - `python -m venv .venv`
  - `source .venv/bin/activate`
- The reproducible interpreter target lives in `.python-version` (`3.12.12`).
- Install local tooling with `make dev`.
- For a frozen environment based on `uv.lock`, use `make repro`.

## Testing And Validation

Use the smallest useful check while iterating, then run the full gate before
merging.

- Fast local loop:
  - `make fmt`
  - `make lint`
  - `make type`
  - `make test`
- If docs changed:
  - `make docs-check`
  - `make docs`
- If the example changed:
  - `make run-example`
- Pre-merge baseline:
  - `make ci`
- Pre-publish baseline:
  - `make release-check`

## Public Vs Private Boundaries

- The supported public surface is whatever is re-exported from
  `src/design_research/__init__.py` and the wrapper submodules:
  `design_research.problems`, `design_research.agents`,
  `design_research.experiments`, and `design_research.analysis`.
- Keep wrapper modules thin and explicit; prefer pass-through imports and curated
  `__all__` lists.
- If internal helper modules are added, prefix them with `_` and keep them out
  of top-level exports unless there is a deliberate API decision.

## Behavioral Guardrails

- Keep tests deterministic and offline by default.
- Update tests, docs, and examples alongside behavior changes.
- Avoid broad dependency growth in the base install.
- Treat this package as an umbrella wrapper; do not duplicate implementation
  logic from sibling repositories.

## Release Naming

- Theme: cartography and wayfinding.
- Monthly release names are shared across milestone titles, release PR titles,
  and release branches.
  - Milestone title / PR title: `{base name} - {Month YYYY}`
  - Release branch: slugified full title, for example `meridian-map-may-2026`
- Milestone descriptions must use:
  - `Tracks {previous month YYYY} work.`
  - `Theme source: <url>`
- Release PR bodies must repeat the same `Theme source:` link used on the
  milestone.
- Never reuse an exact base name or the same primary subject across any month
  or any of the design-research repositories unless the affected `AGENTS.md`
  files are intentionally updated together.
- Before adding a new release name, check the `Release Naming` tables in the
  related repos to avoid repeats.

| Due date | Base name | Source subject |
| --- | --- | --- |
| April 1, 2026 | Atlas Alignment | Atlas |
| May 1, 2026 | Meridian Map | Meridian |
| June 1, 2026 | Compass Course | Compass |
| July 1, 2026 | Legend Line | Map legend |
| August 1, 2026 | Bearing Bridge | Bearing |
| September 1, 2026 | Surveyor Signal | Surveying |
| October 1, 2026 | Cartographer Circuit | Cartography |
| November 1, 2026 | Wayfinder Weave | Wayfinding |
| December 1, 2026 | Transit Trace | Transit |
| January 1, 2027 | North Star Nexus | Pole star |

## Keep This File Up To Date

Update this file whenever contributor workflow changes, especially setup
commands, validation commands, or public API expectations.
