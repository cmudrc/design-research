# Documentation Maintenance

## Build Docs Locally

- `make docs-check`
- `make docs-build`

## Docstring Style

Use Google-style docstrings where policy applies.
Run `make docstrings-check` before merge.

## Page-Writing Conventions

- Keep the homepage short: title, tagline, concise framing, quickstart callout, section-oriented links, and only the minimum ecosystem/contribution notes needed for orientation.
- Keep the root hidden home-page toctree section-first so the PyData header and sidebar stay stable.
- Emphasize that this package is an umbrella namespace and routing layer, not the home for deep implementation details.
- Keep top-level pages focused on discovery, interoperability, and stable imports across the sibling libraries.

## Table vs Prose Rule

Prefer compact tables for scanning. Preserve nuance in narrative paragraphs directly below the table. Do not use tables to carry long explanatory sentences.

## Cross-links

Use `:doc:` for internal links and explicitly point readers to sibling package docs when behavior lives outside the umbrella layer.

## API Page Updates

When public exports change, update:

- `docs/api.rst`
- quickstart/workflow snippets
- ecosystem framing where the top-level namespace changes
