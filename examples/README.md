# Examples

The examples in this repository are intentionally small, recipe-first, and
offline-first unless a live runtime is central to the lesson.

Focused, result-bearing Jupyter tutorials live in `examples/tutorials/`:

- `problems_text_map.ipynb` maps packaged word problems with TF-IDF and t-SNE.
- `problems_truss_grammar.ipynb` applies planar-truss grammar rules by hand.
- `agents_propose_critic.ipynb` refines a rationale with Ollama and the existing
  propose/critic pattern; it is opt-in because it requires a local model.
- `agents_workflow.ipynb` builds a deterministic two-step workflow.
- `experiments_monty_hall.ipynb` compares stay and switch strategies.
- `analysis_reliability.ipynb` estimates agreement among protocol coders.

The remaining examples compose two or more libraries:

- `canonical_artifact_flow.py` is the smallest deterministic all-layer handoff:
  one packaged problem, one public baseline agent, one experiment run path,
  canonical artifacts, and analysis validation.
- `student_laptop_design_study.py` is the smallest application-first decision
  study. It runs the packaged student laptop benchmark, prints the chosen
  laptop configuration, and reports the evaluator's observed market metrics.
- `pump_and_battery_design_portfolio.py` is the packaged engineering portfolio
  example. It runs real pump and battery optimization benchmarks, reports the
  observed objective and feasibility results, and previews a second recipe.
- `long_agent_markov_comparison.py` runs long scripted agent traces under two
  treatments and compares their exported process traces as Markov-chain
  transition matrices.
- `model_size_sweep_regression.py` sweeps model sizes within one model class and
  fits a regression directly from canonical experiment artifacts.
- `partial_factorial_ideation_regression.py` samples a larger model-by-task
  ideation design and fits a linear model without user-facing table plumbing.
- `prompt_framing_study.py` is the canonical live walkthrough. It keeps the
  managed `llama.cpp` runtime, workflow-backed strategy arms, pairwise
  condition comparisons, and markdown reporting.

Run locally with:

```bash
make run-example
make examples-test
```

`make run-example` executes the live canonical walkthrough in
`examples/prompt_framing_study.py`. Install `llama-cpp-python[server]` first.
If you want the default model download path, also install `huggingface-hub`;
otherwise set `LLAMA_CPP_MODEL` to a specific local GGUF file. The live study
defaults to 50 replicates per condition; set `PROMPT_STUDY_REPLICATES` to
run a larger sample.

`make examples-test` stays deterministic and offline-first by default. It runs
all offline examples. Set `RUN_OLLAMA_EXAMPLES=1` for the propose/critic
notebook or `RUN_LLAMA_CPP_EXAMPLES=1` for the managed llama.cpp walkthrough.
The selectors are independent.

Every run writes one pass, fail, or skip record per discovered example to
`artifacts/examples/example_results.json`. `make examples-coverage` consumes
that evidence and rejects records from a different live-runtime selection or
example inventory. It also requires every curated umbrella export to appear in
at least one example.

Focused notebooks retain their displayed results. `make notebooks-check`
verifies source and output hashes without execution; `make notebooks-refresh`
reruns the offline notebooks and updates both outputs and hashes. The
Ollama-backed notebook is refreshed explicitly only when its local model is
available.

Examples use the exact published component versions pinned by the umbrella
package.
