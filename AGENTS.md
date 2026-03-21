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
- The preferred interpreter target lives in `.python-version` (`3.12`).
- Install local tooling with `make dev`.

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
  - `make run-example` (install `llama-cpp-python` first; optionally set `LLAMA_CPP_MODEL` for a specific GGUF file)
  - `make examples-test` (skips the live walkthrough unless `RUN_LIVE_EXAMPLE=1`)
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
- Let the canonical walkthrough fail fast when the `llama.cpp` runtime is missing rather than silently falling back.
- Keep total line coverage at or above 90% in CI and local release work.
- Update tests, docs, and examples alongside behavior changes.
- Avoid broad dependency growth in the base install.
- Treat this package as an umbrella wrapper; do not duplicate implementation
  logic from sibling repositories.

## Release Naming

- Theme: cartography and wayfinding.
- Monthly release names are shared across milestone titles, release PR titles,
  and release branches.
- Milestone due dates should land about one week after the start of the release
  month so new versions of sibling libraries have time to land first.
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
| April 8, 2026 | Atlas Alignment | Atlas |
| May 8, 2026 | Meridian Map | Meridian |
| June 8, 2026 | Compass Course | Compass |
| July 8, 2026 | Legend Line | Map legend |
| August 8, 2026 | Bearing Bridge | Bearing |
| September 8, 2026 | Surveyor Signal | Surveying |
| October 8, 2026 | Cartographer Circuit | Cartography |
| November 8, 2026 | Wayfinder Weave | Wayfinding |
| December 8, 2026 | Transit Trace | Transit |
| January 8, 2027 | North Star Nexus | Pole star |

## Keep This File Up To Date

Update this file whenever contributor workflow changes, especially setup
commands, validation commands, or public API expectations.
