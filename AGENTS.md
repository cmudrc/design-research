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
  - `make run-example` (install `llama-cpp-python[server]`; also install `huggingface-hub` unless `LLAMA_CPP_MODEL` points at a local GGUF file)
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
- Keep wrapper modules thin and trust the sibling libraries to define their own
  public surfaces. Wrapper submodules should mirror each sibling package's
  `__all__` by default rather than maintaining local allowlists.
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
- Monthly work-cycle names are shared across milestone titles, release PR
  titles, and release branches.
- Name the cycle for the month the work is done, not the later drop month.
  - Milestone title / PR title: `{base name} - {Work month YYYY}`
  - Release branch: slugified full title, for example
    `meridian-map-april-2026`
- Milestone due dates should land about one week into the following month so
  new versions of sibling libraries have time to land first.
- Milestone descriptions must use:
  - `Work month: {Month YYYY}.`
  - `Theme source: <url>`
- Release PR bodies must repeat the same `Theme source:` link used on the
  milestone and refer to the same work month named in the title.
- Never reuse an exact base name or the same primary subject across any work
  month or any of the design-research repositories unless the affected
  `AGENTS.md` files are intentionally updated together.
- Before adding a new release name, check the `Release Naming` tables in the
  related repos to avoid repeats.

| Work month | Target drop | Base name | Source subject |
| --- | --- | --- | --- |
| March 2026 | April 8, 2026 | Atlas Alignment | Atlas |
| April 2026 | May 8, 2026 | Meridian Map | Meridian |
| May 2026 | June 8, 2026 | Compass Course | Compass |
| June 2026 | July 8, 2026 | Legend Line | Map legend |
| July 2026 | August 8, 2026 | Bearing Bridge | Bearing |
| August 2026 | September 8, 2026 | Surveyor Signal | Surveying |
| September 2026 | October 8, 2026 | Cartographer Circuit | Cartography |
| October 2026 | November 8, 2026 | Wayfinder Weave | Wayfinding |
| November 2026 | December 8, 2026 | Transit Trace | Transit |
| December 2026 | January 8, 2027 | North Star Nexus | Pole star |

## Keep This File Up To Date

Update this file whenever contributor workflow changes, especially setup
commands, validation commands, or public API expectations.
