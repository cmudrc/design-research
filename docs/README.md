# Documentation Maintenance

## Validate Docs Locally

For every documentation change, run both:

- `make docs-check` — validate generated tutorial material, notebook freshness,
  version pins, navigation, badges, and other cross-file contracts.
- `make docs-build` — perform the strict Sphinx HTML render with warnings as
  errors.

Run `make docs-linkcheck` whenever public links change. `make docs` remains an
alias for `make docs-build`; use the explicit target in contributor guidance so
the two required checks are easy to distinguish.

## Docstring Style

Use Google-style docstrings where policy applies.
Run `make docstrings-check` before merge.

## Page-Writing Conventions

- Keep the homepage short: title, tagline, concise framing, quickstart callout, section-oriented links, and only the minimum ecosystem/contribution notes needed for orientation.
- Keep the root hidden home-page toctree section-first so the PyData header and sidebar stay stable.
- Emphasize that this package is an umbrella namespace and routing layer, not the home for deep implementation details.
- Keep top-level pages focused on discovery, interoperability, and the tested
  wrapper imports across the component libraries.

## Table vs Prose Rule

Prefer compact tables for scanning. Preserve nuance in narrative paragraphs directly below the table. Do not use tables to carry long explanatory sentences.

## Cross-links

Use `:doc:` for internal links and explicitly point readers to sibling package docs when behavior lives outside the umbrella layer.

## Sources Of Truth

- The umbrella docs own the shared package-family identity, two-view
  architecture, tested compatibility matrix, learning path, and
  `ecosystem-platform.svg`.
- Component docs own their detailed APIs, optional dependencies, providers,
  and implementation-specific examples. Link to those docs instead of copying
  material that can drift.
- `docs/compatibility.rst` reports factual package classifiers and the tested
  artifact schema. Do not invent ecosystem maturity labels while the policy in
  issue #12 remains open.

## Branding

- The ecosystem figure is the umbrella source of truth for constituent package
  colors and shared control/runtime framing.
- Keep docs CSS tokens, `drc-light.png`, `drc-dark.png`, and `favicon.ico` aligned with the shared docs theme.
- The umbrella site uses a four-color decorative gradient drawn from agents, problems, analysis, and experiments, while repeated interactive controls stay on the experiments teal pair.

## API Page Updates

When public exports change, update:

- `docs/api.rst`
- quickstart/workflow snippets
- ecosystem framing where the top-level namespace changes
