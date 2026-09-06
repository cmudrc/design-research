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
- `ideation_evidence_to_paper.py` runs 24 deterministic offline ideation
  attempts, retains one failure and two documented exclusions, then uses a
  fresh process to assemble, compile, and bundle the evidence-backed draft.
- `computational_design_evidence_to_paper.py` runs the packaged student-laptop
  problem and seeded baseline agent, retains authentic candidate/evaluator
  records, and carries an artifact-first profile, table, and figure into a
  fresh-process draft and verified bundle.
- `prompt_framing_study.py` is the canonical live walkthrough. It keeps the
  managed `llama.cpp` runtime, workflow-backed strategy arms, pairwise
  condition comparisons, and markdown reporting.

Run locally with:

```bash
make run-example
make examples-test
make live-smoke
```

`make run-example` executes the live canonical walkthrough in
`examples/prompt_framing_study.py`. Install the runtime through the owning
Agents extra:

```bash
python -m pip install "design-research-agents[llama_cpp]==0.7.0"
```

That extra includes the managed llama.cpp server and the Hugging Face download
client. Alternatively, set `LLAMA_CPP_MODEL` to a specific local GGUF file.
The live study defaults to 50 replicates per condition; set
`PROMPT_STUDY_REPLICATES` to choose a different sample size.

`make live-smoke` is the maintainer gate for both model-backed tutorials. It
executes the Ollama notebook once and runs the managed llama.cpp walkthrough
with two replicates per condition (six total runs, four live model calls). Use
`make live-smoke-ollama` or `make live-smoke-llama-cpp` when only one runtime is
available. The Ollama target expects a running local service with `qwen3:8b`;
the llama.cpp target expects the Agents `llama_cpp` extra above, or a local
`LLAMA_CPP_MODEL` GGUF file with the runtime already available. These targets
are for periodic and pre-release checks on model-capable infrastructure;
default CI remains deterministic and offline. A first-time managed startup may
download the default model and waits up to five minutes; override that window
with `LLAMA_CPP_STARTUP_TIMEOUT_SECONDS` when needed.

`make examples-test` stays deterministic and offline-first by default. It runs
all offline examples. Set `RUN_OLLAMA_EXAMPLES=1` for the propose/critic
notebook or `RUN_LLAMA_CPP_EXAMPLES=1` for the managed llama.cpp walkthrough.
The selectors are independent.

The two evidence-to-paper examples accept `--phase run` and `--phase draft` so
the persisted-directory handoff can be inspected directly. With no phase they
orchestrate those operations in separate interpreters. Add
`--require-tectonic` to the draft phase when a missing LaTeX compiler should be
an error rather than a reported skip.

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
