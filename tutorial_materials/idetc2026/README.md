# IDETC 2026 AI Experiments Tutorial Setup

Complete this setup before **AI Experiments in Engineering Design: A Tutorial
on the Design Research Open-Source Ecosystem** at IDETC-CIE 2026 on Sunday,
August 23. This kit prepares and checks your local environment. The current
activity notebooks will be provided separately at the tutorial.

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

## What the preflight checks

The preflight confirms that:

- the commands are using Python 3.12 or newer inside `.venv`;
- Jupyter and the Design Research packages can be imported;
- common data, statistics, optimization, sequence, and model-provider libraries
  are available; and
- a small offline problems-to-agents-to-experiments-to-analysis workflow runs
  successfully.

Provider client libraries are installed so the tutorial can accommodate
several activity directions, but preflight does not require an API key, model
download, or model service.

## On Sunday

Keep this folder and its `.venv`. At the tutorial, download the activity pack
provided by the facilitator and extract its `notebooks/` and `scripts/` folders
here. Open the activity notebook in VS Code and select the same `.venv` kernel.

You do not need the activity notebooks to complete setup. They are distributed
separately so that the tutorial content can reflect the latest package examples
without asking participants to rebuild their environments.

## Troubleshooting

- If `python3.12` is not found on macOS or Linux, confirm that Python 3.12 is
  installed and available on your `PATH`.
- If `py -3.12` is not found on Windows, reinstall Python 3.12 and enable the
  Python launcher option.
- If a notebook cannot import packages but `preflight.py` passes, select the
  `.venv` notebook kernel and restart the notebook.
- If installation fails on a restricted network, save the full terminal error
  and bring it to the tutorial.

Once preflight passes, the environment and offline exercises do not require
network access.
