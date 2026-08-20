# IDETC 2026 AI Experiments Tutorial

This kit supports **AI Experiments in Engineering Design: A Tutorial on the
Design Research Open-Source Ecosystem** at IDETC-CIE 2026 on Sunday, August 23.
The participant exercises are deterministic and run offline after installation.

## Set up before Sunday

Install Python 3.12, VS Code, and the VS Code Python and Jupyter extensions.
Open this extracted folder in VS Code, then use its integrated terminal.

On macOS or Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python preflight.py
```

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python preflight.py
```

The final command should end with:

```text
Preflight passed. You are ready for the tutorial.
```

In VS Code, run `Python: Select Interpreter` from the command palette and select
the interpreter inside `.venv`. Select that same environment as the notebook
kernel.

## Participant notebooks

Start with these five files in `notebooks/`:

- `problems_text_map.ipynb`: map packaged design problems with TF-IDF and t-SNE.
- `problems_truss_grammar.ipynb`: apply design-grammar rules to a planar truss.
- `agents_workflow.ipynb`: build a deterministic two-step agent workflow.
- `experiments_monty_hall.ipynb`: define conditions and run a seeded experiment.
- `analysis_reliability.ipynb`: measure agreement among protocol coders.

Each notebook contains saved output as a reference. You can rerun it from the
top after selecting the `.venv` kernel.

## Composed scripts

The `scripts/` folder contains three offline examples that connect multiple
layers of the stack:

- `canonical_artifact_flow.py` is the smallest all-layer plumbing check. It
  loads a packaged problem, runs a seeded baseline agent twice, exports standard
  experiment artifacts, and validates them with the analysis package.
- `long_agent_markov_comparison.py` compares two scripted design processes as
  Markov chains.
- `partial_factorial_ideation_regression.py` fits a regression from a partial
  factorial ideation study.

Run a script from this folder with the tutorial interpreter. For example:

```bash
.venv/bin/python scripts/canonical_artifact_flow.py
```

On Windows, use `.venv\Scripts\python` instead. Runtime output is written under
`artifacts/` in this folder.

## Model-backed examples

This participant kit does not require Ollama, `llama.cpp`, a model download, or
an API key. Model-backed demonstrations use a separate facilitator setup so
that model availability cannot block the offline exercises.
