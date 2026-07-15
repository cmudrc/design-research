# Focused Tutorial Examples

These Jupyter notebooks introduce one component library at a time before the
composed examples use the umbrella namespace. Their saved outputs are the
results rendered by the documentation site:

- `problems_text_map.ipynb`: map packaged word problems with TF-IDF and t-SNE.
- `problems_truss_grammar.ipynb`: apply a planar-truss grammar manually.
- `agents_propose_critic.ipynb`: use an Ollama-backed propose/critic pattern.
- `agents_workflow.ipynb`: build a deterministic two-step workflow.
- `experiments_monty_hall.ipynb`: model and simulate the Monty Hall study.
- `analysis_reliability.ipynb`: estimate nominal inter-rater reliability.

Run all offline examples from the repository root with:

```bash
make examples-test
```

Use `make notebooks-refresh` to execute the offline notebooks and refresh their
stored results. Run `agents_propose_critic.ipynb` directly in VS Code after
starting Ollama.
