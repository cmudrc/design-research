# Focused Tutorial Examples

These examples introduce one component library at a time before the composed
examples use the umbrella namespace:

- `problems_catalog.py`: search the packaged problem catalog and inspect a
  solver-ready problem contract.
- `agents_workflow.py`: build and run a deterministic two-step workflow.
- `experiments_factorial.py`: define and materialize a reproducible 2x2 study.
- `analysis_reliability.py`: estimate nominal inter-rater reliability.

Run all offline examples from the repository root with:

```bash
make examples-test
```

Each script can also be run directly with `python examples/tutorials/<name>.py`.
