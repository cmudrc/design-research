# Examples

The examples in this repository are intentionally lightweight and
teaching-oriented.

- `real_stack_interoperability.py` is the smallest real end-to-end umbrella
  study. It resolves one packaged decision problem, runs a deterministic
  seeded baseline, exports canonical artifacts, and validates `events.csv`
  through the analysis layer.
- `mechanical_design_stack.py` does the same thing for a packaged
  mechanical-design optimization benchmark and prints a short benchmark
  shortlist first.
- `prompt_framing_study.py` is the canonical composed workflow example. It
  uses umbrella imports, a real packaged problem, a managed llama.cpp workflow
  agent, the April-branch `build_strategy_comparison_study` scaffold, export-
  driven condition-pair permutation tests, markdown reporting helpers, canonical
  experiment artifact export, and event-table validation.
- `basic_usage.py` remains the smallest possible import-surface smoke example.

Run locally with:

```bash
make run-example
make examples-test
```

`make run-example` uses a managed `llama.cpp` runtime. Install
`llama-cpp-python[server]` first. If you want the default model download path,
also install `huggingface-hub`; otherwise set `LLAMA_CPP_MODEL` to point at a
specific local GGUF file. This walkthrough also expects the April 2026
workflow/recipe/reporting APIs from `design-research-agents`,
`design-research-experiments`, and `design-research-analysis`. The study
defaults to eight replicates per condition; set `PROMPT_STUDY_REPLICATES` to
run a larger sample.
The deterministic examples automatically use sibling April workspaces when
they are checked out beside this repo, and otherwise fall back to the
published umbrella dependency set.
`make examples-test` skips the live study walkthrough unless
`RUN_LIVE_EXAMPLE=1`.
