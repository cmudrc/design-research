# Examples

The examples in this repository are intentionally small, recipe-first, and
future-branch oriented.

- `student_laptop_design_study.py` is the smallest application-first decision
  study. It runs the packaged student laptop benchmark, prints the chosen
  laptop configuration, and reports the evaluator's observed market metrics.
- `pump_and_battery_design_portfolio.py` is the packaged engineering portfolio
  example. It runs real pump and battery optimization benchmarks, reports the
  observed objective and feasibility results, and previews a second recipe.
- `prompt_framing_study.py` is the canonical live walkthrough. It keeps the
  managed `llama.cpp` runtime, workflow-backed strategy arms, pairwise
  condition comparisons, and markdown reporting.

Run locally with:

```bash
make run-example
make examples-test
```

`make run-example` executes the live canonical walkthrough in
`examples/prompt_framing_study.py`. Install `design-research[examples]` first.
That extra includes the managed `llama.cpp` client path and the default model
download helper. If you prefer a specific local GGUF file, set
`LLAMA_CPP_MODEL`. The live study defaults to eight replicates per condition;
set `PROMPT_STUDY_REPLICATES` to run a larger sample.

`make examples-test` stays deterministic and offline-first by default. It runs
the two non-live examples and skips the live walkthrough unless
`RUN_LIVE_EXAMPLE=1`.

The examples prefer adjacent sibling worktrees during local development so
they can use the future recipe/workflow/reporting APIs before the pinned PyPI
versions catch up. Keep the sibling repos next to this repo or set
`DESIGN_RESEARCH_WORKSPACE_ROOT=/path/to/your/workspace`. You can also point a
single example layer at a different checkout with repo-specific overrides such
as `DESIGN_RESEARCH_AGENTS_ROOT` or `DESIGN_RESEARCH_EXPERIMENTS_ROOT`.
