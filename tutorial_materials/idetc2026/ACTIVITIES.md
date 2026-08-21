# IDETC 2026 AI Experiments Tutorial Activities

This activity pack is separate from the preflight kit so that the tutorial
notebooks can be updated without changing the participant environment.

Extract the `notebooks/` and `scripts/` folders into the setup folder you used
for preflight. In VS Code or your preferred IDE, select the Python interpreter
and notebook kernel inside that folder's `.venv`.

## Participant notebooks

- `problems_text_map.ipynb`: map packaged design problems with TF-IDF and t-SNE.
- `problems_truss_grammar.ipynb`: apply design-grammar rules to a planar truss.
- `agents_workflow.ipynb`: build and trace a deterministic two-step agent workflow.
- `experiments_monty_hall.ipynb`: define conditions and run a seeded experiment.
- `analysis_reliability.ipynb`: measure agreement among protocol coders.

Each notebook contains saved output as a reference. You can rerun it from the
top after selecting the `.venv` kernel.

## Composed scripts

- `canonical_artifact_flow.py` is a small all-layer plumbing check.
- `long_agent_markov_comparison.py` compares two scripted design processes as
  Markov chains.
- `partial_factorial_ideation_regression.py` fits a regression from a partial
  factorial ideation study.

The supplied activities run offline. Any optional model-backed demonstration
will be identified separately by the facilitator.
